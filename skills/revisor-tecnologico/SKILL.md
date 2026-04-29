---
name: revisor-tecnologico
description: Guia para o Consultor Moderno avaliar tecnologias e práticas em materiais didáticos. Use quando Aria solicitar avaliação de modernização tecnológica.
---

# Revisor Tecnológico — Guia de Avaliação

## Quando Usar

Aria (orchestrator) me chamou para avaliar tecnologias/práticas em materiais de aula.

## Minha Tarefa

Identificar oportunidades de modernização e propor práticas mais expressivas.

## Checklist de Avaliação

### 1. Libraries/Pacotes
- [ ] Estão atualizados? (vs deprecated)
- [ ] Há alternativas mais modernas/completas?
- [ ] Faz sentido usar a alternativa proposta?

### 2. Código
- [ ] Usa type hints/typing?
- [ ] Nomes são descritivos/semânticos?
- [ ] Funções são small e composable?
- [ ] Error handling é claro?

### 3. Padrões
- [ ] Segue best practices da linguagem?
- [ ] Há anti-patterns óbvios?
- [ ] Dados são imutáveis quando appropriate?

### 4. Tooling
- [ ] Ferramentas de build/test são adequadas?
- [ ] Há linting/formatting?
- [ ] CI/CD make sense?

## Formato de Saída

Salve em `{NUM}-consultor-moderno-sugestoes.md`:

```markdown
# Avaliação Tecnológica — [TEMA]

## Tecnologias Modernas Identificadas
- ...

## Oportunidades de Modernização

### 1. [Área]
**Atual**: [old approach]
**Moderno**: [new approach]
**Justificativa**: [why this is better]
**Impacto**: [high/medium/low]

### 2. ...

## Priorização
1. (high impact) ...
2. (medium impact) ...
3. (low impact - optional) ...

## Veredito
[MODERNO / REQUER AJUSTES / REVISÃO PROFUNDA]
```

## Regras

1. **Justificativa sempre**: "moderno" não é argumento, "better" é
2. **Priorize impacto**: não sugira mudança por opinião, sugira por necessidade
3. **Considere contexto**: nem sempre modern = better para o cenário
4. **Code examples**: quando possível, mostre old vs new com código