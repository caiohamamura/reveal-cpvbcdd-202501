---
name: openclaude-review
description: Abre OpenClaude no repositório reveal-cpvbcdd-202501 para revisar, analisar e aceitar alterações propostas pelo usuário. Use quando o professor Caio quiser revisar código, aceitar mudanças via terminal interativo, ou comparar modificações antes de commitá-las.
---

# OpenClaude Review — Revisar e Aplicar Mudanças no reveal-cpvbcdd-202501

## O que faz esta skill

Abre o **OpenClaude** no repositório `reveal-cpvbcdd-202501`, onde você pode:
1. Analisar modificações feitas ou pendentes
2. Revisar diffs e mudanças
3. Aceitar/rejeitar patches via terminal interativo (patch/interactive)
4. Fazer commits com mensagens descritivas
5. Verificar se há conflitos

## Uso

```bash
# Modo direto (recomendado)
bash /home/openclaw/.openclaw/skills/openclaude-review/scripts/review.sh --status
bash /home/openclaw/.openclaw/skills/openclaude-review/scripts/review.sh --diff
bash /home/openclaw/.openclaw/skills/openclaude-review/scripts/review.sh --prompt "sua instrução"

# Modo interativo (requer PTY)
bash /home/openclaw/.openclaw/skills/openclaude-review/scripts/review.sh --interactive
```

## Opções do Script

| Opção | Descrição |
|-------|-----------|
| `--status` | Mostra status do repositório git |
| `--diff` | Mostra diff das mudanças pendentes |
| `--prompt "texto"` | Executa instrução no OpenClaude e gera resumo |
| `--interactive` | Abre terminal interativo do OpenClaude (PTY) |

## Exemplos

```bash
# Ver o que mudou
bash /home/openclaw/.openclaw/skills/openclaude-review/scripts/review.sh --diff

# Analisar arquivos não rastreados
bash /home/openclaw/.openclaw/skills/openclaude-review/scripts/review.sh --prompt "Analyze the untracked files in ciencia-dados/aulas/"

# Pedir para commitar mudanças
bash /home/openclaw/.openclaw/skills/openclaude-review/scripts/review.sh --prompt "Add and commit the plano_aula files in bdd2/planos/"
```

## Resumo Final

Ao final de cada execução, o script mostra:

```
## Resumo das Mudanças

### Arquivos modificados:
- arquivo1.html
- arquivo2.md

### Alterações principais:
- Alteração 1
- Alteração 2

### Status:
✅ Commitado / ⏳ Pendente / ⚠️ Conflitos

### Observações:
...
```

## Comandos Git úteis (dentro do OpenClaude)

- `git diff` — ver modificações não commitadas
- `git diff --staged` — ver staged changes
- `git status` — estado atual do repo
- `git add -p` — adicionar pedaços específicos (interactive patching)
- `git checkout -p` — descartar pedaços específicos
- `git log --oneline -10` — últimos commits
- `git stash` — guardar alterações temporariamente

## Variáveis de Ambiente

O script configura automaticamente:
```bash
CLAUDE_CODE_USE_OPENAI=1
OPENAI_API_KEY=<key>
OPENAI_BASE_URL=https://api.z.ai/api/coding/paas/v4
OPENAI_MODEL=glm-5.1
```