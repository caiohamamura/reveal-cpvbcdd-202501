---
name: aula-orchestrator
description: Orquestra o processo completo de planejamento de aula com múltiplos agentes (alunos, consultor, professor especialista). Use para planejar aulas colaborativamente em passos iterativos com revisão e melhoria contínua.
---

# Aula Orchestrator — Planejamento Colaborativo de Aulas

## O que faz esta skill

Coordena um processo de **5 fases iterativas** para criar uma aula de alta qualidade, envolvendo:
- **Agente Principal** (criador da aula)
- **Professor Especialista** (avaliação pedagógica)
- **Consultor Moderno** (tecnologias e práticas)
- **Aluno Brilhante** (perspectiva avançada)
- **Aluno Mediano** (perspectiva iniciante)

## Informações Necessárias

Para iniciar, você precisa de:
1. **Agente criador da aula** — pasta no workspace (ex: `ciencia-dados`, `iot`)
2. **Tema da aula** — título e resumo do conteúdo
3. **Materiais existentes** — arquivos, códigos, datasets (opcional)

## Fluxo Principal (9 Passos Otimizados)

### FASE 1: Criação Inicial (Passos 1-2)

**1. Agente principal cria proposta inicial**
- Plano de aula detalhado
- Roteiro de aula prática (professor + aluno)
- Materiais suplementares

**2. Revisão única**
- Enviar para **Professor Especialista** E **Consultor Moderno** juntos
- Eles retornam em um único documento consolidado
- Agente implementa melhorias, justifica o que não

### FASE 2: Slides (Passos 3-4)

**3. Abrir OpenClaude para criar slides**
- Usar `reveal-slides` skill
- Seguir plano detalhado e roteiro prático
- Slides devem ser prontos para apresentação

**4. Revisão rápida dos slides**
- Verificar se estão legíveis/funcionais
- Ajuste fino se necessário

### FASE 3: Simulação (Passos 5-7)

**5. Simular aula expositiva**
- Dividir por seções/conforme plano
- Alunos têm acesso aos slides

**6. Coletar feedback**
- Aluno Brilhante: edge cases, conexões
- Aluno Mediano: dúvidas básicas, confusões

**7. Plano de melhorias**
- Agente cria plano de melhorias com base nos feedbacks

### FASE 4: Consolidação (Passos 8-9)

**8. Revisão final pelo Professor Especialista**
- Analisa se melhorias atendem feedbacks
- Propoem ajustes se necessário

**9. Slides finais + Entrega**
- Implementar melhorias via OpenClaude
- Consolidar todos os materiais
- Reportar para Aria (orchestrator)

## Agentes Disponíveis

| Agente | Papel | Workspace | Skill Auxiliar |
|--------|-------|----------|----------------|
| `main` (Aria) | **Orquestrador (EU)** | `/home/openclaw/.openclaw/workspace` | `aula-orchestrator` (SÓ EU TENHO) |
| `ciencia-dados` | Agente Principal — Data Science | `/home/openclaw/.openclaw/workspace/ciencia-dados` | Skills de agente |
| `bdd2` | Agente Principal — Banco de Dados 2 | `/home/openclaw/.openclaw/workspace/bdd2` | Skills de agente |
| `iot` | Agente Principal — IoT | `/home/openclaw/.openclaw/workspace/iot` | Skills de agente |
| `professor-avaliador` | Revisão pedagógica | `/home/openclaw/.openclaw/workspace/professor-avaliador` | `revisor-pedagogico` |
| `consultor-moderno` | Revisão tecnológica | `/home/openclaw/.openclaw/workspace/consultor-moderno` | `revisor-tecnologico` |
| `aluno-brilhante` | Simulação aluno avançado | `/home/openclaw/.openclaw/workspace/aluno-brilhante` | `simulador-aluno` |
| `aluno-mediano` | Simulação aluno iniciante | `/home/openclaw/.openclaw/workspace/aluno-mediano` | `simulador-aluno` |

**IMPORTANTE**: Apenas **EU (Aria/main)** tenho a skill `aula-orchestrator`. Os outros agentes têm skills auxiliares específicas e não devem ver a skill principal para evitar confusão ou loops infinitos.

## Como Iniciar

Basta dizer:

```
Planeje uma aula de [TEMA] no agente [AGENTE]
```

Exemplo:
```
Planeje uma aula de RandomForest com tidymodels no agente ciencia-dados
```

## Output Final

Ao terminar, retorne:

```
## ✅ Aula Planejada: [TEMA]

### Localização dos Arquivos
- Plano de Aula: `caminho/plano-aula.md`
- Roteiro Professor: `caminho/roteiro-professor.md`
- Roteiro Aluno: `caminho/roteiro-aluno.md`
- Slides: `caminho/slides.html`
- Materiais: `caminho/materiais/`

### Resumo do Processo
- Fases completadas: X/5
- Iterações de melhoria: Y
- Feedbacks de alunos incorporados: Z
```

## Notas Importantes

1. **Salvar histórico de interações** — cada interação deve ser salva com prefixo incremental identificando o passo e qual agente fez:
   - Formato: `{NUMERO}-{AGENTE}-{TIPO}.md`
   - Exemplo: `01-agente-principal-plano-inicial.md`, `02-professor-avaliador-revisao.md`, `03-consultor-moderno-sugestoes.md`

2. **Ajustes em novos arquivos** — nunca modificar arquivos existentes, sempre criar novos com versão atualizada:
   - Formato: `{NUMERO}-{AGENTE}-{TIPO}-v{N}.md`
   - Exemplo: `05-agente-principal-plano-v2.md`, `06-professor-avaliador-revisao-v2.md`

3. **Limite de iterações**: Máximo 2 rodadas de revisão para não prolongar infinitamente
4. **Justificativas**: Sempre explicar por que algo não foi implementado
5. **Transcript**: Manter registro das interações para referência
6. **Slides iterativos**: Criar versão inicial, depois melhorar com base no feedback

## Scripts Disponíveis

- `/home/openclaw/.openclaw/skills/aula-orchestrator/scripts/orchestrate.sh` — script auxiliar para criar estrutura de diretórios

## Papéis dos Agentes no Orchestrator

### Agente Principal (ex: ciencia-dados, iot)
- Cria plano de aula, roteiros, materiais
- Coordena rodadas de revisão
- Implementa melhorias
- Abre OpenClaude para criar slides
- Simula aula com alunos

### Professor Especialista (professor-avaliador)
- Avalia clareza pedagógica
- Verifica sequência didática
- Analisa adequação ao público
- Proposta melhorias estruturais

### Consultor Moderno (consultor-moderno)
- Verifica uso de tecnologias modernas
- Propõe libs/packages atualizados
- Analisa código e práticas
- Sugere modernizações

### Alunos (aluno-brilhante, aluno-mediano)
- Simulam presença na aula
- Fazem perguntas do perspective deles
- Identificam pontos de confusão
- Dão feedback sobre clareza