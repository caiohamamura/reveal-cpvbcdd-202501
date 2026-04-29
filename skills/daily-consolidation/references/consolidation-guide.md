# Consolidation Guide — Detailed Reference

## Daily File → MEMORY.md Extraction Patterns

### Pattern 1: Decisions
Raw daily entries often look like:
```
[2026-04-16 14:32] Used GLM instead of DeepSeek for this session
```

Extract to MEMORY.md as:
```markdown
### 2026-04-16
- **Modelo padrão alterado**: DeepSeek V3.2 → GLM (melhor performance no N100)
```

### Pattern 2: Technical Facts
Raw:
```
API Google timeout: context deadline exceeded
Drive bugado no servidor — resolved after fix
```

Extract:
```markdown
### APIs e Serviços
- **API Google timeout crônico**: Pode indicar problema de drive/IO no servidor (18/04)
  - Solução: Verificar saúde do servidor antes de assumir problema de autenticação
```

### Pattern 3: Lessons Learned (LIÇÃO entries)
Raw:
```
⚠️ LIÇÃO: Sempre ler o conteúdo dos emails, nunca julgar pelo assunto
Perdi a reunião do curso de Informática por não ter lido o email
```

Extract:
```markdown
### Lições Aprendidas
- **Email**: SEMPRE ler conteúdo completo, nunca assumir pelo subject
  - Já perdemos reunião do curso de Informática por não ler email
```

### Pattern 4: User Preferences
Raw: Observed across multiple sessions
```
[session] Caio gostou da abordagem prática
[session] Preocupado com empregabilidade dos alunos
```

Extract:
```markdown
### Preferências do Professor Caio
- **Pedagógicas**: Hands-on > teoria pura; projetos reais > exercícios artificiais
- **Preocupações**: Empregabilidade dos alunos, recursos limitados
```

## MEMORY.md Structure Template

```markdown
# MEMORY.md - Long-Term Memory

## Sobre este arquivo
[Brief description — what belongs here]

## Decisões Importantes
### YYYY-MM-DD
- Decision: context and why

## Fatos Técnicos
### ferramentas e Configurações
- Tool X: key info, date configured

### APIs e Serviços
- Service: status, key details

## Lições Aprendidas
- Lesson: context → what to remember

## Preferências do Usuário
- Preference: observed basis

## Contextos de Projeto
### Project Name
- Scope, key dates, current status

## Ações Pendentes
- [ ] Follow-up item (source: date)
- [ ] Another item (source: date)

## Consolidações anteriores
- YYYY-MM-DD: scope of consolidation
```

## Wiki Entity Creation

When you find a significant concept that should be a wiki entity:

1. Create `wiki/main/entities/concept-name.md`:
```markdown
---
pageType: entity
id: entity.<name>
title: <Name>
status: active
updatedAt: YYYY-MM-DDTHH:MM:SSZ
---

# <Name>

## Summary
[2-3 sentence description]

## Key Facts
- Fact 1
- Fact 2

## Related
- [[entities/related-entity]]
- [[sources/related-source]]
```

## Archival Strategy

- **Keep**: Last 30 days of daily files
- **Archive**: 30-90 days → `memory/archive/YYYY-QN/`
- **Delete**: >90 days old (only if explicitly requested)

Archival command:
```bash
mkdir -p memory/archive/2026-Q2
mv memory/2026-01-??.md memory/archive/2026-Q1/ 2>/dev/null
```