# KẾ HOẠCH THỰC THI — "Đắk Lắk Ơi" · Trợ lý Du lịch Đắk Lắk AI

**Đề:** Vòng 2 Thực chiến AI · Bảng 1 · Đội AGENT FORGE
**Ca thi:** 06/10/2026, 09:00 → 11:00 (120 phút) · **Hạn nộp:** 11:10
**Sản phẩm:** Website desktop tiếng Việt, cá nhân hóa lịch trình theo *số người · số ngày · ngân sách · sở thích*
**Tài liệu liên quan:** `out/brief.md` (yêu cầu + ý tưởng) · `out/qa.md` (QA) · `out/manifest.jsonl` (nhật ký chi phí)

> Trạng thái: kế hoạch này được lập lúc **09:16**, tức đã tiêu 16/120 phút. Mọi mốc dưới đây tính từ 09:17.

---

## 1. Nguyên tắc chỉ huy

1. **Có bản chạy được trước 09:45**, rồi mới nâng cấp. Không dồn việc vào phút cuối.
2. **Một đường ống, một lệnh.** Mọi thứ gọi AI đi qua `python tools/mediakit.py`. Không cài, không gọi bất kỳ AI/MCP nào khác.
3. **Ưu tiên theo điểm chấm:** *đúng đề (R1–R12) → chạy được → minh bạch dữ liệu → đẹp.* Thẩm mỹ là lớp cuối, không phải lớp đầu.
4. **Không có số liệu không nguồn.** Chỗ nào chưa xác minh thì dán nhãn *"Dữ liệu mẫu"* ngay trên UI, không giả vờ chính xác.
5. **Nộp sớm.** Đẩy live URL lên hệ thống nộp trước **10:50**, sau đó mới chỉnh tiếp nếu còn giờ.

---

## 2. Hiện trạng máy & việc gỡ chặn (khối 0)

Kết quả khảo sát lúc 09:15:

| # | Hạng mục | Trạng thái | Ảnh hưởng | Cách xử lý |
|---|---|---|---|---|
| B1 | Key gateway | `doctor` báo "Có key" nhưng `GET /v1/models` trả **HTTP 401** | **Chặn toàn bộ** sinh ảnh/AI | Nạp đúng key `sk-...` của BTC vào `THUCCHIEN_API_KEY` (hoặc `~/.thucchien/key`), rồi chạy lại `doctor` |
| B2 | Gateway ảnh đang trỏ nhà cung cấp lab (`config/image-provider.local.json` → `117.1.150.235:31000`) | Sai quy chế thi | Mọi ảnh sinh ra không có audit log BTC | **Đổi tên/xoá** `config/image-provider.local.json` trước khi sinh ảnh đầu tiên |
| B3 | `ffmpeg` / `ffprobe` | Không có | Không dựng/mux video được | Website **không cần ffmpeg**. Nếu cần cài: `brew install ffmpeg` |
| B4 | CLI deploy (`vercel`, `wrangler`, `cloudflared`, `gh`) | Không có cái nào | Chưa có live URL | Dùng phương án deploy mục 6 (ưu tiên Cloudflare Pages kéo-thả) |
| B5 | `npm` | Lỗi quyền ghi `~/.npm` | Cài package bằng npm sẽ fail | Khi cài phải chạy ngoài sandbox (cần quyền) hoặc `npm config set cache /tmp/npm-cache` |
| B6 | `playwright` + Chromium | **OK** | — | Dùng `mediakit shot` để xuất PNG/PDF sổ tay, không cần ffmpeg |
| B7 | Font tiếng Việt | **OK** — 162 file Be Vietnam Pro, có subset `vietnamese` | — | Copy `.woff2` subset vietnamese vào `app/fonts/` |
| B8 | Repo git hiện tại | `origin` = `github.com/thanhtran98/codex-test.git` | **Không phải repo BTC** | Đổi remote sang repo BTC **ngay khi BTC phát repo**, commit từ tài khoản đã đăng ký |

### Lệnh gỡ chặn (chạy tuần tự, không tốn tiền)

```bash
# B1 — kiểm tra key & liệt kê model khả dụng (thay <KEY> bằng key BTC, KHÔNG in ra màn hình)
export THUCCHIEN_API_KEY='<KEY>'
.venv/bin/python tools/mediakit.py doctor
curl -sS -o /tmp/models.json -w '%{http_code}\n' \
  -H "Authorization: Bearer $THUCCHIEN_API_KEY" https://api.thucchien.ai/v1/models
python3 -c "import json;print([m['id'] for m in json.load(open('/tmp/models.json'))['data']])"

# B2 — tắt nhà cung cấp ảnh lab
mv config/image-provider.local.json config/image-provider.local.json.off
.venv/bin/python tools/mediakit.py doctor      # phải hiện "ảnh dùng gateway BTC"

# B6 — xác nhận đường xuất PNG/PDF
.venv/bin/python tools/mediakit.py shot out/work/_smoke.html --out /tmp/smoke.png
```

**Cổng kiểm soát:** cả 3 việc B1, B2, B6 phải xanh trước 09:27. Nếu B1 không xanh → chuyển ngay sang Phương án B ở mục 6 và vẫn dựng web bình thường; web có thể chạy bằng engine cục bộ, phần AI thật ghi rõ trong README là đang chờ key.

---

## 3. Quyết định kiến trúc

### 3.1 Ba phương án đã cân nhắc

| | P/Á A — Static + gọi gateway từ client | P/Á B — Static + serverless proxy | P/Á C — Full-stack (Next.js/Flask) |
|---|---|---|---|
| Cấu trúc | HTML/CSS/JS thuần, `fetch` thẳng tới gateway với key nhúng | HTML/CSS/JS + 1 hàm serverless giữ key | Backend riêng + DB |
| Thời gian dựng | **~15 phút** | ~35 phút | 60 phút+ |
| Rủi ro | **CORS** từ trình duyệt tới gateway (chưa kiểm chứng) | Cần CLI + login + build | Không kịp trong 100 phút |
| Deploy | Kéo-thả / Pages | Vercel CLI / Wrangler | Phức tạp |
| Quy chế | Đề **cho phép** nhúng 1 key vào sản phẩm | An toàn hơn | — |

### 3.2 Chốt
**Đi P/Á A**, kiểm tra CORS trong 5 phút đầu. Đề ghi rõ: *"01 key dành cho 02 máy thi, 01 key tích hợp vào sản phẩm khi cần"* → nhúng key là hợp lệ.

**Fallback nếu CORS chặn (tốn thêm ~20 phút):** dựng Cloudflare Worker ~40 dòng làm proxy, giữ key ở phía server, deploy bằng `npx wrangler deploy`. Đây là P/Á B thu gọn, chỉ một file.

**Fallback nếu deploy bí (tốn 0 phút):** nộp kèm `out/final/dak-lak-oi-demo.html` mở được offline + ảnh chụp các màn hình + video quay màn hình demo; live URL đẩy bù ngay khi thông.

### 3.3 Stack
- **HTML + CSS + JS thuần (ES modules)**, không framework, không bước build → deploy được ở mọi nơi, mở file là chạy.
- **Dữ liệu:** 1 file `data/destinations.json` (điểm đến, món ăn, giá) + 1 file `data/rules.js` (trọng số sở thích, công thức ngân sách).
- **AI:** gọi `POST {GATEWAY}/v1/chat/completions` từ `js/ai.js`, yêu cầu trả **JSON đúng schema**; nếu lỗi/không có key → rơi về engine cục bộ (`js/engine.js`), UI hiện badge "chế độ ngoại tuyến".

---

## 4. Cấu trúc thư mục & phân công file

```
app/
├─ index.html                 # 1 trang, 5 khu: Hero · Nhập liệu · Lịch trình · Chi phí · Văn hóa&Địa phương
├─ css/style.css              # design system: màu, chữ, lưới, thẻ, timeline
├─ js/
│  ├─ main.js                 # điều phối: đọc form → gọi AI/engine → render
│  ├─ ai.js                   # gọi gateway, parse JSON, timeout 20s, fallback
│  ├─ engine.js               # sinh lịch trình + tính chi phí cục bộ (luôn có)
│  ├─ render.js               # render timeline, bảng tiền, thanh ngân sách
│  └─ data.js                 # nạp destinations.json, tra cứu theo id
├─ data/destinations.json     # ~24 điểm đến + ~12 món ăn + bảng giá
├─ fonts/*.woff2              # Be Vietnam Pro subset vietnamese
└─ img/*.jpg                  # ảnh AI sinh qua gateway BTC
out/
├─ final/                     # CHỈ file nộp: so-tay-hanh-trinh.pdf, anh-man-hinh-*.png
└─ work/                      # file trung gian, prompt, bản nháp
```

---

## 5. Đặc tả sản phẩm

### 5.1 Bố cục trang (cuộn dọc, tối ưu ≥1280px)

| Khu | Nội dung | Đáp ứng |
|---|---|---|
| **1. Hero** | Ảnh thiên nhiên Đắk Lắk + tên "Đắk Lắk Ơi" + slogan *"Đắk Lắk dệt riêng hành trình cho bạn"* + CTA cuộn xuống form | R1, R2 |
| **2. Nhập liệu** | 4 ô: số người (stepper) · số ngày (1–7) · ngân sách VND (thanh trượt + ô nhập) · sở thích (chip chọn nhiều: Văn hóa – Thiên nhiên – Ẩm thực – Cà phê – Mạo hiểm – Nghỉ dưỡng) | **R4** |
| **3. Lịch trình** | Timeline theo ngày → khung giờ; mỗi thẻ: tên điểm, ảnh, thời lượng, khoảng cách từ điểm trước, chi phí, nút **"Đổi điểm này"** | **R3, R5** |
| **4. Chi phí** | Bảng 5 nhóm (lưu trú/ăn/di chuyển/vé/dự phòng) × số người; cột giá đơn vị + nguồn; thanh ngân sách đổi màu (xanh ≤ ngân sách, vàng 90–100%, đỏ vượt); nút **"Tối ưu lại cho vừa ngân sách"** | **R5, R10** |
| **5. Văn hóa & Thiên nhiên** | 6 thẻ lớn (buôn, thác, hồ, cà phê, bảo tàng, ẩm thực) + ghi chú ứng xử văn hóa | **R2, R9** |
| **6. Chế độ địa phương** | Biểu đồ mật độ khách theo thứ trong tuần, gợi ý "đi lệch cao điểm", 3 khuyến nghị bảo tồn | **R11** |
| **7. Chân trang** | Nguồn dữ liệu, ngày cập nhật, cảnh báo "dữ liệu mẫu", nút tải sổ tay | **R6, N5** |

### 5.2 Lược đồ dữ liệu `destinations.json`

```json
{
  "diem_den": [
    {
      "id": "buon-ako-dhong",
      "ten": "Buôn Akô Dhông",
      "loai": ["van-hoa", "cong-dong"],
      "mo_ta": "Buôn du lịch cộng đồng giữa Buôn Ma Thuột, nhà sàn, nghề dệt, ẩm thực Êđê.",
      "thoi_luong_phut": 120,
      "gia_ve": 0,
      "gio_mo_cua": "07:00-18:00",
      "toa_do": {"lat": 12.6958, "lng": 108.0533},
      "diem_sang": 4,
      "mua_dep": [11, 12, 1, 2, 3, 4],
      "canh_bao": "Ăn mặc lịch sự, xin phép trước khi chụp ảnh người dân.",
      "nguon": "Cổng TTĐT tỉnh Đắk Lắk (cập nhật DD/MM/2026)",
      "tin_cay": "da-xac-minh"
    }
  ],
  "mon_an": [
    {"id": "bun-do", "ten": "Bún đỏ Buôn Ma Thuột", "loai": ["am-thuc"],
     "gia_binh_quan": 35000, "vi_tri": "TP. Buôn Ma Thuột", "nguon": "...", "tin_cay": "da-xac-minh"}
  ]
}
```

**Quy ước:** `tin_cay` chỉ nhận `da-xac-minh` hoặc `du-lieu-mau`. Giá là **giá/người**. Mọi bản ghi `du-lieu-mau` phải hiện nhãn vàng trên UI và liệt kê ở chân trang.

### 5.3 Công thức ngân sách (phải giải thích được cho BGK)

```
Tổng dự kiến = Lưu trú + Ăn uống + Di chuyển + Vé tham quan + Dự phòng
Lưu trú   = số đêm (= số ngày − 1) × giá phòng × số phòng  (số phòng = ceil(số người / 2))
Ăn uống   = số ngày × 3 bữa × suất bình quân × số người
Di chuyển = (số ngày − 1) × giá thuê xe/ngày + số người × vé máy bay/khứ hồi (nếu chọn)
Vé        = tổng giá vé của các điểm đã chọn × số người
Dự phòng  = 8% × (4 nhóm trên)

Quy tắc thích ứng:
- Nếu Tổng > Ngân sách: bỏ điểm có "điểm sở thích" thấp nhất chưa chọn, hạ hạng lưu trú,
  đổi bữa tối nhà hàng → quán địa phương; lặp tối đa 5 vòng, mỗi vòng hiện 1 dòng giải thích.
- Nếu Ngân sách < mức tối thiểu khả thi: KHÔNG báo lỗi suông — nêu rõ thiếu bao nhiêu
  và gợi ý "đi 2 ngày", "bỏ vé máy bay", "đổi sang tuần thấp điểm".
```

Đây là điểm **ăn tiền nhất với BGK**: minh bạch công thức, không hộp đen.

### 5.4 Chấm điểm sở thích

```
điểm_khớp = 3 × trùng_loại   +  1 × trùng_mùa   −  0.5 × hệ_số_xa
→ sắp giảm dần, cắt theo số ngày, rồi sắp lại theo cụm địa lý (thuật toán láng giềng gần nhất)
  để giảm quãng đường di chuyển trong ngày.
```

Nêu công thức này trong README — chứng minh "AI có cơ sở", không phải bốc ngẫu nhiên.

---

## 6. Kế hoạch dùng AI qua gateway (bắt buộc đúng luật thi)

### 6.1 Dùng AI ở 3 chỗ, không hơn

| # | Việc | Model | Lệnh/đường gọi | Chi phí/lượt |
|---|---|---|---|---|
| A1 | Sinh nội dung lịch trình + lời khuyên theo sở thích | model văn bản của gateway | `POST /v1/chat/completions` từ `js/ai.js` | theo token, rất nhỏ |
| A2 | Ảnh hero + 6 ảnh khu văn hóa/thiên nhiên | `nano-banana-2` | `mediakit image … --ratio 4:3` | $0.0672 × 7 ≈ **$0.47** |
| A3 | 1–2 ảnh nháp để chọn bố cục | `nano-banana-2-lite` | `mediakit image …` | $0.0336 × 2 ≈ **$0.07** |

Tổng ước tính ảnh: **≈ $0.54 / $50**. Ngân sách không phải là vấn đề — **thời gian mới là**.

### 6.2 Prompt ảnh — quy tắc cứng

Mọi prompt phải kết thúc bằng:
`-- no text, no letters, no numbers, no watermark, no logo, no signature`

Và mở đầu bằng bối cảnh thật:
`Ảnh chụp phong cảnh Đắk Lắk, Việt Nam, ánh sáng tự nhiên, …`

> **Tuyệt đối không để model vẽ chữ.** Mọi chữ (tiêu đề, slogan, giá tiền, nhãn) overlay bằng HTML/CSS với Be Vietnam Pro.
> **Không nhờ model vẽ người thật, logo thật, quốc kỳ, bản đồ.**

Prompt mẫu (lưu vào `out/work/prompts-anh.md`):
```
1. Hero:  "Đồi cà phê Đắk Lắk lúc bình minh, sương mù giăng giữa các luống cà phê, núi xa, ảnh phong cảnh
          toàn cảnh, ánh sáng vàng ấm, chân thực, không người -- no text, no letters, no watermark"
2. Buôn:  "Nhà sàn gỗ truyền thống Êđê trong buôn, chiều tà, cây xanh, lối đất đỏ, không người -- no text…"
3. Thác:  "Thác nước lớn giữa rừng nhiệt đới Tây Nguyên, hơi nước, đá bazan đen, không người -- no text…"
4. Hồ:    "Hồ nước ngọt rộng, thuyền độc mộc bên bờ, núi phản chiếu, không người -- no text…"
5. Cà phê:"Ly cà phê đen trên bàn gỗ, hạt cà phê rang, ánh sáng cửa sổ, không người -- no text…"
6. Bảo tàng:"Kiến trúc bảo tàng hiện đại vùng cao nguyên, chiều muộn, không người -- no text…"
7. Ẩm thực:"Mâm cơm Tây Nguyên: cơm lam, gà nướng, rau rừng, lá chuối, không người -- no text…"
```

### 6.3 Prompt AI sinh lịch trình (A1)

```
System: Bạn là chuyên gia du lịch Đắk Lắk. CHỈ trả về JSON đúng schema, không giải thích.
        Không bịa giá ngoài dữ liệu được cấp. Không cam kết về y tế/an toàn.
User:   Du khách: {so_nguoi} người, {so_ngay} ngày, ngân sách {ngan_sach} VND,
        sở thích: {so_thich}. Dữ liệu điểm đến: {json_rut_gon}.
        Hãy trả JSON: {"lich_trinh":[{"ngay":1,"khung_gio":"07:30","diem_id":"...","ly_do":"...",
        "chi_phi":0}], "tong_ket":"...", "goi_y_tiet_kiem":["..."]}
```

**Ràng buộc kỹ thuật trong `ai.js`:** timeout 20s · 1 lần thử lại · validate JSON + kiểm `diem_id` có trong dữ liệu (chống bịa) · sai thì dùng `engine.js`.

---

## 7. Kế hoạch deploy

Xếp theo độ chắc chắn, làm từ trên xuống:

| # | Nền tảng | Cách làm | Thời gian | Ghi chú |
|---|---|---|---|---|
| D1 | **Cloudflare Pages** | Vào dashboard → Create project → **Direct Upload** → kéo thả thư mục `app/` | ~5 phút | Không cần CLI, không cần build. **Chọn cái này.** |
| D2 | Vercel | `npx vercel deploy --prod` (cần login email/GitHub) | ~10 phút | npm lỗi quyền → chạy `npm config set cache /tmp/npm-cache` trước |
| D3 | GitHub Pages | Bật Pages trên repo BTC, trỏ `/app` | ~5 phút | Phụ thuộc quyền trên org BTC |
| D4 | Netlify Drop | Kéo thả tại `app.netlify.com/drop` | ~3 phút | Nhanh nhất nhưng cần tài khoản |

**Kiểm tra sau khi deploy (làm ngay, đừng đợi):**
1. Mở URL bằng cửa sổ ẩn danh (không còn cache/local).
2. Nhập thử: 2 người · 3 ngày · 5.000.000đ · Văn hóa + Cà phê → phải ra lịch trình trong **dưới 3 giây** (engine cục bộ) hoặc **dưới 20 giây** (qua AI).
3. Kiểm tra Console không có lỗi đỏ; thử trên cỡ màn hình 1280×800.
4. **Chép URL vào `out/final/live-url.txt` và nộp lên hệ thống ngay.**

---

## 8. Timeline 100 phút còn lại

| Giờ | Phút | Việc | Kết quả kiểm chứng được |
|---|---|---|---|
| 09:17–09:27 | 10 | **Khối 0:** gỡ chặn B1, B2, B6; test CORS gateway | `doctor` xanh, biết gateway có cho CORS không |
| 09:27–09:30 | 3 | Chốt tên, màu, bảng dữ liệu khung | `out/work/design-note.md` |
| 09:30–09:45 | 15 | Dựng `index.html` + form 4 ô + `engine.js` + render lịch trình | **BẢN CHẠY ĐƯỢC ĐẦU TIÊN** |
| 09:45–09:55 | 10 | Bắn 7 ảnh AI (**chạy nền song song** trong lúc code) | `app/img/*.jpg` |
| 09:55–10:10 | 15 | Bảng chi phí + thanh ngân sách + nút tối ưu lại | Nhập 3 ngân sách khác nhau → 3 kết quả khác nhau |
| 10:10–10:22 | 12 | Tích hợp `ai.js` (gateway thật) + badge nguồn/độ tin cậy | Bấm "Dệt hành trình" thấy log gọi AI |
| 10:22–10:32 | 10 | Khu 5 (Văn hóa & Thiên nhiên) + khu 6 (Chế độ địa phương) | R2, R11 có bằng chứng |
| 10:32–10:40 | 8 | **Deploy live URL** + kiểm tra ẩn danh | URL công khai chạy được |
| 10:40–10:48 | 8 | QA: `out/qa.md`, soát R1–R12, sửa lỗi hiển thị | Bảng QA có tick |
| 10:48–10:55 | 7 | Xuất **sổ tay hành trình PDF** bằng `mediakit shot` | `out/final/*.pdf` |
| 10:55–11:00 | 5 | `git push` (bạn thực hiện) + **nộp bài lên hệ thống** | Bài nộp đã ghi nhận |
| 11:00–11:10 | 10 | Đệm nộp + xử lý trục trặc | — |

**Mốc sống còn:** có live URL trước **10:40**. Trễ mốc này thì cắt khu 6 và ảnh phụ, giữ lại 4 khu cốt lõi R3–R5.

---

## 9. Kiểm thử — ma trận đối chiếu

| Mã | Yêu cầu | Cách kiểm | Đạt khi |
|---|---|---|---|
| R1 | Web desktop hiện đại | Mở 1280×800, 1920×1080 | Không tràn, không vỡ lưới |
| R2 | Văn hóa – thiên nhiên hiện tại | Khu 1 + khu 5 | ≥6 thẻ có ảnh + mô tả |
| R3 | Đi đâu – Ăn gì – Chi phí | 1 lần bấm ra đủ 3 phần | Cả 3 phần cùng màn hình |
| R4 | 4 đầu vào | Thử bỏ trống từng ô | Có thông báo lỗi tiếng Việt, không crash |
| R5 | Lịch trình khả thi, minh bạch | Đọc 1 ngày bất kỳ | Có giờ, thời lượng, khoảng cách, giá, nguồn |
| R6 | Tin cậy, bố cục logic | Kiểm nhãn `du-lieu-mau` | Mọi số chưa xác minh đều có nhãn |
| R7 | Tiếng Việt | Soát toàn bộ chuỗi | Không lọt tiếng Anh ở UI |
| R8 | Dùng AI BTC | Xem Network tab khi bấm nút | Có request tới gateway |
| R9 | Hợp pháp, thuần phong mỹ tục | Đọc khu 5 | Có ghi chú ứng xử; **không** gợi ý cưỡi voi/động vật |
| R10 | Cá nhân hóa + ngân sách | 3 kịch bản ngân sách | Kết quả khác nhau rõ rệt |
| R11 | Điều phối luồng khách | Khu 6 | Có mật độ theo ngày + khuyến nghị |
| R12 | Live URL + GitHub | Mở ẩn danh + xem repo | URL sống, code đã push |
| An toàn | Không lộ key sai chỗ | `grep -ri "sk-" out/final app/js/ai.js` | Chỉ 1 chỗ cấu hình, có ghi chú |

---

## 10. Git & nộp bài

```bash
# Ngay khi BTC phát repo (KHÔNG dùng repo cá nhân):
git remote set-url origin <repo-BTC>
git config user.name  "<tên đã đăng ký>"
git config user.email "<email đã đăng ký>"

# Commit nhỏ, mỗi mốc 1 commit để quay lại được:
git add -A && git commit -m "Khung web + form 4 ô + engine lịch trình"
git add -A && git commit -m "Bảng chi phí + thanh ngân sách co giãn"
git add -A && git commit -m "Tích hợp AI qua gateway BTC + fallback ngoại tuyến"
git add -A && git commit -m "Khu văn hóa thiên nhiên + chế độ địa phương"
git add -A && git commit -m "QA: sửa lỗi hiển thị, thêm nhãn nguồn dữ liệu"
git add -A && git commit -m "Bản nộp: live URL, README, sổ tay PDF"
git push          # ← BẠN tự thực hiện, tôi không push
```

**Hồ sơ nộp (trước 11:10):** tiêu đề · mô tả ngắn · link repo GitHub BTC · Live URL · ảnh chụp màn hình · `so-tay-hanh-trinh.pdf` · ghi chú cho BGK (nêu rõ công thức ngân sách và chỗ nào là dữ liệu mẫu).

**Trong 24h sau đó:** video thuyết trình 3–6 phút (mục 11) + video ghi hình theo yêu cầu BTC.

---

## 11. Kịch bản video thuyết trình (3–6 phút)

| Thời lượng | Nội dung | Ghi chú quay |
|---|---|---|
| 0:00–0:25 | Đặt vấn đề: thông tin du lịch Đắk Lắk phân mảnh, thiếu minh bạch chi phí | Câu hỏi mở, không đọc slide |
| 0:25–1:10 | Demo: nhập 2 người · 3 ngày · 5 triệu · Văn hóa + Cà phê → lịch trình hiện ra | Quay màn hình, phóng to vùng nhập |
| 1:10–2:20 | Mổ xẻ bảng chi phí: công thức, nguồn dữ liệu, thanh ngân sách co giãn, nút tối ưu lại | Đây là phần ghi điểm chính |
| 2:20–3:00 | Khu văn hóa & chế độ địa phương (điều phối luồng khách) | Nêu bối cảnh đề |
| 3:00–4:00 | Quá trình làm: brief → plan → dựng → QA; vai trò của gateway BTC | Chiếu commit log |
| 4:00–4:40 | Hạn chế trung thực + hướng phát triển (dữ liệu thật, đặt chỗ, đa ngôn ngữ) | **Không giấu điểm yếu** |
| 4:40–5:10 | Chốt: *"Đắk Lắk dệt riêng hành trình cho bạn"* | Kết bằng slogan |

---

## 12. Rủi ro & phương án dự phòng

| Rủi ro | Khả năng | Tác động | Phương án |
|---|---|---|---|
| Key gateway 401 kéo dài | Trung bình | Cao | Vẫn dựng web; AI thật chuyển sang gọi từ serverless; ghi rõ trong README |
| CORS chặn gọi từ trình duyệt | **Cao** | Cao | Cloudflare Worker proxy (P/Á B), ~20 phút |
| Không kịp 7 ảnh AI | Trung bình | Thấp | Dùng 2 ảnh + nền gradient CSS; đề không yêu cầu ảnh AI |
| Deploy fail | Trung bình | Cao | Nộp kèm file HTML offline + ảnh chụp + video demo; đẩy URL bù sau |
| Vượt ngân sách $50 | Thấp | Cao | Ảnh ≈ $0.55; gặp `429 Budget` thì dừng ngay, báo bạn |
| Hết giờ khi chưa xong | **Cao** | Cao | Cắt theo thứ tự: khu 6 → ảnh phụ → hiệu ứng; **giữ bằng mọi giá** form + lịch trình + chi phí + live URL |
| Key lộ trong repo | Trung bình | Trung bình | Đưa key vào `js/config.js` gitignored, và `js/config.example.js` để nộp; hoặc dùng biến môi trường của Pages |

---

## 13. Checklist bấm nút nộp

- [ ] Live URL mở được ở cửa sổ ẩn danh
- [ ] Form 4 ô hoạt động, có kiểm tra hợp lệ
- [ ] Lịch trình + ăn uống + bảng chi phí hiện cùng lúc
- [ ] Thanh ngân sách đổi màu đúng ở 3 mức (dưới/vừa/vượt)
- [ ] Không còn chuỗi tiếng Anh trên UI
- [ ] Mọi số liệu chưa xác minh đều có nhãn "Dữ liệu mẫu"
- [ ] Không có chữ do model vẽ trong ảnh
- [ ] Không gợi ý hoạt động gây hại (cưỡi voi, mua động vật hoang dã)
- [ ] `grep -ri "sk-" out/final` không ra key
- [ ] Repo BTC đã push, commit bằng tài khoản đã đăng ký
- [ ] Đã nộp trên hệ thống, `/tmp` không chứa gì cần thiết
- [ ] `mediakit spend` ghi lại con số cuối

---

## 14. Chi phí dự kiến & ngân sách

| Khoản | Số lượng | Đơn giá | Tổng |
|---|---|---|---|
| Ảnh chính `nano-banana-2` | 7 | $0.0672 | $0.47 |
| Ảnh nháp `nano-banana-2-lite` | 2 | $0.0336 | $0.07 |
| Token gọi AI sinh lịch trình (demo) | ~15 lượt | rất nhỏ | < $0.05 |
| **Cộng** | | | **≈ $0.59 / $50** |

Chạy `mediakit spend` sau mỗi nhóm lệnh tốn tiền. Thấy `429 Budget has been exceeded` → dừng ngay.

---

## 15. Việc cần bạn quyết trước khi tôi dựng

| # | Câu hỏi | Mặc định nếu bạn không trả lời |
|---|---|---|
| A | Tên sản phẩm: **"Đắk Lắk Ơi"** hay tên khác? | Dùng "Đắk Lắk Ơi" |
| B | Có cài `ffmpeg` không? (chỉ cần nếu muốn video demo) | Không cài — dùng `mediakit shot` xuất PDF |
| C | Deploy bằng tài khoản Cloudflare/Vercel của ai? | Cloudflare Pages kéo-thả |
| D | Repo BTC đã được phát chưa? Nếu có, cho tôi URL | Giữ repo hiện tại, đổi remote sau |
| E | Nạp key `sk-...` vào `THUCCHIEN_API_KEY` được chưa? | Tôi vẫn dựng web, phần AI chờ key |

---

## 16. Tuyệt đối không làm trong phiên này

- Không dùng MCP nào của phiên làm việc (trình duyệt tự động, tìm kiếm web, plugin ngoài) — tra cứu chỉ qua `mediakit search`.
- Không mở trình duyệt vào bất kỳ nền tảng AI nào.
- Không đọc/in/ghi `.env`, `~/.thucchien/`, `.ai-log/`, không `echo` biến môi trường.
- Không nhờ AI vẽ chữ, logo, người thật, bản đồ, quốc kỳ.
- Không copy template/mã nguồn có sẵn trên mạng.
- Không `git push` thay bạn.
