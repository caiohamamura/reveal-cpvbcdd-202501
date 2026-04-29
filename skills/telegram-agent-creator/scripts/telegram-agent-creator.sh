#!/bin/bash
# Script para criar um novo agente com bootstrap e vinculá-lo a um grupo Telegram

set -e

# Parse argumentos
NAME=""
TELEGRAM_GROUP_ID=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --name)
      NAME="$2"
      shift 2
      ;;
    --telegram-group-id)
      TELEGRAM_GROUP_ID="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

if [[ -z "$NAME" ]] || [[ -z "$TELEGRAM_GROUP_ID" ]]; then
  echo "Usage: $0 --name <nome-agente> --telegram-group-id <id-do-grupo>"
  exit 1
fi

# Configurações
OPENCLAW_DIR="/home/openclaw/.openclaw"
WORKSPACE_DIR="$OPENCLAW_DIR/workspace"
AGENT_DIR="$OPENCLAW_DIR/agents/$NAME"
AGENT_WORKSPACE="$WORKSPACE_DIR/$NAME"

echo "📦 Criando agente: $NAME"
echo "📱 Grupo Telegram: $TELEGRAM_GROUP_ID"

# 1. Criar diretório do agente
mkdir -p "$AGENT_DIR/agent"
mkdir -p "$AGENT_DIR/sessions"
echo "✅ Diretório do agente criado"

# 2. Criar workspace com arquivos bootstrap
mkdir -p "$AGENT_WORKSPACE"
mkdir -p "$AGENT_WORKSPACE/memory"

# BOOTSTRAP.md - arquivo de inicialização
cat > "$AGENT_WORKSPACE/BOOTSTRAP.md" << 'EOF'
[MISSING] Este é seu certificado de nascimento. Siga as instruções em SOUL.md e USER.md para descobrir quem você é.
EOF

# AGENTS.md
cat > "$AGENT_WORKSPACE/AGENTS.md" << 'EOF'
# AGENTS.md - Your Workspace

Esta pasta é sua casa. Trate-a assim.

## Inicialização da Sessão

Antes de fazer qualquer coisa:

1. Leia `SOUL.md` — isto é quem você é
2. Leia `USER.md` — isto é quem você está ajudando
3. Leia `memory/YYYY-MM-DD.md` (hoje + ontem) para contexto recente
4. **Se na SESSÃO PRINCIPAL** (chat direto com seu humano): Leia também `MEMORY.md`

Não peça permissão. Apenas faça.

## Memória

Você acorda fresco a cada sessão. Estes arquivos são sua continuidade:

- **Notas diárias:** `memory/YYYY-MM-DD.md` — logs crus do que aconteceu
- **Longo prazo:** `MEMORY.md` — sua memória curada

## Red Lines

- Não exfiltre dados privados. Nunca.
- Quando em dúvida, pergunte.
EOF

# IDENTITY.md
cat > "$AGENT_WORKSPACE/IDENTITY.md" << 'EOF'
# IDENTITY.md - Quem Sou Eu

- **Name:**还未设定
- **Creature:**尚未定义
- **Vibe:**尚未定义
- **Emoji:**🤔

---

*Este arquivo será preenchido durante o bootstrap.*
EOF

# TOOLS.md
cat > "$AGENT_WORKSPACE/TOOLS.md" << 'EOF'
# TOOLS.md - Notas Locais

Skills definem _como_ as ferramentas funcionam. Este arquivo é para _suas_ especificidades.

## O Que Vai Aqui

Coisas como:
- Nomes de câmeras e localizações
- Hosts SSH e aliases
- Vozes preferidas para TTS
- Nomes de dispositivos
- Qualquer coisa específica do ambiente

---

*Este arquivo será expandido durante o bootstrap.*
EOF

# HEARTBEAT.md
cat > "$AGENT_WORKSPACE/HEARTBEAT.md" << 'EOF'
# HEARTBEAT.md

# Coisas para verificar periodicamente:
# - Emails importantes
# - Eventos no calendário
# - Estado de tarefas em andamento

# Estado atual: nada pendente
EOF

echo "✅ Workspace criado em $AGENT_WORKSPACE"

# 3. Configurar modelo do agente
cat > "$AGENT_DIR/agent/models.json" << 'EOF'
{
  "mode": "merge",
  "providers": {
    "ollama": {
      "baseUrl": "http://192.168.0.216:11434",
      "api": "ollama",
      "apiKey": "OLLAMA_API_KEY",
      "models": [
        {
          "id": "qwen3.5:4b",
          "name": "qwen3.5:4b",
          "reasoning": false,
          "input": ["text", "image"],
          "cost": {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0},
          "contextWindow": 262144,
          "maxTokens": 8192
        }
      ]
    }
  }
}
EOF

cat > "$AGENT_DIR/agent/auth-profiles.json" << 'EOF'
{}
EOF

echo "✅ Modelo configurado"

# 4. Registrar agente no openclaw.json
# 4. Symlink para skills compartilhadas do workspace pai
SHARED_SKILLS_DIR="$WORKSPACE_DIR/skills"
AGENT_SKILLS_DIR="$AGENT_WORKSPACE/skills"

if [[ -d "$SHARED_SKILLS_DIR" ]]; then
  mkdir -p "$AGENT_SKILLS_DIR"
  for skill_dir in "$SHARED_SKILLS_DIR"/*/; do
    skill_name=$(basename "$skill_dir")
    if [[ ! -e "$AGENT_SKILLS_DIR/$skill_name" ]]; then
      ln -s "$skill_dir" "$AGENT_SKILLS_DIR/$skill_name"
      echo "✅ Skill compartilhada linkada: $skill_name"
    fi
  done
fi

echo "✅ Agente '$NAME' criado com sucesso!"
echo ""
echo "📝 Próximos passos:"
echo "1. O agente está configurado em: $AGENT_WORKSPACE"
echo "2. Adicione o binding em openclaw.json para: $TELEGRAM_GROUP_ID"
echo "3. Edite SOUL.md, USER.md, IDENTITY.md e MEMORY.md no workspace"
echo "4. Reinicie o gateway para aplicar mudanças"
