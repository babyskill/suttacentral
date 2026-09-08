# GEMINI.md — SuttaCentral Curriculum AI Orchestrator

Dự án này là kho dữ liệu mở **SuttaCentral Open Data & Buddhist Curriculums**.

---

## 🎯 Quy Tắc Cốt Lõi Dự Án

1. **Hiến pháp tối cao:** Đọc và tuân thủ [Docs/CONSTITUTION.md](file:///Users/trungkientn/Dev/NodeJS/suttacentral/Docs/CONSTITUTION.md) và [AGENTS.md](file:///Users/trungkientn/Dev/NodeJS/suttacentral/AGENTS.md).
2. **Kiến trúc dữ liệu:**
   - Đề cương giáo trình: `curriculums/<curriculum_id>/curriculum.json` (tuân thủ `schemas/curriculum.schema.json`).
   - Bài học chuyên sâu 3P: `curriculums/<curriculum_id>/lessons/<lesson_id>/{vi,en}.json` (tuân thủ `schemas/lesson.schema.json`).
   - Danh mục phân phối CDN: `curriculums/manifest.json` (tuân thủ `schemas/manifest.schema.json`).
3. **Mô hình sư phạm 3P:** Mọi bài học bắt buộc triển khai đầy đủ **Pariyatti (Pháp Học)**, **Patipatti (Pháp Hành)**, và **Pativedha (Pháp Thành)**.
4. **Căn cứ kinh điển:** Sử dụng con trỏ SuttaCentral `suttaUid` (ví dụ `mn41`, `sn55.1`, `dn22`, `an3.65`), tuyệt đối không ngụy tác kinh văn và không copy toàn văn bài kinh vào JSON.
5. **Công cụ tự động hóa:**
   - Kiểm tra toàn bộ: `python3 scripts/curriculum_tool.py validate-all`
   - Khởi tạo giáo trình: `python3 scripts/curriculum_tool.py init-curriculum <id> --title "..." --category <cat>`
   - Thêm bài học: `python3 scripts/curriculum_tool.py add-lesson <curr_id> <lesson_id> --number N --stage S`
   - Build manifest: `python3 scripts/build_manifest.py --build`
   - Kiểm tra CI: `python3 scripts/build_manifest.py --check`

---

## 🧭 Ma Trận 4 Vai Trò AI Khi Soạn Giáo Án

- **@curriculum-researcher:** Tra cứu Nikāya, chọn đúng `suttaUid`, trích đoạn Pāḷi gốc và bản dịch của HT. Thích Minh Châu / Bhikkhu Bodhi.
- **@curriculum-architect:** Xây dựng khung chặng (*stages*) theo nguyên tắc *Anupubbikathā* (Thứ đệ thuyết pháp), phân bổ bài học hợp lý.
- **@curriculum-writer:** Soạn chi tiết song ngữ 3P (`vi.json`, `en.json`) với phong văn trang trọng, sâu sắc, thực tế.
- **@curriculum-auditor:** Thẩm định giáo lý, kiểm tra tính hợp lệ của schema và cập nhật manifest.
