library(ggplot2)

# Dracula colors
BG <- "#282a36"   # dark background
FG <- "#ffffff"    # white foreground
GREEN <- "#50fa7b"
YELLOW <- "#f1fa8c"
GRAY <- "#6272a4"

# ROC Curve with FULL DARK THEME
fpr <- seq(0, 1, length.out = 200)
tpr <- 1 - (1 - fpr)^2.5
roc_df <- data.frame(FPR = fpr, TPR = tpr)

# Create plot
p <- ggplot(roc_df, aes(x = FPR, y = TPR)) +
  # Diagonal reference
  geom_abline(linetype = "dashed", color = GRAY, linewidth = 1.5) +
  # ROC curve
  geom_line(color = GREEN, linewidth = 3) +
  geom_area(fill = GREEN, alpha = 0.2) +
  # AUC text with dark background box
  annotate("text", x = 0.68, y = 0.22, label = "AUC = 0.72", 
           color = YELLOW, size = 18, fontface = "bold",
           family = "sans") +
  labs(title = "ROC Curve", 
       subtitle = "German Credit Risk Model",
       x = "False Positive Rate", 
       y = "True Positive Rate") +
  # Use a completely clean theme
  theme_bw(base_size = 16) +
  theme(
    # CRITICAL: Dark background for entire plot
    panel.background = element_rect(fill = BG, color = NA),
    plot.background = element_rect(fill = BG, color = BG),
    rect = element_rect(fill = BG, color = BG),
    # CRITICAL: White text for everything
    text = element_text(color = FG, face = "bold"),
    title = element_text(color = FG),
    axis.text = element_text(color = FG, face = "bold", size = 14),
    axis.title = element_text(color = FG, face = "bold", size = 14),
    # Title color
    plot.title = element_text(color = GREEN, size = 22, face = "bold"),
    plot.subtitle = element_text(color = FG, size = 13),
    # Grid
    panel.grid.major = element_line(color = "#44475a"),
    panel.grid.minor = element_line(color = "#44475a"),
    # Axes
    axis.line = element_line(color = FG),
    axis.ticks = element_line(color = FG),
    axis.ticks.length = unit(3, "mm"),
    # Margin
    plot.margin = margin(20, 20, 20, 20)
  ) +
  xlim(0, 1) + ylim(0, 1) +
  # Add "Random" label
  annotate("text", x = 0.78, y = 0.08, label = "Random", 
           color = GRAY, size = 11, fontface = "italic")

# Save with EXPLICIT bg
ggsave("/home/openclaw/.openclaw/workspace/reveal-cpvbcdd-202501/ciencia-dados/images/roc-curve.png",
       plot = p, width = 9, height = 5.5, dpi = 200, bg = BG)

cat("ROC Curve regenerated with full dark theme\n")
print(p)
