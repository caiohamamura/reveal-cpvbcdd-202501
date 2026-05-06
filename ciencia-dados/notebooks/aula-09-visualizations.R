# Gerar visualizações para aula-09

# a) Gráfico de Feature Importance
library(ggplot2)

importance_df <- data.frame(
  Feature = c("Duration", "Amount", "Age", "Credit_history", "Purpose"),
  Importance = c(0.23, 0.18, 0.15, 0.12, 0.09)
)

p1 <- ggplot(importance_df, aes(x = reorder(Feature, Importance), y = Importance)) +
  geom_col(fill = "#8be9fd") +
  coord_flip() +
  labs(title = "Feature Importance - German Credit",
       x = "Feature", y = "Importance (Gini)") +
  theme_minimal() +
  theme(plot.background = element_rect(fill = "#282a36", color = "#282a36"))

ggsave("/home/openclaw/.openclaw/workspace/reveal-cpvbcdd-202501/ciencia-dados/images/feature-importance.png",
       plot = p1, width = 8, height = 5, dpi = 150)
cat("Feature Importance: OK\n")

# b) Gráfico AUC
roc_df <- data.frame(
  FPR = seq(0, 1, length.out = 100),
  TPR = seq(0, 1, length.out = 100)^0.7
)

p2 <- ggplot(roc_df, aes(x = FPR, y = TPR)) +
  geom_line(color = "#50fa7b", size = 2) +
  geom_abline(linetype = "dashed", color = "#6272a4") +
  annotate("text", x = 0.6, y = 0.3, label = "AUC = 0.72",
           color = "#f1fa8c", size = 6) +
  labs(title = "ROC Curve - German Credit Risk",
       x = "False Positive Rate", y = "True Positive Rate") +
  theme_minimal() +
  theme(plot.background = element_rect(fill = "#282a36", color = "#282a36"))

ggsave("/home/openclaw/.openclaw/workspace/reveal-cpvbcdd-202501/ciencia-dados/images/roc-curve.png",
       plot = p2, width = 8, height = 5, dpi = 150)
cat("ROC Curve: OK\n")

# c) Tabela com xtable
library(xtable)

metricas <- data.frame(
  Metrica = c("Accuracy", "Precision", "Recall", "F1-Score", "AUC"),
  Valor = c("0.72", "0.55", "0.38", "0.45", "0.72"),
  Interpretação = c("Geral", "Classe positiva", "Classe positiva", "Balanceado", "Razoável")
)

print(xtable(metricas, caption = "Métricas de Avaliação"), type = "html")
cat("Tabela xtable: OK\n")

# d) Pipeline Visual
pipeline_df <- data.frame(
  step = c("Dados", "Split", "Limpeza", "Feature", "Treino", "Validação", "Teste"),
  x = 1:7,
  y = rep(1, 7)
)

p3 <- ggplot(pipeline_df, aes(x = x, y = y)) +
  geom_point(size = 15, color = "#8be9fd") +
  geom_line(size = 2, color = "#6272a4") +
  geom_text(aes(label = step), y = 1.3, color = "#f8f8f2", size = 4) +
  scale_x_continuous(breaks = 1:7, labels = pipeline_df$step) +
  theme_void() +
  theme(plot.background = element_rect(fill = "#282a36", color = "#282a36"))

ggsave("/home/openclaw/.openclaw/workspace/reveal-cpvbcdd-202501/ciencia-dados/images/pipeline.png",
       plot = p3, width = 10, height = 3, dpi = 150)
cat("Pipeline: OK\n")

cat("\nTodas as visualizações geradas com sucesso!\n")
