#!/usr/bin/env python3
"""
curriculum_tool.py — SuttaCentral Curriculum Management & Validation CLI
-----------------------------------------------------------------------
A dedicated CLI for AI agents and human contributors to:
1. Validate all curriculums and 3P deep lessons (vi.json, en.json) against schemas.
2. Initialize new curriculums with standard boilerplate.
3. Scaffold new lessons with bilingual 3P templates.
4. Inspect curriculum status, stage distribution, and translation completeness.
5. List and summarize all practice tracks.

Zero external dependencies: Pure Python 3 standard library.
"""

import argparse
import json
import re
import sys
from pathlib import Path

# Paths
SCRIPTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPTS_DIR.parent
CURRICULUMS_DIR = REPO_ROOT / "curriculums"
SCHEMAS_DIR = REPO_ROOT / "schemas"
TEMPLATES_DIR = REPO_ROOT / "templates"

SUTTA_UID_REGEX = re.compile(r"^[a-z0-9\-]+(\.[0-9]+(\-[0-9]+)?)?$", re.IGNORECASE)
SLUG_REGEX = re.compile(r"^[a-z0-9_]+$")

VALID_CATEGORIES = [
    "foundations",
    "sotapatti",
    "sila",
    "deva",
    "layman",
    "samatha",
    "vipassana",
    "vinaya",
    "general",
]


def load_json(path: Path) -> tuple[dict | None, str | None]:
    """Safely load JSON from file."""
    if not path.exists():
        return None, f"File not found: {path}"
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f), None
    except Exception as e:
        return None, f"JSON parse error in {path.name}: {e}"


def validate_single_curriculum(curr_dir: Path) -> list[str]:
    """Validate curriculum.json and its associated lessons."""
    errors = []
    curr_id = curr_dir.name
    curr_file = curr_dir / "curriculum.json"

    data, err = load_json(curr_file)
    if err:
        return [f"[{curr_id}] {err}"]

    # Required top-level fields
    for req in ("id", "title", "description", "category", "stages"):
        if req not in data:
            errors.append(f"[{curr_id}] Missing required field '{req}' in curriculum.json")

    if data.get("id") != curr_id:
        errors.append(f"[{curr_id}] 'id' ({data.get('id')}) does not match folder name ({curr_id})")

    category = data.get("category")
    if category and category not in VALID_CATEGORIES:
        errors.append(f"[{curr_id}] Invalid category '{category}'. Must be one of {VALID_CATEGORIES}")

    stages = data.get("stages", [])
    if not isinstance(stages, list) or len(stages) == 0:
        errors.append(f"[{curr_id}] 'stages' must be a non-empty list")
        return errors

    syllabus_lessons = {}
    for s_idx, stage in enumerate(stages, 1):
        s_title = stage.get("title", f"Stage {s_idx}")
        lessons = stage.get("lessons", [])
        if not lessons:
            errors.append(f"[{curr_id}] Stage '{s_title}' has no lessons defined")
            continue

        for l_idx, lesson in enumerate(lessons, 1):
            l_id = lesson.get("id")
            if not l_id:
                errors.append(f"[{curr_id}] Lesson #{l_idx} in '{s_title}' missing 'id'")
                continue
            if not SLUG_REGEX.match(l_id):
                errors.append(f"[{curr_id}] Lesson '{l_id}' has invalid slug format (use snake_case)")
            if l_id in syllabus_lessons:
                errors.append(f"[{curr_id}] Duplicate lesson ID '{l_id}' in curriculum.json")
            syllabus_lessons[l_id] = {
                "stageIndex": stage.get("stageIndex", s_idx),
                "lessonNumber": lesson.get("lessonNumber", l_idx),
                "title": lesson.get("title", ""),
                "suttaUid": lesson.get("suttaUid"),
            }

            sutta_uid = lesson.get("suttaUid")
            if sutta_uid and not SUTTA_UID_REGEX.match(str(sutta_uid).strip()):
                errors.append(f"[{curr_id}] Lesson '{l_id}' invalid suttaUid format: '{sutta_uid}'")

    # Check deep lessons directory
    lessons_dir = curr_dir / "lessons"
    if not lessons_dir.exists():
        errors.append(f"[{curr_id}] Missing 'lessons/' directory for deep 3P lesson content")
        return errors

    lesson_folders = [d for d in lessons_dir.iterdir() if d.is_dir()]
    lesson_folder_names = {d.name for d in lesson_folders}

    # Check for missing lesson folders
    for l_id in syllabus_lessons:
        if l_id not in lesson_folder_names:
            errors.append(f"[{curr_id}] Lesson '{l_id}' declared in curriculum.json but missing folder 'lessons/{l_id}'")

    # Check each lesson folder
    for lf in sorted(lesson_folders):
        lf_name = lf.name
        if lf_name not in syllabus_lessons:
            errors.append(f"[{curr_id}] Folder 'lessons/{lf_name}' exists but is not listed in curriculum.json")

        vi_file = lf / "vi.json"
        en_file = lf / "en.json"

        if not vi_file.exists():
            errors.append(f"[{curr_id}/{lf_name}] Missing vi.json")
        else:
            vi_data, vi_err = load_json(vi_file)
            if vi_err:
                errors.append(f"[{curr_id}/{lf_name}] {vi_err}")
            else:
                errors.extend(validate_lesson_content(curr_id, lf_name, vi_data, "vi"))

        if not en_file.exists():
            errors.append(f"[{curr_id}/{lf_name}] Missing en.json")
        else:
            en_data, en_err = load_json(en_file)
            if en_err:
                errors.append(f"[{curr_id}/{lf_name}] {en_err}")
            else:
                errors.extend(validate_lesson_content(curr_id, lf_name, en_data, "en"))

    return errors


def validate_lesson_content(curr_id: str, lesson_id: str, data: dict, lang: str) -> list[str]:
    """Validate 3P structure in vi.json or en.json."""
    errs = []
    prefix = f"[{curr_id}/{lesson_id}/{lang}.json]"

    if data.get("lessonId") != lesson_id:
        errs.append(f"{prefix} 'lessonId' ({data.get('lessonId')}) does not match folder '{lesson_id}'")

    if data.get("curriculumId") != curr_id:
        errs.append(f"{prefix} 'curriculumId' ({data.get('curriculumId')}) does not match '{curr_id}'")

    for req in ("title", "suttaRef", "pariyatti", "patipatti", "pativedha"):
        if req not in data:
            errs.append(f"{prefix} Missing required top-level key '{req}'")

    # suttaRef
    s_ref = data.get("suttaRef", {})
    if not isinstance(s_ref, dict):
        errs.append(f"{prefix} 'suttaRef' must be an object")
    else:
        uid = s_ref.get("uid")
        if not uid or not SUTTA_UID_REGEX.match(str(uid).strip()):
            errs.append(f"{prefix} 'suttaRef.uid' is invalid or missing: '{uid}'")
        if not s_ref.get("title"):
            errs.append(f"{prefix} 'suttaRef.title' is required")

    # pariyatti (3P - 1)
    pariyatti = data.get("pariyatti", {})
    if not isinstance(pariyatti, dict):
        errs.append(f"{prefix} 'pariyatti' must be an object")
    else:
        if len(pariyatti.get("shortSummary", "")) < 10:
            errs.append(f"{prefix} 'pariyatti.shortSummary' too short (< 10 chars)")
        if len(pariyatti.get("expositionMarkdown", "")) < 20:
            errs.append(f"{prefix} 'pariyatti.expositionMarkdown' too short (< 20 chars)")
        concepts = pariyatti.get("coreConcepts", [])
        if not isinstance(concepts, list) or len(concepts) == 0:
            errs.append(f"{prefix} 'pariyatti.coreConcepts' must contain at least 1 concept")
        misconceptions = pariyatti.get("commonMisconceptions", [])
        if not isinstance(misconceptions, list) or len(misconceptions) == 0:
            errs.append(f"{prefix} 'pariyatti.commonMisconceptions' must contain at least 1 item")

    # patipatti (3P - 2)
    patipatti = data.get("patipatti", {})
    if not isinstance(patipatti, dict):
        errs.append(f"{prefix} 'patipatti' must be an object")
    else:
        if len(patipatti.get("practiceGuide", "")) < 10:
            errs.append(f"{prefix} 'patipatti.practiceGuide' too short (< 10 chars)")

    # pativedha (3P - 3)
    pativedha = data.get("pativedha", {})
    if not isinstance(pativedha, dict):
        errs.append(f"{prefix} 'pativedha' must be an object")
    else:
        if len(pativedha.get("reflectionPrompt", "")) < 5:
            errs.append(f"{prefix} 'pativedha.reflectionPrompt' too short (< 5 chars)")
        checklist = pativedha.get("selfAuditChecklist", [])
        if not isinstance(checklist, list) or len(checklist) == 0:
            errs.append(f"{prefix} 'pativedha.selfAuditChecklist' must contain at least 1 item")

    return errs


def cmd_validate_all(args) -> int:
    """Validate all curriculums and lessons."""
    print("==> Running Deep Validation across all SuttaCentral Curriculums ...")
    if not CURRICULUMS_DIR.exists():
        print(f"Error: {CURRICULUMS_DIR} does not exist.")
        return 1

    all_errors = []
    folders = sorted([d for d in CURRICULUMS_DIR.iterdir() if d.is_dir()])

    total_curriculums = 0
    total_lessons = 0

    for folder in folders:
        curr_file = folder / "curriculum.json"
        if not curr_file.exists():
            continue
        total_curriculums += 1
        errs = validate_single_curriculum(folder)
        all_errors.extend(errs)

        # Count lessons
        data, _ = load_json(curr_file)
        if data:
            total_lessons += sum(len(s.get("lessons", [])) for s in data.get("stages", []))

    if all_errors:
        print(f"\n❌ Validation FAILED with {len(all_errors)} errors:")
        for e in all_errors:
            print(f"  - {e}")
        return 1

    print(f"✓ All {total_curriculums} curriculums and {total_lessons} lessons PASSED strict validation!")
    return 0


def cmd_list(args) -> int:
    """List all curriculums."""
    folders = sorted([d for d in CURRICULUMS_DIR.iterdir() if d.is_dir()])
    print(f"\n{'ID':<26} {'Category':<12} {'Lessons':<9} {'Title'}")
    print("-" * 75)

    for folder in folders:
        curr_file = folder / "curriculum.json"
        if not curr_file.exists():
            continue
        data, _ = load_json(curr_file)
        if not data:
            continue
        c_id = data.get("id", folder.name)
        cat = data.get("category", "general")
        title = data.get("title", "")
        stages = data.get("stages", [])
        lesson_cnt = sum(len(s.get("lessons", [])) for s in stages)
        print(f"{c_id:<26} {cat:<12} {lesson_cnt:<9} {title[:32]}")
    print()
    return 0


def cmd_inspect(args) -> int:
    """Inspect a specific curriculum in detail."""
    curr_id = args.curriculum_id
    curr_dir = CURRICULUMS_DIR / curr_id
    curr_file = curr_dir / "curriculum.json"

    if not curr_file.exists():
        print(f"❌ Curriculum '{curr_id}' not found in {CURRICULUMS_DIR}")
        return 1

    data, err = load_json(curr_file)
    if err:
        print(f"❌ {err}")
        return 1

    print(f"\n📖 Curriculum: {data.get('title')} ({data.get('paliTitle', '')})")
    print(f"   ID: {data.get('id')} | Category: {data.get('category')} | Emoji: {data.get('iconEmoji', '📜')}")
    print(f"   Sources: {data.get('canonicalSource', 'N/A')}")
    print(f"   Target: {data.get('targetAudience', 'N/A')}\n")

    stages = data.get("stages", [])
    total_lessons = 0

    for s in stages:
        s_idx = s.get("stageIndex", 1)
        s_title = s.get("title", "")
        lessons = s.get("lessons", [])
        print(f"   🔹 Stage {s_idx}: {s_title} ({len(lessons)} bài)")
        for l in lessons:
            total_lessons += 1
            l_id = l.get("id")
            l_title = l.get("title", "")
            sutta = l.get("suttaUid", "No UID")

            # Check lesson files
            vi_path = curr_dir / "lessons" / l_id / "vi.json"
            en_path = curr_dir / "lessons" / l_id / "en.json"
            vi_status = "✓ VI" if vi_path.exists() else "✗ VI"
            en_status = "✓ EN" if en_path.exists() else "✗ EN"

            print(f"      • [{l_id}] {l_title} (Sutta: {sutta}) [{vi_status} | {en_status}]")

    print(f"\n   Total Stages: {len(stages)} | Total Lessons: {total_lessons}\n")
    return 0


def cmd_init_curriculum(args) -> int:
    """Scaffold a new curriculum."""
    curr_id = args.id
    if not SLUG_REGEX.match(curr_id):
        print(f"❌ Error: ID '{curr_id}' must contain only lowercase letters, digits, and underscores.")
        return 1

    target_dir = CURRICULUMS_DIR / curr_id
    if target_dir.exists():
        print(f"❌ Error: Curriculum directory '{curr_id}' already exists!")
        return 1

    template_file = TEMPLATES_DIR / "curriculum_template.json"
    if not template_file.exists():
        print(f"❌ Error: Template file '{template_file}' not found.")
        return 1

    with open(template_file, "r", encoding="utf-8") as f:
        content = f.read()

    title_vi = args.title or curr_id.replace("_", " ").title()
    title_en = args.title_en or title_vi
    category = args.category if args.category in VALID_CATEGORIES else "general"

    content = content.replace("{{CURRICULUM_ID}}", curr_id)
    content = content.replace("{{TITLE_VI}}", title_vi)
    content = content.replace("{{TITLE_EN}}", title_en)
    content = content.replace("{{PALI_TITLE}}", args.pali_title or "")
    content = content.replace("{{SUBTITLE_VI}}", args.subtitle or f"Lộ trình tu học {title_vi}")
    content = content.replace("{{SUBTITLE_EN}}", f"Study track on {title_en}")
    content = content.replace("{{DESCRIPTION_VI}}", f"Giáo trình tu học {title_vi} căn cứ theo Kinh tạng Pāḷi.")
    content = content.replace("{{DESCRIPTION_EN}}", f"Practice curriculum on {title_en} based on the Pāḷi Canon.")
    content = content.replace("{{CATEGORY}}", category)
    content = content.replace("{{LESSON_ID}}", f"{curr_id}_l01")

    # Create directories
    target_dir.mkdir(parents=True, exist_ok=True)
    lessons_dir = target_dir / "lessons"
    lessons_dir.mkdir(parents=True, exist_ok=True)

    with open(target_dir / "curriculum.json", "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✓ Successfully initialized new curriculum: {curr_id}")
    print(f"  - Config: {target_dir / 'curriculum.json'}")
    print(f"  - Lessons dir: {lessons_dir}")
    print(f"\nNext: Use 'python3 scripts/curriculum_tool.py add-lesson {curr_id} {curr_id}_l01' to create lessons.")
    return 0


def cmd_add_lesson(args) -> int:
    """Scaffold a new bilingual lesson."""
    curr_id = args.curriculum_id
    lesson_id = args.lesson_id

    curr_dir = CURRICULUMS_DIR / curr_id
    if not curr_dir.exists():
        print(f"❌ Error: Curriculum '{curr_id}' not found.")
        return 1

    if not SLUG_REGEX.match(lesson_id):
        print(f"❌ Error: Lesson ID '{lesson_id}' must be snake_case.")
        return 1

    lesson_dir = curr_dir / "lessons" / lesson_id
    if lesson_dir.exists():
        print(f"❌ Error: Lesson directory '{lesson_id}' already exists in '{curr_id}'.")
        return 1

    lesson_dir.mkdir(parents=True, exist_ok=True)

    vi_tmpl = TEMPLATES_DIR / "lesson_vi_template.json"
    en_tmpl = TEMPLATES_DIR / "lesson_en_template.json"

    with open(vi_tmpl, "r", encoding="utf-8") as f:
        vi_raw = f.read()
    with open(en_tmpl, "r", encoding="utf-8") as f:
        en_raw = f.read()

    sutta_uid = args.sutta or "mn1"
    lesson_num = str(args.number or 1)
    stage_idx = str(args.stage or 1)
    title_vi = args.title or f"Bài học {lesson_id}"
    title_en = args.title_en or f"Lesson {lesson_id}"
    routine = args.routine or "r_morning"

    replacements = {
        "{{LESSON_ID}}": lesson_id,
        "{{CURRICULUM_ID}}": curr_id,
        "{{LESSON_NUMBER}}": lesson_num,
        "{{STAGE_INDEX}}": stage_idx,
        "{{TITLE_VI}}": title_vi,
        "{{TITLE_EN}}": title_en,
        "{{PALI_TITLE}}": args.pali_title or "",
        "{{SUTTA_UID}}": sutta_uid,
        "{{SUTTA_TITLE_VI}}": f"Kinh xuất xứ ({sutta_uid.upper()})",
        "{{SUTTA_TITLE_EN}}": f"Canonical Discourse ({sutta_uid.upper()})",
        "{{EXCERPT_PALI}}": "...",
        "{{EXCERPT_TRANSLATION_VI}}": "...",
        "{{EXCERPT_TRANSLATION_EN}}": "...",
        "{{SHORT_SUMMARY_VI}}": f"Tóm tắt nền tảng giáo lý của bài học {title_vi}.",
        "{{SHORT_SUMMARY_EN}}": f"Summary of doctrinal foundations for {title_en}.",
        "{{CONCEPT_TERM_VI}}": "Chánh Kiến",
        "{{CONCEPT_TERM_EN}}": "Right View",
        "{{CONCEPT_PALI}}": "Sammādiṭṭhi",
        "{{CONCEPT_DEF_VI}}": "Sự hiểu biết đúng đắn về thực tại và quy luật nhân quả.",
        "{{CONCEPT_DEF_EN}}": "Correct understanding of reality and karma.",
        "{{MISCONCEPTION_MISTAKE_VI}}": "Hiểu lầm phổ biến...",
        "{{MISCONCEPTION_MISTAKE_EN}}": "Common misconception...",
        "{{MISCONCEPTION_CORRECTION_VI}}": "Sửa lại cho đúng Chánh pháp...",
        "{{MISCONCEPTION_CORRECTION_EN}}": "Canonical correction...",
        "{{PRACTICE_GUIDE_VI}}": "Hướng dẫn thực hành cụ thể trong ngày...",
        "{{PRACTICE_GUIDE_EN}}": "Specific practice instructions for daily life...",
        "{{ROUTINE_ID}}": routine,
        "{{SUGGESTED_VIRTUE_VI}}": "Nuôi dưỡng tâm từ ái và tỉnh giác",
        "{{SUGGESTED_VIRTUE_EN}}": "Cultivating loving-kindness and mindfulness",
        "{{REFLECTION_PROMPT_VI}}": "Hôm nay bạn đã thực hành chánh niệm như thế nào?",
        "{{REFLECTION_PROMPT_EN}}": "How mindfully did you dwell today?",
    }

    for k, v in replacements.items():
        vi_raw = vi_raw.replace(k, v)
        en_raw = en_raw.replace(k, v)

    with open(lesson_dir / "vi.json", "w", encoding="utf-8") as f:
        f.write(vi_raw)
    with open(lesson_dir / "en.json", "w", encoding="utf-8") as f:
        f.write(en_raw)

    print(f"✓ Created lesson '{lesson_id}' for '{curr_id}':")
    print(f"  - {lesson_dir / 'vi.json'}")
    print(f"  - {lesson_dir / 'en.json'}")
    print(f"\nRemember to also record this lesson in '{curr_dir / 'curriculum.json'}' under stage #{stage_idx}!")
    return 0


def main():
    parser = argparse.ArgumentParser(description="SuttaCentral Curriculum Management CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # validate-all
    subparsers.add_parser("validate-all", help="Validate all curriculums and 3P lesson files")

    # list
    subparsers.add_parser("list", help="List all curriculums")

    # inspect
    inspect_parser = subparsers.add_parser("inspect", help="Inspect a single curriculum")
    inspect_parser.add_argument("curriculum_id", help="Curriculum ID (folder name)")

    # init-curriculum
    init_parser = subparsers.add_parser("init-curriculum", help="Initialize a new curriculum")
    init_parser.add_argument("id", help="Curriculum ID (snake_case)")
    init_parser.add_argument("--title", help="Vietnamese title")
    init_parser.add_argument("--title-en", help="English title")
    init_parser.add_argument("--pali-title", help="Pāḷi canonical title")
    init_parser.add_argument("--subtitle", help="Subtitle")
    init_parser.add_argument("--category", choices=VALID_CATEGORIES, default="general", help="Category")

    # add-lesson
    add_parser = subparsers.add_parser("add-lesson", help="Add a new bilingual 3P lesson")
    add_parser.add_argument("curriculum_id", help="Curriculum ID")
    add_parser.add_argument("lesson_id", help="Lesson ID (snake_case)")
    add_parser.add_argument("--number", type=int, default=1, help="Lesson number")
    add_parser.add_argument("--stage", type=int, default=1, help="Stage index")
    add_parser.add_argument("--title", help="Vietnamese title")
    add_parser.add_argument("--title-en", help="English title")
    add_parser.add_argument("--pali-title", help="Pāḷi title")
    add_parser.add_argument("--sutta", help="SuttaCentral UID pointer (e.g. mn41, sn55.1)")
    add_parser.add_argument("--routine", help="Recommended routine ID (e.g. r_morning)")

    args = parser.parse_args()

    if args.command == "validate-all":
        sys.exit(cmd_validate_all(args))
    elif args.command == "list":
        sys.exit(cmd_list(args))
    elif args.command == "inspect":
        sys.exit(cmd_inspect(args))
    elif args.command == "init-curriculum":
        sys.exit(cmd_init_curriculum(args))
    elif args.command == "add-lesson":
        sys.exit(cmd_add_lesson(args))
    else:
        parser.print_help()
        sys.exit(0)


if __name__ == "__main__":
    main()
