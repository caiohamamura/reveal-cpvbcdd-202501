# Daily Consolidation Guide

## Daily Summary Structure

### Frontmatter
```yaml
---
type: daily-summary
date: 2026-04-21
sources:
  - memory/2026-04-21.md
  - memory/dreaming/light/2026-04-21.md
  - memory/dreaming/deep/2026-04-21.md
  - memory/dreaming/rem/2026-04-21.md
consolidatedAt: 2026-04-22T00:00:00Z
---
```

### Sections Explained

**Visão Geral**: One paragraph max. What was the day about in one sentence?

**Sessões**: List each session with time and topic. Example:
- 14:00 UTC — IoT lesson planning, discussed ESP8266 curriculum
- 18:30 UTC — Heartbeat check, found email from DAE CPV

**Decisões**: Only non-obvious decisions. "Used default model" is not a decision; "Switched from DeepSeek to GLM after timeout issues" is.

**Fatos Técnicos**: Write as facts, not stories. Example:
- `gog` email: ariahamamura@gmail.com (inbox for copies of Caio's emails)
- Telegram bot token: configured in TOOLS.md

**Lições Aprendidas**: Format: "[What happened] → [What to remember]". Example:
- "API timeout with no response body → check server health before assuming auth failure"

**Síntese dos Sonhos**: Don't list each dream entry individually. Synthesize themes:
- "Light sleep: session start patterns dominated; Deep: technical configurations surfaced; REM: emotional themes about teaching"
- Quote the most interesting or poetic fragment if one stands out

**Ações**: Keep simple. Use checkbox format for pendentes.

## Source Prioritization

When fragments conflict (e.g., two sessions saying different things):
1. Trust the most recent file timestamp
2. Trust the longest/more detailed entry
3. Note conflict in "Notas" if significant

## Disk Management

- Daily summaries are small (~2-5KB each)
- Keep all summaries indefinitely (they're the condensed history)
- Original fragment files: keep at least 30 days, then optionally archive
- After archiving: the summaries become the primary record

## Example: Synthesizing Multiple Dream Files

If light/deep/rem all have entries for the same day:

```
## Síntese dos Sonhos

**Padrões emergentes:**
- `user` apareceu 1500+ vezes nos fragmentos (reflecte fluxo de mensagens)
- `utc` e `session` são marcadores temporais constantes
- Sonhos REM incluíram reflexões sobre "documentar projetos" e "empregabilidade"

**Fragmento mais marcante (REM):**
> "O ESP8266 como semente — pequeno, barato, cheirando a Wi-Fi 
>  e possibilidades. Treze tópico."
```

## Quality Checklist

Before saving the daily summary, verify:
- [ ] Date in frontmatter matches target date
- [ ] All source files are listed
- [ ] No raw log entries copied verbatim (synthesized, not pasted)
- [ ] Timezones are UTC
- [ ] Actions have clear status (concluída vs pendente)
- [ ] File saved to correct path: `memory/summaries/daily/YYYY-MM-DD.md`