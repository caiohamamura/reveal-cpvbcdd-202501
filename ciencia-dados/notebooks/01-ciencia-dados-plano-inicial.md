# Aula 9: Estrutura Completa de um Projeto de Data Science em R

**Objetivo:** Mostrar o fluxo completo desde tratamento de dados até teste de modelo usando R, preparando o terreno para RandomForest.

**Ponte com aula anterior:** K-NN e Árvores de Decisão já foram vistos individualmente. Agora: como essas peças se encaixam num pipeline real?

**Dataset:** German Credit Data (UCI) — risco de crédito, dados reais e imperfeitos.

**Stack:** R + tidyverse + ranger + yardstick + rsample

---

## Bloco 1 — O Fluxo Completo (50 min)

### Conceito (15 min)

Apresentar o pipeline visual:

```
Dados → Limpeza → Feature Engineering → Split → Treino → Validação → Teste
```

Cada peça já foi vista em aulas anteriores — agora é a primeira vez que veem **tudo junto**.

### Discussão (10 min)

- "O que acontece se você testar no dado que treinou?" (memória vs generalização)
- "Por que não usamos TODOS os dados para treinar?" (overfitting)
- "O que é o teste invisível e por que ele importa?"

### Atividade (15 min)

Entregar o German Credit Data com problema proposital:
- Colunas com missing values
- Variáveis categóricas com muitas categorías
- Feature de renda com outliers

Desafio: os alunos listam os problemas que veem (sem resolver ainda).

---

## Bloco 2 — Train/Test/Validação em Profundidade em R (50 min)

### Conceito (20 min)

**Train/Test Split em R:**
```r
library(rsample)

split <- initial_split(dados, prop = 0.8, strata = target)
treino <- training(split)
teste <- testing(split)
```

- `strata = target` = manter proporção da classe (importante para classificação desbalanceada)
- `prop = 0.8` = 80% treino, 20% teste

**Validação Cruzada (k-fold) em R:**
```r
library(rsample)

cv <- vfold_cv(treino, v = 5, strata = target)
```

- k=5 ou k=10 (mais robusto que single split)
- A cada fold, uma parcela diferente é usada como validação

**Holdout final:**
- Não existe no treinamento (teste é blindado)
- "Você olha o teste só UMA vez — quando escolheu o melhor modelo na validação"

### Código (20 min)

```r
library(rsample)
library(ranger)
library(yardstick)

# Split simples
split <- initial_split(dados, prop = 0.8, strata = target)
treino <- training(split)
teste <- testing(split)

# Modelo ranger
modelo <- ranger(
  formula = target ~ .,
  data = treino,
  num.trees = 100,
  seed = 42
)

# Métricas no teste (única vez!)
pred_teste <- predict(modelo, data = teste)
pred_teste$predictions

# Métricas com yardstick
resultados <- tribble(
  ~metric, ~value,
  'accuracy', accuracy(teste, truth, pred)$`.estimate`,
  'precision', precision(teste, truth, pred)$`.estimate`,
  'recall', recall(teste, truth, pred)$`.estimate`,
  'f1', f_meas(teste, truth, pred)$`.estimate`
)
```

**Onde os alunos travam:** achar que métricas no treino já são o teste — na verdade é otimista demais. O teste real é `predict()` no `teste`.

---

## Bloco 3 — Pipeline Completo em R (50 min)

### Estrutura do Caderno (template completo)

```r
# ============================================================
# PROJETO COMPLETO: German Credit Risk em R
# Fluxo: Dados → Limpeza → Feature Eng → Split → Treino → Validação → Teste
# ============================================================

# 1. Importação e Carregamento
library(tidyverse)
dados <- read_csv("german_credit_data.csv")

# 2. Limpeza
# Missing values
dados <- dados %>%
  mutate_if(is.numeric, ~replace_na(., median(., na.rm = TRUE)))

# 3. Feature Engineering
# Variáveis categóricas
dados <- dados %>%
  mutate(
    target = ifelse(risk == "good", 0, 1),
    across(where(is.character), as.factor)
  ) %>%
  select(-risk)

# 4. Split (ANTES de qualquer transformação!)
library(rsample)
split <- initial_split(dados, prop = 0.8, strata = target)
treino <- training(split)
teste <- testing(split)

# 5. Pré-processamento no treino SOMENTE
# (NÃO fazer no dado completo — isso causa data leakage!)

# 6. Treino com validação cruzada
library(ranger)
cv <- vfold_cv(treino, v = 5, strata = target)

# 7. Treino final e avaliação no teste
modelo_final <- ranger(target ~ ., data = treino, num.trees = 100)
predicoes <- predict(modelo_final, data = teste)

# 8. Métricas (accuracy, precision, recall, f1)
# NO TESTE — única vez que vemos o teste!
```

### ⚠️ ERRO COMUM: Data Leakage

```r
# ❌ ERRADO — data leakage:
dados_scaled <- scale(dados)  # Usa TODOS os dados!
split <- initial_split(dados_scaled)

# ✅ CERTO — scale só no treino:
split <- initial_split(dados)
treino <- training(split)
teste <- testing(split)
treino_scaled <- scale(treino)
teste_scaled <- scale(teste)  # Usa média/desvio do TREINO!
```

---

## Bloco 4 — Ética: COMPAS e Viés Algorítmico (50 min)

### O Caso COMPAS

- **COMPAS** (Correctional Offender Management Profiling for Alternative Sanctions)
- Sistema usado nos EUA para prever reincidência criminal
- **ProPublica descobriu**:黑人 receives higher risk scores even when controlling for prior offenses

### Métricas de Fairness

Quando avaliamos fairness, não basta só accuracy:

| Métrica | Definição | Por que importa |
|---------|-----------|----------------|
| **Accuracy** | % total de acertos | Pode ser alta mas biasada |
| **Precision** | TP / (TP + FP) | "Das pessoas que você classificou como risco, quantas realmente eram?" |
| **Recall** | TP / (TP + FN) | "Das pessoas que eram risco, quantas você encontrou?" |
| **Disparate Impact** | taxa_negativos / taxa_positivos | < 0.8 pode indicar viés |

### Discussão

- "Se o modelo erra mais para um grupo, isso é justo?"
- "Quem é responsável quando o algoritmo erra?"
- "Podemos usar modelos assim em decisões de justiça?"

---

## Exercícios

### Em aula (formativa)

- **Parte 1:** Identificar problemas no dataset German Credit
- **Parte 2:** Treinar modelo no R e verificar métricas de fairness

### Pós-aula (somativa)

- Entrega no Moodle: caderno R com pipeline completo + análise de viés no dataset

---

## Materiais Necessários

- RStudio ou Jupyter com IRkernel
- Pacotes: `tidyverse`, `ranger`, `yardstick`, `rsample`
- Dataset: German Credit Data (UCI)
- Terminal com múltiplas abas

---

## Roteiro de Comandos (base para professor)

```r
# Instalar pacotes (se necessário)
install.packages(c("tidyverse", "ranger", "yardstick", "rsample"))

# Carregar
library(tidyverse)
library(ranger)
library(yardstick)
library(rsample)

# Carregar German Credit Data
url <- "https://archive.ics.uci.edu/ml/machine-learning-databases/statlog/german/german.data"
col_names <- c("Status", "Duration", "Credit_history", "Purpose", "Amount",
               "Savings", "Employment", "Installment_rate", "Personal", "Others",
               "Residence", "Property", "Age", "Installment_plans", "Housing",
               "Existing_credits", "Job", "Liable_population", "Telephone", "Foreign", "Target")
dados <- read.table(url, col.names = col_names, stringsAsFactors = TRUE)
dados$Target <- ifelse(dados$Target == 1, 0, 1)  # 0=bom, 1=mau
```