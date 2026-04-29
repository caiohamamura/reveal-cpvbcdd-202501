---
name: agente-consolidador
description: Orienta o Agente Principal sobre como receber a revisão do Professor Especialista sobre o plano de melhorias e consolidar a versão final do plano e roteiros.
---

# Agente Consolidador — Consolidando Versão Final

## Quando Usar

Você é o **Agente Principal** e recebeu a revisão do **Professor Especialista** sobre seu plano de melhorias.

## Pré-Condição

- Plano de melhorias criado ({NUM}-plano-melhorias.md)
- Revisão do Professor Especialista disponível ({NUM}-professor-avaliador-analise-melhorias.md)

## Sua Tarefa

1. **Analisar** a revisão do Professor Especialista
2. **Decidir** se aceita sugestões ou não
3. **Implementar** ajustes no plano e roteiros
4. **Consolidar** versão final
5. **Preparar** briefing para OpenClaude sobre ajustes nos slides

## Fluxo de Consolidação

```
Revisão do Professor
        │
        ▼
┌─────────────────────────────┐
│ Para cada sugestão do Prof: │
│ 1. Aceitar ou recusar?      │
│ 2. Justificar recusar       │
│ 3. Adaptar se necessário    │
└─────────────────────────────┘
        │
        ▼
Implementar no Plano e Roteiros
        │
        ▼
Consolidar Versão Final
        │
        ▼
Criar briefing para OpenClaude
        │
        ▼
Salvar arquivos consolidados
```

## Checklist de Análise

### Para cada sugestão do Professor:

| Pergunta | Se NÃO | Se SIM |
|----------|--------|--------|
| Faz sentido pedagogicamente? | Recusar | Aceitar |
| É implementável no tempo? | Adaptar ou recusar | Aceitar |
| Resolve o problema identificado? | Propor alternativa | Aceitar |
| Conflita com algo já planejado? | Ajustar para evitar conflito | Recusar |

## Formato de Saída

### 1. Decisões sobre Revisão (`{NUM}-decisoes-revisao-final.md`)

```markdown
# Decisões sobre Revisão do Professor — [TEMA]

## Avaliação das Sugestões do Professor

| Sugestão | Decisão | Justificativa |
|----------|---------|---------------|
| [sugestão 1] | ✅ Aceita | [razão] |
| [sugestão 2] | ❌ Recusada | [razão: conflito/tempo/etc] |
| [sugestão 3] | 🔄 Adaptada | [como foi adaptada] |

## Resumo das Implementações

### Ajustes no Plano de Aula
1. [ajuste 1]
2. [ajuste 2]

### Ajustes no Roteiro Professor
1. [ajuste 1]
2. [ajuste 2]

### Ajustes no Roteiro Aluno
1. [ajuste 1]
2. [ajuste 2]
```

### 2. Plano Consolidado (`plano/plano-aula.md` — ATUALIZADO)

Atualizar com todas as melhorias implementadas.

### 3. Roteiros Consolidados

- `roteiros/roteiro-professor.md` — ATUALIZADO
- `roteiros/roteiro-aluno.md` — ATUALIZADO

### 4. Briefing para OpenClaude (`{NUM}-briefing-slides.md`)

```markdown
# Briefing para Ajuste de Slides — [TEMA]

## Slides a Ajustar
[localização dos slides]

## Mudanças Necessárias

### HIGH Priority (obrigatório)
1. **[Slide X]**: [o que mudar]
   - **Antes**: [descrição atual]
   - **Depois**: [nova descrição]

### MEDIUM Priority (recomendado)
1. **[Slide Y]**: [o que mudar]
   - ...

### LOW Priority (opcional)
1. **[Slide Z]**: [o que mudar]
   - ...

## Justificativa das Mudanças
[explicação breve de por que cada mudança foi necessária]

## Arquivo de Referência
[link para plano consolidado ou descrição do contexto]

## Observações para OpenClaude
- Mantenha o estilo visual consistente
- Use mesma formatação dos slides anteriores
- Adicione notas defal presenter se necessário
```

## Checklist de Consolidação

- [ ] Plano de aula atualizado com todas as melhorias
- [ ] Roteiro professor atualizado
- [ ] Roteiro aluno atualizado
- [ ] Briefing para OpenClaude criado
- [ ] Arquivos numerados salvos (não sobrescrever)

## Regras

1. **Professor tem autoridade final** — exceto se justificativa forte para discordar
2. **Documentar decisões** — aceitar ou recusar, sempre justificar
3. **Não misturar versões** — consolidado = definitivo para esta iteração
4. **Manter rastreabilidade** — arquivo numerado para cada passo

## Após Consolidar

1. Salvar arquivos consolidados
2. Criar briefing para OpenClaude
3. Chamar OpenClaude para ajustar slides
4. Reportar para Aria (orchestrator) que está pronto