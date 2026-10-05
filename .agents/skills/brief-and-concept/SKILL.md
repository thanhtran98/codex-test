---
name: brief-and-concept
description: Biến đề bài truyền thông thành brief, ý tưởng, lời viết và ma trận tuân thủ yêu cầu; cũng dùng cho sản phẩm dạng văn bản (kịch bản, bài viết, caption, kế hoạch truyền thông). Dùng ở BƯỚC ĐẦU của mọi đề, trước khi sinh bất kỳ ảnh hay video nào.
---
# Brief, ý tưởng, lời viết
Bước này quyết định chất lượng. Phần lớn đội sẽ có cùng công cụ và cùng model; khác biệt nằm ở ý tưởng, lời văn tiếng Việt và độ bám đề.

1. **Bảng yêu cầu** (`out/brief.md`): trích từng yêu cầu của đề thành dòng R1, R2... gồm: loại sản phẩm, số lượng, kích thước/độ dài, ngôn ngữ, bắt buộc phải có (logo, slogan, số điện thoại, thông điệp), điều bị cấm, hạn nộp. Tách yêu cầu RÕ RÀNG khỏi yêu cầu NGẦM ĐỊNH (ví dụ: đúng đối tượng, phù hợp văn hóa).
2. **Đối tượng và thông điệp**: ai xem, họ xem ở đâu (mạng xã hội, TV, in), họ cần làm gì sau khi xem, giọng điệu. Chốt MỘT thông điệp chính.
3. **Dữ kiện**: nếu cần số liệu hoặc sự kiện thật, chạy `mediakit search`, ghi nguồn vào brief. Không có nguồn thì không dùng con số.
4. **Ý tưởng**: nêu 3 hướng, mỗi hướng 2 dòng (insight, ý tưởng lớn, hình ảnh chủ đạo). Chọn 1 hướng và nói rõ lý do; ưu tiên hướng cụ thể, gần gũi văn hóa Việt Nam, dễ làm đẹp bằng công cụ hiện có.
5. **Lời viết**: tiêu đề (ngắn, dễ nhớ), câu chốt/slogan (≤ 8 từ), nội dung phụ, lời kêu gọi hành động. Viết có dấu, đọc to một lần để kiểm tra nhịp và chính tả. Nếu đề đã cho sẵn slogan thì KHÔNG sửa.
6. **Ma trận tuân thủ**: bảng `Yêu cầu → sản phẩm nào, vị trí nào đáp ứng`. Ô nào còn trống là việc chưa làm. `$qa-checklist` sẽ đối chiếu lại bảng này.
7. **Sản phẩm dạng văn bản** (kịch bản, bài viết, caption, kế hoạch): viết thẳng vào `out/final/*.md` (hoặc định dạng đề yêu cầu), đúng độ dài, cấu trúc rõ, không lặp ý.

Gợi ý vận hành: bước này nên dùng model mạnh hơn mặc định (người dùng đổi bằng `/model`, ví dụ `gpt-6.1-sol`); chi phí token rất nhỏ so với ngân sách.
