---
name: agente-planejador-melhorias
description: Orienta o Agente Principal sobre como analisar feedbacks dos alunos e planejar melhorias no plano de aula. Aprenda a identificar padrões e criar plano de ação.
---

# Agente Planejador Melhorias — Analisando Feedback e Planejando Ajustes

## Quando Usar

Você é o **Agente Principal** e coletou todos os feedbacks dos alunos (Brilhante e Mediano) durante a simulação.

## Pré-Condição

- Arquivos de feedback dos alunos separados por bloco e perfil
- Resumo agregado de feedbacks disponível

## Sua Tarefa

1. **Analisar** todos os feedbacks
2. **Identificar padrões** de dificuldade/confusão
3. **Priorizar** melhorias por impacto
4. **Criar plano** de ajustes específicos

## Fluxo de Análise

```
Feedbacks dos Alunos (vários arquivos)
           │
           ▼
┌─────────────────────────────┐
│ 1. Agregar pontos comuns    │
│    - Quais conceitos confudem? │
│    - Quais exemplos falharam?  │
│    - Quais termos não claros?  │
└─────────────────────────────┘
           │
           ▼
┌─────────────────────────────┐
│ 2. Identificar padrões       │
│    - Padrão de confusão?      │
│    - Exemplo que ninguém entendeu? │
│    - Conceito que precisa mais tempo? │
└─────────────────────────────┘
           │
           ▼
┌─────────────────────────────┐
│ 3. Priorizar melhorias       │
│    HIGH: afeta compreensão   │
│    MEDIUM: atrapalha mas não bloqueia │
│    LOW: nice to have         │
└─────────────────────────────┘
           │
           ▼
┌─────────────────────────────┐
│ 4. Criar plano de melhorias  │
│    - O que mudar no plano?    │
│    - O que mudar nos slides?  │
│    - O que mudar no roteiro?  │
└─────────────────────────────┘
           │
           ▼
   Salvar em {NUM}-plano-melhorias.md
```

## Checklist de Análise

### Padrões Comuns de Confusão

| Padrão | Sinal nos Feedbacks | Ação Possible |
|--------|---------------------|---------------|
| Conceito abstrato demais | "não entendi X" | Adicionar exemplo concreto |
| Termo não definido | "o que é Y?" | Adicionar definição/glossário |
| Exemplo complexo | "como isso se aplica?" | Simplificar ou substituir |
| Pré-requisito faltante | "não entendi porque..." | Adicionar revisão/ponte |
| Tomada de decisão rápida | "saltou etapas" | Dividir em menores |
| Falta de prática | "como faço na prática?" | Adicionar exercício |

### Priorização

| Prioridade | Critério | Ação |
|------------|----------|------|
| HIGH | Bloqueia compreensão do conceito core | Mudar agora |
| MEDIUM | Atrapalha mas não bloqueia | Ajustar se tempo |
| LOW | Melhoria cosm ética | Se sobrar tempo |

## Formato de Saída

Salve em `{NUM}-plano-melhorias.md`:

```markdown
# Plano de Melhorias — [TEMA]

## Análise dos Feedbacks

### Feedbacks Analisados
- arquivo1 (Aluno Brilhante - Bloco 1)
- arquivo2 (Aluno Mediano - Bloco 1)
- arquivo3 (Aluno Brilhante - Bloco 2)
- ...

### Padrões Identificados

| Padrão | Frequência | Impacto | Exemplo |
|--------|-----------|---------|---------|
| Conceito X confunde | 3/4 feedbacks | HIGH | "ninguém entendeu feature importance" |
| Termo Y não definido | 2/4 feedbacks | MEDIUM | "o que é mtry?" |

## Melhorias Planejadas

### HIGH Priority (mudar agora)

1. **[Problema]**: [descrição]
   - **Ação**: [o que mudar]
   - **Onde**: [plano/slides/roteiro]
   - **Antes**: [como estava]
   - **Depois**: [como ficará]

### MEDIUM Priority (se tempo)

1. **[Problema]**: [descrição]
   - **Ação**: [o que mudar]
   - ...

### LOW Priority (opcional)

1. **[Problema]**: [descrição]
   - ...

## Impacto nas Entregas

| Entrega | Mudanças Necessárias |
|----------|---------------------|
| Plano de Aula | [lista ou "nenhuma"] |
| Roteiro Professor | [lista ou "nenhuma"] |
| Roteiro Aluno | [lista ou "nenhuma"] |
| Slides | [lista ou "nenhuma"] |

## Estimativa de Tempo para Implementação

- HIGH priority: ~X minutos para ajustar
- MEDIUM priority: ~Y minutos para ajustar
- Total estimado: ~Z minutos

## Próximo Passo

Após criar este plano, enviar para **Professor Especialista** analisar se as melhorias realmente atendem aos feedbacks.

Salvar em: `{NUM}-plano-melhorias.md`
```

## Regras

1. **Basear em evidências** — não imaginar problemas, usar feedback real
2. **Ser específico** — "mudar conceito X" não serve, "adicionar exemplo de Y" sim
3. **Considerar tempo** — melhoriasfeasible dentro do tempo de aula
4. **Documentar rationale** — por que cada melhoria foi priorizada assim

##Após Criar o Plano

1. Salvar em arquivo numerado
2. Enviar para Professor Especialista revisar (via sessions_send)
3. Aguardar avaliação antes de implementar