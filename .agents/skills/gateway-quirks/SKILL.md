---
name: gateway-quirks
description: Quy tắc gọi gateway AI Thực Chiến (ảnh, ảnh tham chiếu, video Veo, giọng đọc, tra cứu, kiểm tra ảnh, chi phí, giới hạn tốc độ, lỗi 429). BẮT BUỘC đọc trước khi sinh ảnh, video, giọng nói, tra cứu hoặc chọn model cho bất kỳ sản phẩm truyền thông nào.
---
# Gateway AI Thực Chiến: điểm cần nhớ
Mọi việc gọi AI đi qua `python tools/mediakit.py <lệnh>`. Mỗi lệnh in đường dẫn file (hoặc văn bản) ra stdout và ghi `out/manifest.jsonl`.

## Lệnh
| Lệnh | Dùng để |
|---|---|
| `doctor` | Kiểm tra môi trường (key, ffmpeg, playwright, font, gateway). Không tốn tiền. |
| `image "<prompt>" --out out/work/x.png [--model nano-banana-2] [--ratio 3:4] [--ref a.png --ref b.png]` | Sinh ảnh. `--ref` giữ nhân vật/sản phẩm nhất quán. |
| `tts "<văn bản>" --out out/work/vo.mp3 [--model ...] [--voice Zephyr]` | Giọng đọc. |
| `video "<prompt>" --out out/work/c1.mp4 [--model veo-3.1-lite-generate-001] [--seconds 4\|6\|8] [--size 1280x720] [--image anh_dau.png]` | Sinh clip 4–8 giây. |
| `shot file.html --out out/final/x.png [--width 1080 --height 1350 --scale 1]` | HTML → PNG, hoặc `.pdf` để ra PDF. `--full` chụp cả trang dài. |
| `sheet video.mp4 --out out/work/sheet.png` | Lưới khung hình đều nhau để kiểm tra video. |
| `review a.png [b.png] [--question "..."]` | Model thị giác đọc ảnh: chép lại chữ, bắt lỗi dấu, bố cục. Dùng khi cần QA bằng "mắt". |
| `search "<câu hỏi>" [--engine gemini\|openai]` | Tra cứu dữ kiện có nguồn. CHƯA kiểm chứng với gateway thật. |
| `spend` | Chi phí: sổ cục bộ + key + cả đội (ngân sách còn lại). |
| `mux video.mp4 --audio vo.mp3 [--music nhac.mp3] --out x.mp4` | Ghép giọng đọc (và nhạc nền nhỏ) vào video, BỎ âm thanh gốc của Veo. |
| `concat c1.mp4 c2.mp4 ... --out x.mp4` | Nối nhiều clip. |

## Model và giá (USD, theo bảng giá BTC)
- Ảnh: `nano-banana-2-lite` $0.034 (nháp), `nano-banana-2` $0.067 (mặc định), `nano-banana-pro` $0.134 (đẹp nhất, giới hạn thấp 48.000 TPM). `gpt-image-2.5-flare|sunburst` tính theo token, dùng `--size` và `--quality low`. KHÔNG dùng tên `nano-banana` (Google ngừng hỗ trợ).
- Video Veo 3.1: lite $0.05/giây (720p), $0.08 (1080p); fast $0.10 (720p), $0.12 (1080p); full $0.40/giây. Tính tiền ngay khi tạo job, kể cả khi không tải về. Mất 30 giây đến vài phút.
- Giọng đọc: `gemini-2.5-flash-preview-tts`, `gemini-3.1-flash-tts-preview` (giọng Zephyr, Kore...), `gpt-4o-mini-tts` (giọng alloy, nova...; ≈ $0.015/phút). Chất lượng tiếng Việt CHƯA kiểm chứng: nghe thử trước khi dùng.
- Ngân sách đội: $50 (key thi), $1 (key diễn tập). Giá chỉ là tham khảo; số thật xem `mediakit spend`.

## Bẫy thường gặp
- Tỷ lệ ảnh chỉ nhận `1:1, 3:4, 4:3, 16:9, 9:16`. Cần 4:5 thì dùng 3:4 rồi `background-size: cover` (mediakit tự đổi 4:5 → 3:4).
- `--ref` đi qua `/chat/completions` với model nano-banana; chưa kiểm chứng giữ nhân vật tốt đến đâu. Kiểm tra bằng mắt.
- Veo 3.1 có thể sinh kèm âm thanh. Nếu dùng giọng đọc TTS thì phải `mux` để thay âm gốc.
- Model ảnh dễ vẽ sai chữ có dấu: không nhờ nó vẽ chữ.
- Giới hạn tính THEO ĐỘI (mọi key dùng chung): tối đa 10 request song song mỗi key; Veo 52 RPM; ảnh Nano Banana 60 RPM; key diễn tập chỉ 20 RPM và 100.000 TPM. 429 thường do chính đội bắn dồn: mediakit tự thử lại với độ trễ tăng dần.
- `429 Budget has been exceeded` = hết ngân sách đội: dừng ngay, báo người dùng. Chờ không giúp được.
- Chi phí: header `x-litellm-response-cost` (trường `cost`); không có thì mediakit ghi `est_cost` (ước tính từ bảng giá).
