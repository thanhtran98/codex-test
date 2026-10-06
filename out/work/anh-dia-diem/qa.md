# Kiểm tra bổ sung ảnh địa điểm

- Đã rà soát 17 địa điểm: ban đầu 7 ảnh đang hiển thị, 10 vị trí trống.
- Đã bổ sung 8 ảnh tải từ internet và gắn 1 ảnh Chư Yang Sin có sẵn.
- Đạt: 16/16 ảnh đang gắn được giải mã thành công, trả HTTP 200 và có mô tả tiếng Việt.
- Đạt: kiểm tra thực tế trình duyệt, 16 ảnh có kích thước tự nhiên lớn hơn 0; không tràn ngang ở khung kiểm tra.
- Đạt: cú pháp JavaScript; 9 ảnh bổ sung có liên kết nguồn trên giao diện và bản ghi trong app/data/image-sources.json.
- Đã loại ảnh logo do nguồn Gia Long trả về và thay bằng ảnh thác từ Cục Du lịch Quốc gia.
- Còn thiếu: ảnh xác minh đúng thủy điện Buôn Trấp; không dùng ảnh hồ Ea Kao gần mục này trong bài gốc.
- Giấy phép tái sử dụng ảnh nguồn công khai chưa được xác minh, đã ghi trong dữ liệu nguồn.
- Không gọi model AI; không phát sinh chi phí AI trong lần bổ sung. Lệnh spend báo sổ cục bộ 0 USD; không đọc được ngân sách gateway.
- Kiểm tra thị giác thực hiện trực tiếp; không gọi mediakit review vì gateway không đọc được ngân sách.
