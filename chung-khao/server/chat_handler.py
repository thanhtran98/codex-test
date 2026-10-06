"""Endpoint hội thoại cho website, gọi gateway BTC qua tools/mediakit.py chat.

Chỉ nhận POST /api/chat với danh sách messages xen kẽ user/assistant, kết thúc
bằng vai user. Key do mediakit tự nạp từ môi trường; backend không nhận key
từ trình duyệt và không ghi key vào mã nguồn.
"""

import json
import os
import pathlib
import subprocess

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
REPO_DIR = BASE_DIR.parent

SYSTEM_MESSAGE = (
    "Bạn là trợ lý Đắk Lắk Ơi, trả lời bằng tiếng Việt có dấu, ngắn gọn, "
    "thân thiện, chỉ hỗ trợ du lịch Đắk Lắk. Hỏi số ngày, số người, sở thích "
    "và ngân sách khi cần gợi ý hành trình. Không bịa giá, giờ mở cửa, khoảng "
    "cách, nguồn hay tình trạng đường đi. Nêu rõ thông tin cần xác minh với "
    "đơn vị quản lý. Không coi ngân sách là báo giá. Khuyến khích du lịch có "
    "trách nhiệm, không khuyên tắm thác hay vào khu cấm. Không có khả năng "
    "tra cứu trực tiếp trong cuộc chat. Không yêu cầu thông tin cá nhân nhạy "
    "cảm. Không nhận mình đã đặt dịch vụ."
)


def run_chat(messages, model=None):
    model = model or os.environ.get("THUCCHIEN_CHAT_MODEL", "gemini-3.1-flash-lite")
    python_bin = str(BASE_DIR / ".venv" / "bin" / "python")
    if not os.path.exists(python_bin):
        python_bin = str(REPO_DIR / ".venv" / "bin" / "python")
    if not os.path.exists(python_bin):
        python_bin = "python3"

    payload = [{"role": "system", "content": SYSTEM_MESSAGE}] + messages
    cmd = [
        python_bin,
        str(BASE_DIR / "tools" / "mediakit.py"),
        "chat",
        "--model", model,
        "--max-tokens", "600",
    ]
    env = os.environ.copy()
    proc = subprocess.run(
        cmd,
        input=json.dumps(payload, ensure_ascii=False),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=40,
        cwd=str(BASE_DIR),
        env=env,
    )
    if proc.returncode != 0:
        raise RuntimeError(_gateway_error(proc.stderr))
    text = proc.stdout.strip()
    if not text:
        raise RuntimeError("Trợ lý chưa có câu trả lời.")
    return text


def _gateway_error(stderr):
    if "Budget" in stderr or "HẾT NGÂN SÁCH" in stderr:
        return "Ngân sách AI đã hết. Trợ lý tạm dừng nhận câu hỏi."
    if "401" in stderr:
        return "Trợ lý chưa được cấu hình khóa API hợp lệ trên máy chủ."
    return "Gateway đang bận hoặc cấu hình chưa hợp lệ."
