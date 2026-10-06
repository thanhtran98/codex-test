# Đắk Lắk Ơi — Trợ lý Du lịch Đắk Lắk AI

Mã nguồn vòng chung khảo nằm trong thư mục [`chung-khao/`](chung-khao/).

Website desktop tiếng Việt giúp du khách giải bài toán **Đi đâu – Ăn gì – Chi phí thế nào**
qua vài thao tác. Giao diện giới thiệu điểm đến, món ăn và nguồn dữ liệu; bộ lập lịch
gọi backend Python để tạo 3 phương án hành trình, tính tiền minh bạch và có gợi ý AI.

## Chạy nhanh

```bash
cd chung-khao
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python server/app.py
```

Mở `http://127.0.0.1:8000`.

Để kích hoạt gợi ý AI và chat nổi, đặt biến môi trường `THUCCHIEN_API_KEY` (khóa gateway
do BTC cấp, có tiền tố theo quy định của gateway) trước khi chạy server. Backend gọi
`tools/mediakit.py chat` qua gateway duy nhất của BTC; không đưa khóa vào mã nguồn hay trình duyệt.

## Cấu trúc

- `chung-khao/app/` — giao diện và dữ liệu: `index.html`, `styles.css`, `app.js`, `chat.js`, `data/`, `images/`.
- `chung-khao/server/app.py` — Flask, kiểm tra đầu vào, giới hạn gọi, API.
- `chung-khao/server/engine.py` — nguồn duy nhất cho lịch trình và công thức tiền.
- `chung-khao/server/gateway.py` — gọi CLI mediakit chọn phương án, có fallback theo quy tắc.
- `chung-khao/server/chat_handler.py` — endpoint chat nổi gọi gateway BTC.
- `chung-khao/tools/mediakit.py` — CLI gateway BTC (được mở rộng thêm subcommand `chat`).
- `chung-khao/assets/fonts/` — font Be Vietnam Pro phục vụ nội bộ.

## API

- `GET /api/meta` — danh mục và nguồn.
- `POST /api/lap-lich` — tạo 3 phương án theo quy tắc (không tốn AI).
- `POST /api/tu-van` — AI chọn phương án và giải thích.
- `POST /api/doi-diem` — đổi điểm và tính lại tiền/lịch.
- `POST /api/chat` — hội thoại trợ lý.

## Kiểm thử

```bash
cd chung-khao
python server/tests/test_engine.py
```

## Ghi chú dữ liệu

Giá, giờ hoạt động và mô tả điểm đến là dữ liệu tham khảo, đối chiếu ngày 06/10/2026,
có thể thay đổi theo đơn vị cung cấp. Danh mục nguồn ở `chung-khao/app/data/sources.json`.
