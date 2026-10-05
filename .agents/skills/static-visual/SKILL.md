---
name: static-visual
description: Thiết kế sản phẩm hình tĩnh cho chiến dịch truyền thông: poster, tờ rơi, banner, ảnh bìa, thumbnail, infographic, carousel nhiều trang, có chữ tiếng Việt. Dùng khi đề yêu cầu ảnh ấn phẩm hoặc hình minh họa kèm chữ.
---
# Sản phẩm hình tĩnh
Quy trình: nền ảnh bằng AI + chữ và bố cục bằng HTML/CSS → chụp thành PNG/PDF. Đọc `$brief-and-concept` (đã có brief, lời viết) và `$gateway-quirks` trước.

## Kích thước thường dùng (`--width/--height`; tỷ lệ ảnh nền `--ratio`)
| Loại | Kích thước | Ảnh nền |
|---|---|---|
| Poster dọc | 1080×1350 | 3:4 (cover) |
| Story/Reel bìa | 1080×1920 | 9:16 |
| Bài đăng vuông | 1080×1080 | 1:1 |
| Banner/thumbnail ngang | 1920×1080 | 16:9 |
| A4 dọc in (150 dpi) | 1240×1754 | 3:4 |
| A5 dọc in | 874×1240 với `--scale 2` (ra 1748×2480) | 3:4 |
Theo kích thước đề yêu cầu nếu có.

## Các bước
1. Phác bố cục bằng lời: vùng nào là hình, tiêu đề, thông điệp phụ, CTA, logo. Chừa sẵn vùng trống cho chữ.
2. Sinh 2–3 phương án nền bằng `mediakit image` (`nano-banana-2-lite` để nháp); prompt có "no text, no letters, no watermark", mô tả chủ thể, ánh sáng, bảng màu, góc nhìn, vùng trống. Cần nhất quán thương hiệu/sản phẩm thì thêm `--ref` ảnh do đề cung cấp. Chọn 1 phương án, nâng cấp model nếu cần.
3. Dựng `out/work/<tên>.html`: nền dùng `background-image` (`background-size: cover`), chữ dùng `@font-face` trỏ `assets/fonts/` (Be Vietnam Pro hoặc Noto Sans). Phân cấp rõ: tiêu đề lớn, MỘT thông điệp chính, thông tin phụ, một CTA. Lề an toàn ≥ 6%. Chữ trên nền phức tạp phải có lớp phủ gradient hoặc khối màu để đủ tương phản. Logo/slogan của đề chèn nguyên bản.
4. Xuất: `python tools/mediakit.py shot out/work/<tên>.html --out out/final/<tên>.png --width 1080 --height 1350` (đuôi `.pdf` để ra PDF in).
5. Infographic/carousel: mỗi trang một HTML (hoặc một HTML nhiều `.page` có `page-break-after: always` khi xuất PDF), dùng chung CSS để nhất quán; mỗi trang một ý.
6. Chạy `$qa-checklist` (có `mediakit review` để bắt lỗi dấu).

## Chữ trong ảnh do model vẽ
Mặc định KHÔNG. Chỉ khi đội đã thử và xác nhận (ghi vào `AGENTS.md`) rằng Nano Banana vẽ đúng dấu tiếng Việt cho tiêu đề ngắn, mới được dùng cho tiêu đề lớn, và vẫn phải `review` từng chữ.
