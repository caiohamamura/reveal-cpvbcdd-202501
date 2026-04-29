---
name: agente-simulador-aula
description: Orienta o Agente Principal sobre como ministrar a aula simulada para os alunos (Brilhante e Mediano). Aprenda a apresentar conteúdo e coletar feedback.
---

# Agente Simulador Aula — Ministrando para os Alunos

## Quando Usar

Você é o **Agente Principal** e chegou a hora de simular a aula com os alunos para testar se o material funciona.

## Pré-Condição

- Slides criados e disponíveis
- Plano de aula dividido em blocos/seções
- Alunos disponíveis (via sessions_send)

## Sua Tarefa

1. **Dividir** a aula em blocos (conforme plano)
2. **Apresentar** cada bloco como se fosse aula real
3. ** Coletar** feedback dos alunos após cada bloco
4. **Documentar** feedbacks

## Fluxo de Simulação

```
PARA CADA bloco do plano:
    │
    ├─→ Mostrar slides do bloco ao Aluno Brilhante
    │
    ├─→ "Ministrar" conteúdo (explicar como professor)
    │
    ├─→ Coletar perguntas do Aluno Brilhante
    │
    ├─→ Documentar feedback do Aluno Brilhante
    │
    ├─→ Mostrar slides do bloco ao Aluno Mediano
    │
    ├─→ "Ministrar" conteúdo novamente
    │
    ├─→ Coletar perguntas do Aluno Mediano
    │
    └─→ Documentar feedback do Aluno Mediano
```

## Como "Ministrar" Cada Bloco

### Passo 1: Apresentar Slides
```
"Aluno, aqui estão os slides da Seção [N]. 
Por favor, visualize enquanto explico o conteúdo."
```

### Passo 2: Explicar (como professor)
- Siga a sequência do plano de aula
- Use linguagem adequada ao perfil dos alunos
- Para Aluno Brilhante: mais teoria, conexões, "e se..."
- Para Aluno Mediano: mais exemplos,analogias,確認理解

### Passo 3: Coletar Feedback
```
"Alguma dúvida? Pergunta? Algo que não ficou claro?"
```

### Passo 4: Registrar
Documente em `{NUM}-{tipo-aluno}-feedback-bloco{N}.md`

## Formato de Feedback dos Alunos

Para **Aluno Brilhante** (`{NUM}-aluno-brilhante-feedback-bloco{N}.md`):

```markdown
# Feedback — Aluno Brilhante — Bloco {N}

## Slides Revisados
[slinks ou descrição do conteúdo do bloco]

## Perguntas Feitas
1. [pergunta 1 - edge case / conexão / teoria]
2. [pergunta 2 - implicação / alternativa]

## Pontos de Confusão
- [ponto que gerou dúvida aprofundada]
- [conceito que precisa mais contexto]

## Sugestões do Aluno
1. [sugestão construtiva]
2. [sugestão construtiva]

## Avaliação do Entendimento
[Excelente entendeu / Bom com dúvidas / needs improvement]

## Observations for Improvement
- [observação sobre slides/conteúdo]
```

Para **Aluno Mediano** (`{NUM}-aluno-mediano-feedback-bloco{N}.md`):

```markdown
# Feedback — Aluno Mediano — Bloco {N}

## Slides Revisados
[slides ou descrição do conteúdo do bloco]

## Perguntas Feitas
1. [pergunta básica - significado de termo]
2. [pergunta básica - como fazer na prática]
3. [confirmação - isso está certo?]

## Pontos de Confusão
- [termo não definido claramente]
- [conceito muito abstrato sem exemplo]
- [passo dado como óbvio mas não é]

## Dúvidas Específicas
1. [o que não entendi]
2. [o que preciso ver novamente]

## Avaliação do Entendimento
[Excelente / Bom / Confuso / Lost]

## Recomendações
- [como melhorar clareza para iniciantes]
- [exemplo concreto que ajudaria]
```

## Dicas de Ministry

### Para Aluno Brilhante:
- Não pule teorias — ele quer entender fundamentos
- Acompanhe suas perguntas até o fim
- Mostre conexões com outros temas
- Desafie com "e se..."

### Para Aluno Mediano:
- Pare em exemplos concretos
- Use analogias do dia a dia
- Confirme se entendeu antes de avançar
- Não assuma que "óbvio" é óbvio

## Regras

1. **Não antecipe feedback** — deixe os alunos perguntarem naturalmente
2. **Seja consistente** — mesma apresentação para ambos (só estilo varia)
3. **Documente tudo** — cada feedback em arquivo separado
4. **Após bloco** — aguarde feedback completo antes de avançar
5. **NúmeroSequencial** — bloco1, bloco2, etc.

## Após Coletar Todos os Feedbacks

Salve resumo agregado em `{NUM}-resumo-feedbacks-alunos.md`