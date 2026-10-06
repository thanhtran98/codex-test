# Vòng chung khảo — Đắk Lắk Ơi

Thư mục nộp bài / làm việc cho đội **AGENT FORGE** (`AITC-987`).

## Hướng dẫn

- Toàn bộ mã nguồn chạy ứng dụng nằm trong thư mục này.
- Chạy ứng dụng từ thư mục này để các đường dẫn dữ liệu và gateway hoạt động đúng.
- Không đẩy secret (API key, `.env`, password) lên repo.

```
chung-khao/
├── api/               ← điểm vào triển khai Vercel
├── app/               ← giao diện, dữ liệu và ảnh
├── assets/fonts/      ← font giao diện
├── server/             ← Flask API và bộ lập lịch
├── tools/              ← gateway mediakit của BTC
├── requirements.txt
└── README.md           ← file này
```

## Chạy cục bộ

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python server/run_local.py
```

Mở `http://127.0.0.1:8000`.


## Cấu hình hỏi đáp

Hộp hỏi đáp `/api/chat` dùng API `http://117.1.150.235:31000/v1`, model `deepseek-v4.1-flash`.
Chạy `python3 server/run_local.py` và nhập khóa khi được hỏi; nội dung nhập được ẩn, không ghi xuống tệp.
Khóa chỉ tồn tại trong tiến trình, cần nhập lại khi khởi động lại máy chủ.
Có thể cấu hình từ môi trường triển khai qua `CHAT_API_KEY`, `CHAT_API_BASE_URL`, `CHAT_MODEL`.
Trình duyệt chỉ gọi API nội bộ `/api/chat`, không nhận khóa.
Chức năng nút “Lấy gợi ý AI” của bộ lập lịch giữ cấu hình riêng trong `server/gateway.py`.
