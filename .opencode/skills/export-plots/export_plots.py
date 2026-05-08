#!/usr/bin/env python3
"""
Export plots from Python code with Dracula dark theme validation and generation.
Usage:
    python3 export_plots.py --check images/*.png    # Validate existing images
    python3 export_plots.py notebook.ipynb --output-dir images/ --dpi 150  # Extract from notebook
"""

import argparse
import json
import os
import sys
from pathlib import Path


# Dracula theme colors (for reference)
DRACULA = {
    "background": "#282a36",
    "current_line": "#44475a",
    "selection": "#44475a",
    "foreground": "#f8f8f2",
    "comment": "#6272a4",
    "cyan": "#8be9fd",
    "green": "#50fa7b",
    "orange": "#ffb86c",
    "pink": "#ff79c6",
    "purple": "#bd93f9",
    "red": "#ff5555",
    "yellow": "#f1fa8c",
}

DEFAULT_PALETTE = [DRACULA["purple"], DRACULA["green"], DRACULA["cyan"],
                   DRACULA["pink"], DRACULA["orange"], DRACULA["yellow"]]


def apply_dracula_theme():
    """Set matplotlib/seaborn to Dracula dark theme."""
    import matplotlib.pyplot as plt
    import matplotlib as mpl

    mpl.rcParams.update({
        "figure.facecolor": DRACULA["background"],
        "axes.facecolor": DRACULA["background"],
        "axes.edgecolor": DRACULA["foreground"],
        "axes.labelcolor": DRACULA["foreground"],
        "text.color": DRACULA["foreground"],
        "xtick.color": DRACULA["foreground"],
        "ytick.color": DRACULA["foreground"],
        "grid.color": DRACULA["current_line"],
        "grid.alpha": 0.6,
        "legend.facecolor": DRACULA["current_line"],
        "legend.edgecolor": DRACULA["foreground"],
        "legend.labelcolor": DRACULA["foreground"],
        "lines.color": DRACULA["purple"],
        "patch.edgecolor": DRACULA["foreground"],
        "boxplot.flierprops.markerfacecolor": DRACULA["red"],
    })

    try:
        import seaborn as sns
        sns.set_style("darkgrid")
        # Override seaborn defaults
        sns.set_palette(DEFAULT_PALETTE)
    except ImportError:
        pass


def is_valid_png(filepath: str) -> bool:
    """Check if a file is a valid PNG with reasonable size."""
    if not os.path.exists(filepath):
        print(f"  MISSING: {filepath}")
        return False

    size = os.path.getsize(filepath)
    if size < 1024:
        print(f"  TOO SMALL ({size} bytes): {filepath}")
        return False

    with open(filepath, "rb") as f:
        header = f.read(8)
        if header != b'\x89PNG\r\n\x1a\n':
            print(f"  NOT A PNG: {filepath}")
            return False

    # Quick size check with PIL if available
    try:
        from PIL import Image
        img = Image.open(filepath)
        w, h = img.size
        if w < 80 or h < 80:
            print(f"  TOO SMALL ({w}x{h}): {filepath}")
            return False
    except ImportError:
        pass

    return True


def check_images(paths: list[str]) -> dict:
    """Validate a list of image files. Returns summary dict."""
    results = {"ok": [], "failed": []}
    for path in paths:
        if is_valid_png(path):
            size_kb = os.path.getsize(path) / 1024
            print(f"  OK ({size_kb:.1f} KB): {path}")
            results["ok"].append(path)
        else:
            results["failed"].append(path)

    print(f"\nResults: {len(results['ok'])} valid, {len(results['failed'])} invalid")
    return results


def main():
    parser = argparse.ArgumentParser(description="Dracula-themed plot exporter")
    parser.add_argument("--check", nargs="+", metavar="IMAGE", help="Validate image files")
    parser.add_argument("--output-dir", default="images", help="Output directory")
    parser.add_argument("--dpi", type=int, default=150, help="DPI for generated images")
    args = parser.parse_args()

    if args.check:
        results = check_images(args.check)
        if results["failed"]:
            sys.exit(1)
    else:
        print("Use --check to validate images, or run a generator script directly.")
        print("Example: python3 .opencode/skills/export-plots/generate_cluster_plots.py")


if __name__ == "__main__":
    main()
