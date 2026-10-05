# PLAN — Poster dọc 1080×1350 cho chiến dịch "Đội mũ bảo hiểm"

## 0. Chặn kỹ thuật phát hiện khi kiểm tra máy (cần bạn bật đèn xanh)
Chạy `mediakit doctor` và khảo sát máy, có 4 điểm phải xử lý TRƯỚC khi dựng:

1. **Gateway trả 401.** `spend` báo: key gửi lên là `aitc…8b75` nhưng gateway đòi key bắt đầu bằng `sk-`.
   ⇒ Key đang đặt trong biến môi trường chưa đúng loại, hoặc đây là token AI-Log chứ không phải key gateway.
   **Cần bạn đặt lại `THUCCHIEN_API_KEY` cho đúng key `sk-...` của BTC.** Chưa có bước này thì mọi lệnh sinh ảnh đều hỏng.
2. **Thiếu `playwright` + Chromium.** Lệnh `shot` (HTML→PNG) chạy bằng `pw.chromium.launch()`; máy chưa có gói này.
   ⇒ Cần cài: `pip install playwright` và `python -m playwright install chromium` (máy đã có sẵn Google Chrome nên có phương án dự phòng).
3. **Thiếu ffmpeg/ffprobe.** Chỉ cần cho video/`sheet`/`mux`; poster không dùng. Chưa cài, để nguyên.
4. **`assets/fonts/` trống.** Skill yêu cầu Be Vietnam Pro hoặc Noto Sans để chữ có dấu chuẩn.
   ⇒ Cần tải 1 font tiếng Việt (.ttf/.woff2) vào `assets/fonts/`. Phương án chữa cháy: dùng `Arial Unicode.ttf` có sẵn trên macOS (đủ dấu nhưng kém "chất" hơn).

## 1. Sản phẩm giao
| Mã | File | Kích thước | Ghi chú |
|---|---|---|---|
| P1 | `out/final/poster-doi-mu-bao-hiem.png` | 1080×1350 | Bản nộp chính |
| P2 | `out/final/poster-doi-mu-bao-hiem-vuong.png` | 1080×1080 | Tuỳ chọn cho feed |

## 2. Các bước và thời gian dự kiến
| # | Việc | Công cụ / model | Thời gian |
|---|---|---|---|
| 1 | Duyệt brief + plan (bạn) | — | ~5 phút |
| 2 | Sửa chặn kỹ thuật (key, playwright, font) | pip / tải font | 5–10 phút |
| 3 | Dựng **bản hoàn chỉnh đầu tiên** (nền 1 ảnh nháp + chữ HTML) vào `out/final/` | `image` `nano-banana-2-lite` + `shot` | 10–15 phút |
| 4 | Sinh 1–2 phương án nền tốt hơn, so và chọn | `image` `nano-banana-2` | 10–15 phút |
| 5 | Dựng bản cuối, chỉnh phân cấp chữ, tương phản | HTML/CSS + `shot` | 15–20 phút |
| 6 | QA: `review` + mắt người + ma trận tuân thủ → `out/qa.md` | `review` | 10 phút |
| 7 | (Tuỳ chọn) bản vuông P2 | `shot` | 5 phút |

Tổng ≈ **55–75 phút** sau khi gỡ chặn. Bản hoàn chỉnh đầu tiên có trước mốc 30% thời gian.

## 3. Chi phí dự kiến
| Khoản | Đơn giá | SL | Thành tiền |
|---|---|---|---|
| Ảnh nháp nền | `nano-banana-2-lite` $0.0336 | 2 | $0.0672 |
| Ảnh nền chính | `nano-banana-2` $0.0672 | 2 | $0.1344 |
| `review` QA | theo token (rất nhỏ) | 2 | ≈$0.01 |
| **Cộng** | | | **≈$0.21** |
| P3 `mediakit search` (tuỳ chọn) | theo token | 1 | ≈$0.02–0.05 |

**Ngân sách hiện tại:** key diễn tập $1/key thi $50. `mediakit spend` chưa đọc được do lỗi 401 ⇒ chưa có số thật, sẽ chạy lại sau khi sửa key.
Toàn bộ nằm trong hạn mức; **poster này không tốn tiền video.**

## 4. Bố cục phác (1080×1350, lề an toàn ≥6% ≈ 65px)
- Dải trên (y 0–70): nhãn đài, chữ nhỏ, trên nền gradient tối.
- Khối ảnh chủ đạo (y 70–820): bạn trẻ đội mũ, tay cài quai, doodle bay quanh; **không chữ trong ảnh**.
- Headline (y 820–1010): `ĐỘI MŨ ĐI, CHUYỆN NHỎ MÀ CHẤT`, chữ lớn, có khối nền để đủ tương phản.
- Câu chốt: `Đội mũ — cài quai — đi đúng luật` (dải màu).
- 3 bullet việc đúng + CTA: `Đội mũ là quyết định của tớ. Còn bạn?`
- Đáy (y 1250–1290): hashtag.
- Vùng dành sẵn cho logo thật: nếu bạn cung cấp sau, chèn nguyên bản vào góc trên trái.

## 5. Cần bạn quyết khi duyệt
1. Đồng ý hướng A (nét bút và ước mơ) không, hay đổi sang B/C?
2. Bộ lời viết ở mục 6 của brief có dùng được không (đặc biệt headline và câu chốt)?
3. Cho phép cài `playwright` + Chromium và tải 1 font tiếng Việt vào `assets/fonts/`?
4. Có cần P2 (bản vuông cho feed) và P3 (thêm số liệu có nguồn) không?
5. Bạn có logo/kênh/slogan/số liệu thật để mình chèn nguyên bản không? (nếu có, bỏ vào `assets/input/`)
