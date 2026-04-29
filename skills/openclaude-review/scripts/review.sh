#!/bin/bash
# OpenClaude Review Script
# Abre OpenClaude no reveal-cpvbcdd-202501 para revisar e aplicar mudanças

set -e

REPO_DIR="/home/openclaw/.openclaw/workspace/reveal-cpvbcdd-202501"
SKILL_DIR="/home/openclaw/.openclaw/skills/openclaude-review"

# Função para mostrar uso
usage() {
    echo "Uso: $0 [opção] [argumento]"
    echo ""
    echo "Opções:"
    echo "  --prompt \"instrução\"  Executa instrução no OpenClaude e faz resumo"
    echo "  --diff              Mostra diff das mudanças pendentes"
    echo "  --status            Mostra status do repositório"
    echo "  --interactive       Abre terminal interativo do OpenClaude"
    echo "  --help              Mostra esta ajuda"
    echo ""
    echo "Exemplos:"
    echo "  $0 --prompt \"revisar as mudanças\""
    echo "  $0 --diff"
    echo "  $0 --interactive"
}

# Verifica se é para Interactive Mode (sem argumento ou --interactive)
if [[ "$1" == "--interactive" ]] || [[ -z "$1" ]]; then
    echo "🔍 Abrindo OpenClaude no repositório: $REPO_DIR"
    echo "📂 Diretório: $(pwd)"
    echo ""
    
    # Exportar variáveis OpenClaude
    export CLAUDE_CODE_USE_OPENAI=1
    export OPENAI_API_KEY="021d2bbeb8224a42bf01d83100616c3c.EVM4Z6mSMNbQLYFJ"
    export OPENAI_BASE_URL="https://api.z.ai/api/coding/paas/v4"
    export OPENAI_MODEL="glm-5.1"
    
    cd "$REPO_DIR"
    
    # Abrir terminal interativo PTY
    exec openclaude
    exit 0
fi

# Parse argumentos
case "$1" in
    --diff)
        cd "$REPO_DIR"
        echo "📋 Diff das mudanças pendentes:"
        git diff --stat
        echo ""
        git diff
        ;;
    --status)
        cd "$REPO_DIR"
        echo "📊 Status do repositório:"
        git status
        ;;
    --prompt)
        PROMPT="$2"
        if [[ -z "$PROMPT" ]]; then
            echo "❌ Erro: --prompt requer um argumento"
            exit 1
        fi
        
        cd "$REPO_DIR"
        
        # Exportar variáveis OpenClaude
        export CLAUDE_CODE_USE_OPENAI=1
        export OPENAI_API_KEY="021d2bbeb8224a42bf01d83100616c3c.EVM4Z6mSMNbQLYFJ"
        export OPENAI_BASE_URL="https://api.z.ai/api/coding/paas/v4"
        export OPENAI_MODEL="glm-5.1"
        
        echo "🔍 Analisando mudanças no repositório..."
        
        # Mostrar diff antes
        echo ""
        echo "=== Mudanças pendentes ==="
        git diff --stat 2>/dev/null || echo "Nenhuma mudança pendente"
        echo ""
        
        # Executar OpenClaude com prompt
        openclaude --print "$PROMPT" 2>&1
        EXIT_CODE=$?
        
        echo ""
        echo "=== Resumo ==="
        
        # Mostrar status e diff novamente para contexto
        git status --short
        
        echo ""
        echo "✅ Revisão concluída"
        
        exit $EXIT_CODE
        ;;
    --help|-h)
        usage
        exit 0
        ;;
    *)
        echo "❌ Opção desconhecida: $1"
        usage
        exit 1
        ;;
esac