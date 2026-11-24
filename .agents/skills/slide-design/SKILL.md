---
name: slide-design
description: >-
  Design and refine Reveal.js teaching slides with intentional visual direction,
  pedagogical clarity, and Prof. Caio's illustrated presentation style. Use when
  creating new decks, planning slide layouts, choosing visual assets, or upgrading
  text-heavy/generic slides into visual-first teaching decks.
---

# Slide Design

Use this skill whenever designing or reviewing Reveal.js course decks in this repository. The goal is never decorative polish — it is **visual intuition**: every slide should let students *see* the mechanism, architecture, artifact, or tradeoff at a glance.

## Choose the Right Visual Register

Pick the register that fits the lesson before writing HTML:

1. **Illustrated Concept-Driven Style (Default for Inteligência Artificial & conceptual CS lessons)**
   Modeled on Prof. Caio's Google Slides (`2026IA - Aula 11 - Do VAE ao Stable Diffusion`).
   - **One visual hero per slide** (seminal paper figure, custom illustrated diagram/infographic, real plot/sample grid, or equation breakdown) paired with **0–3 short lines (≤35 words)**.
   - **Chronological, problem-driven arc**: *Limitation of method A → Key insight → Seminal paper B → Visual proof*.
   - **Progressive visual deconstruction**: walk through the *same* paper abstract, architecture diagram, or equation step by step using highlight overlays, arrows, and 1-line plain-Portuguese captions (`data-auto-animate` or `fragment`).
   - **IFSP green-striped section dividers**: open major lesson chapters with `<section-banner>` (`../img/fundo.png`).
   - **Contextual notebooks**: place `.colab-pill` notebook links directly below the slide where the concept lands.
   - Read [illustrated-style-guide.md](./references/illustrated-style-guide.md) for the exact layout recipes and HTML patterns.

2. **Artifact-Driven Operational Style (BDD, IoT, Ciência de Dados labs)**
   - Lead with **real artifacts**: actual SQL/Python code + executed output, file trees, query plans, real notebook plots (RevealD3 + Plotly), hardware/circuit photos, API responses.
   - Keep comparisons concrete and grounded in classroom datasets and real commands.

## Non-Negotiable Visual Rules

- **NO crude icon/CSS cartoons**: NEVER fake real scenes, objects, or scientific visuals with FontAwesome icons (`fa-car-side`, `fa-plane`), colored CSS circles/blobs, or raw `clip-path` shapes. Use real photos, cropped paper figures, Python/Matplotlib plots, clean technical SVGs, or AI-generated custom illustrations/infographics (see `visual-assets` skill).
- **NO generic card-grid spam**: Do NOT default to 3–4 column `artifact-card` walls or repetitive `pipeline-node` dark-box chains slide after slide. Use them sparingly only when comparing genuinely discrete operational items.
- **Sparsity over completeness**: Slides support a live spoken lecture — they are NOT a textbook chapter. Prefer 1 visual + 1–2 intuitive sentences over 6 dense bullet points.
- **White framing for light figures**: Place paper headers, cropped paper figures, white-background diagrams, and plots inside `.figure-card` or `<paper-card>` so they pop cleanly on Dracula (`#282a36`) with crisp contrast.
- **Fit the 960×700 logical canvas**: Never overflow vertically or horizontally, never overlap IFSP branding or controls, and keep dimensions stable across fragments.
- **Colorblind-safe accents**: Reserve `#ff5555` (red) for explicit errors/wrong answers. Prefer `#8be9fd` (cyan), `#f1fa8c` (yellow), `#ff79c6` (pink), `#50fa7b` (green), `#ffb86c` (orange), and `#bd93f9` (purple) with intentional hierarchy — do not rainbow-decorate every element.
- **Fragments serve teaching only**: Use fragments to reveal progressive highlights/arrows on a figure, break down a formula term-by-term, sync code highlighting, or stage exercise steps. Show static reference lists and section banners all at once.

## Pre-Delivery Visual Review

Before declaring any deck done:

1. Cover slide gives an immediate visual signal of the topic (real tool logos, iconic image, or concrete visual — not a generic 2-box Mermaid graph).
2. Major sections open cleanly (`<section-banner>` in IA/conceptual decks) with clear narrative transitions.
3. Complex architectures, papers, and formulas are unpacked progressively rather than dumped in a wall of text.
4. Zero crude FontAwesome/CSS-blob substitutes for real visuals.
5. Every image has concise pt-BR `alt` text, valid binary >1KB, and crisp attribution (`<p class="source">`).
6. Zero overflow on the 960×700 canvas (verify via `validate-slides` skill).
