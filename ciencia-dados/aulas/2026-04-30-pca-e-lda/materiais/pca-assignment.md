# Exercícios — PCA: Análise de Componentes Principais

**Ciência de Dados — Aula 11**

---

## Parte 1: Fundamentos Estatísticos

### Exercício 1 — Variância manual

Dado o conjunto $X = \{2, 4, 4, 4, 5, 5, 7, 9\}$:

1. Calcule a média $\bar{x}$.
2. Calcule a variância $\text{Var}(X)$ usando a fórmula $\frac{1}{n-1}\sum(x_i - \bar{x})^2$.
3. Confirme o resultado com `np.var(X, ddof=1)`.

### Exercício 2 — Covariância

Considere as variáveis:

| i | X | Y |
|---|---|---|
| 1 | 1 | 3 |
| 2 | 2 | 5 |
| 3 | 3 | 4 |
| 4 | 4 | 6 |
| 5 | 5 | 8 |

1. Calcule $\text{Cov}(X, Y)$ manualmente.
2. A covariância é positiva ou negativa? O que isso significa?
3. Confirme com `np.cov(X, Y)`.

### Exercício 3 — Matriz de covariância

Para os dados abaixo (3 variáveis, 4 amostras):

$$
X = \begin{bmatrix} 1 & 2 & 1 \\ 2 & 3 & 1 \\ 3 & 5 & 2 \\ 4 & 6 & 3 \end{bmatrix}
$$

1. Centralize os dados: $X_c = X - \mu$.
2. Calcule a matriz de covariância $3 \times 3$.
3. Quais pares de variáveis têm a maior covariância?

---

## Parte 2: Autovetores e Autovalores

### Exercício 4 — Verificação de autovetor

Dada a matriz $A = \begin{bmatrix} 4 & 1 \\ 2 & 3 \end{bmatrix}$:

1. Use `np.linalg.eig(A)` para encontrar autovalores e autovetores.
2. Para cada par $(\lambda, \vec{v})$, verifique que $A\vec{v} = \lambda\vec{v}$.
3. Os autovetores são ortogonais? Calcule $\vec{v_1} \cdot \vec{v_2}$.

### Exercício 5 — Interpretação geométrica

Para a matriz $A = \begin{bmatrix} 2 & 0 \\ 0 & 5 \end{bmatrix}$:

1. Encontre os autovalores e autovetores.
2. Se $\vec{v} = (1, 1)$, qual é o resultado de $A\vec{v}$?
3. Desenhe (ou plote) o vetor $\vec{v}$ e $A\vec{v}$. O que aconteceu em cada eixo?

---

## Parte 3: PCA com NumPy (passo a passo)

### Exercício 6 — PCA manual

Use os dados:

$$
X = \begin{bmatrix} 2.5 & 2.4 \\ 0.5 & 0.7 \\ 2.2 & 2.9 \\ 1.9 & 2.2 \\ 3.1 & 3.0 \end{bmatrix}
$$

Execute o workflow de 4 passos:

1. **Centralize:** $X_c = X - \mu$
2. **Covariância:** $C = \frac{X_c^T X_c}{n-1}$
3. **Decomponha:** autovalores $\lambda$ e autovetores $V$ de $C$
4. **Projetor:** $PC = X_c \cdot V$

Responda:

- Qual é o autovalor dominante ($\lambda_1$)?
- Que porcentagem da variância total a PC1 explica?
- Plote os dados no espaço original e no espaço PCA (lado a lado).

### Exercício 7 — Reconstrução

Usando o resultado do Exercício 6:

1. Reconstrua os dados usando **apenas PC1**: $\hat{X} = PC_1 \cdot V_1^T + \mu$.
2. Calcule o erro médio quadrático: $\text{MSE} = \frac{1}{n}\sum(X - \hat{X})^2$.
3. Compare visualmente $X$ e $\hat{X}$ em um gráfico. Onde o erro é maior?

---

## Parte 4: PCA com scikit-learn

### Exercício 8 — Iris com sklearn

Use o dataset Iris (`sklearn.datasets.load_iris`):

1. Normalize os dados com `StandardScaler`.
2. Aplique PCA com 2 componentes.
3. Plote o scatter 2D colorido por espécie.
4. Quantos componentes são necessários para explicar ≥ 95% da variância?

### Exercício 9 — Gráfico de cotovelo

Ainda com Iris:

1. Aplique PCA sem restrição de componentes.
2. Plote o gráfico de cotovelo (variância individual + acumulada).
3. Anote no gráfico qual é o ponto de "cotovelo".
4. Justifique sua escolha de $k$ com base no gráfico.

### Exercício 10 — Comparação de reconstrução

Para $k = 1, 2, 3, 4$ componentes:

1. Calcule o erro de reconstrução $\text{MSE}(k) = \frac{1}{n}\|X - \hat{X}_k\|^2$.
2. Plote MSE vs. $k$.
3. Compare com a variância **não** explicada: $1 - \sum_{i=1}^{k}\lambda_i/\sum\lambda_i$. São iguais? Por quê?

---

## Parte 5: Interpretação e Reflexão

### Exercício 11 — Questões conceituais

Responda em até 3 linhas cada:

1. Por que PCA exige centralização dos dados?
2. Se duas variáveis têm covariância zero, o que isso significa para PCA?
3. Por que os autovetores de PCA são ortonormais?
4. É possível que PC1 tenha **menos** variância que uma variável original? Por quê?
5. PCA é sensível à escala das variáveis? O que acontece se não normalizarmos?

### Exercício 12 — Aplicação prática

Escolha um dataset do scikit-learn (`load_wine`, `load_breast_cancer`, ou `load_digits`):

1. Quantas variáveis (features) ele tem?
2. Aplique PCA e determine o número ideal de componentes (justifique).
3. Plote a projeção 2D e interprete: as classes estão bem separadas?
4. Qual variável original mais contribui para PC1? (Dica: examine `pca.components_[0]`).

---

## Entrega

- Notebooks com código executável e saídas visíveis.
- Gráficos com título, rótulos nos eixos e legenda.
- Respostas textuais nas células markdown do notebook.
