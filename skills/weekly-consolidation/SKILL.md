---
name: weekly-consolidation
description: >
  Consolidate 7 daily summaries into a weekly summary that gets ingested into the wiki vault.
  Contrasts new weekly content against long-term MEMORY.md to identify conflicts, reinforcements,
  and new patterns. Use on Mondays (or start of new week) to review previous week.
  Triggers on: "consolidar semana", "weekly summary", "resumo semanal", "ingest wiki weekly",
  "consolidação semanal".
---

# Weekly Consolidation

## Overview

At the start of each week, consolidate the previous 7 daily summaries into one weekly summary.
This weekly summary is then ingested into the wiki vault as a source page.
Additionally, the week is contrasted against long-term MEMORY.md to identify:
- **Conflicts**: Things the week contradicted from long-term memory
- **Reinforcements**: Things the week confirmed or expanded upon
- **New patterns**: First-time observations or concepts
- **Evolutions**: Things that changed meaning/intensity since last recorded

## When to Use

- **Weekly trigger**: Every Monday (00:00-06:00 UTC) or start of new week
- **Manual**: User says "consolidar semana", "resumo semanal", "weekly digest"
- **Before big planning sessions**: Week-in-review before new project phases
- **Monthly retrospective**: First weekly of month → also update MEMORY.md highlights

## Workflow

### Step 1 — Collect Daily Summaries

Find all daily summaries from target week:
```bash
# Determine week boundaries (previous Monday to Sunday UTC)
# Example for 2026-04-22 (Wednesday):
# Week to consolidate: 2026-04-13 (Mon) to 2026-04-19 (Sun)

WEEK_START="2026-04-13"
WEEK_END="2026-04-19"

# List all daily summaries in range
for d in 13 14 15 16 17 18 19; do
  f="memory/summaries/daily/2026-04-${d}.md"
  [ -f "$f" ] && echo "Found: $f"
done
```

### Step 2 — Read All Daily Summaries

Read all 7 daily summaries in chronological order. Look for:
- Recurring topics or decisions
- Evolution of ongoing projects
- Contradictions between days
- Notable events or milestones

### Step 3 — Read Long-Term Memory

```bash
cat MEMORY.md
```

Key areas to check for contrast:
- Decisions (have any changed?)
- User preferences (any new observations?)
- Technical configs (any updates?)
- Project status (progress? blockers?)
- Pending actions (any resolved?)

### Step 4 — Generate Week Analysis

#### Part A: Week Narrative
Write a coherent summary of the week:
```markdown
# Semana de YYYY-MM-DD a YYYY-MM-DD

## Visão Geral da Semana
[2-3 sentences: What happened this week? What was the focus?]

## Temas Principais
- Theme 1: [what happened, across which days]
- Theme 2: [what happened, across which days]
- Theme 3: [what happened, across which days]

## Marcos e Conclusões
- [Date] — Milestone: [description]
- [Date] — Conclusion: [description]

## Desenvolvimento de Projetos
- Project: status update
```

#### Part B: Contrast Against Long-Term Memory

```markdown
## Contrast with Long-Term Memory

### Confirmações (+)
- [Long-term fact] — Week [confirmed/expanded]: [details]
- [Long-term fact] — Week reinforced: [details]

### Contradições (~)
- [Long-term claim] — Week contradicts: [what changed and why]
- [Long-term claim] — Week challenges: [new evidence]

### Evolusções → 
- [Concept from MEMORY.md] — Week added nuance: [what new understanding emerged]
- [Preference from MEMORY.md] — Week shifted: [new observation]

### Padrões Novos ★
- First observation: [thing seen for first time this week]
- New pattern: [recurring behavior or preference detected]
```

### Step 5 — Ingest into Wiki

```bash
openclaw wiki ingest memory/summaries/weekly/YYYY-WNN.md
```

Where WNN = week number (e.g., W16 = 16th week of year).

### Step 6 — Update MEMORY.md (if new significant facts)

If the week produced genuinely new knowledge not yet in MEMORY.md:
- Add to MEMORY.md under appropriate section
- Note source: "Consolidado da semana YYYY-WNN"

### Step 7 — Archive Daily Summaries (optional)

After successful consolidation:
- Move the 7 daily summaries to `memory/summaries/weekly-archive/YYYY/`
- Keep the weekly summary in `memory/summaries/weekly/`

## Wiki Ingestion Details

Weekly summaries become wiki sources with:
- `sourceType: weekly-consolidation`
- `week: YYYY-WNN`
- `dateRange: YYYY-MM-DD to YYYY-MM-DD`
- Auto-linked to relevant entities/concepts via wiki search

Run after ingestion:
```bash
openclaw wiki compile
openclaw wiki lint
```

## Principles

1. **7-into-1**: One week = one weekly summary (not 7 mini-summaries)
2. **Narrative > list**: Tell the story of the week, don't just enumerate
3. **Contrast is key**: The value is in comparing to MEMORY.md — don't skip Step 3
4. **Quality over speed**: If unsure about a contrast interpretation, note it as "possible" rather than making assumptions
5. **Weekly feeds wiki**: The weekly summary is the primary unit for wiki ingestion

## Output Location

```
memory/summaries/weekly/YYYY-WNN.md   ← weekly summary (ingested to wiki)
memory/summaries/daily/YYYY-MM-DD.md   ← daily summaries (source material)
memory/summaries/weekly-archive/YYYY/  ← archived dailies (after consolidation)
```

## Quick Commands

```bash
# List existing weekly summaries
ls memory/summaries/weekly/

# Find the most recent weekly summary
ls -t memory/summaries/weekly/*.md | head -3

# Check current week number
date +%G-V
```

## Resources

See `references/weekly-guide.md` for detailed patterns, contrast examples, and wiki integration specifics.