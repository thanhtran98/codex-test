# Media Agent: cài đặt và chạy (phiên bản 2)

Bộ khung agent sản xuất nội dung truyền thông cho vòng chung khảo AI Thực Chiến, chạy bằng Codex CLI qua gateway của BTC.
Đề chưa biết trước (video, ảnh/poster, truyện, văn bản...), nên bộ khung viết theo hướng generic: **đề → brief → sản phẩm → QA**.

## Cấu trúc
```
AGENTS.md                      Sổ tay chung và luật cứng (Codex đọc đầu phiên)
.agents/skills/                6 skill: gateway-quirks, brief-and-concept, static-visual, comic-story, video-short, qa-checklist
tools/mediakit.py              CLI duy nhất gọi gateway (doctor, image, tts, video, shot, sheet, review, search, spend, mux, concat)
codex-config/thucchien.config.toml   Cấu hình Codex trỏ vào gateway
tests/run_tests.py             Kiểm thử mediakit với gateway giả (không tốn tiền)
assets/input|fonts|music/      Tài nguyên do đề cung cấp, font tiếng Việt, nhạc được phép dùng
out/                           brief.md, plan.md, qa.md, manifest.jsonl, final/ (file nộp), work/ (trung gian)
```

## Đã thay đổi so với phiên bản đầu
- `mediakit.py`: sửa lỗi retry làm mất file ảnh khi image-to-video; hết ngân sách thì dừng ngay thay vì thử lại; ghi chi phí video (ước tính khi header không có) không bị đếm đôi; thêm `--ref` (ảnh tham chiếu), chuẩn hóa tỷ lệ (4:5 → 3:4), chờ font tải xong trước khi chụp, và các lệnh mới `doctor`, `review`, `search`, `spend`, `mux`, `concat`.
- Chuỗi `#số` chống cache trong prompt ảnh đổi thành câu dặn model không vẽ chữ hay số.
- Skill viết lại có dấu, generic: bỏ `poster-flyer`; thêm `brief-and-concept` (ma trận tuân thủ, văn bản), `static-visual`, `comic-story`. Sửa kích thước A5 (bản cũ ghi sai).
- AGENTS.md: giao bản hoàn chỉnh sớm, tài nguyên đề cung cấp dùng nguyên bản, cấm in biến môi trường/key, kiểm tra chi phí định kỳ.
- Cấu hình Codex thêm `shell_environment_policy` (xem Bước 2b).

## Thông tin đã xác nhận với BTC
Được mang sẵn công cụ/khung (đã xác nhận, nên giữ văn bản trả lời); framework chạy cục bộ được phép nếu không gọi model AI ngoài; chỉ có $1 để diễn tập, $50 khi thi; đề bí mật, có thể không cần video.

## Cài đặt (làm đúng thứ tự)
**Bước 0. Phần mềm nền**: Node.js 22+, Python 3.10+, git, ffmpeg (có ffprobe). Windows: cài Git for Windows (Git Bash cho hook AI Log).
```
pip install -r requirements.txt
python -m playwright install chromium
npm install -g @openai/codex
```
Bỏ font có dấu tiếng Việt (Be Vietnam Pro hoặc Noto Sans, .ttf/.woff2) vào `assets/fonts/`.

**Bước 1. Key và kiểm tra môi trường (không tốn tiền)**: đặt `THUCCHIEN_API_KEY` (macOS/Linux: `export` trong `~/.zshrc`; Windows: `setx`), mở lại terminal, rồi:
```
python tools/mediakit.py doctor
python tools/mediakit.py spend
python tests/run_tests.py
```
`doctor` phải báo OK hết (font và key). `run_tests.py` phải báo TẤT CẢ ĐẠT.

**Bước 2. Codex qua gateway**: chép `codex-config/thucchien.config.toml` vào `~/.codex/` (Windows: `%USERPROFILE%\.codex\`), rồi `git init`, commit, `codex --profile thucchien`. Gõ lần lượt:
1. `Đọc AGENTS.md và liệt kê các skill bạn thấy.`
2. `Chạy: python tools/mediakit.py doctor` — dòng "Có key" phải OK. Nếu không, xem Bước 2b.
3. `Mở out/work/test.png và mô tả ảnh.` (sau khi đã có ảnh test ở Bước 4) — biết model có nhìn được ảnh không; nếu không, QA dựa vào `mediakit review` và người duyệt.

**Bước 2b. Nếu agent không thấy key**: Codex có thể lọc biến tên chứa KEY. Khối `[shell_environment_policy]` trong cấu hình đã tắt việc lọc (CHƯA kiểm chứng; nếu Codex báo lỗi cấu hình ở khối này thì xóa nó). Phương án chắc chắn hơn: tạo file `~/.thucchien/key` chỉ chứa key (mediakit tự đọc khi biến môi trường vắng). Nhớ rằng agent không được in key (AGENTS.md cấm) vì log gửi nguyên văn lên BTC.

**Bước 3. AI Log của BTC (bắt buộc, làm trước khi cài thêm skill ngoài)**: chép template hook của BTC vào gốc repo và GỘP (không ghi đè) `.agents/`, `.gitignore`, `.env.example`, `AGENTS.md`; kiểm tra bằng `git diff`. Chạy script setup hook, điền `.env` (token `aitc_...`), đặt `git remote add origin ...`, rồi gõ một prompt trong Codex, xem `.ai-log/session.jsonl` có dòng mới và `python scripts/submit_log.py` báo 202.

**Bước 4. Thử công cụ rẻ (≈ $0.05)**:
```
python tools/mediakit.py image "ban công buổi sáng, ánh sáng ấm, no text" --out out/work/test.png --model nano-banana-2-lite --ratio 3:4
python tools/mediakit.py tts "Xin chào các bạn" --out out/work/test.mp3
python tools/mediakit.py review out/work/test.png
```
Nghe giọng đọc tiếng Việt; thử `--model gpt-4o-mini-tts --voice nova` nếu giọng đầu lỗi.

**Bước 5. Chạy agent bằng một đề poster** (xem kế hoạch ngân sách dưới đây), có bấm giờ.

## Kế hoạch thử trên key $1 (key diễn tập: 20 RPM, 5 song song, 100.000 TPM)
Ước tính ≈ $0.5–0.65: smoke test ≈ $0.04, một phiên Codex làm poster ≈ $0.10–0.25 (token, cần đo thực tế), 2–3 ảnh nền lite ≈ $0.10, một ảnh thử chữ do model vẽ ≈ $0.034, tùy chọn một clip Veo lite 4 giây ≈ $0.20. Dừng khi `mediakit spend` cho thấy còn dưới ≈ $0.35. Nếu gặp 429 liên tục, đó là trần tốc độ của key diễn tập, không phải lỗi bộ khung; giữ AGENTS.md/SKILL.md ngắn và đừng kết luận về tốc độ từ lần chạy này.

Việc đầu tiên khi có key $50: chạy một clip Veo lite 4 giây để kiểm tra đường ống video (đề có thể không cần video, nhưng đây là đường ống chưa từng chạy thật).

## CHƯA kiểm chứng với gateway thật (hãy thử và ghi kết quả vào đây)
- `--ref` (ảnh tham chiếu qua `/chat/completions`) có giữ được nhân vật không.
- `mediakit search` (Google Search grounding qua `googleSearch` hoặc `--engine openai`).
- `mediakit spend` (đường dẫn `/key/info`, `/team/info`).
- `mediakit review` với model `gemini-3.1-flash-lite` đọc ảnh.
- Khối `shell_environment_policy` trong cấu hình Codex; Codex có nhìn được ảnh không.
- Giọng đọc tiếng Việt của từng model TTS; Veo lite có kèm âm thanh không; lệnh `shot` trên máy bạn (Chromium).
- Tên model trong bảng giá có thể thay đổi: kiểm tra lại trang bảng giá của BTC trước ngày thi.

## Lab test với nhà cung cấp ảnh bên ngoài (tạm thời)
Mặc định mọi lệnh đi gateway BTC. Riêng **sinh ảnh** có thể trỏ sang nhà cung cấp khác để thử nghiệm, KHÔNG cần sửa code:
- Cách 1 — biến môi trường: `MEDIAKIT_IMAGE_BASE_URL`, `MEDIAKIT_IMAGE_API_KEY`, `MEDIAKIT_IMAGE_MODEL`, `MEDIAKIT_IMAGE_MODE` (`images`|`chat`), `MEDIAKIT_IMAGE_RATIO_FIELD` (mặc định `aspect_ratio`, đặt rỗng để không gửi tỷ lệ), `MEDIAKIT_IMAGE_AUTH` (`bearer`|`raw`|`api-key`|`none`), `MEDIAKIT_IMAGE_EXTRA_JSON` (JSON gắn thêm vào body).
- Cách 2 — file `config/image-provider.local.json` (đã gitignore; mẫu ở `config/image-provider.example.json`).
- Quay về BTC: bỏ hết biến `MEDIAKIT_IMAGE_*` và xoá/đổi tên file `.local.json`. `mediakit doctor` sẽ hiện đang dùng nhà cung cấp nào.
- `mediakit spend` KHÔNG đọc được chi phí của nhà cung cấp ngoài; chỉ có sổ cục bộ.
- **Nhắc lại luật thi:** khi vào đề thật phải dùng gateway của BTC.

## Mẹo vận hành
- Bước brief/ý tưởng nên dùng model mạnh hơn (`/model` → `gpt-6.1-sol`), phần dựng dùng `gpt-6-luna`.
- Mỗi lỗi lặp lại hai lần: thêm một dòng luật vào AGENTS.md.
- Nhớ `git push` cuối buổi để log được gửi.
