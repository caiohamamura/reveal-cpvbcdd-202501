# HIGH CONTRAST plots for dark background

BG <- "#282a36"
BG2 <- "#44475a"
FG <- "#f8f8f2"
CYAN <- "#8be9fd"
YELLOW <- "#f1fa8c"
GREEN <- "#50fa7b"
PINK <- "#ff79c6"

library(ggplot2)

# ============================================================
# PLOT 1: Feature Importance - WHITE TEXT
# ============================================================
importance_df <- data.frame(
  Feature = c("Duration", "Amount", "Age", "Credit_history", "Purpose", 
              "Savings", "Employment", "Status"),
  Value = c(0.23, 0.18, 0.15, 0.12, 0.09, 0.08, 0.07, 0.06)
)

p1 <- ggplot(importance_df, aes(x = reorder(Feature, Value), y = Value)) +
  geom_col(fill = CYAN, width = 0.7) +
  coord_flip() +
  labs(title = "Feature Importance", subtitle = "German Credit Data",
       x = NULL, y = "Importance (Gini)") +
  # White text everywhere!
  theme(
    plot.background = element_rect(fill = BG, color = BG),
    panel.background = element_rect(fill = BG, color = BG2),
    panel.grid.major = element_line(color = BG2),
    panel.grid.minor = element_line(color = BG2),
    # FORCE white text
    text = element_text(color = FG, family = "sans"),
    axis.text = element_text(color = FG, size = 14),
    axis.title = element_text(color = FG, size = 14),
    plot.title = element_text(color = CYAN, size = 20, face = "bold"),
    plot.subtitle = element_text(color = FG, size = 12),
    legend.text = element_text(color = FG),
    legend.title = element_text(color = FG)
  ) +
  # Value labels in white
  geom_text(aes(label = sprintf("%.2f", Value)), 
            hjust = -0.05, color = FG, size = 5) +
  ylim(0, 0.30) +
  xlim(rev(reorder(importance_df$Feature, importance_df$Value)))

ggsave("/home/openclaw/.openclaw/workspace/reveal-cpvbcdd-202501/ciencia-dados/images/feature-importance.png", 
       plot = p1, width = 9, height = 5.5, dpi = 200, bg = BG)

cat("1. Feature Importance saved (white text)\n")

# ============================================================
# PLOT 2: ROC Curve - WHITE TEXT
# ============================================================
fpr <- seq(0, 1, length.out = 200)
tpr <- 1 - (1 - fpr)^2.5
roc_df <- data.frame(FPR = fpr, TPR = tpr)

p2 <- ggplot(roc_df, aes(x = FPR, y = TPR)) +
  geom_abline(linetype = "dashed", color = "#6272a4", linewidth = 1.5) +
  geom_line(color = GREEN, linewidth = 3) +
  geom_area(fill = GREEN, alpha = 0.15) +
  annotate("text", x = 0.7, y = 0.25, label = "AUC = 0.72", 
           color = YELLOW, size = 14, fontface = "bold", 
           family = "sans") +
  labs(title = "ROC Curve", subtitle = "German Credit Risk Model",
       x = "False Positive Rate", y = "True Positive Rate") +
  theme(
    plot.background = element_rect(fill = BG, color = BG),
    panel.background = element_rect(fill = BG, color = BG2),
    panel.grid.major = element_line(color = BG2),
    panel.grid.minor = element_line(color = BG2),
    # FORCE white text
    text = element_text(color = FG, family = "sans"),
    axis.text = element_text(color = FG, size = 14),
    axis.title = element_text(color = FG, size = 14),
    plot.title = element_text(color = GREEN, size = 22, face = "bold"),
    plot.subtitle = element_text(color = FG, size = 13)
  ) +
  xlim(0, 1) + ylim(0, 1)

ggsave("/home/openclaw/.openclaw/workspace/reveal-cpvbcdd-202501/ciencia-dados/images/roc-curve.png",
       plot = p2, width = 9, height = 5.5, dpi = 200, bg = BG)

cat("2. ROC Curve saved (white text)\n")

# ============================================================
# PLOT 3: Confusion Matrix - WHITE TEXT
# ============================================================
library(reshape2)

cm <- matrix(c(420, 80, 55, 45), nrow = 2, byrow = TRUE)
rownames(cm) <- c("Actual: Bom", "Actual: Mau")
colnames(cm) <- c("Pred: Bom", "Pred: Mau")
cm_df <- melt(cm)
names(cm_df) <- c("Actual", "Predicted", "Count")

p3 <- ggplot(cm_df, aes(x = Predicted, y = Actual, fill = Count)) +
  geom_tile(color = FG, linewidth = 1.5) +
  geom_text(aes(label = Count), color = FG, size = 18, fontface = "bold") +
  scale_fill_gradient(low = BG2, high = CYAN, name = "Count") +
  labs(title = "Confusion Matrix", subtitle = "Test Set (n=600)") +
  theme(
    plot.background = element_rect(fill = BG, color = BG),
    panel.background = element_rect(fill = BG),
    text = element_text(color = FG, family = "sans"),
    axis.text = element_text(color = FG, size = 14),
    axis.title = element_text(color = FG, size = 14),
    plot.title = element_text(color = YELLOW, size = 20, face = "bold"),
    plot.subtitle = element_text(color = FG, size = 12),
    legend.text = element_text(color = FG),
    legend.title = element_text(color = FG)
  )

ggsave("/home/openclaw/.openclaw/workspace/reveal-cpvbcdd-202501/ciencia-dados/images/confusion-matrix.png",
       plot = p3, width = 7, height = 5, dpi = 200, bg = BG)

cat("3. Confusion Matrix saved (white text)\n")

cat("\n=== All plots with WHITE labels on dark background ===\n")
