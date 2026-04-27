# Aula 9: Estrutura Completa de um Projeto de Data Science

**Objetivo:** Mostrar o fluxo completo desde tratamento de dados até teste de modelo, preparando o terreno para RandomForest.

**Ponte com aula anterior:** K-NN e Árvores de Decisão já foram vistos individualmente. Agora: como essas peças se encaixam num pipeline real?

**Dataset:** German Credit Data (UCI) — risco de crédito, dados reais e imperfeitos.

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

## Bloco 2 — Treinamento/Teste/Validação em Profundidade (50 min)

### Conceito (20 min)

**Train/Test Split:**
- Por que 70/30 ou 80/20? (trade-off entre ter dados suficientes para treinar vs validar)
- `random_state` = reprodutibilidade (mesmo split toda vez)
- `stratify=y` = manter proporção da classe (importante para classificação desbalanceada)
- Vizual: como o dado é dividido (80% treino → fit, 20% teste → nunca visto até o final)

**Validação Cruzada (k-fold):**
- k=5 ou k=10 (mais robusto que single split)
- A cada fold, uma parcela diferente é usada como validação
- Resultado: média das k folds = score mais estável
- Comparação visual: single split muda muito, k-fold estabiliza

**Holdout final:**
- Não existe no treinamento (teste é blindado)
- "Você olha o teste só UMA vez — quando escolheu o melhor modelo na validação"

### Código (20 min)

```python
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeClassifier

# Split simples (para entender)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Árvore simples treinada
tree = DecisionTreeClassifier(max_depth=3, random_state=42)
tree.fit(X_train, y_train)

# Acurácia no teste (invisível durante desenvolvimento)
print(f"Teste: {tree.score(X_test, y_test):.3f}")

# Validação cruzada (mais robusta)
cv_scores = cross_val_score(tree, X, y, cv=5, scoring='accuracy')
print(f"CV médio: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")
```

**Onde os alunos travam:** achar que `score()` no modelo treinado já é o teste — na verdade é treino. O teste real é `score(X_test, y_test)`.

---

## Bloco 3 — Pipeline Completo no Código (50 min)

### Estrutura do Caderno (template completo)

```python
# ============================================================
# PROJETO COMPLETO: German Credit Risk
# Fluxo: Dados → Limpeza → Feature Eng → Split → Treino → Validação → Teste
# ============================================================

# 1. Importação e Carregamento
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('german_credit_data.csv')
print(f"Shape: {df.shape}")
print(df.head())

# 2. EDA Rápida
print("\n--- Missing values ---")
print(df.isnull().sum())
print("\n--- Dtypes ---")
print(df.dtypes)

# 3. Tratamento
# 3a. Variáveis categóricas → OneHotEncoding
df_encoded = pd.get_dummies(df, columns=['Purpose', 'Housing'], drop_first=True)

# 3b. Missing values (exemplo simples: fill com mediana)
df_encoded['Credit_amount'].fillna(df_encoded['Credit_amount'].median(), inplace=True)

# 3c. Normalização (para qualquer modelo que precise)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 4. Split (AGORA sim, depois de tratar!)
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

# 5. Treino com Validação Cruzada
tree = DecisionTreeClassifier(max_depth=4, random_state=42)

# Validação cruzada ANTES do teste final
cv_scores = cross_val_score(tree, X_train, y_train, cv=5, scoring='accuracy')
print(f"CV Score: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")

# Fit final nos dados de treino
tree.fit(X_train, y_train)

# 6. Teste final (OLHAR SÓ AGORA, DEPOIS DE ESCOLHER O MODELO)
y_pred = tree.predict(X_test)
print("\n--- Teste Final ---")
print(classification_report(y_test, y_pred))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
```

### Dica Pedagógica
**Onde os alunos travam:**
1. Fazem split ANTES do tratamento (vazamento de informação)
2. Avaliam no dado de treino achando que é o teste real
3. Esquecem `stratify=y` em dados desbalanceados

---

## Bloco 4 — Overfitting, Underfitting e Ética (50 min)

### Conceito (15 min)

**Overfitting vs Underfitting — a curva de aprendizado:**

```
Complexidade do Modelo
    |
    |     /¯¯¯¯¯¯¯¯¯ (overfitting: treino alto, teste baixo)
    |    /
    |   /                  ___ (modelo bom)
    |  /
    | /
    |/_________ (underfitting: treino baixo, teste baixo)
    |
    └──────────────────────────────────
         Pouco          Ótimo         Muito
         (under)      (equilibrado)   (over)
```

Código para visualizar:
```python
import matplotlib.pyplot as plt

depths = range(1, 15)
train_scores = []
test_scores = []

for d in depths:
    t = DecisionTreeClassifier(max_depth=d, random_state=42)
    t.fit(X_train, y_train)
    train_scores.append(t.score(X_train, y_train))
    test_scores.append(t.score(X_test, y_test))

plt.plot(depths, train_scores, label='Treino', marker='o')
plt.plot(depths, test_scores, label='Teste', marker='x')
plt.xlabel('Profundidade da Árvore')
plt.ylabel('Acurácia')
plt.title('Overfitting: quanto mais profundo, treino sobe, teste estagna/caí')
plt.legend()
plt.show()
```

### Discussão Ética (20 min)

**Perguntas para a turma:**
1. "Se o modelo erra mais em pessoas de baixa renda, isso é justo?"
2. "Quando usamos dados históricos, estamos perpetuando vieses?"
3. "O teste invisível existe para proteger o modelo de quê?"
4. "Quem é responsável quando o modelo erra?"

**Slides rápidos:**
- Viés de seleção no split (dados não representativos)
- "Modelo bom não é só acurácia alta — é acurácia alta para TODOS os grupos"
- Exemplo real: COMPAS (racismo em algoritmos de justiça criminal)

### Atividade Final (15 min)

**Exercício de ética:** Listar 3 decisões de design neste pipeline que poderiam causar viés, e como evitá-las.

---

## Datasets Recomendados

| Dataset | Uso | Link |
|---------|-----|------|
| German Credit Data | Pipeline completo + ética | UCI Repository |
| Telco Customer Churn | Classificação binária | IBM Kaggle |
| Heart Disease UCI | Variáveis numéricas + categóricas | UCI Repository |

---

## Próxima Aula: RandomForest (Aula 10)

**Conexão:** Árvores de Decisão foram o modelo do bloco 3. Agora: e se combinarmos muitas árvores?

**Novos conceitos:**
- Ensemble de árvores (bagging)
- Random Forest: floresta de árvores com aleatoriedade
- Feature importance
- Parâmetros: n_estimators, max_depth, bootstrap

---

## Resumo dos Conceitos-Chave

| Conceito | Bloco | Por que importa |
|----------|-------|-----------------|
| Pipeline completo | 1-3 | Nunca mais fazer código bagunçado |
| Train/Test Split | 2 | Separar dado seen from unseen |
| Validação Cruzada | 2 | Escolher modelo sem trapaça |
| Holdout test | 2 | Medir generalização real |
| Overfitting/Underfitting | 4 | Entender limites do modelo |
| Ethics | 4 | Responsabilidade do cientista |

---

*Plano de aula gerado por Leila — Assistente de Design Instrucional*
*Workspace: ciência-dados | Data: 2026-04-26*