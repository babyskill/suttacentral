# SuttaCentral Buddhist Curriculums — Codebase Architecture

Repository này quản lý kho dữ liệu mở về kinh tạng Pāḷi và hệ thống giáo trình tu học Phật giáo chuẩn mực, phục vụ phân phối qua CDN cho ứng dụng di động và web.

---

## 📁 Cấu Trúc Tổng Thể

```text
babyskill/suttacentral/
├── .github/
│   └── workflows/ci.yml             # CI Action tự động chạy kiểm tra tính hợp lệ & SHA-256
├── Docs/
│   └── CONSTITUTION.md              # Hiến pháp bất biến về giáo lý & quy chuẩn soạn thảo
├── curriculums/
│   ├── manifest.json                # Danh mục trung tâm: metadata, SHA-256, số bài học
│   ├── <curriculum_id>/             # Thư mục từng giáo trình (snake_case)
│   │   ├── curriculum.json          # Tầng 1: Đề cương, chặng, danh sách bài học
│   │   └── lessons/                 # Tầng 2: Nội dung chuyên sâu từng bài
│   │       └── <lesson_id>/
│   │           ├── vi.json          # Nội dung bài học tiếng Việt (chuẩn 3P)
│   │           └── en.json          # Nội dung bài học tiếng Anh (chuẩn 3P)
├── schemas/
│   ├── curriculum.schema.json       # JSON Schema cho file curriculum.json
│   ├── lesson.schema.json           # JSON Schema cho file lessons/*/{vi,en}.json
│   └── manifest.schema.json         # JSON Schema cho file manifest.json
├── scripts/
│   ├── build_manifest.py            # Công cụ quét, tính SHA-256 & sinh manifest.json
│   └── curriculum_tool.py           # CLI quản trị, khởi tạo, kiểm tra & tra cứu giáo trình
├── templates/
│   ├── curriculum_template.json     # Mẫu chuẩn cho curriculum.json
│   ├── lesson_vi_template.json      # Mẫu chuẩn cho vi.json
│   └── lesson_en_template.json      # Mẫu chuẩn cho en.json
├── .project-identity                # Hồ sơ danh tính dự án
├── AGENTS.md                        # Hướng dẫn chi tiết cho AI Agents trong soạn giáo án
├── CONTRIBUTING.md                  # Hướng dẫn người đóng góp cộng đồng
├── README.md                        # Giới thiệu tổng quan & các liên kết CDN
└── *.db.tar.gz                      # Cơ sở dữ liệu SQLite Tam Tạng Pāḷi (VI, EN, PLI)
```

---

## 🔄 Các Lớp Dữ Liệu (Data Layers)

1. **Lớp Kinh Tạng Cội Nguồn (Canonical Database Layer):**
   - SQLite DBs (`suttacentral_vi.db`, `suttacentral_en.db`, `suttacentral_pli.db`).
   - Cung cấp toàn văn kinh văn Nikāya tra cứu bằng mã con trỏ định danh `suttaUid`.

2. **Lớp Đề Cương Giáo Trình (Curriculum Outline Layer):**
   - File `curriculums/<curriculum_id>/curriculum.json`.
   - Chứa metadata: phân loại (`category`), nguồn kinh điển (`canonicalSource`), truyền thống (`traditionLineage`), đối tượng (`targetAudience`), các chặng (`stages`), và danh mục bài học tóm tắt.

3. **Lớp Chi Tiết Bài Học 3P (Deep Lesson Layer):**
   - Thư mục `curriculums/<curriculum_id>/lessons/<lesson_id>/`.
   - Song ngữ `vi.json` và `en.json` chia thành 3 phần:
     - `pariyatti`: Pháp học, khái niệm Pāḷi, luận giải, phá tà kiến.
     - `patipatti`: Pháp hành, bài tập ứng dụng thực tế, routine ID, đức tính đề xuất.
     - `pativedha`: Pháp thành, câu hỏi tự vấn, bảng kiểm soát tâm tính.

4. **Lớp Phân Phối & Kiểm Thử (Distribution & CI Layer):**
   - `manifest.json`: Tệp chỉ mục chứa danh sách mọi giáo trình kèm mã băm SHA-256 chống giả mạo / nhận diện bản cập nhật.
   - Scripts kiểm thử và CI trên GitHub Actions đảm bảo không có link hỏng hay sai cấu trúc.

---

## 🛠️ Bộ Công Cụ Tự Động Hóa

```bash
# 1. Quét và kiểm tra toàn diện cả giáo trình và bài học
python3 scripts/curriculum_tool.py validate-all

# 2. Khởi tạo một giáo trình mới
python3 scripts/curriculum_tool.py init-curriculum <curriculum_id> --title "Tiêu đề" --category sila

# 3. Thêm một bài học mới song ngữ
python3 scripts/curriculum_tool.py add-lesson <curriculum_id> <lesson_id> --number 1 --stage 1 --sutta mn41

# 4. Tự động tính hash và cập nhật manifest.json
python3 scripts/build_manifest.py --build

# 5. Kiểm tra tính toàn vẹn (chế độ CI)
python3 scripts/build_manifest.py --check
```
