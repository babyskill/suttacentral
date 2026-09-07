## Tóm tắt Thay đổi (Summary of Changes)
<!-- Mô tả ngắn gọn về giáo án mới được thêm hoặc nội dung được cập nhật -->

## Loại Đóng góp (Contribution Type)
- [ ] Thêm giáo án mới (`curriculums/<new_id>/curriculum.json`)
- [ ] Sửa đổi/Cập nhật bài học trong giáo án hiện có
- [ ] Bổ sung dịch thuật (English / Pāḷi)
- [ ] Cải tiến công cụ tự động hóa (`scripts/` hoặc `.github/`)

## Danh mục Kiểm tra trước khi gửi PR (Pre-submission Checklist)
- [ ] Đã chạy lệnh kiểm tra tự động thành công:
  ```bash
  python3 scripts/build_manifest.py --build
  python3 scripts/build_manifest.py --check
  ```
- [ ] Tệp `manifest.json` đã được cập nhật chính xác (khớp SHA-256 và số lượng bài học).
- [ ] Định dạng file JSON tuân thủ chuẩn UTF-8 không BOM.
- [ ] Toàn bộ con trỏ `suttaUid` đã được xác minh tồn tại trên cơ sở dữ liệu SuttaCentral.
- [ ] Tên Pāḷi sử dụng đúng ký tự dấu nguyên âm / phụ âm chuẩn quốc tế (ā, ī, ū, ṭ, ḍ, ṅ, ñ, ṃ...).
