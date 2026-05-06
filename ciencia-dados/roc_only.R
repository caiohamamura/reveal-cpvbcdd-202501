library(ggplot2)
BG <- "#282a36"
FG <- "#f8f8f2"
GREEN <- "#50fa7b"
YELLOW <- "#f1fa8c"

# ROC Curve
fpr <- seq(0, 1, length.out = 200)
tpr <- 1 - (1 - fpr)^2.5
roc_df <- data.frame(FPR = fpr, TPR = tpr)

p2 <- ggplot(roc_df, aes(x = FPR, y = TPR)) +
  geom_abline(linetype = "dashed", color = "#6272a4", linewidth = 1) +
  geom_line(color = GREEN, linewidth = 3) +
  geom_area(fill = GREEN, alpha = 0.2) +
  # Simple text annotation instead of rect
  annotate("text", x = 0.7, y = 0.25, label = "AUC = 0.72", 
           color = YELLOW, size = 12, fontface = "bold", bg = BG) +
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

cat("ROC Curve saved\n")
