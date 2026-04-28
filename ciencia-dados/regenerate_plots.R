# Regenerate plots with HIGH CONTRAST for dark background (Dracula theme)

# Colors from Dracula theme
BG <- "#282a36"
FG <- "#f8f8f2"
CYAN <- "#8be9fd"
YELLOW <- "#f1fa8c"
GREEN <- "#50fa7b"

library(ggplot2)

# ============================================================
# PLOT 1: Feature Importance (HIGH CONTRAST)
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
       x = "", y = "Importance (Gini)") +
  theme_dark(16) +
  theme(
    plot.background = element_rect(fill = BG, color = BG),
    panel.background = element_rect(fill = BG),
    panel.grid.major = element_line(color = "#44475a"),
    panel.grid.minor = element_line(color = "#44475a"),
    text = element_text(color = FG),
    axis.text = element_text(color = FG, size = 14)
  ) +
  geom_text(aes(label = sprintf("%.2f", Value)), 
            hjust = -0.1, color = FG, size = 4) +
  ylim(0, 0.30)

ggsave("/home/openclaw/.openclaw/workspace/reveal-cpvbcdd-202501/ciencia-dados/images/feature-importance.png", 
       plot = p1, width = 8, height = 5, dpi = 200, bg = BG)

cat("1. Feature Importance saved\n")

# ============================================================
# PLOT 2: ROC Curve (HIGH CONTRAST)
# ============================================================
fpr <- seq(0, 1, length.out = 200)
tpr <- 1 - (1 - fpr)^2.5

roc_df <- data.frame(FPR = fpr, TPR = tpr)

p2 <- ggplot(roc_df, aes(x = FPR, y = TPR)) +
  geom_abline(linetype = "dashed", color = "#6272a4", size = 1) +
  geom_line(color = GREEN, size = 3) +
  geom_area(fill = GREEN, alpha = 0.2) +
  annotate("rect", x = 0.5, y = 0.08, xmax = 0.88, ymax = 0.38,
           fill = BG, color = GREEN, size = 2) +
  annotate("text", x = 0.69, y = 0.23, label = "AUC = 0.72", 
           color = YELLOW, size = 10, fontface = "bold") +
  labs(title = "ROC Curve", subtitle = "German Credit Risk Model",
       x = "False Positive Rate", y = "True Positive Rate") +
  theme_dark(16) +
  theme(
    plot.background = element_rect(fill = BG, color = BG),
    panel.background = element_rect(fill = BG),
    panel.grid.major = element_line(color = "#44475a"),
    text = element_text(color = FG),
    axis.text = element_text(color = FG, size = 12)
  ) +
  xlim(0, 1) + ylim(0, 1)

ggsave("/home/openclaw/.openclaw/workspace/reveal-cpvbcdd-202501/ciencia-dados/images/roc-curve.png",
       plot = p2, width = 8, height = 5, dpi = 200, bg = BG)

cat("2. ROC Curve saved\n")

# ============================================================
# PLOT 3: Confusion Matrix
# ============================================================
library(reshape2)

cm <- matrix(c(420, 80, 55, 45), nrow = 2, byrow = TRUE)
rownames(cm) <- c("Actual: Bom", "Actual: Mau")
colnames(cm) <- c("Pred: Bom", "Pred: Mau")
cm_df <- melt(cm)
names(cm_df) <- c("Actual", "Predicted", "Count")

p3 <- ggplot(cm_df, aes(x = Predicted, y = Actual, fill = Count)) +
  geom_tile(color = FG, size = 1) +
  geom_text(aes(label = Count), color = FG, size = 16, fontface = "bold") +
  scale_fill_gradient(low = BG, high = CYAN) +
  labs(title = "Confusion Matrix", subtitle = "Test Set (n=600)") +
  theme_dark(16) +
  theme(
    plot.background = element_rect(fill = BG, color = BG),
    panel.background = element_rect(fill = BG),
    text = element_text(color = FG),
    axis.text = element_text(color = FG, size = 14)
  )

ggsave("/home/openclaw/.openclaw/workspace/reveal-cpvbcdd-202501/ciencia-dados/images/confusion-matrix.png",
       plot = p3, width = 6, height = 4, dpi = 200, bg = BG)

cat("3. Confusion Matrix saved\n")

cat("\n=== All plots regenerated with HIGH CONTRAST ===\n")
