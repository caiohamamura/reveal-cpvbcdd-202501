---
name: notebook-runner
description: Executa cadernos Jupyter (.ipynb) e instala dependências necessárias. Use para rodar notebooks, instalar pacotes, e executar células de forma programática. Suporta Python, R, Julia.
---

# Notebook Runner — Executar .ipynb e Gerenciar Dependências

## O que faz esta skill

1. **Executa notebooks** (.ipynb) usando papermill ou nbconvert
2. **Instala dependências** Python/R automaticamente
3. **Suporta múltiplas linguagens**: Python, R, Julia
4. **Parâmetros variáveis** para execução com papermill
5. **Saída limpa** em HTML ou executed notebook

## Uso

```bash
# Executar notebook com parâmetros
bash /home/openclaw/.openclaw/skills/notebook-runner/scripts/run.sh --notebook caminho/arquivo.ipynb

# Executar com parâmetros
bash /home/openclaw/.openclaw/skills/notebook-runner/scripts/run.sh --notebook caminho/arquivo.ipynb --param variable=value

# Apenas instalar dependências
bash /home/openclaw/.openclaw/skills/notebook-runner/scripts/run.sh --install

# Apenas instalar pacote específico
bash /home/openclaw/.openclaw/skills/notebook-runner/scripts/run.sh --pkg nome-pacote

# Verificar ambiente
bash /home/openclaw/.openclaw/skills/notebook-runner/scripts/run.sh --check
```

## Opções do Script

| Opção | Descrição |
|-------|-----------|
| `--notebook <file>` | Notebook .ipynb para executar |
| `--param <key=value>` | Parâmetros para o papermill (pode repetir) |
| `--output <file>` | Arquivo de saída (default: input_executed.ipynb) |
| `--kernel <name>` | Kernel Jupyter (python3, ir, julia) |
| `--install` | Instalar todas as dependências |
| `--install-r` | Instalar R e IRkernel |
| `--pkg <name>` | Instalar pacote Python específico |
| `--check` | Verificar ambiente instalado |
| `--help` | Mostrar ajuda |

## Dependências Python

O script instala automaticamente:
- `papermill` — execução programática de notebooks
- `nbconvert` — conversão e execução de notebooks
- `jupyter` — kernel Jupyter

```bash
pip3 install --break-system-packages papermill nbconvert jupyter
```

## Linguagens Suportadas

### R

Para executar notebooks R, instale R e IRkernel:

```bash
# Instalar R
sudo apt install r-base

# No R, instalar IRkernel
R -e "install.packages(c('IRkernel', 'IRdisplay'))"
R -e "IRkernel::installspec(user = FALSE)"

# Pacotes R necessários para ML
R -e "install.packages(c('tidymodels', 'ranger', 'vip', 'yardstick', 'ggplot2', 'palmerpenguins'))"
```

Para executar notebook R:
```bash
# via papermill com kernel ir
papermill notebook.ipynb output.ipynb -k ir

# via Rscript (sem kernel)
R -e "rmarkdown::render('notebook.ipynb')"
```

### Python

```bash
pip3 install --break-system-packages papermill nbconvert jupyter
```

### Julia

```bash
# No Julia
using Pkg
Pkg.add("IJulia")
```

## Exemplo de Uso Programático

```python
import papermill as pm

# Executar notebook com parâmetros
pm.execute_notebook(
    'input.ipynb',
    'output.ipynb',
    parameters=dict(variable=value),
    kernel_name='ir'  # para R
)
```

## Saída

O script mostra:
- Status da instalação
- Progresso da execução
- Tempo de execução
- Erros (se houver)

## Notas

- Papermill permite passagem de parâmetros para notebooks
- Notebooks são executados com kernel Python3 por padrão
- Para R, use `--kernel ir` se IRkernel estiver instalado
- Sem R, notebooks R podem ser convertidos para .Rmd e executados via Rscript