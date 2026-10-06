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
python server/app.py
```

Mở `http://127.0.0.1:8000`.
