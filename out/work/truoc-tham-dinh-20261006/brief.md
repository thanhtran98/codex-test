# BRIEF — Vòng 2 Thực chiến AI: "Trợ lý Du lịch Đắk Lắk AI" (Web Desktop)

Ngày soạn: 06/10/2026 · Ca thi 09:00–11:00 · Hạn nộp 11:10 · Đội AGENT FORGE (Bảng 1)

## 0. Tài nguyên đề cung cấp
- Gateway BTC: 2 API key `sk-...` (đã có trong hồ sơ đề), hạn mức **$50/đội**.
- Repo GitHub do BTC tạo sẵn trong org BTC (bắt buộc làm bài trên đó, commit bằng tài khoản đã đăng ký).
- Đề KHÔNG cấp logo/ảnh/slogan/ số liệu cho chủ đề này → phải tự viết nội dung, số liệu phải có nguồn.
- MCP bên thứ ba (OpenAI/Anthropic/Perplexity/Tavily, mọi tunnel/proxy) bị CẤM.

## 1. Bảng yêu cầu
| Mã | Yêu cầu (trích đề) | Loại |
|---|---|---|
| R1 | Sản phẩm là **website desktop** "Trợ lý Du lịch Đắk Lắk AI", hiện đại, trực quan | RÕ |
| R2 | Giới thiệu trọn vẹn vẻ đẹp văn hóa – thiên nhiên Đắk Lắk **hiện tại** | RÕ |
| R3 | Giải bài toán **Đi đâu – Ăn gì – Chi phí thế nào** chỉ qua vài thao tác | RÕ |
| R4 | Nhận tối thiểu 4 đầu vào: số người, số ngày, **ngân sách (VND)**, sở thích | RÕ |
| R5 | Xuất ra **lịch trình hợp lý, minh bạch, khả thi** trước khi đi | RÕ |
| R6 | Thông tin đầy đủ, **tin cậy**, bố cục logic, giao diện thẩm mỹ, thân thiện | RÕ |
| R7 | Ngôn ngữ **tiếng Việt** | RÕ |
| R8 | Phải dùng AI thật qua **gateway BTC**; sáng tạo mới, không cover sản phẩm có sẵn | RÕ |
| R9 | Hợp pháp, giáo dục, phù hợp thuần phong mỹ tục | RÕ |
| R10 | Cá nhân hóa theo sở thích VÀ ngân sách (bối cảnh đề) | RÕ |
| R11 | Hỗ trợ địa phương **điều phối luồng khách + bảo tồn văn hóa** + chuyển đổi số (bối cảnh đề) | RÕ |
| R12 | Nộp **Live URL** (giữ ≥4 tuần) + link GitHub BTC + tài liệu bổ sung, trước 11:10 | RÕ |
| N1 | Không dùng AI tạo sinh tích hợp trong phần mềm thiết kế (Photoshop/Canva/CapCut…) | NGẦM |
| N2 | Không mở web AI ngoài; mọi prompt phải tạo trong ca thi | NGẦM |
| N3 | Không sao chép template/mã nguồn có sẵn trên Internet | NGẦM |
| N4 | Có audit log: commit/push bằng tài khoản đã đăng ký | NGẦM |
| N5 | Du khách trong VÀ ngoài nước (bối cảnh) → cần minh bạch, dễ đọc kể cả người ít tiếng Việt | NGẦM |
| N6 | Tài liệu nộp trong 24h: video thuyết trình 3–6 phút + video ghi hình theo BTC | NGẦM |

## 2. Đối tượng & thông điệp
- **Chính**: người 20–35 tuổi, du lịch tự túc, đi 2–4 người, ngân sách hữu hạn, lười gom thông tin rải rác.
- **Phụ**: gia đình có trẻ nhỏ; khách nước ngoài; cán bộ Sở VHTTDL/doanh nghiệp địa phương (đọc phần luồng khách).
- Xem ở đâu: mở web trên laptop trước chuyến đi 1–3 tuần; hay tra Google "lịch trình Đắk Lắk 3 ngày".
- Cần làm gì sau khi xem: tin vào con số → chốt lịch trình → lưu/in/chia sẻ.
- **Thông điệp chính**: *"Đắk Lắk dệt riêng hành trình cho bạn"* — mỗi con số đều có nguồn, mỗi ngày đều khả thi.

## 3. Ý tưởng — 3 hướng
**H1. "Bản đồ dệt thổ cẩm".** Insight: khách sợ lịch trình "trên giấy" không khớp thực tế. Ý tưởng lớn: mỗi ngày đi là một **dải thổ cẩm**, mỗi điểm dừng là một **hoa văn** — lịch trình vừa là kế hoạch vừa là vật kỷ niệm (in ra/in PDF). Hình chủ đạo: nền hoa văn hình học Êđê vẽ bằng CSS/SVG, ảnh thật Đắk Lắk làm điểm nhấn. → vừa "bảo tồn văn hóa" (R11) vừa khác biệt.

**H2. "Sổ chi tiêu minh bạch".** Insight: rào cản lớn nhất là TIỀN. Ý tưởng lớn: coi chuyến đi như một **bảng chi phí sống**, kéo ngân sách là lịch trình tự co giãn (bỏ/đổi điểm), mọi mục ghi rõ giá + nguồn. Mạnh về R5/R10 nhưng dễ khô khan, thiếu cảm xúc.

**H3. "Buôn làng kể chuyện".** Insight: khách muốn hiểu văn hóa thật, không phải check-in. Ý tưởng lớn: mỗi buôn là một **nhân vật kể chuyện** (già làng, nghệ nhân dệt, chủ vườn cà phê) dẫn khách đi. Rất cảm xúc nhưng khó đảm bảo "tin cậy, minh bạch chi phí" trong 120 phút.

**Chọn: H1 + vay phần "thanh ngân sách" của H2.** Lý do: bám đủ R1–R11, hình ảnh đặc trưng Đắk Lắk, dựng được bằng HTML/CSS (không phụ thuộc model vẽ chữ), và có điểm nhấn khác biệt cho BGK.

## 4. Lời viết
- Tên sản phẩm: **Đắk Lắk Ơi** — Trợ lý du lịch cá nhân hóa.
- Slogan (7 từ): **"Đắk Lắk dệt riêng hành trình cho bạn"**
- Tiêu đề trang chủ: "Đi đâu – Ăn gì – Tốn bao nhiêu: để Đắk Lắk Ơi lo."
- CTA: "Dệt hành trình của tôi" · "Đổi điểm này" · "Tải sổ tay PDF"

## 5. Ma trận tuân thủ (điền dần, QA đối chiếu)
| Yêu cầu | Đáp ứng bằng |
|---|---|
| R1 | Trang desktop 1 màn hình chính + khu kết quả, tối ưu ≥1280px |
| R2 | Hero ảnh thiên nhiên + mục "Văn hóa & Thiên nhiên" (buôn, thác, hồ, cà phê) |
| R3 | Form 4 ô → lịch trình + ăn uống + bảng chi phí trong 1 lần bấm |
| R4 | 4 input bắt buộc, có kiểm tra hợp lệ |
| R5 | Timeline theo ngày/khung giờ, khoảng cách, giờ mở cửa, chi phí, cảnh báo |
| R6 | Nguồn dữ liệu ghi trên từng số; nêu rõ "dữ liệu mẫu" nếu chưa xác minh |
| R7 | Toàn bộ UI + nội dung tiếng Việt có dấu |
| R8 | Gọi gateway BTC bằng `mediakit.py` (sinh nội dung/ảnh), có ảnh minh họa |
| R9 | Không hứa hẹn y tế/tài chính; tôn trọng văn hóa, cảnh báo điểm nguy hiểm |
| R10 | Trọng số sở thích + thanh ngân sách co giãn theo tổng tiền |
| R11 | "Chế độ địa phương": mật độ khách theo ngày, gợi ý đi lệch cao điểm |
| R12 | Live URL (Vercel/Cloudflare) + repo BTC + README |
| N1–N4 | Chỉ dùng công cụ CLI/BTC gateway; không copy template; commit tài khoản đã đăng ký |
| N5 | Nút đổi ngôn ngữ VI/EN tối giản (nếu kịp) |
| N6 | Kịch bản + video thuyết trình 3–6 phút (ngoài ca thi) |

## 6. Dữ kiện cần xác minh (bắt buộc `mediakit search` trước khi đưa vào web)
Danh sách điểm tham quan, giờ mở cửa, giá vé, khoảng cách, mùa đẹp/mùa mưa, món ăn đặc trưng, giá tham khảo. **Chưa xác minh thì ghi nhãn "Dữ liệu mẫu".**
