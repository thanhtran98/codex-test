"""Hỏi đáp qua API tương thích OpenAI, khóa chỉ nằm ở phía máy chủ."""

import os
import requests

CHAT_API_BASE_URL = "http://117.1.150.235:31000/v1"
CHAT_MODEL = "deepseek-v4.1-flash"

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
    key = os.environ.get("CHAT_API_KEY", "").strip()
    if not key:
        raise RuntimeError("Trợ lý chưa được cấu hình khóa API trên máy chủ.")
    base_url = os.environ.get("CHAT_API_BASE_URL", CHAT_API_BASE_URL).rstrip("/")
    try:
        response = requests.post(
            base_url + "/chat/completions",
            headers={"Authorization": "Bearer " + key},
            json={
                "model": model or os.environ.get("CHAT_MODEL", CHAT_MODEL),
                "messages": [{"role": "system", "content": SYSTEM_MESSAGE}] + messages,
                "max_tokens": 1200,
                "stream": False,
            },
            timeout=(5, 35),
            allow_redirects=False,
        )
    except requests.Timeout:
        raise RuntimeError("Trợ lý phản hồi quá lâu. Vui lòng gửi lại câu hỏi.") from None
    except requests.RequestException:
        raise RuntimeError("Chưa kết nối được máy chủ hỏi đáp. Vui lòng thử lại.") from None

    if response.status_code in (401, 403):
        raise RuntimeError("Máy chủ hỏi đáp từ chối xác thực. Vui lòng kiểm tra cấu hình khóa API.")
    if response.status_code == 429:
        raise RuntimeError("Máy chủ hỏi đáp đang giới hạn yêu cầu hoặc hết hạn mức. Vui lòng thử lại sau.")
    if response.status_code != 200:
        raise RuntimeError("Máy chủ hỏi đáp tạm thời không thể xử lý yêu cầu.")
    try:
        reply = response.json()["choices"][0]["message"]["content"]
    except (ValueError, KeyError, IndexError, TypeError):
        raise RuntimeError("Máy chủ hỏi đáp trả về dữ liệu không hợp lệ.") from None
    if not isinstance(reply, str) or not reply.strip():
        raise RuntimeError("Trợ lý chưa có câu trả lời. Vui lòng thử lại.")
    return reply.strip()
