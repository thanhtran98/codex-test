# Brief chốt để duyệt — Trợ lý Du lịch Đắk Lắk AI

**Phiên bản:** thẩm định ngày 06/10/2026. **Trạng thái:** chờ người dùng duyệt trước khi thực thi.
**Tên sản phẩm:** Đắk Lắk Ơi. **Dòng mô tả luôn đi kèm:** Trợ lý Du lịch Đắk Lắk AI.
**Thông điệp:** Dệt hành trình, rõ chi phí.
**Tài liệu thực thi:** [Kế hoạch](plan.md). **Kiểm tra tài liệu:** [QA](qa.md).

## 1. Căn cứ và tài nguyên

Nguồn yêu cầu chính là `Chi tiết bài thi Vòng 2 - Thực chiến AI.html`, các mục “Hướng dẫn thi”, “Đề thi & Nội dung”, “Nộp Bài” và hộp xác nhận nộp bài. Hai nghiên cứu đầu vào là bản brief/kế hoạch trước thẩm định và `review_idea.md`. Bản phản biện là ý kiến tư vấn, không phải nguồn xác nhận dữ kiện du lịch hay barem chấm điểm.

| Tài nguyên | Có gì và cách sử dụng |
|---|---|
| Đề thi | Website desktop tiếng Việt; bốn đầu vào bắt buộc; yêu cầu lịch trình, thông tin tin cậy và live URL |
| Hạ tầng BTC | Hai key dùng chung hạn mức 50 USD; repo trong tổ chức GitHub của BTC; tài khoản commit/push đã đăng ký |
| Logo, ảnh, slogan, dữ liệu du lịch | Không thấy bộ tài nguyên riêng cho sản phẩm trong đề; `assets/input/` chưa có tài nguyên sử dụng được cho chủ đề này |
| Font sẵn có | Be Vietnam Pro trong `assets/fonts/`; dùng đủ tập ký tự Latin và tiếng Việt, kiểm tra giấy phép khi đóng gói |
| Tài liệu địa phương | Chưa có bộ nguồn đã kiểm chứng. Phải thu thập qua `mediakit search` và lưu phần công khai trong `assets/input/`, kèm URL, ngày nguồn và ngày tra cứu |
| Tệp đề gốc | Có dữ liệu xác thực riêng của đội; không sao chép vào thư mục tài nguyên công khai, bản nộp hoặc commit |

Không coi ngân sách 50 USD được cấp ban đầu là số dư hiện tại. Không đưa thông tin xác thực vào tài liệu hay giao diện.

## 2. Yêu cầu chính thức và lựa chọn của đội

Các mã dưới đây thay thế hệ mã cũ. “Bắt buộc” là yêu cầu trực tiếp; “bối cảnh đề” là mục tiêu sản phẩm cần thể hiện, không tự diễn giải thành một hệ thống quản lý đầy đủ.

| Mã | Yêu cầu | Căn cứ / tính chất |
|---|---|---|
| R1 | Một website desktop hiện đại, trực quan, thẩm mỹ, thân thiện | Đề — bắt buộc |
| R2 | Giới thiệu văn hóa và thiên nhiên Đắk Lắk **hiện tại**, phục vụ du khách trong và ngoài nước | Đề — bắt buộc; phạm vi địa lý phải xác minh |
| R3 | Giải quyết “Đi đâu – Ăn gì – Chi phí thế nào” qua vài thao tác | Đề — bắt buộc |
| R4 | Nhận số người, số ngày, ngân sách VND, sở thích | Đề — bắt buộc |
| R5 | Lịch trình hợp lý, minh bạch và khả thi trước khi đi | Đề — bắt buộc |
| R6 | Thông tin đầy đủ, tin cậy, bố cục logic | Đề — bắt buộc |
| R7 | Ngôn ngữ tiếng Việt | Đề — bắt buộc; tiếng Anh không được yêu cầu |
| R8 | Sản phẩm sáng tạo mới với AI qua API được cấp | Đề — bắt buộc; đội chọn có AI hoạt động ngay trong sản phẩm để thể hiện rõ vai trò |
| R9 | Hợp pháp, phù hợp giáo dục và thuần phong mỹ tục; không sao chép sản phẩm sẵn có | Đề — bắt buộc |
| R10 | Cá nhân hóa theo nhu cầu, sở thích và ngân sách | Nội dung và bối cảnh đề |
| R11 | Hỗ trợ điều phối luồng khách, bảo tồn văn hóa, chuyển đổi số; tạo cầu nối doanh nghiệp/cơ quan quản lý | Bối cảnh đề; thể hiện bằng chức năng có giới hạn và giải thích được |
| C1 | Mọi năng lực AI trong quá trình thi đi qua gateway BTC, không AI ngoài hay tính năng AI tích hợp bị cấm | Hướng dẫn — bắt buộc rõ ràng |
| C2 | Toàn bộ quá trình làm bài trên repo BTC; commit/push bằng tài khoản đã đăng ký | Hướng dẫn — bắt buộc rõ ràng |
| C3 | Tự tạo trong ca thi; không chép nguyên mẫu mã nguồn/template trên Internet | Hướng dẫn — bắt buộc rõ ràng |
| C4 | Chứng minh nguồn gốc bằng audit log gateway và lịch sử repo BTC | Hướng dẫn — bắt buộc rõ ràng |
| D1 | 120 phút thực hiện: 09:00–11:00 ngày 06/10/2026; thêm 10 phút nộp, hạn giao diện 11:10 | Đề và thông tin thời gian; chủ động hoàn tất sản phẩm trước 11:00 |
| D2 | Live URL duy trì ít nhất 4 tuần, link source trên repo BTC, tài liệu bổ sung | Mục nộp bài — bắt buộc |
| D3 | Trong 24 giờ từ khi kết thúc: video thuyết trình 3–6 phút và video ghi hình theo hướng dẫn BTC | Mục nộp bài — bắt buộc; dự kiến hạn 11:00 ngày 07/10/2026 |
| D4 | Không thể chỉnh sửa bài nộp sau xác nhận | Hộp xác nhận nộp bài — ràng buộc thao tác |

Không có barem điểm số chi tiết trong tệp đề. Mọi thứ tự ưu tiên trong kế hoạch là quyết định chuyên môn, không phải lời hứa về điểm của BGK.

## 3. Đối tượng, phạm vi và điều còn phải xác minh

- Đối tượng chính: người tự lên kế hoạch cho nhóm nhỏ, cần nhìn rõ lịch trình và tổng tiền. Không mặc định độ tuổi là yêu cầu của đề.
- Nhu cầu: nhập thông tin → có phương án → hiểu lý do và chi phí → đổi một lựa chọn → lưu/in hành trình.
- Bản đầu hỗ trợ nhóm 1–8 người lớn, 1–3 ngày; đây là giới hạn thử nghiệm của đội, hiển thị công khai. Không áp giá người lớn cho trẻ em một cách ngầm định.
- Ngân sách là **tổng ngân sách cả nhóm, toàn chuyến trong vùng đã chọn**; chưa gồm chi phí đến/rời vùng, mua sắm và dịch vụ ngoài danh sách. Hiện rõ trước khi nhập tiền.
- Phạm vi “Đắk Lắk hiện tại” là cổng kiểm tra dữ liệu: phải đối chiếu nguồn hành chính chính thức cập nhật về sắp xếp địa giới, đặc biệt quan hệ với địa bàn Phú Yên trước đây. Chưa tra cứu được trong phiên thẩm định; không tự coi danh sách điểm quanh Buôn Ma Thuột là đại diện đủ toàn tỉnh.
- Nếu nguồn xác nhận phạm vi có cả cao nguyên và duyên hải, danh mục giới thiệu phải có cả hai; chia vùng để lập lịch trình riêng, không ghép chuyến xuyên vùng khi chưa có dữ liệu di chuyển. Mỗi vùng có điểm bắt đầu/kết thúc và giả định lưu trú rõ ràng. Không sinh bản đồ.
- Giờ mở cửa, giá, tên đơn vị hành chính mới, khoảng cách, hoạt động với voi, món ăn và quy tắc văn hóa cụ thể đều chờ kiểm chứng. Khi thiếu, ghi đúng “Chưa xác minh” hoặc loại khỏi lịch trình tự động; không điền số 0 để thay cho chưa biết.

## 4. Ba hướng ý tưởng và quyết định

| Hướng | Giá trị | Quyết định |
|---|---|---|
| Dệt hành trình | Cảm xúc địa phương, gợi cá nhân hóa; có nguy cơ trang trí lấn át chức năng | Giữ làm câu chuyện và điểm nhấn thị giác; timeline thẳng, dễ đọc |
| Sổ chi phí minh bạch | Giải quyết rào cản quyết định chuyến đi; dễ chứng minh bằng thao tác | Chọn làm nền tảng chức năng, hiển thị cả giả định và khoản chưa bao gồm |
| Buôn làng kể chuyện | Tạo chiều sâu văn hóa nhưng cần nguồn và quyền sử dụng câu chuyện/nhân vật | Chưa triển khai nhân vật kể chuyện trong ca thi |

**Chốt:** “Đắk Lắk Ơi — Trợ lý Du lịch Đắk Lắk AI”: công cụ lập hành trình theo vùng, minh bạch dự toán, AI chọn và giải thích phương án từ dữ liệu đã kiểm tra. Bộ quy tắc quyết định tính khả thi và tính tiền. Họa tiết hình học chỉ là trang trí tự thiết kế, không tự nhận là hoa văn Êđê chuẩn hay bằng chứng bảo tồn văn hóa.

Giữ tên thân thiện vì đề không yêu cầu hình ảnh một cổng chính quyền. Không đổi sang tên hoặc lời hứa hàm ý đại diện chính thức cho tỉnh. Slogan mới có 7 từ, không phải slogan do đề cung cấp.

## 5. Nội dung giao diện đã chốt

| Vị trí | Lời viết |
|---|---|
| Tên / mô tả | Đắk Lắk Ơi / Trợ lý Du lịch Đắk Lắk AI |
| Slogan | Dệt hành trình, rõ chi phí. |
| Dòng mở | Chọn gu khám phá. Xem lịch trình và dự toán cho cả nhóm. |
| Ngân sách | Ngân sách cả nhóm (VND) |
| Phạm vi tiền | Dự toán trong vùng đã chọn; chưa gồm chi phí đến/rời vùng và mua sắm. |
| Nút chính | Lập hành trình |
| Nút phụ | Đổi điểm · Xem cách tính · Xem nguồn · In / Lưu PDF |
| Kết quả ban đầu | Phương án theo quy tắc đã sẵn sàng. Đang lấy gợi ý AI. |
| AI thành công | AI đề xuất phương án này dựa trên sở thích của bạn. |
| AI không khả dụng | AI tạm thời chưa khả dụng. Bạn vẫn có thể xem và chỉnh phương án theo quy tắc. |
| Giá thiếu nguồn hiện hành | Ước tính để lập kế hoạch; cần xác nhận với đơn vị cung cấp. |
| Không đủ tiền | Chưa tìm được phương án phù hợp trong danh mục hiện có. Xem khoản chênh lệch và lựa chọn điều chỉnh. |
| Trách nhiệm | Xin phép trước khi chụp ảnh; tuân thủ hướng dẫn tại điểm đến; không chọn hoạt động cưỡi voi hoặc tiếp xúc động vật gây hại. |

Không có bộ đếm khách trực tuyến, biểu đồ mật độ thật, ưu đãi tự đặt hay huy hiệu chứng nhận. Không để AI tự viết “mẹo bản địa độc quyền”, giá hoặc địa chỉ không có trong nguồn.

## 6. Ma trận đáp ứng và bằng chứng phải có

| Mã | Sản phẩm / vị trí đáp ứng | Bằng chứng nghiệm thu |
|---|---|---|
| R1, R7 | Giao diện hai cột, tiếng Việt, chữ HTML/CSS với Be Vietnam Pro | Xem ở 1280×800 và 1440×900; bàn phím sử dụng được, không tràn |
| R2 | Thẻ khám phá theo vùng, nguồn địa giới hiện hành, nội dung văn hóa/thiên nhiên | Danh mục phủ vùng đã xác minh; ghi rõ vùng hỗ trợ lập lịch |
| R3, R4 | Form bốn đầu vào và lựa chọn vùng mặc định; kết quả có điểm đi, bữa ăn, dự toán | Một lần bấm ra đủ ba nhóm thông tin; kiểm tra đầu vào sai |
| R5 | Lịch trình theo cụm, thời lượng, chặng di chuyển, bữa ăn, khoảng nghỉ | Không chồng giờ; có nguồn/giả định cho chặng và giờ hoạt động |
| R6 | Nguồn ở từng dữ kiện, đơn vị tính và nhãn giá | Không dùng “đã xác minh” bao trùm bản ghi khi chỉ biết tên địa điểm |
| R8, R10 | AI chọn phương án hợp lệ và giải thích; engine kiểm tra, tính tiền | Một lượt gateway thật được kiểm chứng, đổi sở thích có tác động đến kết quả |
| R9 | Nội dung có nguồn, bộ lọc hoạt động không phù hợp, gợi ý ứng xử | Không gắn nhãn chứng nhận hoặc cam kết địa phương chưa được xác nhận |
| R11 | Nút đổi sang điểm cùng vùng; tóm tắt phân bổ điểm dừng của hành trình đang xem; liên kết nguồn/đơn vị công khai khi có | Thay điểm phải tính lại tiền và lịch; ghi rõ không phản ánh lượng khách thực tế |
| C1–C4 | Quy trình gateway, repo BTC, nguồn gốc thay đổi | Xác nhận hạ tầng hợp lệ, commit và audit log thực tế; chưa có thì chưa đạt |
| D1–D2, D4 | Live URL, repo, hồ sơ nộp và kiểm tra trước xác nhận | Kiểm tra ẩn danh; có người chịu trách nhiệm duy trì 4 tuần; biên nhận nộp |
| D3 | Video thuyết trình và ghi hình | Nộp trong hạn riêng, không tính ảnh AI/video du lịch là thay thế |

**Trạng thái:** ma trận trên là tiêu chí cần thực hiện, chưa phải bằng chứng sản phẩm đã đạt. Phiên này chỉ chốt tài liệu; chưa sản xuất, triển khai hay nộp bài.
