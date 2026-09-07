# SuttaCentral Open Data & Buddhist Curriculums
### Kho Dữ Liệu Mở Kinh Điển Tam Tạng Pāḷi & Giáo Án Tu Học Phật Giáo

[![CI — Validate SuttaCentral Curriculums](https://github.com/babyskill/suttacentral/actions/workflows/ci.yml/badge.svg)](https://github.com/babyskill/suttacentral/actions/workflows/ci.yml)
[![jsDelivr CDN](https://data.jsdelivr.com/v1/package/gh/babyskill/suttacentral/badge)](https://www.jsdelivr.com/package/gh/babyskill/suttacentral)
[![License: MIT & CC0](https://img.shields.io/badge/License-MIT%20%26%20CC0-blue.svg)](LICENSE)
[![Maintenance Cost](https://img.shields.io/badge/Server%20Cost-0%20VND-brightgreen.svg)](#triết-lý-thiết-kế)

---

## 📖 Giới Thiệu (Overview)

Repository này là kho lưu trữ dữ liệu Phật học công cộng, cung cấp:
1. **Cơ sở dữ liệu Tam Tạng Pāḷi (Tipiṭaka - Sutta Piṭaka SQLite Databases):** Kinh tạng Pāḷi bản gốc, bản dịch tiếng Việt (HT. Thích Minh Châu và các dịch giả uy tín), bản dịch tiếng Anh (Bhikkhu Sujato, Bhikkhu Bodhi) và Từ điển Pāḷi - Việt.
2. **Hệ thống Giáo án Tu học Phật giáo (Buddhist Practice Curriculums):** Các lộ trình thực hành từ Sơ cơ đến Nhập Lưu, Cư sĩ, Thập Thiện, Giới Luật và Thiền Định dưới định dạng JSON có cấu trúc chặt chẽ.

Dữ liệu được phân phối trực tiếp qua hạ tầng mạng phân phối nội dung toàn cầu (CDN) hoàn toàn miễn phí, hỗ trợ các ứng dụng di động (như Ứng dụng Phật Giáo / HabittrackerBuddhism), trang web, và công cụ nghiên cứu hoạt động theo phương thức **Offline-First**.

---

## 🏛️ Triết Lý Thiết Kế (Design Philosophy)

- **Trường Tồn Vĩnh Viễn (Zero-Maintenance & Perpetuity):** Dự án hoàn toàn dựa trên Git-native và CDN công cộng (GitHub Raw + jsDelivr Mirror). Không cần server backend, không phát sinh chi phí duy trì hàng tháng (0 VNĐ). Dự án vẫn tiếp tục phục vụ cộng đồng kể cả khi người khởi tạo ban đầu không còn duy trì.
- **Bảo Toàn Chánh Pháp (Doctrinal Integrity):** Giáo án không sửa đổi, không ngụy tác và không hardcode bản kinh. Các bài học liên kết trực tiếp bằng con trỏ `suttaUid` (ví dụ `sn55.1`, `dn31`, `mn41`) trỏ vào kho dữ liệu SQLite kinh tạng chuẩn mực.
- **Offline-First & Riêng Tư (Privacy-Preserving):** Ứng dụng di động đóng gói sẵn bản sao dữ liệu. Khi có mạng, ứng dụng tự động kiểm tra mã băm SHA-256 trong `manifest.json` để tải cập nhật hoặc giáo án mới vào bộ nhớ thiết bị. Mọi tiến độ học tập của người dùng được lưu trữ cục bộ trên máy cá nhân.

---

## 📂 Cấu Trúc Thư Mục (Directory Structure)

```text
babyskill/suttacentral/
├── .github/
│   ├── workflows/ci.yml             # Tự động hóa kiểm tra tính hợp lệ & SHA-256
│   ├── ISSUE_TEMPLATE/              # Mẫu đề xuất giáo án & báo lỗi
│   └── PULL_REQUEST_TEMPLATE.md     # Checklist cho người đóng góp
├── curriculums/
│   ├── manifest.json                # Mục lục trung tâm: phiên bản, mã băm SHA-256, số bài học
│   ├── sotapatti_magga/             # Lộ trình Nhập Lưu (19 bài / 4 chặng)
│   │   └── curriculum.json
│   ├── pancasila_human/             # Bảo toàn thân người — Ngũ giới (6 bài / 5 chặng)
│   │   └── curriculum.json
│   ├── dasa_kusala_deva/            # Thập thiện nghiệp đạo (3 bài / 3 chặng)
│   │   └── curriculum.json
│   └── ghihattha_layman/            # Cư sĩ tinh tấn (4 bài / 4 chặng)
│       └── curriculum.json
├── schemas/
│   ├── curriculum.schema.json       # JSON Schema đặc tả giáo án
│   └── manifest.schema.json         # JSON Schema đặc tả manifest
├── scripts/
│   └── build_manifest.py            # Công cụ Python tự động kiểm tra & cập nhật manifest
├── pali_viet_dict.db.tar.gz         # Cơ sở dữ liệu Từ điển Pāḷi - Việt
├── suttacentral_vi.db.tar.gz        # Cơ sở dữ liệu Kinh tạng tiếng Việt (SQLite)
├── suttacentral_en.db.tar.gz        # Cơ sở dữ liệu Kinh tạng tiếng Anh (SQLite)
├── suttacentral_pli.db.tar.gz       # Cơ sở dữ liệu Kinh tạng tiếng Pāḷi gốc (SQLite)
├── CONTRIBUTING.md                  # Hướng dẫn đóng góp bài học / giáo án mới
├── LICENSE                          # Giấy phép nguồn mở (MIT & CC0)
└── README.md
```

---

## 🌐 Các Điểm Phân Phối CDN (CDN Endpoints)

Hệ thống cung cấp cơ chế dự phòng kép (Dual-CDN Fallback):

### 1. Primary: GitHub Raw
- **Manifest:** `https://raw.githubusercontent.com/babyskill/suttacentral/main/curriculums/manifest.json`
- **Curriculum mẫu:** `https://raw.githubusercontent.com/babyskill/suttacentral/main/curriculums/sotapatti_magga/curriculum.json`

### 2. Fallback: jsDelivr Global CDN Mirror (Tự động chuyển tiếp khi mạng chập chờn)
- **Manifest:** `https://cdn.jsdelivr.net/gh/babyskill/suttacentral@main/curriculums/manifest.json`
- **Curriculum mẫu:** `https://cdn.jsdelivr.net/gh/babyskill/suttacentral@main/curriculums/sotapatti_magga/curriculum.json`

---

## ⚙️ Công Cụ Tự Động Hóa (Automation & CLI Tooling)

Dự án tích hợp sẵn công cụ dòng lệnh bằng Python (thuần thư viện chuẩn, không cần cài thêm gói ngoài):

```bash
# 1. Quét và cập nhật manifest.json (tự động tính SHA-256, đếm bài học, tăng versionCode)
python3 scripts/build_manifest.py --build

# 2. Kiểm tra tính hợp lệ và độ đồng bộ (dùng trong CI/CD)
python3 scripts/build_manifest.py --check
```

Mỗi lần có ai đó tạo Pull Request hoặc thêm giáo án mới, GitHub Actions sẽ tự động kích hoạt `scripts/build_manifest.py --check` để đảm bảo không xảy ra lỗi cú pháp hay sai lệch mã băm.

---

## 🤝 Hướng Dẫn Đóng Góp (Contributing)

Xem chi tiết tại [CONTRIBUTING.md](CONTRIBUTING.md).

Mọi Phật tử, hành giả và nhà nghiên cứu đều được chào đón đóng góp giáo án mới:
1. Fork repository và tạo nhánh mới.
2. Thêm thư mục giáo án trong `curriculums/<curriculum_id>/curriculum.json`.
3. Chạy `python3 scripts/build_manifest.py --build`.
4. Mở Pull Request vào nhánh `main`.

---

## 📜 Bản Quyền & Giấy Phép (License)

- **Mã nguồn, JSON Schemas & Scripts:** Được phát hành theo giấy phép [MIT License](LICENSE).
- **Văn bản Giáo án & Dữ liệu Phật học:** Được cúng dường cho cộng đồng theo hiến tặng phạm vi công cộng [Creative Commons Zero (CC0 1.0 Universal) Public Domain Dedication](LICENSE).

*Nguyện cho Chánh Pháp được trường tồn, đem lại an lạc và hạnh phúc cho số đông chúng sinh.*
