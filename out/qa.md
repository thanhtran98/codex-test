# QA — Sản phẩm MVP "Đắk Lắk Ơi"

**Ngày kiểm tra:** 06/10/2026, phiên thực thi MVP local.
**Phạm vi:** kiểm thử backend/engine, giao diện desktop và hồ sơ tối thiểu.
**Kết luận:** MVP chạy được cục bộ; CHƯA đạt nghiệm thu nộp bài vì còn thiếu live URL,
repo BTC hợp lệ và bằng chứng gọi AI thật qua gateway (key hiện báo 401 do sai loại key).

## 1. Đã kiểm và đạt (local)

- Engine sinh 3 phương án cho 1–8 người, 1–3 ngày; công thức tiền khớp:
  đêm = ngày − 1, phòng = ceil(người/2), dự phòng = 8% cơ sở.
- API `/api/lap-lich` trả đúng cấu trúc; `/api/doi-diem` tính lại tiền và lịch.
- Giao diện hai cột, tiếng Việt đủ dấu, font Be Vietnam Pro phục vụ nội bộ (`chung-khao/assets/fonts/`).
- Form 4 đầu vào bắt buộc; hiển thị 3 thẻ chi phí, lịch từng ngày, trạng thái đủ/vượt ngân sách.
- Test trình duyệt 1440×900: không lỗi console, không lỗi JS, không tràn chính tả (screenshot `out/work/screenshot/desktop-1440x900.png`).
- Test tự động `chung-khao/server/tests/test_engine.py` đạt toàn bộ.
- Không có key/token trong `out/final/` (xem mục 4).

## 2. Chưa đạt / còn thiếu

- **Live URL:** chưa có (`out/final/live-url.txt` đang ghi "CHƯA CÓ").
- **Repo BTC:** chưa xác minh repo do BTC quản lý; repo hiện tại là repo làm việc cá nhân.
- **AI thật:** gateway trả 401 với thông báo "LiteLLM Virtual Key expected. Received=aitc…, expected to start with 'sk-'". Key đang nạp là token log `aitc_...`, chưa phải key gateway `sk-...`. Cần người dùng cấp key `sk-...` vào `THUCCHIEN_API_KEY` (host/môi trường) rồi chạy lại `mediakit doctor`.
- **Ảnh minh họa:** chưa có (P1, không bắt buộc P0).
- **Deploy:** chưa deploy backend Flask lên host; chưa kiểm tra cold start/công khai 4 tuần.

## 3. Fallback đã xác nhận

- Khi AI lỗi (returncode 1 do 401), backend trả `is_fallback=true`, `selected_code` theo
  quy tắc sở thích, UI hiển thị "Gợi ý theo quy tắc (AI chưa trả kết quả)". Lập lịch vẫn dùng được.

## 4. Rà soát bí mật

- `grep -ril "aitc_\|THUCCHIEN_API_KEY" out/final` — không có kết quả.
- Đã gỡ key `sk-...` hardcode khỏi `chung-khao/server/gateway.py` (trước đó tồn tại trong phiên thực thi).
- Không đọc/ghi `.env` hay thư mục chứa key; không in key.

## 5. Việc cần làm tiếp

1. Người dùng cấp key gateway `sk-...` vào biến môi trường host và chạy `mediakit doctor`
   để xác minh key/model thật.
2. Deploy lên host hỗ trợ Python (ưu tiên Render), điền live URL và repo BTC vào `out/final/`.
3. Chạy lại `mediakit spend` để có chi phí đội thực tế.
4. Đối chiếu ma trận R1–R11, C1–C4, D1–D4 trong `out/brief.md` sau khi có live URL và AI thật.
