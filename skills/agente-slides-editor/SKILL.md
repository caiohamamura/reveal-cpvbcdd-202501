---
name: agente-slides-editor
description: Orienta o Agente Principal sobre como solicitar ajustes de slides ao OpenClaude. Aprenda a criar briefing eficiente e integrar mudanças.
---

# Agente Slides Editor — Solicitando Ajustes ao OpenClaude

## Quando Usar

Você é o **Agente Principal** e precisa que o **OpenClaude** ajuste os slides da aula com base no plano de melhorias consolidado.

## Pré-Condição

- Briefing de slides preparado ({NUM}-briefing-slides.md)
- Slides originais disponíveis
- Plano consolidado明确了 mudanças necessárias

## Sua Tarefa

1. **Preparar** briefing completo para OpenClaude
2. **Chamar** OpenClaude via wrapper
3. **Acompanhar** execução
4. **Validar** resultado
5. **Integrar** aos materiais

## Opções de Execução

### Opção 1: Via Wrapper (Recomendado para comandos únicos)
```bash
source ~/openclaude.sh <repo_dir> "instruções"
```

### Opção 2: Via sessions_spawn (para processos mais longos)
```bash
sessions_spawn mode=run runtime=subagent task="..." timeout=300
```

## Como Preparar o Briefing

O briefing deve incluir:

1. **Contexto**: qual aula, qual tema
2. **Slides atuais**: localização do arquivo
3. **Mudanças necessárias**: lista completa com justificativa
4. **Restrições**: estilo visual, formatação,等技术约束

## Exemplo de Briefing Completo

```
# Briefing: Ajuste de Slides — RandomForest

## Contexto
- Aula: RandomForest com tidymodels
- Agente: ciencia-dados
- Arquivo: reveal-cpvbcdd-202501/ciencia-dados/aula-randomforest.html
- Versão: v2 (após feedback dos alunos)

## Slides a Ajustar

### Slide 12 (Feature Importance)
- **Antes**: Usava matplotlib para gráfico
- **Depois**: Usar vip() do R com ggplot2 styling
- **Justificativa**: Alunos confusos com matplotlib em aula de R

### Slide 15 (Exemplo de Código)
- **Antes**: Código com randomForest()
- **Depois**: Código com rand_forest() + set_engine("ranger")
- **Justificativa**: Consultor sugeriu tidymodels moderno

## Restrições
- Manter Dracula theme
- Manter estrutura do reveal.js
- Não alterar layout geral, só conteúdo

## Arquivos de Referência
- Plano consolidado: ciencia-dados/aulas/.../plano/plano-aula.md
- Roteiro: ciencia-dados/aulas/.../roteiros/roteiro-professor.md
```

## Fluxo de Execução

```
Preparar Briefing
        │
        ▼
Chamar OpenClaude (via wrapper ou sessions_spawn)
        │
        ▼
Aguardar execução
        │
        ▼
Validar Resultado
        │
    OK? ──→ SIM ──→ Integrar aos materiais
        │
        NÃO ──→ Ajustar briefing e repetir
```

## Checklist de Validação

Após OpenClaude entregar os slides ajustados:

### Verificar Completude
- [ ] Todas as mudanças solicitadas foram aplicadas?
- [ ] Nenhum slide foi removido sem necessidade?
- [ ] Novos slides seguem mesma formatação?

### Verificar Qualidade
- [ ] Código compila/renderiza corretamente?
- [ ] Links internos funcionando?
- [ ] Imagens/diagramas preservados?

### Verificar Estilo
- [ ] Dracula theme consistente?
- [ ] Fonts e cores padronizadas?
- [ ] Mermaid diagrams formatados?

## Se Ajustes Necessários

Se OpenClaude não entregou conforme esperado:

1. Identificar pontos específicos que precisam correção
2. Criar novo briefing com pontos específicos
3. Chamar OpenClaude novamente com correções
4. Iterar até ficar bom

## Após Conclusão

1. Copiar slides finais para `slides/aula-slides-final.html`
2. Atualizar referências nos roteiros
3. Documentar em `{NUM}-slides-ajustados.md`
4. Reportar para Aria (orchestrator) conclusão

## Formato Final de Documentação

Salve em `{NUM}-slides-ajustados.md`:

```markdown
# Slides Ajustados — [TEMA]

## Data do Ajuste
[YYYY-MM-DD]

## Mudanças Aplicadas

| Slide | Mudança | Status |
|-------|---------|--------|
| Slide 12 | Adicionado gráfico vip | ✅ |
| Slide 15 | Código atualizado para tidymodels | ✅ |
| ... | ... | ... |

## Arquivo Final
[localização dos slides finais]

## Validação
- [x] Slides renderizam corretamente
- [x] Código compila
- [x] Estilo consistente

## Observações
[alguma observação relevant]
```

## Regras

1. **Briefing detalhado** — mais contexto = melhor resultado
2. **Iterar se necessário** — não aceitar resultado ruim
3. **Validar sempre** — não assumir que está bom
4. **Manter backup** — slides originais não são sobrescritos até confirmar
5. **Documentar** — registrar o que foi feito para referência future

## Dicas de Eficiência

- Agrupar mudanças relacionadas no mesmo briefing
- Priorizar mudanças HIGH antes de MEDIUM/LOW
- Se muitas mudanças, considerar quebrar em múltiplos briefings
- Manter referência do briefing junto aos slides finais