---
name: daily-consolidation
description: >
  Consolidate all daily memory fragments (memory/YYYY-MM-DD.md and memory/dreaming/*/YYYY-MM-DD.md)
  into a single structured daily summary. Use at end of day or start of next day.
  Triggers on: "consolidar diário", "daily summary", "resumo do dia", "consolidar sonhos", "end of day".
---

# Daily Consolidation

## Overview

At end of day (or start of next day), consolidate all memory fragments from that calendar day
into one structured daily summary file: `memory/summaries/daily/YYYY-MM-DD.md`.

This includes:
- Raw daily log: `memory/YYYY-MM-DD.md`
- Dream reports: `memory/dreaming/light/YYYY-MM-DD.md`, `dreaming/deep/`, `dreaming/rem/`

## When to Use

- **Daily trigger**: End of day (23:00-00:30 UTC) or beginning of next day
- **Manual**: User says "consolidar diário", "resumo do dia", "consolidar sonhos"
- **Session start**: If last session was >18h ago and no daily summary exists for yesterday

## Workflow

### Step 1 — Identify Target Date

Use the date of the most recent memory file:
```bash
ls -t memory/*.md | grep -v TEMPLATE | grep -v heartbeat-state | head -1
# Returns most recent file like "2026-04-21.md" → target date = 2026-04-21
```

### Step 2 — Gather All Fragments for That Date

Collect all files with the target date in filename:
```bash
# Daily log
TARGET="2026-04-21"
cat memory/${TARGET}.md

# Dream files (all phases)
cat memory/dreaming/light/${TARGET}.md 2>/dev/null
cat memory/dreaming/deep/${TARGET}.md 2>/dev/null
cat memory/dreaming/rem/${TARGET}.md 2>/dev/null
```

### Step 3 — Extract Key Information

From all fragments, extract and synthesize:

1. **Sessões do dia**: How many sessions, what was discussed
2. **Decisões tomadas**: Choices made, configurations changed
3. **Fatos técnicos**: Tool setups, API changes, errors encountered
4. **Lições aprendidas**: Lessons, mistakes fixed, warnings noted
5. **Sonhos**: Dream entries (light/deep/rem) — synthesize patterns and insights
6. **Ações concluídas**: Tasks completed, projects advanced
7. **Ações pendentes**: Follow-ups still open
8. **Humor/energia do dia**: (inferred from session patterns)

### Step 4 — Write Daily Summary

Create `memory/summaries/daily/YYYY-MM-DD.md`:

```markdown
---
type: daily-summary
date: YYYY-MM-DD
sources: [memory/YYYY-MM-DD.md, dreaming/*/YYYY-MM-DD.md]
---

# Resumo Diário — YYYY-MM-DD

## Visão Geral
[1-2 sentence summary of the day]

## Sessões
- HH:MM UTC — [topic or activity]
- HH:MM UTC — [topic or activity]

## Decisões
- Decision: context

## Fatos Técnicos
- Technical fact: details

## Lições Aprendidas
- Lesson: what to remember

## Síntese dos Sonhos
[Dream patterns across light/deep/rem — what surfaced, themes, insights]

## Ações
### Concluídas
- Completed task

### Pendentes
- [ ] Open follow-up

## Notas
[Any other significant observations]
```

### Step 5 — Verify and Log

- Save the file
- Log consolidation in heartbeat-state.json
- Optionally remove redundant fragment files (keep originals unless disk space is low)

## Principles

1. **One day = one summary**: Aggregate all fragments from that calendar day
2. **Synthesis over copy**: Don't just concatenate — create a coherent narrative
3. **Preserve source files**: Keep original fragments (summaries are additions, not replacements)
4. **Time-zone aware**: Use UTC timestamps consistently
5. **Dream integration**: Treat dream phases as equal sources with daily logs

## Quick Command

```bash
# Quick check if today's summary exists
ls memory/summaries/daily/$(date +%Y-%m-%d).md 2>/dev/null && echo "EXISTS" || echo "MISSING"
```

## Resources

See `references/daily-guide.md` for detailed patterns and examples.