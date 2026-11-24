---
name: create-slides
description: >-
  Create or refactor Reveal.js HTML slide decks for IFSP Campus Capivari courses
  (IA, BDD1, BDD2, Ciência de Dados, IoT). Use when asked to create a new lesson,
  build slides for a topic, or add sections to an existing deck.
---

# Create Slides

Generate complete, validated Reveal.js `.html` slide decks following this repository's static Vue 3 + Reveal.js 5.2.1 architecture.

## Required Companion Context

Before writing HTML:
1. Check the target course's `AGENTS.md` (e.g., `ia/AGENTS.md`, `bdd2/AGENTS.md`, `ciencia-dados/AGENTS.md`, `iot/AGENTS.md`).
2. Load `slide-design` (and for IA/conceptual decks, read `slide-design/references/illustrated-style-guide.md`).
3. Use `visual-assets` for real paper figures, custom illustrations, plots, or extracted images.
4. Consult [references/components-and-patterns.md](./references/components-and-patterns.md) for Vue components and layout recipes, and [references/gotchas.md](./references/gotchas.md) for framework pitfalls.

Ask for course name, lesson number, and topic only if missing and not inferable from context.

## File Placement

- Decks: `<course>/aulaNN-<slug>.html` (`ia/`, `bdd1/`, `bdd2/`, `ciencia-dados/`, `iot/`)
- Lesson images: `<course>/images/aulaNN/` (or `bdd2/planos/aulaNN_<slug>_assets/` in `bdd2/`)
- Standalone RevealD3 Plotly charts: `<course>/aulas/<plot-name>.html`

## Exact HTML Boilerplate

```html
<!DOCTYPE html>
<html lang="pt-BR">

<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />

  <title>{CURSO} - {TITULO}</title>

  <link rel="stylesheet" href="../dist/reset.css" />
  <link rel="stylesheet" href="../dist/reveal.css" />
  <link rel="stylesheet" href="../dist/theme/dracula.css" />
  <link rel="stylesheet" href="../dist/custom.css" />
  <link rel="stylesheet" href="../dist/highlight/dracula.css" />
  <link rel="stylesheet" href="../plugin/poll/style.css" />
  <link rel="stylesheet" href="../plugin/customcontrols/style.css" />
  <link rel="stylesheet" href="../plugin/chalkboard/style.css" />
</head>

<body>

  <div id="app" class="reveal">
    <div class="slides">

      <!-- SLIDE 1: Capa (4-space indentation inside <div class="slides">) -->
      <section data-auto-animate>
        <header1 aula="{NUM}" curso="{CURSO}" title-size="24" title="{TITULO}">
          <!-- Iconic local visual / tool logos -->
        </header1>
      </section>

    </div>
  </div>

  <script src="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/js/all.min.js"></script>
  <script src="../dist/reveal.js"></script>
  <script src="../plugin/notes/notes.js"></script>
  <script src="../plugin/math/math.js"></script>
  <script src="../plugin/markdown/markdown.js"></script>
  <script src="../plugin/highlight/highlight.js"></script>
  <script src="../plugin/zoom/zoom.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/reveal.js-mermaid-plugin@11.6.0/plugin/mermaid/mermaid.js"></script>
  <script src="../plugin/leader-line.min.js"></script>
  <script src="../dist/vue.js"></script>
  <script src="../slides_template/header1.js"></script>
  <script src="../components/components.js"></script>
  <!-- Local plugins (NEVER CDN for chalkboard) -->
  <script src="../plugin/poll/plugin.js"></script>
  <script src="../plugin/customcontrols/plugin.js"></script>
  <script src="../plugin/chalkboard/plugin.js"></script>
  <!-- socket.io BEFORE init.js; seminar AFTER init.js -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.7.5/socket.io.min.js"></script>
  <script src="../slides_template/init.js"></script>
  <script src="../plugin/seminar/plugin.js"></script>

  <script>
    window.app = mountSlideApp();
  </script>

</body>
</html>
```

Include `<script src="../plugin/reveald3/reveald3.js"></script>` before `init.js` only when the deck uses `<reveald3-plot>`.

## Structural Rules

1. **4-space indentation** for all HTML inside `<div class="slides">`.
2. **`mountSlideApp()` as a regular `<script>`** (never `type="module"`).
3. **Super sections for major chapters**: wrap each major topic in a parent `<section>` with balanced comment markers:
   ```html
      <!-- ============================================================
         Etapa N: {NOME DA ETAPA}
         ============================================================ -->
      <section>

        <section data-auto-animate>
          <section-banner eyebrow="Etapa N" title="{TÍTULO}" subtitle="{SUBTÍTULO}"></section-banner>
        </section>

        <!-- slides da etapa -->

      </section><!-- fim Etapa N -->
   ```
   Cover, standalone review/quiz, summary, and references stay at top level (siblings of super sections, never nested inside them).
4. **Language & audience**: Brazilian Portuguese (`pt-BR`), direct to students. English technical terms are fine. Never write Chinese/CJK characters. Never include teacher meta-commentary or internal environment/tool names (`micromamba`, `opencode`, etc.).
5. **Code blocks**: Put ordinary code as raw text directly inside `<code-block lang="...">`. Use `<textarea>` ONLY when the code contains `<` or `>` that the HTML parser would mangle (e.g., `#include <Arduino.h>`). **NEVER** put `<script>` inside `<code-block>`.
6. **LeaderLine**: Always use explicit closing tags (`<leader-line ...></leader-line>`) and **kebab-case** props (`start-socket`, `end-socket`, `middle-label`, `start-plug`, `end-plug`).
7. **Fragments sparingly**: Use `<ls-u>` only for motivation, exercise steps, or final recap. Use plain `<ul>` for definitions/reference lists. Do NOT fragment section divider slides.
8. **Images**: Every `<img>` needs concise pt-BR `alt` text, either `width` OR `height` (not both), valid local binary >1KB (or verified HTTP 200), and attribution (`<p class="source">Fonte: ...</p>`).

## Mandatory QA Gate

After creating or editing any deck, run the `validate-slides` skill:
1. Static check:
   ```bash
   python3 .agents/skills/validate-slides/scripts/validate_slide_deck.py <deck.html>
   ```
   Must exit with **0 errors**.
2. Browser overflow check (canvas 960×700) using `.agents/skills/validate-slides/scripts/check_overflow.js` on a local server (`python3 -m http.server 8000`). Confirm `over: []`, zero broken images, and clean console.
3. Verify external links return HTTP 200.
