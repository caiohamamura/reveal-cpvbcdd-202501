#!/bin/bash
# Aula Orchestrator - Script Principal
# Coordena o processo completo de planejamento de aula colaborativo

set -e

SKILL_DIR="/home/openclaw/.openclaw/skills/aula-orchestrator"
WORKSPACE_DIR="/home/openclaw/.openclaw/workspace"
REVEAL_REPO="$WORKSPACE_DIR/reveal-cpvbcdd-202501"

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[ORCHESTRATOR]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

# Função para mostrar uso
usage() {
    echo "Uso: $0 --agente <nome> --tema <tema> [--resumo <resumo>]"
    echo ""
    echo "Opções:"
    echo "  --agente <nome>    Workspace do agente que cria a aula (ex: ciencia-dados, iot)"
    echo "  --tema <tema>      Tema/título da aula"
    echo "  --resumo <texto>  Resumo opcional do conteúdo"
    echo "  --help            Mostrar esta ajuda"
    echo ""
    echo "Exemplo:"
    echo "  $0 --agente ciencia-dados --tema \"RandomForest\" --resumo \"Aula sobre ensemble learning\""
}

# Parse argumentos
AGENTE=""
TEMA=""
RESUMO=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --agente)
            AGENTE="$2"
            shift 2
            ;;
        --tema)
            TEMA="$2"
            shift 2
            ;;
        --resumo)
            RESUMO="$2"
            shift 2
            ;;
        --help|-h)
            usage
            exit 0
            ;;
        *)
            error "Opção desconhecida: $1"
            usage
            exit 1
            ;;
    esac
done

# Validar argumentos
if [[ -z "$AGENTE" ]] || [[ -z "$TEMA" ]]; then
    error "Parâmetros obrigatórios: --agente e --tema"
    usage
    exit 1
fi

# Verificar se workspace existe
AGENTE_DIR="$WORKSPACE_DIR/$AGENTE"
if [[ ! -d "$AGENTE_DIR" ]]; then
    error "Workspace não encontrado: $AGENTE_DIR"
    exit 1
fi

# Criar slug para o tema (sem espaços, lowercase)
SLUG=$(echo "$TEMA" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-')
DATA=$(date +%Y-%m-%d)

log "=============================================="
log "  AULA ORCHESTRATOR - Planejamento Colaborativo"
log "=============================================="
log "Agente: $AGENTE"
log "Tema: $TEMA"
log "Slug: $SLUG"
log "Resumo: ${RESUMO:-N/A}"
log "=============================================="

# FASE 1: Criação da estrutura de diretórios
log "${BLUE}FASE 1: Criando estrutura de diretórios${NC}"

AULA_DIR="$AGENTE_DIR/aulas/$DATA-$SLUG"

mkdir -p "$AULA_DIR"/{plano,roteiros,materiais,slides,feedback}

log "Diretório criado: $AULA_DIR"

# Salvar metadata
cat > "$AULA_DIR/.metadata.json" << EOF
{
  "agente": "$AGENTE",
  "tema": "$TEMA",
  "slug": "$SLUG",
  "resumo": "$RESUMO",
  "criado_em": "$(date -Iseconds)",
  "fase_atual": 1,
  "contador_interacoes": 0
}
EOF

log "Metadata salva em $AULA_DIR/.metadata.json"

# Criar template inicial
info "Estrutura criada:"
tree "$AULA_DIR" 2>/dev/null || ls -la "$AULA_DIR"

echo ""
echo "=============================================="
echo " PRÓXIMOS PASSOS:"
echo "=============================================="
echo ""
echo "1. AGENTE PRINCIPAL cria proposta inicial:"
echo "   - Salvar como: $AULA_DIR/01-{agente}-{tipo}.md"
echo "   - Copiar para: $AULA_DIR/plano/plano-aula.md"
echo "   - Criar roteiros em: $AULA_DIR/roteiros/"
echo ""
echo "2. Revisar com especialistas:"
echo "   - Professor Especialista: $AULA_DIR/02-professor-avaliador-revisao.md"
echo "   - Consultor Moderno: $AULA_DIR/03-consultor-moderno-sugestoes.md"
echo ""
echo "3. Iterar melhorias (novos arquivos com numeração incremental)"
echo ""
echo "4. Criar slides via OpenClaude"
echo ""
echo "5. Simular com alunos (feedback em arquivos numerados)"
echo ""
echo "6. Consolidar plano final em: $AULA_DIR/plano/plano-aula.md"
echo ""
echo "=============================================="