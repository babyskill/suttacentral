# HIẾN PHÁP SOẠN THẢO GIÁO ÁN PHẬT GIÁO
### SuttaCentral Buddhist Curriculums Constitution
*Phiên bản: 1.0.0 | Ngày hiệu lực: 2026-09-08*

---

## Lời Mở Đầu (Preamble)

Tài liệu này xác lập các nguyên tắc tối cao và bất biến chi phối toàn bộ quy trình biên soạn, thẩm định, cấu trúc dữ liệu và phát hành giáo án tu học Phật giáo trong kho lưu trữ **SuttaCentral Open Data**.

Mục tiêu tối thượng là: **Bảo tồn Chánh Pháp nguyên bản, trong sáng, không bị bóp méo, phục vụ việc tu học giải thoát khổ đau cho muôn loài.**

---

## Điều 1: Căn Cứ Kinh Điển Bất Biến (Doctrinal Immutability)

1. **Tam Tạng Pāḷi Làm Trọng Tâm:**
   - Mọi giáo lý, nguyên lý và bài học bắt buộc phải bắt nguồn trực tiếp từ Kinh Tạng (*Sutta Piṭaka*) thuộc 5 bộ Nikāya (*Dīgha, Majjhima, Saṃyutta, Aṅguttara, Khuddaka*) và các bộ Luật/Luận (*Vinaya, Abhidhamma*) hoặc chú giải chuẩn Theravāda (*Aṭṭhakathā*).
   - Tuyệt đối cấm đưa vào các tư tưởng ngụy tác, mê tín dị đoan, bói toán, cúng sao giải hạn, phù chú, hoặc các giáo thuyết trái nghịch Tam Pháp Ấn (*Vô thường - Anicca, Khổ - Dukkha, Vô ngã - Anattā*), Tứ Diệu Đế (*Cattāri Ariyasaccāni*) và Duyên Khởi (*Paṭiccasamuppāda*).

2. **Cấm Ngụy Tác & Cấm Gán Ép Văn Tự:**
   - Cấm bịa đặt lời dạy của Đức Phật hoặc chư Thánh Tăng.
   - Khi trích dẫn kinh điển, phải giữ đúng ngữ cảnh của bài kinh (*Sutta*), không cắt xén làm sai lệch ý nghĩa giải thoát của Thế Tôn.

3. **Tôn Trọng Dịch Bản Chuẩn Mực:**
   - Tiếng Việt: Ưu tiên bản dịch của Trưởng lão Hoà thượng Thích Minh Châu và các dịch giả uy tín, có căn cứ Pāḷi chuẩn xác.
   - Tiếng Anh: Ưu tiên bản dịch của Bhikkhu Bodhi, Bhikkhu Sujato, I.B. Horner, hoặc Rhys Davids.
   - Thuật ngữ Pāḷi phải có dấu phụ chuẩn quốc tế (ví dụ: *dukkha, anattā, jhāna, magga, phala*).

---

## Điều 2: Mô Hình Sư Phạm Ba Chân Vạc (3P Framework)

Mọi bài học trong hệ thống phải tuân thủ nghiêm ngặt mô hình sư phạm 3P:

```text
┌────────────────────────────────────────────────────────┐
│                   3P PEDAGOGY ENGINE                   │
├───────────────────┬───────────────────┬────────────────┤
│    PARIYATTI      │     PATIPATTI     │   PATIVEDHA    │
│    (Pháp Học)     │    (Pháp Hành)    │  (Pháp Thành)  │
├───────────────────┼───────────────────┼────────────────┤
│ • Kinh văn gốc    │ • Bài tập thân/tâm│ • Tự vấn tối   │
│ • Thuật ngữ Pāḷi  │ • Thói quen định  │ • Checklist    │
│ • Phá ngộ nhận    │ • Routine Id      │ • Thước đo     │
│ • Luận giải sáng  │ • Đức tính gợi ý  │   chuyển hóa   │
└───────────────────┴───────────────────┴────────────────┘
```

1. **Pariyatti (Pháp Học / Chánh Kiến):**
   - Cung cấp nền tảng tri thức đúng đắn.
   - Giải thích thuật ngữ Pāḷi rõ ràng, có định nghĩa mạch lạc.
   - Luôn có mục `commonMisconceptions` (Phá vỡ các hiểu lầm phổ biến) để giải độc tà kiến.

2. **Patipatti (Pháp Hành / Ứng Dụng Đời Thường):**
   - Không dừng lại ở lý thuyết suông; phải chuyển hóa thành hành động cụ thể trong ngày (thói quen, oai nghi, lời nói, cách tư duy, thực hành thiền).
   - Liên kết với mã định danh thói quen (`recommendedRoutineId`) để ứng dụng di động kích hoạt nhắc nhở hành trì.

3. **Pativedha (Pháp Thành / Tự Thẩm Định Chuyển Hóa):**
   - Đưa ra câu hỏi quán chiếu buổi tối (`reflectionPrompt`) giúp hành giả tự nhìn lại nội tâm.
   - Cung cấp bảng kiểm tự soi rọi (`selfAuditChecklist`) định lượng sự tiến bộ tâm linh.

---

## Điều 3: Nguyên Tắc Kiến Trúc Dữ Liệu (Data Architecture)

1. **Con Trỏ Kinh Văn Động (Dynamic Sutta Pointer):**
   - Tuyệt đối **KHÔNG** copy toàn bộ văn bản dài hàng chục trang của bài kinh vào file giáo án JSON.
   - Phải sử dụng trường `suttaUid` (ví dụ `mn41`, `sn55.1`, `dn22`, `an8.54`) để ứng dụng phía máy khách (Client Apps) tự động truy vấn vào cơ sở dữ liệu SQLite cục bộ.
   - Chỉ trích dẫn một đoạn trích ngắn tinh túy (*Key Excerpt*) trong `excerptPali` và `excerptTranslation`.

2. **Cấu Trúc Hai Tầng Thống Nhất:**
   - **Tầng 1 (Curriculum Metadata & Syllabus):** Nằm tại `curriculums/<curriculum_id>/curriculum.json`, chứa thông tin khái quát, các chặng (*stages*), và danh mục bài học tóm tắt.
   - **Tầng 2 (Deep Lesson Content):** Nằm tại `curriculums/<curriculum_id>/lessons/<lesson_id>/{vi,en}.json`, chứa toàn văn nội dung 3P chi tiết.

3. **Nguyên Tắc Song Ngữ Song Hành (Bilingual Parity):**
   - Mọi bài học phải có đầy đủ cặp file `vi.json` và `en.json`.
   - Cấu trúc key của `vi.json` và `en.json` phải đồng nhất 100%.

---

## Điều 4: Tính Bền Vững & Zero Server Cost

1. **Git-Native & Vĩnh Viễn:**
   - Dữ liệu nằm trọn vẹn trong Git repository này, được đồng bộ qua GitHub và CDN toàn cầu (jsDelivr Mirror).
   - Không phụ thuộc vào server trung gian thu phí, không phát sinh chi phí duy trì hàng tháng (0 VNĐ).

2. **Offline-First & Tôn Trọng Quyền Riêng Tư:**
   - Thiết kế ưu tiên tối đa cho ứng dụng di động chạy offline.
   - File `curriculums/manifest.json` ghi nhận mã băm SHA-256 của từng giáo trình để ứng dụng nhận diện cập nhật thông minh.
   - Không thu thập dữ liệu người dùng. Mọi tiến trình học tập được lưu cục bộ trên máy cá nhân.

---

## Điều 5: Trách Nhiệm Của AI Agent & Người Biên Soạn

1. **Thái Độ Cung Kính & Cẩn Trọng:**
   - Tiếp cận kinh điển với tâm khiêm cung, tôn kính Tam Bảo.
   - Văn phong trang trọng, trong sáng, dễ tiếp thu, hướng thiện và giải thoát.

2. **Quy Trình Kiểm Tra Bắt Buộc (Mandatory Verification Gate):**
   - Mọi giáo trình trước khi commit bắt buộc phải vượt qua:
     1. `python3 scripts/curriculum_tool.py validate-all`
     2. `python3 scripts/build_manifest.py --check`
   - Bất kỳ lỗi schema, sai lệch mã băm hoặc thiếu file bài học song ngữ đều không được phép đưa vào nhánh chính.
