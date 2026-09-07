# Hướng Dẫn Đóng Góp (Contributing Guidelines)

Tri ân công đức quý thiện tri thức, quý hành giả và các lập trình viên đã cùng chung tay xây dựng và gìn giữ kho dữ liệu Phật học mở **SuttaCentral Open Data & Buddhist Curriculums**.

Dự án được thiết kế theo nguyên tắc: **Thuần Git-native, 0 VNĐ chi phí duy trì máy chủ, mở vĩnh viễn và trường tồn theo thời gian**.

---

## 📜 Nguyên Tắc Cốt Lõi (Core Dhamma Principles)

1. **Chánh Pháp Vô Thượng (Canonical Authenticity):**
   - Mọi bài học bắt buộc phải căn cứ trên Tam Tạng Pāḷi (*Tipiṭaka - Sutta Piṭaka*) hoặc hệ thống Chú giải (*Aṭṭhakathā*) Theravāda chính thống.
   - Tuyệt đối không đưa vào tà kiến, mê tín dị đoan, bói toán, bùa chú, hoặc các giáo lý đi ngược lại tinh thần Vô thường (*Anicca*), Khổ (*Dukkha*), Vô ngã (*Anattā*), Tứ Diệu Đế (*Cattāri Ariyasaccāni*) và Duyên Khởi (*Paṭiccasamuppāda*).
2. **Nguyên Tắc Con Trỏ Kinh Văn (Dynamic Sutra Pointers):**
   - **Không hardcode toàn văn bài kinh** vào file giáo án JSON.
   - Thay vào đó, trường `suttaUid` trỏ trực tiếp đến mã định danh SuttaCentral (ví dụ `sn55.1`, `mn41`, `dn22`, `an3.65`, `khp5`). Khi người dùng mở bài học, ứng dụng di động sẽ tự động nạp toàn văn bài kinh từ cơ sở dữ liệu SQLite cục bộ.
3. **Song Ngữ Ưu Tiên (Bilingual Support):**
   - Khuyến khích cung cấp đầy đủ cả tiếng Việt và tiếng Anh (`titleEn`, `subtitleEn`, `descriptionEn`, `summaryEn`, `practiceGuideEn`, `reflectionPromptEn`).
   - Tên Pāḷi cần sử dụng đúng chuẩn phiên âm quốc tế (ā, ī, ū, ṭ, ḍ, ṅ, ñ, ṃ...).

---

## 🛠️ Quy Trình Thêm Giáo Án Mới (Step-by-Step)

### Bước 1: Tạo Thư Mục Giáo Án
Đặt tên thư mục theo định dạng snake_case phản ánh chủ đề:
```bash
curriculums/<curriculum_id>/curriculum.json
```
*Ví dụ:* `curriculums/vipassana_foundations/curriculum.json`

### Bước 2: Biên Soạn File `curriculum.json`
Mẫu cấu trúc chuẩn:
```json
{
  "id": "vipassana_foundations",
  "title": "Nền Tảng Minh Sát Tuệ — Bốn Niệm Xứ Căn Bản",
  "titleEn": "Foundations of Vipassanā — Satipaṭṭhāna Essentials",
  "paliTitle": "Satipaṭṭhāna Bhāvanā",
  "subtitle": "An trú trong Chánh niệm tỉnh giác trên Thân, Thọ, Tâm, Pháp",
  "subtitleEn": "Abiding in mindful awareness of Body, Feelings, Mind, Dhamma",
  "description": "Lộ trình hướng dẫn thực hành thiền Tứ Niệm Xứ căn bản dựa trên Đại Niệm Xứ (DN 22 / MN 10)...",
  "category": "vipassana",
  "iconEmoji": "🧘",
  "estimatedDuration": "8 bài / 4 Chặng",
  "canonicalSource": "DN 22, MN 10, SN 47",
  "traditionLineage": "Theravāda Satipaṭṭhāna Vipassanā",
  "stages": [
    {
      "stageIndex": 1,
      "title": "Chặng 1: Quán Thân Trên Thân",
      "paliTitle": "Kāyānupassanā",
      "objective": "Thiết lập chánh niệm hơi thở và tứ oai nghi",
      "lessons": [
        {
          "id": "vipassana_l01",
          "lessonNumber": 1,
          "title": "Bài 1: Hơi Thở Vào, Hơi Thở Ra (Ānāpānasati)",
          "paliTitle": "Ānāpāna Pabba",
          "summary": "Thở vô dài biết thở vô dài, thở ra dài biết thở ra dài...",
          "suttaUid": "mn118",
          "suttaTitle": "Kinh Nhập Tức Xuất Tức Niệm (MN 118)",
          "recommendedRoutineId": "r_breathing",
          "practiceGuide": "Dành 15 phút buổi sáng tọa thiền theo dõi hơi thở tự nhiên tại cửa mũi.",
          "reflectionPrompt": "Bạn có nhận biết được khoảnh khắc tâm phóng dật và nhẹ nhàng đưa tâm trở về hơi thở không?"
        }
      ]
    }
  ]
}
```

### Bước 3: Chạy Kiểm Tra và Cập Nhật Tự Động
Chạy script kiểm tra và tạo lại `manifest.json`:
```bash
python3 scripts/build_manifest.py --build
```
Script sẽ tự động:
- Xác thực cú pháp JSON và các trường bắt buộc.
- Đếm tổng số bài học (`totalLessons`).
- Tính toán mã băm SHA-256 chính xác của file `curriculum.json`.
- Tự động cập nhật `curriculums/manifest.json` và tăng `versionCode`.

Kiểm tra lại lần cuối:
```bash
python3 scripts/build_manifest.py --check
```
Nếu hiển thị `✓ manifest.json is valid and completely up-to-date`, bạn đã sẵn sàng!

### Bước 4: Tạo Pull Request
1. Commit các thay đổi với thông điệp rõ ràng:
   ```bash
   git add curriculums/
   git commit -m "feat(curriculum): add vipassana_foundations study track"
   git push origin <your-feature-branch>
   ```
2. Mở Pull Request vào nhánh `main`. GitHub Actions CI sẽ tự động chạy để kiểm tra tính hợp lệ.

---

## 💡 Hỗ Trợ & Thảo Luận
Nếu bạn có bất kỳ câu hỏi nào về nguồn kinh văn Pāḷi hoặc cách xây dựng lộ trình, hãy mở một Issue theo mẫu **New Curriculum Proposal** để cùng thảo luận với cộng đồng.
