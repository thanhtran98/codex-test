# QA — Poster "Đội mũ bảo hiểm" (bản v1 hoàn chỉnh)

File kiểm: `out/final/poster-doi-mu-bao-hiem.png` — 1080×1350, PNG 8-bit, do `shot` xuất.
Người kiểm: agent (nhìn ảnh trực tiếp). `mediakit review` CHƯA chạy được vì gateway trả 401.

## 1. Đúng đề
| Mã | Yêu cầu | Kết quả |
|---|---|---|
| R1 | Poster dọc 1080×1350 | ĐẠT (`file` xác nhận 1080 x 1350) |
| R2 | Chiến dịch "Đội mũ bảo hiểm", có dấu ấn đài | ĐẠT (dải trên: "ĐÀI TRUYỀN HÌNH · CHIẾN DỊCH AN TOÀN GIAO THÔNG") |
| R3 | Hướng học sinh cấp 3 | ĐẠT (kicker "HỌC SINH CẤP 3 · XE ĐẠP ĐIỆN VÀ XE MÁY", giọng teen) |
| R5 | Chữ tiếng Việt có dấu, đúng chính tả | ĐẠT (đã soát từng dòng, xem mục 2) |
| R6 | Thông điệp đội mũ + cài quai | ĐẠT (headline, câu chốt, 3 bullet) |
| R7 | Giọng teen, không lên gân | ĐẠT ("Chuyện nhỏ mà chất", "quyết định của tớ") |
| R8 | CTA + hashtag | ĐẠT |
| R9 | Không bịa số liệu | ĐẠT (poster không có con số nào) |
| R10 | Phương án cho feed | CHƯA (bản vuông để ở bước sau, miễn phí) |
| R1b | Thông điệp chính đọc được trong 3 giây | ĐẠT (headline lớn, tương phản cao, đọc ngay) |

## 2. Chữ và hình
- Chép lại chữ trên poster (tự đọc): `ĐÀI TRUYỀN HÌNH · CHIẾN DỊCH AN TOÀN GIAO THÔNG` / `HỌC SINH CẤP 3 · XE ĐẠP ĐIỆN VÀ XE MÁY` / `ĐỘI MŨ ĐI, CHUYỆN NHỎ MÀ CHẤT` / `Đội mũ — cài quai — đi đúng luật` / `Không phải vì bị nhắc, mà vì bạn quan trọng với người ở nhà.` / `1 Chọn mũ vừa đầu` / `2 Cài quai qua cằm` / `3 Chở đúng số người` / `Đội mũ là quyết định của tớ. Còn bạn?` / `#ĐỘI MŨ` / `#ĐộiMũBảoHiểm` / `#AnToànGiaoThông`.
- Dấu tiếng Việt: đủ và đúng (Ộ, Ũ, Ệ, Ẩ, Ậ, Ắ, Ớ, Ệ, Ằ, Ộ, Ắ...). Không thấy lỗi dấu.
- Tràn lề: không. Lề an toàn 65px (≈6%); đã sửa lỗi tràn ở bản v1.
- Tương phản: chữ trắng/đỏ/vàng trên nền xanh đậm, đủ đọc; khối CTA có nền vàng đặc.
- Không có chữ, logo, người thật, thương hiệu thật do model sinh ra — bản này **không dùng AI**, toàn bộ hình là vector SVG + CSS.
- Không có quốc kỳ, bản đồ, địa danh, ngày tháng.
- Logo: đề không cung cấp ⇒ đã chừa vùng góc trên trái, chưa chèn gì giả.

## 3. An toàn và file nộp
- Nội dung an toàn, không cam kết y tế/tài chính; thuần phong mỹ tục.
- `out/final/` chỉ chứa 1 file nộp. Không có key/token.
- Đã kiểm `grep -ril "aitc_\|THUCCHIEN_API_KEY" out/final` → không kết quả.

## 4. Việc còn lại
- `mediakit review` (QA bằng model thị giác) — chờ gateway thật.
- Nâng cấp nền bằng ảnh AI (`wan2.7-image` hoặc `nano-banana-2`) khi có gateway — thay lớp nền vector, giữ nguyên chữ HTML.
- Bản vuông 1080×1080 cho feed (P2).
