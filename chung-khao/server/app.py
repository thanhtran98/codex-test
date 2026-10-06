"""Web server cho Trợ lý Du lịch Đắk Lắk AI.

Phục vụ app/ tĩnh và hai API:
- GET  /api/meta          -> danh mục vùng, nhãn sở thích, nguồn dữ liệu
- POST /api/lap-lich      -> sinh tối đa 3 phương án theo quy tắc (không tốn AI)
- POST /api/tu-van        -> gọi AI qua gateway chọn 1 phương án và giải thích
- GET  /api/health        -> kiểm tra tiến trình

Mọi lời gọi AI đều đi qua tools/mediakit.py bằng subprocess; backend không
nhận key từ trình duyệt và không ghi key vào mã nguồn.
"""

import json
import os
import threading
import time
from collections import defaultdict, deque

from flask import Flask, jsonify, request, send_from_directory

import engine
import gateway
import chat_handler

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_DIR = os.path.join(BASE_DIR, "app")
FONTS_DIR = os.path.join(BASE_DIR, "assets", "fonts")

app = Flask(__name__, static_folder=APP_DIR, static_url_path="/static")

# Giới hạn gọi đơn giản theo IP (chỉ giảm áp lực, không phải hạn mức bền vững).
_RATE_WINDOW = 60.0
_RATE_LIMIT = 12
_rate_log = defaultdict(deque)


def _client_ip():
    return request.headers.get("X-Forwarded-For", request.remote_addr or "unknown").split(",")[0].strip()


def _rate_allowed(key):
    now = time.monotonic()
    q = _rate_log[key]
    while q and now - q[0] > _RATE_WINDOW:
        q.popleft()
    if len(q) >= _RATE_LIMIT:
        return False
    q.append(now)
    return True


def _json_error(message, status=400):
    return jsonify({"ok": False, "error": message}), status


def _parse_pax(value):
    try:
        pax = int(value)
    except (TypeError, ValueError):
        return None
    if pax < 1 or pax > 8:
        return None
    return pax


def _parse_days(value):
    try:
        days = int(value)
    except (TypeError, ValueError):
        return None
    if days < 1 or days > 3:
        return None
    return days


def _parse_budget(value):
    try:
        budget = int(float(value))
    except (TypeError, ValueError):
        return None
    if budget < 500000 or budget > 50000000:
        return None
    return budget


def _validate_plan_input(data):
    if not isinstance(data, dict):
        return None, "Dữ liệu yêu cầu không đúng định dạng."

    pax = _parse_pax(data.get("pax"))
    if pax is None:
        return None, "Số người đi phải là số nguyên từ 1 đến 8."

    days = _parse_days(data.get("days"))
    if days is None:
        return None, "Số ngày đi phải là số nguyên từ 1 đến 3."

    budget = _parse_budget(data.get("budget"))
    if budget is None:
        return None, "Ngân sách phải là số từ 500.000 đến 50.000.000 đồng."

    preference = str(data.get("preference", "")).strip()
    if len(preference) > 200:
        return None, "Sở thích quá dài."

    cluster = str(data.get("cluster", "bmt")).strip()
    allowed_clusters = {c["id"] for c in engine.load_catalog()["clusters"]}
    if cluster not in allowed_clusters:
        cluster = "bmt"

    return {
        "pax": pax,
        "days": days,
        "budget": budget,
        "preference": preference,
        "cluster": cluster,
    }, None


@app.get("/")
def index():
    return send_from_directory(APP_DIR, "index.html")


@app.get("/fonts/<path:filename>")
def fonts(filename):
    return send_from_directory(FONTS_DIR, filename)


@app.get("/styles.css")
def styles_css():
    return send_from_directory(APP_DIR, "styles.css")


@app.get("/app.js")
def app_js():
    return send_from_directory(APP_DIR, "app.js")


@app.get("/chat.js")
def chat_js():
    return send_from_directory(APP_DIR, "chat.js")


@app.get("/images/<path:filename>")
def images(filename):
    return send_from_directory(os.path.join(APP_DIR, "images"), filename)


@app.get("/api/health")
def health():
    return jsonify({"ok": True, "time": time.time()})


@app.get("/api/meta")
def meta():
    catalog = engine.load_catalog()
    return jsonify({
        "ok": True,
        "clusters": catalog["clusters"],
        "preferences": [
            {"id": "van-hoa", "label": "Văn hóa & di sản"},
            {"id": "thien-nhien", "label": "Thiên nhiên & sinh thái"},
            {"id": "ca-phe", "label": "Cà phê & lối sống"},
            {"id": "tong-hoa", "label": "Tổng hòa văn hóa và thiên nhiên"},
        ],
        "sources": catalog.get("sources", []) if "sources" in catalog else engine.load_sources()["sources"],
        "data_note": "Dữ liệu tham khảo, đối chiếu ngày 06/10/2026; giá có thể thay đổi theo đơn vị cung cấp.",
    })


@app.post("/api/lap-lich")
def lap_lich():
    if not _rate_allowed("lap-lich:" + _client_ip()):
        return _json_error("Quá nhiều yêu cầu. Vui lòng thử lại sau giây lát.", 429)

    try:
        data = request.get_json(silent=True) or {}
    except Exception:
        data = {}

    clean, err = _validate_plan_input(data)
    if err:
        return _json_error(err)

    result = engine.generate_trip_plans(
        pax=clean["pax"],
        days=clean["days"],
        user_budget=clean["budget"],
        preference=clean["preference"],
        cluster=clean["cluster"],
    )
    result["ok"] = True
    result["ai_status"] = "pending"
    return jsonify(result)


@app.post("/api/tu-van")
def tu_van():
    if not _rate_allowed("tu-van:" + _client_ip()):
        return _json_error("Quá nhiều yêu cầu. Vui lòng thử lại sau giây lát.", 429)

    try:
        data = request.get_json(silent=True) or {}
    except Exception:
        data = {}

    clean, err = _validate_plan_input(data)
    if err:
        return _json_error(err)

    result = engine.generate_trip_plans(
        pax=clean["pax"],
        days=clean["days"],
        user_budget=clean["budget"],
        preference=clean["preference"],
        cluster=clean["cluster"],
    )
    options = result["options"]
    ai = gateway.consult_ai_for_plan(
        user_input={
            "pax": clean["pax"],
            "days": clean["days"],
            "budget": clean["budget"],
            "preference": clean["preference"],
        },
        options=options,
    )
    # Chỉ chấp nhận mã hợp lệ; nếu AI trả mã lạ thì dùng phương án quy tắc.
    if ai.get("selected_code") not in ("A", "B", "C"):
        ai["selected_code"] = result["default_option"]
        ai["is_fallback"] = True

    return jsonify({
        "ok": True,
        "ai": ai,
        "default_option": result["default_option"],
        "options": options,
        "responsible_rules": result["responsible_rules"],
    })


@app.post("/api/doi-diem")
def doi_diem():
    if not _rate_allowed("doi-diem:" + _client_ip()):
        return _json_error("Quá nhiều yêu cầu. Vui lòng thử lại sau giây lát.", 429)

    try:
        data = request.get_json(silent=True) or {}
    except Exception:
        data = {}

    pax = _parse_pax(data.get("pax"))
    if pax is None:
        return _json_error("Số người đi phải là số nguyên từ 1 đến 8.")
    days = _parse_days(data.get("days"))
    if days is None:
        return _json_error("Số ngày đi phải là số nguyên từ 1 đến 3.")

    current = data.get("destinations")
    old_id = str(data.get("old_id", "")).strip()
    new_id = str(data.get("new_id", "")).strip()
    acc_type = str(data.get("acc_type", "hotel")).strip()

    if not isinstance(current, list) or not old_id or not new_id or old_id == new_id:
        return _json_error("Thiếu thông tin để đổi điểm.")

    catalog = engine.load_catalog()
    known = {d["id"] for d in catalog["destinations"]}
    if old_id not in known or new_id not in known or old_id not in current:
        return _json_error("Điểm đến không hợp lệ.")

    if acc_type not in catalog["accommodations"]:
        acc_type = "hotel"

    result = engine.swap_destination_in_plan(
        current_destinations=current,
        old_dest_id=old_id,
        new_dest_id=new_id,
        pax=pax,
        days=days,
        acc_type=acc_type,
    )
    result["ok"] = True
    return jsonify(result)


@app.post("/api/chat")
def chat():
    if not _rate_allowed("chat:" + _client_ip()):
        return _json_error("Quá nhiều yêu cầu. Vui lòng thử lại sau giây lát.", 429)
    try:
        data = request.get_json(silent=True) or {}
    except Exception:
        data = {}
    messages = data.get("messages") if isinstance(data, dict) else None
    if not isinstance(messages, list) or not 1 <= len(messages) <= 11:
        return _json_error("Tin nhắn không hợp lệ.", 400)

    cleaned = []
    for index, message in enumerate(messages):
        expected = "user" if index % 2 == 0 else "assistant"
        if (not isinstance(message, dict) or message.get("role") != expected
                or not isinstance(message.get("content"), str)
                or not 1 <= len(message["content"].strip()) <= 4000):
            return _json_error("Tin nhắn không hợp lệ.", 400)
        cleaned.append({"role": message["role"], "content": message["content"]})
    if cleaned[-1]["role"] != "user":
        return _json_error("Tin nhắn không hợp lệ.", 400)

    try:
        reply = chat_handler.run_chat(cleaned)
    except Exception as exc:
        return _json_error(str(exc), 502)
    return jsonify({"ok": True, "reply": reply})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    app.run(host="0.0.0.0", port=port, debug=False)
