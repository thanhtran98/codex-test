---
name: comic-story
description: Làm truyện tranh, storyboard, truyện ảnh hoặc chuỗi ảnh kể chuyện nhiều khung/nhiều trang cho chiến dịch truyền thông, giữ nhân vật và phong cách nhất quán, bóng thoại tiếng Việt bằng HTML. Dùng khi đề yêu cầu truyện, comic, storyboard, câu chuyện bằng hình.
---
# Truyện tranh / chuỗi ảnh kể chuyện
Khó nhất là nhất quán nhân vật và chữ có dấu. Giải pháp: khóa phong cách bằng một câu cố định, dùng ảnh tham chiếu `--ref`, và để HTML vẽ mọi bóng thoại.

1. **Kịch bản** (`out/work/story.md`): mở – thân – kết; thông điệp truyền thông nằm ở khung cuối kèm CTA nếu là quảng bá. Mặc định 1 trang 4–6 khung (hoặc theo đề). Mỗi khung: cảnh, hành động, góc máy, thoại (≤ 12 từ mỗi bóng).
2. **Hồ sơ nhân vật** (`out/work/characters.md`): mỗi nhân vật có ngoại hình cố định (tuổi, tóc, trang phục và màu, đặc điểm dễ nhận). Tạo MỘT câu "khóa phong cách" (nét vẽ, bảng màu, ánh sáng) và dán nguyên văn vào mọi prompt.
3. **Ảnh chuẩn nhân vật**: sinh 1 ảnh cho từng nhân vật (nền trơn, tư thế đứng, `nano-banana-2`). Duyệt rồi dùng ảnh này làm `--ref` cho mọi khung sau. Nếu đề có sẵn mascot/nhân vật thì dùng chính ảnh đó.
4. **Từng khung**: `mediakit image "<khóa phong cách>. <mô tả nhân vật>. <hành động, góc máy>. no text, no speech bubbles, no letters" --ref nhanvat.png --ratio <tỷ lệ khung>`. Tối đa 2 lần sinh lại mỗi khung (ngân sách). Nhân vật lệch nhiều thì sinh lại với `--ref`, đừng chấp nhận.
5. **Dàn trang bằng HTML**: CSS grid cho các khung, viền khung, bóng thoại và chú thích bằng HTML/SVG, font có dấu trong `assets/fonts/`. Mỗi trang một `.page` kích thước cố định.
6. **Xuất**: PNG từng trang (`shot ... --out out/final/trang1.png`) và một PDF gộp nếu đề cần (`shot truyen.html --out out/final/truyen.pdf --width W --height H`, với `.page{page-break-after:always}`).
7. Chạy `$qa-checklist`: nhân vật nhất quán qua các khung, thoại đọc được, đúng thứ tự đọc, bóng thoại không che mặt nhân vật.
