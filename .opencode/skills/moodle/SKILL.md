---
name: moodle
description: Moodle LMS scraping and interaction — list courses, assignments, submissions, grades. Use webfetch first, curl fallback for authenticated pages.
license: MIT
compatibility: opencode
metadata:
  audience: instructors
  domain: education
---

# Moodle Skill

Interact with Moodle LMS at `https://ead.cpv.ifsp.edu.br`.

## Access Pattern

**Prefer `webfetch` tool over raw curl.** Use this decision flow:

1. **Public pages** (course search, public content) → `webfetch` directly
2. **Authenticated pages** → try `webfetch` first; if login redirect detected, fall back to curl with cookie from `TOOLS.md`

### webfetch (preferred)

```
webfetch({ url: "https://ead.cpv.ifsp.edu.br/course/search.php?search=CPVCIDA" })
```

The webfetch tool returns markdown by default. Use `format: "html"` when you need to parse raw HTML structure (e.g., extracting assignment IDs, form fields).

### curl (fallback for authenticated pages)

When webfetch can't authenticate:

```bash
curl -s -b "MoodleSession=$MOODLE_TOKEN" \
  "https://ead.cpv.ifsp.edu.br/course/view.php?id=1498"
```

Detect expired cookie: response contains `login/index.php` redirect or `303` status.
Update token in `.env` when expired.

## Courses

| ID | Code | Name |
|----|------|------|
| 1639 | CPVIOTS | IoT |
| 1486 | CPVBDD2 | Banco de Dados II |
| 1498 | CPVCIDA | Ciência de Dados |

## Common Operations

### Search courses

```
webfetch({ url: "https://ead.cpv.ifsp.edu.br/course/search.php?search=<QUERY>" })
```

Then grep for `course/view.php?id=(\d+)` to extract course IDs.

### List assignments on a course

```
webfetch({ url: "https://ead.cpv.ifsp.edu.br/course/view.php?id=<COURSE_ID>", format: "html" })
```

Extract: `assign/view.php\?id=(\d+)` for assignment cmids.

### View assignment details

```
webfetch({ url: "https://ead.cpv.ifsp.edu.br/mod/assign/view.php?id=<CMID>" })
```

### View assignment submissions

```
webfetch({ url: "https://ead.cpv.ifsp.edu.br/mod/assign/view.php?id=<CMID>&action=grading" })
```

### Download submissions (batch)

Use the grading-skill scripts:

```bash
python3 .opencode/skills/grading-skill/scripts/download_submissions.py <CMID> --output /tmp/subs_<CMID>/
```

## REGRA DE OURO

**NUNCA envie notas ao Moodle sem autorização explícita do Caio.**

Workflow: consultar → testar → mostrar resultados no chat → aguardar autorização → submeter.

## Quick Grading (POST)

Moodle quick grading submits to `POST /mod/assign/view.php` with form data:

```python
data = {
    "id": cmid,
    "action": "quickgrade",
    "sesskey": sesskey,
    "_qf__mod_assign_quick_grading_form": "1",
    "sendstudentnotifications": "on",
    "perpage": "-1",
}
# Per-student fields:
data[f"grademodified_{user_id}"] = ""
data[f"gradeattempt_{user_id}"] = "0"
data[f"quickgrade_{user_id}"] = "90"       # grade
data[f"quickgrade_comments_{user_id}"] = "feedback text"
```

Extract `user_id` from `<tr class="user<id>">` in the grading table (use BeautifulSoup: `tr.select("[class^=user]")`).

### Get student groups (participants page)

```bash
curl -s -b "MoodleSession=$MOODLE_TOKEN" "https://ead.cpv.ifsp.edu.br/user/index.php?id=<COURSE_ID>&group=<GROUP_ID>"
```

Extract names from `<a href="...user/view...">`. Group IDs found in the group selector dropdown on the same page.

## Colab Notebooks

Students often submit Google Colab links as online text. Download via Google Drive:

```bash
# Extract FILE_ID from Colab URL (the string after /drive/)
curl -s -L -o output.ipynb "https://drive.google.com/uc?export=download&id=<FILE_ID>"
```

Check validity: parse as JSON, verify `nbformat` key exists. Public notebooks work; private ones redirect to Google login.

## Gotchas

- **webfetch no cookies** — always falls back to login redirect for authenticated pages. Use curl for anything behind Moodle auth.
- **download_submissions.py cookie** — script has hardcoded cookie (line 19). Update when token changes.
- **Group folder suffixes** — Moodle downloadall ZIP extracts as `Grupo C_332_assignsubmission_file/`. The numeric suffix is the group ID, not student ID. Strip to match plain group names.
- **Grading skill not auto-discovered** — if skill doesn't appear in available_skills, check: directory name matches `name` in frontmatter exactly, SKILL.md is uppercase, no stray `.md` files in `.opencode/skills/`.
