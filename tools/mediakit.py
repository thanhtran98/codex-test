#!/usr/bin/env python3
"""mediakit - CLI duy nhất nói chuyện với gateway AI Thực Chiến.

Lệnh: doctor | image | tts | video | shot | sheet | review | search | spend | mux | concat
Mỗi lệnh in ĐƯỜNG DẪN FILE đã tạo (hoặc kết quả văn bản) ra stdout và ghi 1 dòng vào out/manifest.jsonl.
Key lấy từ biến môi trường THUCCHIEN_API_KEY; nếu Codex lọc mất biến này thì đọc từ file
$THUCCHIEN_KEY_FILE hoặc ~/.thucchien/key. KHÔNG bao giờ đọc .env, KHÔNG bao giờ in key.
"""
import argparse, base64, json, mimetypes, os, pathlib, random, re, shutil, subprocess, sys, time
import requests

BASE = os.environ.get("THUCCHIEN_BASE_URL", "https://api.thucchien.ai/v1").rstrip("/")
ROOT = BASE[:-3] if BASE.endswith("/v1") else BASE          # các endpoint quản trị nằm ngoài /v1
OUT = pathlib.Path(os.environ.get("MEDIAKIT_OUT", "out"))

RATIOS = {"1:1", "3:4", "4:3", "16:9", "9:16"}               # gateway chỉ nhận các tỷ lệ này
RATIO_ALIAS = {"4:5": "3:4", "2:3": "3:4", "5:4": "4:3", "3:2": "4:3", "9:19": "9:16", "21:9": "16:9"}
# giá tham khảo (USD) từ bảng giá BTC, chỉ để ước tính khi header không trả chi phí
VIDEO_PRICE = {"veo-3.1-lite-generate-001": (0.05, 0.08), "veo-3.1-fast-generate-001": (0.10, 0.12),
               "veo-3.1-generate-001": (0.40, 0.40)}          # (720p, 1080p) mỗi giây
IMAGE_PRICE = {"nano-banana-2": 0.0672, "nano-banana-2-lite": 0.0336, "nano-banana-pro": 0.134}

# --- Nhà cung cấp ẢNH riêng (lab test) -------------------------------------
# Cách cấu hình (ưu tiên biến môi trường, sau đó tới file cấu hình):
#   1. Biến môi trường MEDIAKIT_IMAGE_* ; hoặc
#   2. File config/image-provider.local.json (đã gitignore) — mẫu ở config/image-provider.example.json
# Bỏ trống hết -> tự động quay về gateway BTC, không cần sửa code.
def _load_image_config():
    """Nạp config ảnh từ file JSON (không chứa key trong repo: file .local.json đã gitignore)."""
    path = os.environ.get("MEDIAKIT_IMAGE_CONFIG") or "config/image-provider.local.json"
    f = pathlib.Path(path)
    if not f.is_file():
        return {}
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except ValueError:
        die(f"{path} không phải JSON hợp lệ.")


_IMGCFG = _load_image_config()


def _cfg(env_name, json_key, default=""):
    v = os.environ.get(env_name)
    if v not in (None, ""):
        return v
    v = _IMGCFG.get(json_key)
    return default if v in (None, "") else str(v)


IMG_BASE = _cfg("MEDIAKIT_IMAGE_BASE_URL", "base_url").rstrip("/")
IMG_KEY = _cfg("MEDIAKIT_IMAGE_API_KEY", "api_key").strip()
IMG_MODE = (_cfg("MEDIAKIT_IMAGE_MODE", "mode", "images") or "images").strip().lower()   # images | chat
IMG_MODEL = _cfg("MEDIAKIT_IMAGE_MODEL", "model").strip()
IMG_RATIO_FIELD = _cfg("MEDIAKIT_IMAGE_RATIO_FIELD", "ratio_field", "aspect_ratio").strip()      # rỗng = không gửi tỷ lệ
IMG_AUTH = (_cfg("MEDIAKIT_IMAGE_AUTH", "auth", "bearer") or "bearer").strip().lower()    # bearer|raw|api-key|none
IMG_EXTRA = _cfg("MEDIAKIT_IMAGE_EXTRA_JSON", "extra_json").strip()                         # JSON gắn thêm vào body


def image_provider():
    """(base, key, mode, model_env, ratio_field, auth, extra_json). base rỗng -> gateway BTC."""
    return (IMG_BASE or BASE, IMG_KEY or KEY, IMG_MODE, IMG_MODEL,
            IMG_RATIO_FIELD, IMG_AUTH, IMG_EXTRA)


def image_extra_body():
    if not IMG_EXTRA:
        return {}
    try:
        return json.loads(IMG_EXTRA)
    except ValueError:
        die("MEDIAKIT_IMAGE_EXTRA_JSON không phải JSON hợp lệ.")


def load_key():
    k = os.environ.get("THUCCHIEN_API_KEY", "").strip()
    if k:
        return k
    for f in (os.environ.get("THUCCHIEN_KEY_FILE"), str(pathlib.Path.home() / ".thucchien" / "key")):
        if f and pathlib.Path(f).is_file():
            return pathlib.Path(f).read_text(encoding="utf-8").strip()
    return ""


KEY = load_key()


def die(msg):
    text = "LOI: " + str(msg)
    for k in (KEY, IMG_KEY):
        if k:
            text = text.replace(k, "***")
    sys.exit(text)


def need_key():
    if not KEY:
        die("Thiếu key. Đặt THUCCHIEN_API_KEY (hoặc file ~/.thucchien/key). Chạy `mediakit doctor` để kiểm tra.")


def log(kind, **kw):
    OUT.mkdir(parents=True, exist_ok=True)
    kw.update(kind=kind, ts=time.strftime("%Y-%m-%dT%H:%M:%S"))
    with open(OUT / "manifest.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(kw, ensure_ascii=False) + "\n")


def cost_of(r, est=None):
    """Ưu tiên chi phí gateway trả về trong header; không có thì dùng ước tính (est_cost)."""
    h = r.headers.get("x-litellm-response-cost") if r is not None else None
    return {"cost": float(h)} if h else ({"est_cost": round(est, 4)} if est is not None else {})


def req(method, path, retries=4, root=False, base=None, key=None, auth="bearer", **kw):
    """Gọi gateway. Tự thử lại khi 429 (không phải hết budget)/5xx/lỗi mạng; 404 thì thử đường dẫn có/không có /v1.
    `base`/`key` để dùng nhà cung cấp khác (mặc định: gateway BTC). Body tệp phải là bytes để thử lại không bị rỗng."""
    key = key or KEY
    if not key:
        die("Thiếu key. Đặt THUCCHIEN_API_KEY (hoặc file ~/.thucchien/key). Chạy `mediakit doctor` để kiểm tra.")
    b = (base or BASE).rstrip("/")
    if b == BASE.rstrip("/"):
        bases = [ROOT] if root else [BASE, ROOT if BASE != ROOT else BASE + "/v1"]
    else:
        bases = [b]
    if auth == "none":
        headers = {}
    elif auth == "api-key":
        headers = {"api-key": key}
    elif auth == "raw":
        headers = {"Authorization": key}
    else:
        headers = {"Authorization": f"Bearer {key}"}
    last = "chưa gọi được"
    for i in range(retries):
        try:
            r = requests.request(method, bases[0] + path, headers=headers, timeout=(15, 300), **kw)
            if r.status_code == 404 and len(bases) > 1:
                r = requests.request(method, bases[1] + path, headers=headers, timeout=(15, 300), **kw)
        except requests.RequestException as e:
            last = f"lỗi mạng: {type(e).__name__}"
            time.sleep(2 ** i + random.random()); continue
        if r.status_code == 429 and "udget" in r.text:
            die("429 HẾT NGÂN SÁCH (Budget has been exceeded). Dừng lại và báo người dùng; chờ không có tác dụng.")
        if r.status_code in (429, 500, 502, 503, 504):
            last = f"{r.status_code}: {r.text[:200]}"
            wait = float(r.headers["retry-after"]) if r.headers.get("retry-after", "").replace(".", "").isdigit() else 2 ** i + random.random()
            time.sleep(min(wait, 30)); continue
        if r.status_code >= 400:
            die(f"{r.status_code}: {r.text[:500]}")
        return r
    die(f"thất bại sau {retries} lần thử ({last})")


def norm_ratio(r):
    r = RATIO_ALIAS.get(r, r)
    if r not in RATIOS:
        die(f"tỷ lệ {r} không hợp lệ. Dùng: {', '.join(sorted(RATIOS))}")
    return r


def data_url(path):
    p = pathlib.Path(path)
    if not p.is_file():
        die(f"không thấy file tham chiếu: {path}")
    mime = mimetypes.guess_type(p.name)[0] or "image/png"
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()


def extract_image(j):
    """Lấy ảnh từ phản hồi /images/generations hoặc /chat/completions; trả về bytes."""
    try:
        d = j["data"][0]
        if d.get("b64_json"):
            return base64.b64decode(d["b64_json"])
        if d.get("url"):
            return requests.get(d["url"], timeout=120).content
    except (KeyError, IndexError, TypeError):
        pass
    try:
        m = j["choices"][0]["message"]
        for im in m.get("images") or []:
            u = im["image_url"]["url"]
            return base64.b64decode(u.split(",", 1)[1])
        txt = m.get("content") or ""
        if isinstance(txt, list):
            txt = " ".join(x.get("text", "") for x in txt if isinstance(x, dict))
        g = re.search(r"data:image/[a-z]+;base64,([A-Za-z0-9+/=]+)", txt)
        if g:
            return base64.b64decode(g.group(1))
    except (KeyError, IndexError, TypeError):
        pass
    die("phản hồi không chứa ảnh: " + json.dumps(j, ensure_ascii=False)[:300])


def chat_text(r):
    m = r.json()["choices"][0]["message"].get("content") or ""
    return " ".join(x.get("text", "") for x in m if isinstance(x, dict)) if isinstance(m, list) else m


# ---------------------------------------------------------------- lệnh
def cmd_image(a):
    p = pathlib.Path(a.out); p.parent.mkdir(parents=True, exist_ok=True)
    base, key, mode, model_env, ratio_field, auth, _extra = image_provider()
    model = model_env or a.model
    ratio = norm_ratio(a.ratio)
    nonce = "\n\n(Mã biến thể: không phải nội dung ảnh, tuyệt đối không vẽ chữ hay số.)"
    if a.ref:
        if base == BASE and model.startswith("gpt-image"):
            die("--ref chỉ hỗ trợ model nano-banana-*. Dùng --model nano-banana-2.")
        parts = [{"type": "text", "text": f"{a.prompt}\nTỷ lệ khung hình đầu ra: {ratio}. Giữ nhất quán với ảnh tham chiếu.{nonce}"}]
        parts += [{"type": "image_url", "image_url": {"url": data_url(x)}} for x in a.ref]
        r = req("POST", "/chat/completions", base=base, key=key, auth=auth,
                json={"model": model, "messages": [{"role": "user", "content": parts}]})
    elif mode == "chat":
        content = [{"type": "text", "text": a.prompt + nonce}]
        if IMG_RATIO_FIELD:
            content[0]["text"] = f"{a.prompt}\nTỷ lệ khung hình đầu ra: {ratio}.{nonce}"
        body = {"model": model, "messages": [{"role": "user", "content": content}]}
        body.update(image_extra_body())
        r = req("POST", "/chat/completions", base=base, key=key, auth=auth, json=body)
    else:
        body = {"model": model, "prompt": a.prompt + nonce}
        if model.startswith("gpt-image"):
            body.update(size=a.size, quality=a.quality)
        elif IMG_RATIO_FIELD:
            body[IMG_RATIO_FIELD] = ratio
        body.update(image_extra_body())
        r = req("POST", "/images/generations", base=base, key=key, auth=auth, json=body)
    p.write_bytes(extract_image(r.json()))
    log("image", model=model, ratio=ratio, ref=a.ref, provider=("gateway BTC" if base == BASE else base),
        prompt=a.prompt, file=str(p), **cost_of(r, IMAGE_PRICE.get(model)))
    print(p)


def cmd_tts(a):
    p = pathlib.Path(a.out); p.parent.mkdir(parents=True, exist_ok=True)
    r = req("POST", "/audio/speech", json={"model": a.model, "input": a.text, "voice": a.voice})
    if "json" in r.headers.get("content-type", "") or len(r.content) < 500:
        die("TTS không trả về âm thanh: " + r.text[:300])
    p.write_bytes(r.content)
    log("tts", model=a.model, voice=a.voice, chars=len(a.text), file=str(p), **cost_of(r))
    print(p)


def cmd_video(a):
    p = pathlib.Path(a.out); p.parent.mkdir(parents=True, exist_ok=True)
    data = {"model": a.model, "prompt": a.prompt, "seconds": str(a.seconds), "size": a.size}
    if a.image:
        ip = pathlib.Path(a.image)
        if not ip.is_file():
            die(f"không thấy ảnh đầu: {a.image}")
        files = {"input_reference": (ip.name, ip.read_bytes(), mimetypes.guess_type(ip.name)[0] or "image/png")}
        r = req("POST", "/videos", data=data, files=files)
    else:
        r = req("POST", "/videos", json=data)
    vid = r.json()["id"]; t0 = time.time()
    hd = a.size in ("1920x1080", "1080x1920")
    price = VIDEO_PRICE.get(a.model, (0.05, 0.08))[1 if hd else 0]
    est = price * a.seconds                               # tính tiền ngay khi tạo job, kể cả khi thất bại/hết giờ
    log("video_job", model=a.model, job=vid, seconds=a.seconds, size=a.size, pending_cost=round(est, 4), prompt=a.prompt)
    print(f"job {vid[:24]}... đang chạy (ước tính ${est:.2f})", file=sys.stderr)
    while True:
        s = req("GET", f"/videos/{vid}").json()
        if s.get("status") == "completed":
            break
        if s.get("status") == "failed":
            die(f"VIDEO THẤT BẠI (job {vid}): {json.dumps(s, ensure_ascii=False)[:400]}")
        if time.time() - t0 > a.timeout:
            die(f"HẾT GIỜ sau {a.timeout}s, job {vid} (vẫn bị tính tiền). Lùi về ảnh tĩnh.")
        time.sleep(a.poll)
    c = req("GET", f"/videos/{vid}/content")
    p.write_bytes(c.content)
    log("video", model=a.model, job=vid, seconds=a.seconds, size=a.size, prompt=a.prompt, file=str(p),
        elapsed=round(time.time() - t0), **cost_of(c, est))
    print(p)


def cmd_shot(a):  # HTML -> PNG/PDF bằng playwright
    from playwright.sync_api import sync_playwright
    p = pathlib.Path(a.out); p.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": a.width, "height": a.height}, device_scale_factor=a.scale)
        pg.goto(pathlib.Path(a.html).resolve().as_uri())
        pg.evaluate("document.fonts.ready")                # chờ font tiếng Việt tải xong
        pg.wait_for_timeout(500)
        if p.suffix.lower() == ".pdf":
            pg.pdf(path=str(p), width=f"{a.width}px", height=f"{a.height}px", print_background=True)
        else:
            pg.screenshot(path=str(p), full_page=a.full)
        b.close()
    log("shot", html=a.html, file=str(p), size=f"{a.width}x{a.height}@{a.scale}x"); print(p)


def probe_duration(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                       capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        die(f"không đọc được độ dài: {path}")


def cmd_sheet(a):  # lưới khung hình đều nhau để QA video
    p = pathlib.Path(a.out); p.parent.mkdir(parents=True, exist_ok=True)
    every = max(0.2, probe_duration(a.video) / (a.cols * a.rows))
    subprocess.run(["ffmpeg", "-y", "-i", a.video, "-vf", f"fps=1/{every:.3f},scale=320:-1,tile={a.cols}x{a.rows}",
                    "-frames:v", "1", str(p)], check=True, capture_output=True)
    print(p)


REVIEW_Q = ("Bạn là người kiểm tra chất lượng. Với ảnh này: (1) chép lại CHÍNH XÁC từng dòng chữ nhìn thấy, "
            "(2) chỉ ra lỗi chính tả/thiếu dấu/sai dấu tiếng Việt, (3) nêu chữ bị che, tràn lề hoặc khó đọc, "
            "(4) nêu logo/thương hiệu/người thật/lá cờ/bản đồ xuất hiện (nếu có) và có vẻ sai không. Trả lời ngắn gọn bằng tiếng Việt.")


def cmd_review(a):  # model có thị giác đọc ảnh để QA (khi model của Codex không nhìn được ảnh)
    parts = [{"type": "text", "text": a.question or REVIEW_Q}] + \
            [{"type": "image_url", "image_url": {"url": data_url(x)}} for x in a.files]
    r = req("POST", "/chat/completions", json={"model": a.model, "max_tokens": 1200,
                                               "messages": [{"role": "user", "content": parts}]})
    out = chat_text(r)
    log("review", model=a.model, files=a.files, **cost_of(r)); print(out)


def cmd_search(a):  # tra cứu dữ kiện có nguồn. CHƯA kiểm chứng với gateway thật.
    if a.engine == "openai":
        r = req("POST", "/responses", json={"model": a.model, "input": a.query, "tools": [{"type": "web_search"}],
                                            "max_output_tokens": 1500})
        j = r.json(); text = j.get("output_text") or json.dumps(j, ensure_ascii=False)[:3000]
    else:
        body = {"model": a.model, "max_tokens": 1500, "tools": [{"googleSearch": {}}],
                "messages": [{"role": "user", "content": a.query + "\nTrả lời bằng tiếng Việt, ngắn gọn, kèm nguồn."}]}
        r = req("POST", "/chat/completions", json=body)
        text = chat_text(r)
    log("search", model=a.model, engine=a.engine, query=a.query, **cost_of(r)); print(text)


def local_ledger():
    """Tổng chi phí ghi trong out/manifest.jsonl (job video chưa xong vẫn tính vì gateway tính tiền ngay khi tạo)."""
    f = OUT / "manifest.jsonl"
    total, pend, done = 0.0, {}, set()
    if f.is_file():
        for line in f.read_text(encoding="utf-8").splitlines():
            try:
                e = json.loads(line)
            except ValueError:
                continue
            if e.get("kind") == "video_job":
                pend[e["job"]] = e.get("pending_cost", 0)
            else:
                total += e.get("cost", e.get("est_cost", 0)) or 0
                if e.get("kind") == "video":
                    done.add(e.get("job"))
    return round(total + sum(v for k, v in pend.items() if k not in done), 4)


def cmd_spend(a):  # ngân sách còn lại; /team/info là nơi có số liệu cả đội
    print(f"sổ cục bộ (manifest, ước tính): ${local_ledger()}")
    if IMG_BASE:
        print(f"LƯU Ý: ảnh đang đi nhà cung cấp riêng ({IMG_BASE}); số dưới đây của gateway BTC KHÔNG gồm chi phí ảnh.")
    try:
        ki = req("GET", "/key/info", root=True).json()
        info = ki.get("info", ki)
        print(f"key: spend=${info.get('spend')}")
        tid = info.get("team_id")
        if tid:
            ti = req("GET", "/team/info", root=True, params={"team_id": tid}).json()
            t = ti.get("team_info", ti)
            print(f"team: spend=${t.get('spend')} max_budget=${t.get('max_budget')}")
        else:
            print("không thấy team_id; xem trang Kiểm tra chi tiêu của BTC")
    except SystemExit:
        print("không đọc được số của gateway BTC (key lỗi/không kết nối); sổ cục bộ ở trên vẫn dùng được.")


def cmd_mux(a):  # ghép video + giọng đọc (+ nhạc nền); mặc định bỏ âm thanh gốc của Veo
    p = pathlib.Path(a.out); p.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-y", "-i", a.video, "-i", a.audio] + (["-i", a.music] if a.music else [])
    if a.music:
        fc = f"[1:a]volume=1.0[v];[2:a]volume={a.music_volume}[m];[v][m]amix=inputs=2:duration=first:dropout_transition=0[a]"
        cmd += ["-filter_complex", fc, "-map", "0:v", "-map", "[a]"]
    else:
        cmd += ["-map", "0:v", "-map", "1:a"]
    cmd += ["-c:v", "copy", "-c:a", "aac", "-shortest", str(p)]
    subprocess.run(cmd, check=True, capture_output=True); log("mux", file=str(p)); print(p)


def cmd_concat(a):  # nối nhiều clip cùng codec/kích thước; mã hóa lại để an toàn
    p = pathlib.Path(a.out); p.parent.mkdir(parents=True, exist_ok=True)
    lst = p.with_suffix(".txt")
    lst.write_text("".join(f"file '{pathlib.Path(x).resolve().as_posix()}'\n" for x in a.clips), encoding="utf-8")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c:v", "libx264", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", str(p)], check=True, capture_output=True)
    lst.unlink(); log("concat", file=str(p), clips=len(a.clips)); print(p)


def cmd_doctor(a):  # kiểm tra môi trường, không tốn tiền
    ok = True
    def row(name, good, note=""):
        nonlocal ok
        ok &= bool(good); print(f"[{'OK ' if good else 'LOI'}] {name} {note}")
    row("Python >= 3.10", sys.version_info >= (3, 10), sys.version.split()[0])
    row("Có key (không in ra)", bool(KEY), "" if KEY else "-> đặt THUCCHIEN_API_KEY hoặc ~/.thucchien/key")
    for t in ("ffmpeg", "ffprobe", "git"):
        row(t, shutil.which(t))
    try:
        import playwright  # noqa
        row("playwright", True)
    except ImportError:
        row("playwright", False, "-> pip install playwright && python -m playwright install chromium")
    fonts = [f for f in pathlib.Path("assets/fonts").rglob("*") if f.suffix.lower() in (".ttf", ".otf", ".woff", ".woff2")]
    row("font tiếng Việt trong assets/fonts/", fonts, f"({len(fonts)} file)")
    if KEY:
        try:
            r = requests.get(BASE + "/models", headers={"Authorization": f"Bearer {KEY}"}, timeout=20)
            row("gateway trả lời /models", r.status_code == 200, f"(HTTP {r.status_code})")
        except requests.RequestException as e:
            row("gateway trả lời /models", False, type(e).__name__)
    if IMG_BASE:
        row("ảnh đang dùng nhà cung cấp riêng", True,
            f"({IMG_BASE} · mode={IMG_MODE} · auth={IMG_AUTH}"
            + (f" · model={IMG_MODEL}" if IMG_MODEL else "") + ")")
        row("có key cho nhà cung cấp ảnh", bool(IMG_KEY), "" if IMG_KEY else "-> thiếu MEDIAKIT_IMAGE_API_KEY")
    else:
        row("ảnh đang dùng gateway BTC", True, "(bỏ trống MEDIAKIT_IMAGE_* để quay về BTC)")
    sys.exit(0 if ok else 1)


def main():
    ap = argparse.ArgumentParser(prog="mediakit"); sp = ap.add_subparsers(dest="c", required=True)
    sp.add_parser("doctor").set_defaults(f=cmd_doctor)
    i = sp.add_parser("image"); i.add_argument("prompt"); i.add_argument("--out", required=True)
    i.add_argument("--model", default="nano-banana-2"); i.add_argument("--ratio", default="3:4", help="1:1 3:4 4:3 16:9 9:16 (4:5 -> 3:4)")
    i.add_argument("--ref", action="append", help="ảnh tham chiếu (nhân vật/sản phẩm/logo), có thể lặp lại")
    i.add_argument("--size", default="1024x1024"); i.add_argument("--quality", default="low"); i.set_defaults(f=cmd_image)
    t = sp.add_parser("tts"); t.add_argument("text"); t.add_argument("--out", required=True)
    t.add_argument("--model", default="gemini-2.5-flash-preview-tts"); t.add_argument("--voice", default="Zephyr"); t.set_defaults(f=cmd_tts)
    v = sp.add_parser("video"); v.add_argument("prompt"); v.add_argument("--out", required=True)
    v.add_argument("--model", default="veo-3.1-lite-generate-001"); v.add_argument("--seconds", type=int, default=4, choices=[4, 6, 8])
    v.add_argument("--size", default="1280x720", choices=["1280x720", "1920x1080", "720x1280", "1080x1920"])
    v.add_argument("--image"); v.add_argument("--poll", type=int, default=10); v.add_argument("--timeout", type=int, default=600); v.set_defaults(f=cmd_video)
    s = sp.add_parser("shot"); s.add_argument("html"); s.add_argument("--out", required=True)
    s.add_argument("--width", type=int, default=1080); s.add_argument("--height", type=int, default=1350)
    s.add_argument("--scale", type=float, default=1.0); s.add_argument("--full", action="store_true"); s.set_defaults(f=cmd_shot)
    h = sp.add_parser("sheet"); h.add_argument("video"); h.add_argument("--out", required=True)
    h.add_argument("--cols", type=int, default=4); h.add_argument("--rows", type=int, default=3); h.set_defaults(f=cmd_sheet)
    rv = sp.add_parser("review"); rv.add_argument("files", nargs="+"); rv.add_argument("--question")
    rv.add_argument("--model", default="gemini-3.1-flash-lite"); rv.set_defaults(f=cmd_review)
    se = sp.add_parser("search"); se.add_argument("query"); se.add_argument("--engine", choices=["gemini", "openai"], default="gemini")
    se.add_argument("--model", default=None); se.set_defaults(f=cmd_search)
    sp.add_parser("spend").set_defaults(f=cmd_spend)
    m = sp.add_parser("mux"); m.add_argument("video"); m.add_argument("--audio", required=True); m.add_argument("--music")
    m.add_argument("--music-volume", type=float, default=0.15); m.add_argument("--out", required=True); m.set_defaults(f=cmd_mux)
    c = sp.add_parser("concat"); c.add_argument("clips", nargs="+"); c.add_argument("--out", required=True); c.set_defaults(f=cmd_concat)
    a = ap.parse_args()
    if a.c == "search" and not a.model:
        a.model = "gpt-6-luna" if a.engine == "openai" else "gemini-3.6-flash"
    a.f(a)


if __name__ == "__main__":
    main()
