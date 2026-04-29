# Workflow — Orchestrator de Aulas (9 Passos)

## Visão Geral

```
┌─────────────────────────────────────────────────────────────────┐
│                      FASE 1: CRIAÇÃO                            │
│  1. Criar plano inicial                                         │
│  2. Revisão única (Professor + Consultor juntos)                │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FASE 2: SLIDES                             │
│  3. OpenClaude cria slides                                       │
│  4. Revisão rápida                                              │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FASE 3: SIMULAÇÃO                          │
│  5. Simular aula com alunos                                     │
│  6. Coletar feedback (Brilhante + Mediano)                      │
│  7. Plano de melhorias                                          │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FASE 4: CONSOLIDAÇÃO                        │
│  8. Revisão final pelo Professor                                │
│  9. Slides finais + Entrega                                     │
└─────────────────────────────────────────────────────────────────┘
```

## Estrutura de Diretórios

```
aulas/[data]-[tema-slug]/
├── 01-agente-principal-plano-inicial.md
├── 02-revisao-consolidada.md              ← Professor + Consultor juntos
├── 03-plano-v2-implementado.md            ← Após implementar mudanças
├── plano/
│   └── plano-aula.md                      ← Sempre a versão mais atual
├── roteiros/
│   ├── roteiro-professor.md
│   └── roteiro-aluno.md
├── slides/
│   ├── aula-slides.html                   ← Versão inicial
│   └── aula-slides-final.html             ← Versão após simulação
└── feedback/
    ├── 04-aluno-brilhante-bloco1.md
    ├── 05-aluno-mediano-bloco1.md
    ├── 06-aluno-brilhante-bloco2.md
    ├── 07-aluno-mediano-bloco2.md
    └── 08-resumo-feedbacks.md             ← Consolidado
```

## Regra de Numeração

- **Primeiros 3 arquivos**: criação e revisão inicial
- **Feedbacks dos alunos**: bloco sequencial (04, 05, 06...)
- **Resumo e plano de melhorias**: últimos da sequência
- **Plano e roteiros**: sempre em `/plano/` e `/roteiros/`

## Passo a Passo Detalhado

### PASSO 1: Criar Plano Inicial

**Responsável**: Agente principal (ciencia-dados / bdd2 / iot)

1. Criar diretório `aulas/[data]-[tema-slug]/`
2. Criar `01-agente-principal-plano-inicial.md` com:
   - Objetivos de aprendizagem (algoritmo de bloom)
   - Conteúdo programático
   - Sequência didática
   - Exercícios e avaliações
   - Materiais necessários

3. Criar roteiros em `/roteiros/`:
   - `roteiro-professor.md` — passos para ministrar
   - `roteiro-aluno.md` — o que aluno precisa.prepare

### PASSO 2: Revisão Única

**Responsável**: Professor Especialista + Consultor Moderno

1. Agente envia plano para ambos revisores
2. Revisor pedagógico avalia clareza e estrutura
3. Revisor tecnológico avalia tools e práticas
4. Ambos retornam **documento único consolidado**
5. Agente cria `02-revisao-consolidada.md`
6. Agente implementa mudanças e justifica o que não
7. Salva em `03-plano-v2-implementado.md`

### PASSO 3: Criar Slides (OpenClaude)

**Responsável**: OpenClaude via wrapper/sessions_spawn

1. Agente cria briefing detalhado
2. Chama OpenClaude com `reveal-slides` skill
3. Slides gerados em `slides/aula-slides.html`
4. Agente verifica funcionamento

### PASSO 4: Revisão Rápida dos Slides

**Responsável**: Agente principal

1. Abrir slides no browser
2. Verificar:
   - Conteúdo está legível
   - Código compila/renderiza
   - Links funcionais
   - Flow faz sentido
3. Ajuste fino se necessário

### PASSO 5: Simular Aula

**Responsáveis**: Agente + Aluno Brilhante + Aluno Mediano

1. Dividir conteúdo em blocos (conforme roteiro)
2. Para cada bloco:
   - Apresentar slides ao Aluno Brilhante
   - "Ministrar" conteúdo (explicar como professor)
   - Coletar perguntas e feedback
   - Repetir com Aluno Mediano

### PASSO 6: Coletar Feedback

**Responsável**: Agente documenta

1. Salvar feedback do Aluno Brilhante: `04-aluno-brilhante-bloco1.md`
2. Salvar feedback do Aluno Mediano: `05-aluno-mediano-bloco1.md`
3. Continuar para cada bloco
4. Consolidar em `08-resumo-feedbacks.md`

### PASSO 7: Plano de Melhorias

**Responsável**: Agente principal

1. Analisar todos os feedbacks
2. Identificar padrões (o que confunde, o que falta)
3. Priorizar: HIGH / MEDIUM / LOW
4. Criar `09-plano-melhorias.md`

### PASSO 8: Revisão Final

**Responsável**: Professor Especialista

1. Enviar plano de melhorias para Professor
2. Professor verifica se mudanças resolvem feedbacks
3. Professor pode propor ajustes
4. Agente implementa ajustes finais

### PASSO 9: Slides Finais + Entrega

**Responsável**: Agente + OpenClaude

1. Criar briefing para OpenClaude com mudanças
2. OpenClaude ajusta slides
3. Salvar em `slides/aula-slides-final.html`
4. Consolidar materiais finais
5. Reportar para Aria (orchestrator): "Aula [tema] pronta para entrega"

## Critérios de Qualidade

### Plano Inicial ✅
- [ ] Objetivos claros e mensuráveis
- [ ] Sequência didática faz sentido
- [ ] Exemplos adequados ao nível
- [ ] Tempo viável para conteúdo

### Slides ✅
- [ ] Legíveis em qualquer tamanho
- [ ] Código funcional
- [ ] Fluxo narrativo coerente
- [ ] Visual consistente (Dracula theme)

### Simulação ✅
- [ ] Aluno Brilhante consegue follow
- [ ] Aluno Mediano não se perde
- [ ] Feedbacks documentados

### Entrega ✅
- [ ] Todos materiais organizados
- [ ] Slides finais funcionais
- [ ] Readme/delta documentando mudanças

## Exemplo de Execução

```bash
# 1. Agente cria estrutura
cd ciencia-dados
mkdir aulas/2026-04-27-randomforest/

# 2. Cria plano inicial
# → 01-agente-principal-plano-inicial.md

# 3. Envia para revisão
# → 02-revisao-consolidada.md

# 4. Implementa
# → 03-plano-v2-implementado.md

# 5. OpenClaude cria slides
# → slides/aula-slides.html

# 6. Simula com alunos
# → 04-aluno-brilhante-bloco1.md...08-resumo-feedbacks.md

# 7. Plano de melhorias
# → 09-plano-melhorias.md

# 8. Revisão final + ajustes

# 9. Slides finais
# → slides/aula-slides-final.html
```