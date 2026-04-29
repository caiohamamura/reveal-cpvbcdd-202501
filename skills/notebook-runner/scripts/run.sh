#!/bin/bash
# Notebook Runner — Executar .ipynb e instalar dependências

set -e

SKILL_DIR="/home/openclaw/.openclaw/skills/notebook-runner"
NOTEBOOK=""
OUTPUT=""
PARAMS=""
KERNEL="python3"

# Função para mostrar uso
usage() {
    echo "Uso: $0 [opção]"
    echo ""
    echo "Opções:"
    echo "  --notebook <file>   Notebook .ipynb para executar"
    echo "  --param <key=value> Parâmetro para o papermill (pode repetir)"
    echo "  --output <file>     Arquivo de saída (default: input_executed.ipynb)"
    echo "  --kernel <name>     Kernel Jupyter (python3, ir, julia) - default: python3"
    echo "  --install           Instalar todas as dependências Python"
    echo "  --install-r         Instalar R e IRkernel"
    echo "  --pkg <name>        Instalar pacote Python específico"
    echo "  --check             Verificar ambiente"
    echo "  --help              Mostrar esta ajuda"
    echo ""
    echo "Exemplos:"
    echo "  $0 --install"
    echo "  $0 --notebook aula.ipynb"
    echo "  $0 --notebook aula.ipynb --kernel ir"
    echo "  $0 --notebook aula.ipynb --param data=valor --output saida.ipynb"
}

# Função para verificar ambiente
check_env() {
    echo "🔍 Verificando ambiente..."
    echo ""
    
    # Python
    if command -v python3 &> /dev/null; then
        echo "✅ Python: $(python3 --version)"
    else
        echo "❌ Python: não encontrado"
    fi
    
    # pip
    if command -v pip3 &> /dev/null; then
        echo "✅ pip3: $(pip3 --version | cut -d' ' -f1-2)"
    else
        echo "❌ pip3: não encontrado"
    fi
    
    # Jupyter packages
    echo ""
    echo "📦 Pacotes Jupyter instalados:"
    pip3 list 2>/dev/null | grep -iE "jupyter|papermill|nbconvert" || echo "  Nenhum pacote Jupyter encontrado"
    
    # Kernels disponíveis
    echo ""
    echo "🔮 Kernels Jupyter disponíveis:"
    if [[ -d ~/.local/share/jupyter/kernels ]]; then
        ls ~/.local/share/jupyter/kernels 2>/dev/null | while read k; do
            echo "  - $k"
        done
    elif [[ -d /usr/local/share/jupyter/kernels ]]; then
        ls /usr/local/share/jupyter/kernels 2>/dev/null | while read k; do
            echo "  - $k"
        done
    else
        echo "  Nenhum kernel encontrado"
    fi
    
    # R
    if command -v R &> /dev/null; then
        echo ""
        echo "✅ R: $(R --version | head -1)"
        # Check for IRkernel
        if R -e "require(IRkernel)" 2>/dev/null; then
            echo "✅ IRkernel: instalado"
        else
            echo "⚠️ IRkernel: não instalado (use --install-r)"
        fi
    else
        echo ""
        echo "⚠️ R: não instalado (use --install-r para instalar)"
    fi
    
    echo ""
}

# Função para instalar dependências Python
install_deps() {
    echo "📦 Instalando dependências Python..."
    
    pip3 install --break-system-packages papermill nbconvert jupyter
    
    echo "✅ Dependências Python instaladas!"
    echo ""
    pip3 list | grep -iE "jupyter|papermill|nbconvert"
}

# Função para instalar R e IRkernel
install_r() {
    echo "📦 Instalando R e IRkernel..."
    
    # Verificar se R está instalado
    if ! command -v R &> /dev/null; then
        echo "⚠️ R não está instalado."
        echo "Para instalar R, execute:"
        echo "  sudo apt update && sudo apt install -y r-base"
        echo ""
        echo "Após instalar R, execute este script novamente com --install-r"
        return 1
    fi
    
    echo "✅ R encontrado: $(R --version | head -1)"
    
    # Instalar IRkernel e IRdisplay
    echo "📦 Instalando IRkernel e IRdisplay..."
    R -e "install.packages(c('IRkernel', 'IRdisplay'), repos='https://cloud.r-project.org')"
    
    # Registrar kernel
    echo "📦 Registrando kernel Jupyter para R..."
    R -e "IRkernel::installspec(user = FALSE)"
    
    # Instalar pacotes úteis para ML
    echo "📦 Instalando pacotes R para Machine Learning..."
    R -e "install.packages(c('tidymodels', 'ranger', 'vip', 'yardstick', 'ggplot2', 'palmerpenguins', 'recipes', 'rsample', 'parsnip', 'workflows'), repos='https://cloud.r-project.org')"
    
    echo ""
    echo "✅ R e dependências instalados!"
    echo ""
    echo "Kernels disponíveis:"
    R -e "IRkernel:: kernelspecs()"
}

# Função para instalar pacote específico
install_pkg() {
    local pkg="$1"
    if [[ -z "$pkg" ]]; then
        echo "❌ Erro: --pkg requer nome do pacote"
        exit 1
    fi
    echo "📦 Instalando $pkg..."
    pip3 install --break-system-packages "$pkg"
    echo "✅ $pkg instalado!"
}

# Função para executar notebook
run_notebook() {
    local nb="$1"
    shift
    
    if [[ ! -f "$nb" ]]; then
        echo "❌ Erro: Notebook não encontrado: $nb"
        exit 1
    fi
    
    # Verificar se papermill está instalado
    if ! pip3 show papermill &> /dev/null; then
        echo "⚠️ papermill não instalado. Instalando..."
        install_deps
    fi
    
    # Gerar output name
    if [[ -z "$OUTPUT" ]]; then
        local basename="${nb%.ipynb}"
        OUTPUT="${basename}_executed.ipynb"
    fi
    
    echo "📓 Executando notebook: $nb"
    echo "📝 Saída: $OUTPUT"
    echo "🔮 Kernel: $KERNEL"
    
    # Construir comando papermill
    local cmd="papermill \"$nb\" \"$OUTPUT\" -k \"$KERNEL\""
    
    # Adicionar parâmetros
    if [[ -n "$PARAMS" ]]; then
        for p in $PARAMS; do
            local key="${p%%=*}"
            local val="${p#*=}"
            cmd="$cmd -p $key $val"
            echo "  📌 Parâmetro: $key = $val"
        done
    fi
    
    echo ""
    echo "⏳ Executando..."
    echo ""
    
    # Executar
    $cmd
    
    echo ""
    echo "✅ Concluído!"
    echo "📁 Output: $OUTPUT"
}

# Parse argumentos
if [[ $# -eq 0 ]]; then
    usage
    exit 0
fi

while [[ $# -gt 0 ]]; do
    case "$1" in
        --notebook)
            NOTEBOOK="$2"
            shift 2
            ;;
        --output)
            OUTPUT="$2"
            shift 2
            ;;
        --kernel)
            KERNEL="$2"
            shift 2
            ;;
        --param)
            PARAMS="$PARAMS $2"
            shift 2
            ;;
        --install)
            install_deps
            exit 0
            ;;
        --install-r)
            install_r
            exit 0
            ;;
        --pkg)
            install_pkg "$2"
            exit 0
            ;;
        --check)
            check_env
            exit 0
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
done

# Executar notebook se fornecido
if [[ -n "$NOTEBOOK" ]]; then
    run_notebook "$NOTEBOOK"
fi