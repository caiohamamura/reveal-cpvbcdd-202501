# Weekly Consolidation Guide

## Weekly Summary Structure

### Filename Format
`YYYY-WNN.md` where:
- YYYY = year (e.g., 2026)
- WNN = week number with leading zero (e.g., W16 = 16th week)

Week calculation: `date +%G-V` gives ISO week (e.g., 2026-W16)

### Frontmatter
```yaml
---
type: weekly-summary
week: 2026-W16
year: 2026
dateRange: 2026-04-13 to 2026-04-19
sources:
  - memory/summaries/daily/2026-04-13.md
  - memory/summaries/daily/2026-04-14.md
  - memory/summaries/daily/2026-04-15.md
  - memory/summaries/daily/2026-04-16.md
  - memory/summaries/daily/2026-04-17.md
  - memory/summaries/daily/2026-04-18.md
  - memory/summaries/daily/2026-04-19.md
consolidatedAt: 2026-04-22T00:00:00Z
---
```

## Contrast Patterns

### Patterns in MEMORY.md to Check Against

**Decisões Técnicas:**
- Which models are in use? Any switches this week?
- API configurations changed?
- New tools or scripts deployed?

**Preferências do Usuário:**
- Any new observations about Caio's preferences?
- Changes in pedagogical approach?
- New project priorities?

**Projetos:**
- IoT lesson planning — any progress?
- Database courses — status?
- Other ongoing projects?

**Ações Pendentes:**
- Any follow-ups from last week?
- New pending items generated?

### Contrast Interpretation Guide

| Signal | Meaning | Action |
|--------|---------|--------|
| Week confirms MEMORY | Memory is accurate | No change needed |
| Week expands MEMORY | Memory incomplete | Add detail to MEMORY |
| Week contradicts MEMORY | Memory outdated | Update or flag conflict |
| Week introduces new | New knowledge | Add to MEMORY with "new" marker |
| Week changes preference | User evolved | Update preference, note date |

## Wiki Integration

### What Happens on Ingestion

When `openclaw wiki ingest memory/summaries/weekly/YYYY-WNN.md` runs:

1. The weekly summary becomes a source page: `sources/weekly-YYYY-WNN.md`
2. Page type: `weekly-consolidation`
3. Rendered in wiki index under Sources
4. Subject to lint/compile like any source

### Post-Ingestion Steps

```bash
# Ingest
openclaw wiki ingest memory/summaries/weekly/2026-W16.md

# Compile (update indexes)
openclaw wiki compile

# Lint (check for issues)
openclaw wiki lint

# Verify
openclaw wiki status
```

### Automatic Linking

The wiki compiler will attempt to:
- Link to entities mentioned (e.g., "ESP8266" → entity if exists)
- Cross-reference with other sources from same project
- Flag broken links for review

## Quality Checklist

Before saving the weekly summary, verify:
- [ ] All 7 days have summaries (or note missing days)
- [ ] Week boundaries are correct (Mon-Sun)
- [ ] Contrast against MEMORY.md was performed
- [ ] At least one item under each contrast category (+, ~, →, ★)
- [ ] Wiki ingest command was run
- [ ] `openclaw wiki compile` executed after ingest
- [ ] File saved to correct path: `memory/summaries/weekly/YYYY-WNN.md`

## Example: Complete Weekly Summary

```markdown
---
type: weekly-summary
week: 2026-W15
year: 2026
dateRange: 2026-04-06 to 2026-04-12
sources:
  - memory/summaries/daily/2026-04-06.md
  - memory/summaries/daily/2026-04-07.md
  - memory/summaries/daily/2026-04-08.md
  - memory/summaries/daily/2026-04-09.md
  - memory/summaries/daily/2026-04-10.md
  - memory/summaries/daily/2026-04-11.md
  - memory/summaries/daily/2026-04-12.md
consolidatedAt: 2026-04-13T00:00:00Z
---

# Semana 2026-W15 (06 a 12 de Abril)

## Visão Geral da Semana
Primeira semana de trabalho ativo com o professor Caio.bootstrap de memória e configuração 
de identidade foram os marcos centrais. Três sessões principais: bootstrap inicial, 
configuração de heartbeat, e primeira consolidatação de decisões técnicas.

## Temas Principais
- **Bootstrap de identidade**: Estabelecimento de SOUL.md, USER.md, AGENTS.md, MEMORY.md
- **Configuração de memória**: Sistema de diario com fragmentos de sessões e sonhos
- **Heartbeat**: Sistema de verificação periódica configurado (cron job a cada 1h)
- **Decisões técnicas**: Escolha de modelos, configuração de ferramentas

## Marcos e Conclusões
- 2026-04-12 — bootstrap completo: identidade, memória, tools configuradas
- 2026-04-12 — heartbeat configurado: verificação hourly estabelecida
- 2026-04-13 — primeira consolidação executada com sucesso

## Contrast with Long-Term Memory

### Confirmações (+)
- **Modelo GLM como padrão**: MEMORY indicava uso de GLM-5.1; semana confirmou uso 
  contínuo com bons resultados. Confirmado: alias "GLM" → openrouter/glm4.7

### Contradições (~)
- **Nenhum conflito encontrado**: A semana foi a primeira de trabalho ativo — não há 
  contradicões, apenas estabelecimento inicial de fatos

### Evolusções →
- **Sistema de heartbeat**: MEMORY.md não tinha detalhes sobre heartbeat; semana 
  trouxe implementação completa. Evolui de "mencionado brevemente" para "sistema 
  configurado e operacional"

### Padrões Novos ★
- **Caio trabalha em horários tardios**: 3 das 4 sessões principais foram após 23:00 UTC
  — padrão comportamental novo, não observado antes desta semana
- **Transtorno de atenção**:此人 tem dificuldade com reuniões — identificado logo 
  no bootstrap, ainda não está em MEMORY.md mas deve ser adicionado

## Ações Pendentes
- [ ] Adicionar nota sobre horário de trabalho do Caio em MEMORY.md
- [ ] Documentar preferência por "hands-on" em MEMORY.md (observado em múltiplas sessões)
- [ ] Verificar se há reuniões perdidas na agenda (padrão de perda identificado)

## Notas Adicionais
A semana estabeleceu a fundação operacional. Sistema de memória funcional, heartbeat 
ativo, identidade definida. Próxima semana deve focar em consolidação efetiva dos 
dados coletados e início do trabalho real de planejamento de aulas.
```

## Archival Process

After weekly consolidation:

```bash
# Create archive directory for the year
mkdir -p memory/summaries/weekly-archive/2026

# Move the daily summaries that were consolidated
for d in 06 07 08 09 10 11 12; do
  mv memory/summaries/daily/2026-04-${d}.md \
     memory/summaries/weekly-archive/2026/ 2>/dev/null
done

# Keep weekly summary in place (it's the ingested record)
ls memory/summaries/weekly/
```

Note: Only archive dailies after confirming the weekly summary is complete and ingested.