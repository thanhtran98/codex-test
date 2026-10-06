import json
import os
import pathlib
import subprocess

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
REPO_DIR = BASE_DIR.parent

def consult_ai_for_plan(user_input, options, model="gemini-3.1-flash-lite"):
    """
    Gọi CLI mediakit chat thông qua subprocess để nhận tư vấn lựa chọn phương án và lời khuyên du lịch.
    Đảm bảo fallback an toàn nếu gateway gặp sự cố.
    """
    pax = user_input.get("pax", 2)
    days = user_input.get("days", 2)
    budget = user_input.get("budget", 5000000)
    pref = user_input.get("preference", "Tổng hòa văn hóa và thiên nhiên")
    
    options_summary = []
    for opt in options:
        options_summary.append({
            "code": opt["code"],
            "name": opt["name"],
            "total_cost": opt["budget"]["breakdown"]["total"],
            "per_pax": opt["budget"]["breakdown"]["per_pax"],
            "destinations": [d["name"] for d in opt.get("destination_details", [])],
            "budget_status": opt["budget_check"]["status_text"]
        })
        
    prompt = f"""Bạn là Trợ lý Du lịch Đắk Lắk AI thông thái, am hiểu sâu sắc văn hóa Tây Nguyên và du lịch có trách nhiệm.
Khách du lịch có yêu cầu sau:
- Số người: {pax} người lớn
- Số ngày: {days} ngày
- Ngân sách: {budget:,} VND
- Sở thích: "{pref}"

Dưới đây là 3 phương án hành trình do hệ thống lập lịch đề xuất:
{json.dumps(options_summary, ensure_ascii=False, indent=2)}

Nhiệm vụ của bạn:
1. Chọn 01 phương án phù hợp nhất (trả về mã: "A", "B", hoặc "C") dựa trên sự tương thích với sở thích và tính tối ưu ngân sách.
2. Viết lời giải thích ngắn gọn, súc tích (khoảng 2-3 câu) vì sao phương án này là may đo tốt nhất cho đoàn.
3. Đưa ra 01 lời khuyên thực địa hữu ích khi đến Đắk Lắk (ví dụ về thời gian di chuyển, trang phục hoặc cách thưởng thức ẩm thực).
4. Đưa ra 01 lời nhắc văn minh & trách nhiệm (nhấn mạnh Đắk Lắk không cưỡi voi, giữ gìn môi trường thác ghềnh hoặc xin phép khi vào nhà dài).

Hãy trả về DUY NHẤT một đối tượng JSON hợp lệ theo đúng cấu trúc sau (không kèm markdown ngoài JSON):
{{
  "selected_code": "A",
  "reasoning": "Lời giải thích vì sao chọn phương án này...",
  "practical_tip": "Lời khuyên thực địa hữu ích...",
  "responsible_reminder": "Lời nhắc ứng xử văn hóa & bảo tồn..."
}}
"""

    env = os.environ.copy()
    # Key do mediakit tự nạp từ môi trường/THUCCHIEN_KEY_FILE theo quy chế;
    # backend không nhận hay lưu key từ trình duyệt và không ghi key vào mã nguồn.

    python_bin = str(BASE_DIR / ".venv" / "bin" / "python")
    if not os.path.exists(python_bin):
        python_bin = str(REPO_DIR / ".venv" / "bin" / "python")
    if not os.path.exists(python_bin):
        python_bin = "python3"

    cmd = [
        python_bin,
        str(BASE_DIR / "tools" / "mediakit.py"),
        "chat",
        "--model", model,
        "--temperature", "0.4",
        "--max-tokens", "800",
        "--json-mode",
        "--prompt", prompt
    ]

    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=12,
            cwd=str(BASE_DIR),
            env=env
        )
        
        if proc.returncode != 0:
            return fallback_ai_response(options, pref, error_note=f"Gateway trả về lỗi (code {proc.returncode})")

        output_text = proc.stdout.strip()
        # Tìm khối JSON trong output nếu có
        start_idx = output_text.find("{")
        end_idx = output_text.rfind("}")
        if start_idx != -1 and end_idx != -1:
            json_str = output_text[start_idx:end_idx+1]
            data = json.loads(json_str)
            code = data.get("selected_code", "").upper()
            if code not in ["A", "B", "C"]:
                code = "A"
            return {
                "success": True,
                "is_fallback": False,
                "selected_code": code,
                "reasoning": data.get("reasoning", "Phương án được AI tối ưu dựa trên sở thích và dự toán của bạn."),
                "practical_tip": data.get("practical_tip", "Nên khởi hành sớm vào buổi sáng để tận hưởng không khí trong lành của cao nguyên."),
                "responsible_reminder": data.get("responsible_reminder", "Chung tay bảo tồn đàn voi Tây Nguyên: Trải nghiệm ngắm voi tự nhiên, tuyệt đối không tham gia cưỡi voi.")
            }
        else:
            return fallback_ai_response(options, pref, error_note="Không đọc được cấu trúc JSON từ AI")
            
    except subprocess.TimeoutExpired:
        return fallback_ai_response(options, pref, error_note="AI phản hồi quá 12 giây, hệ thống kích hoạt phương án quy tắc tự động")
    except Exception as e:
        return fallback_ai_response(options, pref, error_note=str(e))

def fallback_ai_response(options, pref, error_note=""):
    """
    Quy tắc chọn phương án fallback khi AI không khả dụng, đảm bảo tính liên tục của trải nghiệm.
    """
    pref_lower = (pref or "").lower()
    selected_code = "A"
    if any(k in pref_lower for k in ["văn hóa", "cồng chiêng", "di sản", "lịch sử", "buôn"]):
        selected_code = "B"
    elif any(k in pref_lower for k in ["thiên nhiên", "thác", "sinh thái", "voi", "rừng"]):
        selected_code = "C"

    return {
        "success": True,
        "is_fallback": True,
        "error_note": error_note,
        "selected_code": selected_code,
        "reasoning": f"Hệ thống tự động đề xuất phương án {selected_code} theo bộ quy tắc tối ưu, cân đối hoàn hảo giữa sở thích '{pref}' và ngân sách nhóm.",
        "practical_tip": "Nên mang theo áo khoác nhẹ vì biên độ nhiệt ngày và đêm ở Đắk Lắk chênh lệch khá lớn.",
        "responsible_reminder": "Tôn trọng không gian văn hóa cồng chiêng và nếp sống nhà dài bản địa; tuân thủ mô hình du lịch ngắm voi thân thiện không cưỡi voi."
    }
