---
name: qa-checklist
description: Kiểm tra chất lượng trước khi nộp bất kỳ sản phẩm truyền thông nào (video, poster, truyện, văn bản): đối chiếu ma trận yêu cầu của đề, dấu tiếng Việt, bố cục, độ dài, nội dung an toàn, file nộp. Dùng trước khi báo hoàn thành.
---
# QA trước khi nộp
Với mỗi file trong `out/final/`, kiểm tra rồi ghi kết quả vào `out/qa.md` (mục nào đạt/không đạt, đã sửa gì).

## 1. Đúng đề
- [ ] Đối chiếu từng dòng R1, R2... trong ma trận tuân thủ của `out/brief.md`: yêu cầu nào chưa có bằng chứng thì chưa xong.
- [ ] Đúng loại file, kích thước/độ dài, số lượng, tên file theo đề.
- [ ] Tài nguyên do đề cung cấp (logo, slogan, số liệu) có mặt, đúng nguyên bản.
- [ ] Thông điệp chính rõ trong 3 giây đầu; có lời kêu gọi hành động nếu là quảng bá.

## 2. Chữ và hình
- [ ] Chạy `mediakit review <ảnh>` (video: ảnh từ `mediakit sheet`) VÀ tự nhìn: chữ tiếng Việt đúng chính tả, đủ dấu, không tràn lề, không bị che, đủ tương phản.
- [ ] Không có chữ, logo, người thật, thương hiệu thật bị model vô tình sinh ra.
- [ ] Việt Nam: không có quốc kỳ/bản đồ do AI vẽ (hoặc đã dùng file chuẩn do đề cung cấp); địa danh, tên riêng, ngày tháng đúng; trang phục, bối cảnh phù hợp.
- [ ] Số liệu có nguồn trong brief.
- [ ] Truyện/chuỗi ảnh: nhân vật nhất quán qua các khung, thứ tự đọc đúng.

## 3. Video
- [ ] Âm thanh không vỡ, không cắt cụt; giọng đọc rõ; không còn âm gốc lẫn vào; phụ đề khớp giọng; không khung hình lỗi (xem `sheet`); độ dài đúng (`ffprobe`).

## 4. An toàn và file nộp
- [ ] Nội dung không vi phạm pháp luật, thuần phong mỹ tục; không cam kết y tế/tài chính vô căn cứ.
- [ ] `out/final/` chỉ chứa file nộp. Tìm key và token: `grep -ril "aitc_\|THUCCHIEN_API_KEY" out/final` không ra kết quả; không có đường dẫn máy cá nhân trong sản phẩm.

Có mục không đạt: sửa rồi kiểm tra lại, tối đa 2 vòng; còn lỗi thì ghi rõ trong tóm tắt cuối.
