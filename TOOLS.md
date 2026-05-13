# TOOLS.md - Environment-Specific Notes

## Moodle

- **Base:** `https://ead.cpv.ifsp.edu.br`
- **Token:** stored in `.env` as `MOODLE_TOKEN` *(updated 2026-05-13)*

### Courses

| ID | Code | Name |
|----|------|------|
| 1639 | CPVIOTS | IoT |
| 1486 | CPVBDD2 | Banco de Dados II |
| 1498 | CPVCIDA | Ciência de Dados |

### Access Rules

**SEMPRE que uma pergunta for sobre aulas, tarefas, disciplinas ou atividades no Moodle**, consultar o Moodle primeiro.

Use the `webfetch` tool for all Moodle interactions:

```
webfetch({ url: "https://ead.cpv.ifsp.edu.br/course/view.php?id=1498" })
```

For authenticated access, append `?sesskey=...` or pass the session cookie. If webfetch returns a login redirect (302 to `/login/`), fall back to curl with the cookie from .env:

```bash
source .env && curl -s -b "MoodleSession=$MOODLE_TOKEN" "https://ead.cpv.ifsp.edu.br/course/view.php?id=1498"
```

When the cookie expires (302 redirect), ask Caio for a new token and update `.env`.

### Moodle Skill

Load the `moodle` skill for full Moodle API patterns (scraping, assignments, submissions).
