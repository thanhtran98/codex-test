---
name: video-short
description: Sản xuất video ngắn 15–60 giây (quảng cáo, tin ngắn, giới thiệu, reel) từ đề bài: kịch bản, shot list, clip Veo, ảnh động, giọng đọc, phụ đề, dựng phim. Chỉ dùng khi đề thật sự yêu cầu video; nếu đề cho phép, ưu tiên phương án rẻ và chắc chắn hơn (ảnh động).
---
# Video ngắn
Veo chỉ ra clip 4–8 giây, nên video dài = nhiều cảnh ghép. Luôn có đường lui về ảnh tĩnh. Đọc `$brief-and-concept` và `$gateway-quirks` trước.

1. **Kịch bản** (`out/work/script.md`): 4–8 cảnh; mỗi cảnh có ý chính, lời đọc (nếu có), mô tả hình, độ dài (4/6/8 giây). Tổng đúng độ dài đề yêu cầu. Lời đọc ngắn, đúng nhịp.
2. **Giọng đọc**: `mediakit tts` từng đoạn, đo bằng `ffprobe`, chỉnh kịch bản theo độ dài thật. Nghe thử tiếng Việt trước khi dùng cả bộ.
3. **Hình**: khóa nhân vật/bối cảnh bằng ảnh đầu: sinh ảnh cảnh bằng `mediakit image` (có `--ref` nếu cần) rồi `mediakit video ... --image anh_dau.png` để Veo làm chuyển động. Prompt Veo: 1 chủ thể, 1 hành động, góc máy, ánh sáng, "no text". Chạy song song tối đa 3 job. Thử trước 1 cảnh bằng `veo-3.1-lite-generate-001` 4 giây; đủ đẹp thì dùng luôn cho cảnh khác, chưa đủ thì thử `veo-3.1-fast-generate-001`. Cảnh khó hoặc chậm quá 5 phút: chuyển động từ ảnh tĩnh bằng ffmpeg `zoompan` hoặc HTML.
4. **Dựng**: `mediakit concat c1.mp4 c2.mp4 ... --out out/work/noi.mp4`, rồi `mediakit mux out/work/noi.mp4 --audio out/work/vo.mp3 [--music assets/music/nhac.mp3] --out out/work/co_tieng.mp4` (bỏ âm gốc của Veo). Nhạc nền chỉ dùng file do đội tự tạo/được phép, đặt trong `assets/music/`.
5. **Phụ đề và chữ**: viết `out/work/sub.srt` theo thời gian giọng đọc, đốt vào video: `ffmpeg -i in.mp4 -vf "subtitles=out/work/sub.srt:fontsdir=assets/fonts:force_style='FontName=Be Vietnam Pro,Fontsize=22,Outline=2'" -c:a copy out/final/video.mp4`. Chữ lớn (tiêu đề, CTA) có thể làm bằng HTML + `mediakit shot` rồi `overlay`. Framework dựng video chạy cục bộ (như HyperFrames) được phép nếu không gọi AI ngoài gateway.
6. **Xuất** `out/final/video.mp4` (1280×720 hoặc 720×1280, hoặc theo đề). Kiểm tra: `mediakit sheet`, nghe lại toàn bộ âm thanh, `ffprobe` độ dài.
7. Chạy `$qa-checklist`.
