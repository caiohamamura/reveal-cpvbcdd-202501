---
name: validate-slides
description: Run deterministic validation checks for Reveal.js slide decks in this repository.
---

Use this skill after creating or editing Reveal.js slide HTML files.

## Deterministic Checks

Run the bundled validator instead of recreating ad hoc shell/Python snippets:

```bash
python .opencode/skills/validate-slides/scripts/validate_slide_deck.py bdd2/aula13-redis-nosql.html
```

For multiple files:

```bash
python .opencode/skills/validate-slides/scripts/validate_slide_deck.py bdd2/*.html
```

## What It Checks

- HTML parses with Python `HTMLParser`
- No Chinese characters in student-facing HTML
- No `<script>` tags inside `<code-block>`
- `FASE N` comment blocks are closed with matching `fim Fase N` before the next phase starts
- Local `href` and `src` references exist on disk
- Every `<img>` tag has non-empty `alt`
- Local images are valid binary files larger than 1KB when Pillow is available

## Expected Workflow

1. Edit the deck.
2. Run `validate_slide_deck.py` on the changed HTML file.
3. Fix every `ERROR`.
4. Treat `WARN` messages as review items; fix them when relevant.
5. Report the validation outcome to the user.

## Notes

- Remote URL status/MIME checks are intentionally not included yet because they require network access and can be flaky.
- Browser visual QA is still separate; this script covers deterministic static checks only.
