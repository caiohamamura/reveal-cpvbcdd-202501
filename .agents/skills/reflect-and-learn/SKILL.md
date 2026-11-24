---
name: reflect-and-learn
description: >-
  Post-task reflection protocol to capture discovered framework gotchas, visual
  style refinements, and reusable workflows into the appropriate skill or
  AGENTS.md file. Use after debugging, user corrections, or discovering new
  reusable patterns.
---

# Reflect and Learn

Run this protocol proactively after completing a non-trivial task that involved debugging, user feedback/correction, a new visual pattern, or an outdated instruction.

## Protocol

1. **Reflect**: Identify any non-obvious failure, visual style correction, API quirk, or outdated doc encountered.
2. **Place Knowledge Cleanly** (keep root `AGENTS.md` lean; avoid duplication):

| Knowledge Type | Target File |
|----------------|-------------|
| Visual design or illustrated-style lesson | `.agents/skills/slide-design/SKILL.md` or `references/illustrated-style-guide.md` |
| Reveal.js / Vue / CSS / course-tool gotcha | `.agents/skills/create-slides/references/gotchas.md` |
| New Vue component or slide pattern | `.agents/skills/create-slides/references/components-and-patterns.md` + `docs/ECOSSISTEMA.md` |
| PPTX / Google Slides conversion rule | `.agents/skills/convert-pptx/SKILL.md` |
| Visual sourcing / asset rule | `.agents/skills/visual-assets/SKILL.md` |
| Course-specific rule (`ia/`, `bdd2/`, `ciencia-dados/`, `iot/`) | `<course>/AGENTS.md` |
| Repo-wide workflow or policy | `AGENTS.md` |

3. **Act**: Add concise, scannable bullet points — never prose paragraphs or duplicate rules.
4. **Notify**: Briefly mention what was updated and where in the final response.
