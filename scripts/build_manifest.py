#!/usr/bin/env python3
"""
build_manifest.py — SuttaCentral Curriculums Builder & Validator
----------------------------------------------------------------
This script automates:
1. Scanning all curriculums in `curriculums/*/curriculum.json`.
2. Strict schema and structural integrity checks (SuttaCentral UIDs, lesson numbering, bilingual texts).
3. Computing SHA-256 integrity hashes for each curriculum file.
4. Auto-generating or verifying `curriculums/manifest.json`.
5. Zero external dependencies: runs on pure Python 3 standard library.

Usage:
  python3 scripts/build_manifest.py --build    # Build/update manifest.json
  python3 scripts/build_manifest.py --check    # Verify in CI (fails if out of sync or invalid)
"""

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# Base paths
SCRIPTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPTS_DIR.parent
CURRICULUMS_DIR = REPO_ROOT / "curriculums"
MANIFEST_PATH = CURRICULUMS_DIR / "manifest.json"

# Regex for SuttaCentral UID (e.g. sn55.1, mn41, dn22, an3.65, khp5, snp1.8, etc.)
SUTTA_UID_REGEX = re.compile(r"^[a-z0-9\-]+(\.[0-9]+(\-[0-9]+)?)?$", re.IGNORECASE)


def compute_sha256(file_path: Path) -> str:
    """Calculate the hex SHA-256 hash of a file."""
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def validate_curriculum(curr_dir: Path, curr_data: dict) -> list[str]:
    """Validate curriculum structure and business rules."""
    errors = []
    folder_name = curr_dir.name
    curr_id = curr_data.get("id")

    if not curr_id:
        errors.append(f"[{folder_name}] Missing 'id' field.")
    elif curr_id != folder_name:
        errors.append(f"[{folder_name}] 'id' ({curr_id}) does not match folder name ({folder_name}).")

    for field in ("title", "description", "category", "stages"):
        if field not in curr_data:
            errors.append(f"[{folder_name}] Missing required top-level field: '{field}'.")

    stages = curr_data.get("stages", [])
    if not isinstance(stages, list) or len(stages) == 0:
        errors.append(f"[{folder_name}] 'stages' must be a non-empty list.")
        return errors

    seen_lesson_ids = set()
    total_lessons = 0

    for s_idx, stage in enumerate(stages, 1):
        st_title = stage.get("title", f"Stage {s_idx}")
        lessons = stage.get("lessons", [])
        if not isinstance(lessons, list) or len(lessons) == 0:
            errors.append(f"[{folder_name}] Stage '{st_title}' has no lessons.")
            continue

        for l_idx, lesson in enumerate(lessons, 1):
            total_lessons += 1
            l_id = lesson.get("id")
            if not l_id:
                errors.append(f"[{folder_name}] Lesson #{l_idx} in '{st_title}' missing 'id'.")
            elif l_id in seen_lesson_ids:
                errors.append(f"[{folder_name}] Duplicate lesson id: '{l_id}'.")
            else:
                seen_lesson_ids.add(l_id)

            if not lesson.get("title"):
                errors.append(f"[{folder_name}] Lesson '{l_id}' missing 'title'.")
            if not lesson.get("summary"):
                errors.append(f"[{folder_name}] Lesson '{l_id}' missing 'summary'.")

            sutta_uid = lesson.get("suttaUid")
            if sutta_uid and not SUTTA_UID_REGEX.match(str(sutta_uid).strip()):
                errors.append(
                    f"[{folder_name}] Lesson '{l_id}' has invalid suttaUid format: '{sutta_uid}'."
                )

    return errors


def collect_curriculums() -> tuple[list[dict], list[dict], list[str]]:
    """Scan and process all curriculum directories."""
    all_errors = []
    meta_entries = []
    curr_details = []

    if not CURRICULUMS_DIR.exists():
        return [], [], [f"Curriculums directory not found: {CURRICULUMS_DIR}"]

    # Sort folders alphabetically for deterministic output
    folders = sorted([d for d in CURRICULUMS_DIR.iterdir() if d.is_dir()])

    for folder in folders:
        curr_file = folder / "curriculum.json"
        if not curr_file.exists():
            continue

        try:
            with open(curr_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            all_errors.append(f"[{folder.name}] JSON parse error: {e}")
            continue

        errs = validate_curriculum(folder, data)
        if errs:
            all_errors.extend(errs)
            continue

        file_sha256 = compute_sha256(curr_file)
        stages = data.get("stages", [])
        total_lessons = sum(len(s.get("lessons", [])) for s in stages)

        meta = {
            "id": data["id"],
            "curriculumId": data["id"],
            "title": data.get("title", ""),
            "titleEn": data.get("titleEn"),
            "paliTitle": data.get("paliTitle"),
            "subtitle": data.get("subtitle"),
            "subtitleEn": data.get("subtitleEn"),
            "description": data.get("description", ""),
            "descriptionEn": data.get("descriptionEn"),
            "category": data.get("category", "general"),
            "iconEmoji": data.get("iconEmoji", "📜"),
            "estimatedDuration": data.get("estimatedDuration"),
            "estimatedDurationEn": data.get("estimatedDurationEn"),
            "totalLessons": total_lessons,
            "canonicalSource": data.get("canonicalSource"),
            "canonicalSourceEn": data.get("canonicalSourceEn"),
            "traditionLineage": data.get("traditionLineage"),
            "traditionLineageEn": data.get("traditionLineageEn"),
            "targetAudience": data.get("targetAudience"),
            "curriculumPath": f"assets/data/curriculums/{data['id']}/curriculum.json",
            "sha256": file_sha256,
        }

        # Auto-detect local thumbnail image if present
        for t_ext in ("thumbnail.webp", "thumbnail.png", "thumbnail.jpg", "thumbnail.svg"):
            if (folder / t_ext).exists():
                meta["thumbnail"] = t_ext
                break

        # Clean null values if not required
        meta_clean = {k: v for k, v in meta.items() if v is not None}

        meta_entries.append(meta_clean)
        curr_details.append(data)

    return meta_entries, curr_details, all_errors


def run_build(check_only: bool = False) -> int:
    print(f"==> Scanning curriculums in {CURRICULUMS_DIR} ...")
    meta_entries, _, errors = collect_curriculums()

    if errors:
        print("\n❌ Validation Errors found:")
        for err in errors:
            print(f"  - {err}")
        return 1

    print(f"✓ Successfully processed {len(meta_entries)} curriculums.")

    # Read existing manifest
    old_manifest = {}
    current_version_code = 1
    current_version_str = "1.0.0"

    if MANIFEST_PATH.exists():
        try:
            with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
                old_manifest = json.load(f)
                current_version_code = old_manifest.get("versionCode", 1)
                current_version_str = old_manifest.get("version", "1.0.0")
        except Exception as e:
            print(f"Warning: Could not read existing manifest: {e}")

    # Check differences
    old_metas = {m["id"]: m for m in old_manifest.get("curriculums", [])}
    has_changes = False

    if len(old_metas) != len(meta_entries):
        has_changes = True
    else:
        for new_meta in meta_entries:
            m_id = new_meta["id"]
            if m_id not in old_metas:
                has_changes = True
                break
            old_meta = old_metas[m_id]
            if (
                old_meta.get("sha256") != new_meta.get("sha256")
                or old_meta.get("totalLessons") != new_meta.get("totalLessons")
            ):
                has_changes = True
                break

    if check_only:
        if not MANIFEST_PATH.exists():
            print("❌ Error: manifest.json does not exist!")
            return 1
        if has_changes:
            print("❌ Error: manifest.json is OUT OF SYNC with curriculum files!")
            print("Run 'python3 scripts/build_manifest.py --build' to regenerate.")
            return 1
        print("✓ manifest.json is valid and completely up-to-date.")
        return 0

    # Building new manifest
    new_version_code = current_version_code
    if has_changes:
        new_version_code += 1
        v_parts = current_version_str.split(".")
        if len(v_parts) == 3 and v_parts[2].isdigit():
            new_patch = int(v_parts[2]) + 1
            current_version_str = f"{v_parts[0]}.{v_parts[1]}.{new_patch}"
        print(f"==> Changes detected! Bumping version to {current_version_str} (versionCode: {new_version_code})")
    else:
        print(f"==> No changes detected. Keeping version {current_version_str} (versionCode: {new_version_code})")

    new_manifest = {
        "version": current_version_str,
        "versionCode": new_version_code,
        "generatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "curriculums": meta_entries,
    }

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(new_manifest, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"✓ Successfully generated {MANIFEST_PATH.relative_to(REPO_ROOT)}")
    for m in meta_entries:
        print(f"  • [{m['category']}] {m['id']}: {m['totalLessons']} lessons (SHA-256: {m['sha256'][:10]}...)")

    return 0


def main():
    parser = argparse.ArgumentParser(description="SuttaCentral Curriculums Builder & Validator")
    parser.add_argument("--build", action="store_true", help="Generate or update manifest.json")
    parser.add_argument("--check", action="store_true", help="Verify integrity without modifying files")

    args = parser.parse_args()

    if not args.build and not args.check:
        # Default to build
        args.build = True

    sys.exit(run_build(check_only=args.check))


if __name__ == "__main__":
    main()
