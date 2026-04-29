---
name: agente-revisor-feedback
description: Orienta o Agente Principal sobre como processar feedback dos revisores. Aprenda a avaliar, implementar ou rejeitar sugestões com justificativa.
---

# Agente Revisor Feedback — Processando Feedback dos Especialistas

## Quando Usar

Você é o **Agente Principal** e recebeu feedback do **Professor Especialista** e **Consultor Moderno** sobre seu plano inicial.

## Sua Tarefa

1. **Analisar** cada sugestão
2. **Decidir** se implementa ou não
3. **Justificar** decisões
4. **Documentar** em novo arquivo numerado

## Fluxo de Processamento

```
Feedbacks Recebidos
        │
        ▼
┌─────────────────────────────┐
│ Para cada sugestão:          │
│ 1. É viável no tempo?       │
│ 2. Melhora a didática?      │
│ 3. É consistente com Object? │
│ 4. Ajusta no escopo?         │
└─────────────────────────────┘
        │
        ▼
   Implementar? ──→ SIM ──→ Implementar
        │
        NÃO ──→ Documentar justificativa
        │
        ▼
   Salvar em arquivo numerado
```

## Checklist de Avaliação

### Para cada sugestão,responda:

| Pergunta | Se NÃO | Se SIM |
|----------|--------|--------|
| Cabe no tempo de aula? | Rejeitar com justificativa | Considerar |
| Melhora compreensão? | Rejeitar ou adaptar | Implementar |
| Agrega valor prático? | Descartar | Incluir |
| É consistente com objetivos? | Rejeitar | Implementar |
| Requer recursos adicionais? | Avaliarviabilidade | Adaptar ou recusar |

## Critérios de Rejeição (com justificativa)

- **Tempo**: "Esta atividade requer 30min extras que não temos no bloco"
- **Escopo**: "Este tema é mais adequado para aula futura"
- **Conflito**: "Esta sugestão contradiz o objetivo de..."
- **Duplicação**: "Este conceito já é coberto no Bloco 2"
- **Complexidade**: "Este exemplo é complexo demais para o nível atual"

## Formato de Saída

Salve em `{NUM}-agente-principal-plano-v2.md` (ou v3, v4...):

```markdown
# Plano de Aula — [TEMA] — Versão {N}

## Decisões sobre Sugestões

### Da Revisão Pedagógica

| Sugestão | Decisão | Justificativa |
|----------|---------|---------------|
| [sugestão 1] | ✅ Implementada | [razão] |
| [sugestão 2] | ❌ Rejeitada | [razão: tempo/confisco/etc] |
| [sugestão 3] | 🔄 Adaptada | [como foi adaptada] |

### Da Revisão Tecnológica

| Sugestão | Decisão | Justificativa |
|----------|---------|---------------|
| [sugestão 1] | ✅ Implementada | [razão] |
| [sugestão 2] | ❌ Rejeitada | [razão] |

## Resumo das Mudanças

1. **Adicionado**: [o que foi adicionado]
2. **Removido**: [o que foi removido]
3. **Modificado**: [o que foi modificado]

## Plano Atualizado (resumo)

[resumo do plano com mudanças incorporadas]
```

## Regras Importantes

1. **Documentar TODAS as decisões** — implementar ou não, sempre justifique
2. **Não descartar feedback** — se rejeitar, explicar por quê
3. **Manter coerência** — mudanças não podem contradizer objetivos
4. **Salvar novo arquivo** — nunca sobrescrever o original
5. **Número incremental** — v2, v3, etc.

## Exemplo de Justificativa

```
❌ Rejeitada: "Adicionar exemplo de XGBoost"
Justificativa: "O tema da aula é RandomForest. XGBoost seria conteúdo 
para aula futura de Boosting. O tempo do bloco atual (50min) não 
suportaintroduzir outro algoritmo."
```