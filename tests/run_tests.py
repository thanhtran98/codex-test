#!/usr/bin/env python3
"""Kiểm thử mediakit.py với gateway GIẢ chạy cục bộ (không tốn tiền, không cần mạng, cần ffmpeg).
Chạy từ thư mục gốc repo:  python tests/run_tests.py
Lưu ý: chỉ kiểm tra logic gọi API theo tài liệu BTC; KHÔNG thay thế việc thử với gateway thật. Lệnh `shot` không được kiểm thử ở đây."""
import json, os, pathlib, subprocess, sys, time

HERE = pathlib.Path(__file__).resolve().parent
TMP = HERE / "tmp"; TMP.mkdir(exist_ok=True)
KIT = str(HERE.parent / "tools" / "mediakit.py")
(TMP / "ref.png").write_bytes(b"PNGDATA123")
env = dict(os.environ, THUCCHIEN_BASE_URL="http://127.0.0.1:8765/v1", THUCCHIEN_API_KEY="TESTKEY", MEDIAKIT_OUT="out")
for f in ("out", "state.json"):
    p = TMP / f
    if p.is_file(): p.unlink()
    elif p.is_dir():
        for x in p.iterdir(): x.unlink()
srv = subprocess.Popen([sys.executable, str(HERE / "fake_gateway.py")], cwd=TMP, stdout=open(TMP / "server.log", "w"), stderr=subprocess.STDOUT)
time.sleep(4)
fails = []

def run(name, *args, expect=0, contains=None):
    r = subprocess.run([sys.executable, KIT, *args], cwd=TMP, env=env, capture_output=True, text=True, timeout=90)
    out = r.stdout + r.stderr
    ok = r.returncode == expect and (contains is None or contains in out)
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else f"\n   exit={r.returncode} {out[:300]}"))
    if not ok: fails.append(name)

try:
    run("image: 4:5 đổi thành 3:4", "image", "poster", "--out", "out/a.png", "--ratio", "4:5", "--model", "nano-banana-2-lite")
    run("image: tỷ lệ sai bị từ chối", "image", "x", "--out", "out/b.png", "--ratio", "7:3", expect=1, contains="không hợp lệ")
    run("image: --ref (chat/completions)", "image", "nhân vật", "--out", "out/c.png", "--ref", "ref.png")
    run("tts: tự lùi về đường dẫn không có /v1", "tts", "Xin chào", "--out", "out/v.mp3")
    run("video: image-to-video, retry sau 429", "video", "cảnh", "--out", "out/v.mp4", "--image", "ref.png", "--poll", "1")
    st = json.loads((TMP / "state.json").read_text())
    good = len(st["file_ok"]) == 2 and all(x[1] for x in st["file_ok"])
    print(("PASS " if good else "FAIL ") + "video: file ảnh vẫn đủ ở lần retry"); (fails.append("retry file") if not good else None)
    run("hết ngân sách: dừng ngay", "image", "BUDGET", "--out", "out/d.png", expect=1, contains="HẾT NGÂN SÁCH")
    run("review", "review", "out/a.png", contains="Chữ")
    run("search", "search", "tai nạn giao thông", contains="nguồn")
    run("spend", "spend", contains="max_budget")
    run("sheet", "sheet", "fake.mp4", "--out", "out/sheet.png")
    run("mux", "mux", "fake.mp4", "--audio", "fake.mp3", "--out", "out/mux.mp4")
    run("mux + nhạc nền", "mux", "fake.mp4", "--audio", "fake.mp3", "--music", "fake.mp3", "--out", "out/mux2.mp4")
    run("concat", "concat", "fake.mp4", "fake.mp4", "--out", "out/cat.mp4")
    run("doctor (font thiếu nên exit 1 là đúng)", "doctor", expect=1, contains="gateway trả lời")
    # nhà cung cấp ảnh riêng: ghi đè model qua biến môi trường (dùng cùng gateway giả)
    r = subprocess.run([sys.executable, KIT, "image", "nhà cung cấp riêng", "--out", "out/e.png"],
                       cwd=TMP, env=dict(env, MEDIAKIT_IMAGE_MODEL="wan2.7-image"),
                       capture_output=True, text=True, timeout=90)
    man = (TMP / "out" / "manifest.jsonl").read_text(encoding="utf-8")
    prov_ok = r.returncode == 0 and "wan2.7-image" in man
    print(("PASS " if prov_ok else "FAIL ") + "image: ghi đè model cho nhà cung cấp ảnh riêng")
    if not prov_ok: fails.append("provider model")
    m = (TMP / "out" / "manifest.jsonl").read_text(encoding="utf-8")
    print(("PASS " if "TESTKEY" not in m else "FAIL ") + "key không lọt vào manifest")
    if "TESTKEY" in m: fails.append("key leak")
finally:
    srv.kill()
print("\nKẾT QUẢ:", "TẤT CẢ ĐẠT" if not fails else f"{len(fails)} LỖI: {fails}")
sys.exit(1 if fails else 0)
