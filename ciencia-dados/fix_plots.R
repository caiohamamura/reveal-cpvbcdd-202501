library(ggplot2)

# Cores Dracula
BG <- "#282a36"
BG2 <- "#44475a"
FG <- "#ffffff"  # BRANCO puro, não #f8f8f2
CYAN <- "#8be9fd"
YELLOW <- "#f1fa8c"
GREEN <- "#50fa7b"

# ============================================================
# FEATURE IMPORTANCE - CORRIGIDO
# ============================================================
importance_df <- data.frame(
  Feature = c("Duration", "Amount", "Age", "Credit_history", "Purpose", 
              "Savings", "Employment", "Status"),
  Value = c(0.23, 0.18, 0.15, 0.12, 0.09, 0.08, 0.07, 0.06)
)

# NÃO usar theme_dark() - usar theme_minimal() com override manual
p1 <- ggplot(importance_df, aes(x = reorder(Feature, Value), y = Value)) +
  geom_col(fill = CYAN, width = 0.7) +
  coord_flip() +
  labs(title = "Feature Importance", 
       subtitle = "German Credit Data",
       x = NULL, y = "Importance (Gini)") +
  # NUNCA usar theme_dark - criar tema do zero
  theme_minimal(base_size = 16, base_family = "sans") +
  theme(
    # Fundo
    rect = element_rect(fill = BG, color = BG),
    panel.background = element_rect(fill = BG),
    plot.background = element_rect(fill = BG),
    # Grid lines
    panel.grid.major = element_line(color = BG2),
    panel.grid.minor = element_line(color = BG2),
    panel.grid = element_line(color = BG2),
    # Texto FORÇADO BRANCO
    text = element_text(color = FG),
    title = element_text(color = FG),
    axis.text = element_text(color = FG, size = 14, face = "bold"),
    axis.title = element_text(color = FG, size = 14),
    plot.title = element_text(color = CYAN, size = 22, face = "bold"),
    plot.subtitle = element_text(color = FG, size = 13),
    # Lines and ticks
    axis.line = element_line(color = FG),
    axis.ticks = element_line(color = FG),
    # Margin
    plot.margin = margin(20, 20, 20, 20)
  ) +
  # Labels dos valores em BRANCO
  geom_text(aes(label = sprintf("%.2f", Value)), 
            hjust = -0.05, color = FG, size = 5, fontface = "bold") +
  ylim(0, 0.30) +
  xlim(rev(reorder(importance_df$Feature, importance_df$Value)))

# Salvar
ggsave("/home/openclaw/.openclaw/workspace/reveal-cpvbcdd-202501/ciencia-dados/images/feature-importance.png", 
       plot = p1, width = 9, height = 5.5, dpi = 200)

cat("1. Feature Importance - check file\n")

# ============================================================
# ROC CURVE - CORRIGIDO
# ============================================================
fpr <- seq(0, 1, length.out = 200)
tpr <- 1 - (1 - fpr)^2.5
roc_df <- data.frame(FPR = fpr, TPR = tpr)

p2 <- ggplot(roc_df, aes(x = FPR, y = TPR)) +
  geom_abline(linetype = "dashed", color = "#6272a4", linewidth = 1.5) +
  geom_line(color = GREEN, linewidth = 3) +
  geom_area(fill = GREEN, alpha = 0.15) +
  # Anotação com box escuro atrás
  annotate("text", x = 0.68, y = 0.22, label = "AUC = 0.72", 
           color = YELLOW, size = 16, fontface = "bold",
           family = "sans") +
  labs(title = "ROC Curve", 
       subtitle = "German Credit Risk Model",
       x = "False Positive Rate", 
       y = "True Positive Rate") +
  theme_minimal(base_size = 16, base_family = "sans") +
  theme(
    rect = element_rect(fill = BG, color = BG),
    panel.background = element_rect(fill = BG),
    plot.background = element_rect(fill = BG),
    panel.grid.major = element_line(color = BG2),
    panel.grid.minor = element_line(color = BG2),
    panel.grid = element_line(color = BG2),
    # Texto FORÇADO BRANCO
    text = element_text(color = FG),
    title = element_text(color = FG),
    axis.text = element_text(color = FG, size = 14, face = "bold"),
    axis.title = element_text(color = FG, size = 14),
    plot.title = element_text(color = GREEN, size = 22, face = "bold"),
    plot.subtitle = element_text(color = FG, size = 13),
    axis.line = element_line(color = FG),
    axis.ticks = element_line(color = FG),
    plot.margin = margin(20, 20, 20, 20)
  ) +
  xlim(0, 1) + ylim(0, 1)

ggsave("/home/openclaw/.openclaw/workspace/reveal-cpvbcdd-202501/ciencia-dados/images/roc-curve.png",
       plot = p2, width = 9, height = 5.5, dpi = 200)

cat("2. ROC Curve - check file\n")

cat("\n=== DONE ===\n")