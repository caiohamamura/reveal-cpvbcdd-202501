---
name: telegram-agent-creator
description: Cria um novo agente com bootstrap personalizado que pergunta ao usuário para montar sua memória, SOUL e IDENTITY antes de se vincular a um grupo Telegram. Use quando você precisa provisionar um novo agente específico para um canal ou grupo Telegram, com configuração personalizada via perguntas ao usuário.
---

# Telegram Agent Creator

Esta skill cria agentes independentes com bootstrapping personalizado, ideal para provisionar múltiplos agentes para grupos ou canais diferentes.

## Como Funciona

1. **Recebe:**
   - `name`: Nome/alias do novo agente
   - `telegramGroupId`: ID do grupo Telegram (ex: `-5189152367`)

2. **O script cria:**
   - Estrutura de diretórios do agente (`agents/<name>/`)
   - Workspace com templates (`workspace/<name>/`)
   - Configuração do modelo
   - Binding no `openclaw.json`

3. **Após executar o script:**
   - Vincule o binding manualmente no `openclaw.json`
   - O novo agente tendrá seu bootstrap interativo na primeira vez que for executado

## Uso

```bash
./scripts/telegram-agent-creator.sh --name <nome-agente> --telegram-group-id <id-do-grupo>
```

## Exemplo

```bash
./scripts/telegram-agent-creator.sh --name "ciencia-dados" --telegram-group-id "-5195384852"
```

## Estrutura Criada

```
agents/<name>/
├── agent/
│   ├── models.json
│   └── auth-profiles.json
└── sessions/

workspace/<name>/
├── BOOTSTRAP.md
├── AGENTS.md
├── IDENTITY.md (template vazio)
├── SOUL.md (template vazio)
├── USER.md (template vazio)
├── MEMORY.md (template vazio)
├── HEARTBEAT.md
├── TOOLS.md
├── memory/
└── skills/  ← symlinks para skills em workspace/skills/
```

## Skills Compartilhadas

O script cria automaticamente symlinks de todas as skills em `workspace/skills/` para o diretório `skills/` do novo agente. Isso garante que skills genéricas (como `reveal-slides`) fiquem disponíveis para todos os agentes automaticamente.

## Bindings no openclaw.json

O script NÃO modifica o `openclaw.json` automaticamente. Após executar o script, adicione manualmente:

```json
{
  "id": "ciencia-dados",
  "name": "ciencia-dados",
  "workspace": "/home/openclaw/.openclaw/workspace/ciencia-dados",
  "agentDir": "/home/openclaw/.openclaw/agents/ciencia-dados/agent"
}
```

E no `bindings`:

```json
{
  "type": "route",
  "agentId": "ciencia-dados",
  "match": {
    "channel": "telegram",
    "peer": {
      "kind": "group",
      "id": "-5195384852"
    }
  }
}
```

## Perguntas de Bootstrap

Após criar o agente, use `references/bootstrap-questions.md` para guiar o novo agente na configuração de seus arquivos de identidade.
