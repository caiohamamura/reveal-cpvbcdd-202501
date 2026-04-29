---
name: reveal-slides
description: Generate educational slides using reveal.js with Vue components, Dracula theme, and rich visual elements. Use when creating lecture slides, class presentations, or any HTML-based slide deck. Triggers on "criar slides", "gerar slides", "slides de aula", "apresentação", "reveal.js".
---

# Reveal.js Slides Generator — CPVBCDD Framework

Generate complete, ready-to-present HTML slide decks using the CPVBCDD Reveal.js framework with Vue components.

## References

- **Template completo:** `references/template.md`
- **Boilerplate correto:** `references/boilerplate.md`
- **Exemplo de aula antiga:** Repo `reveal-cpvbcdd-202501/bdd2/materialized_views.html`

## ⚠️ CRITICAL ISSUES (from Caio's feedback)

The previous slides had 10 major problems. This skill MUST produce slides without these issues:

1. ❌ Missing `<header1>` cover slide → ✅ MUST use `<header1>` component
2. ❌ Missing `init.js` and `mountSlideApp()` → ✅ MUST include `init.js` and call `mountSlideApp()`
3. ❌ Missing `.fragment.auto` handler → ✅ Handled by `init.js` automatically
4. ❌ No `<code-block>` used → ✅ MUST use for all code; wrap content in `<textarea>` when it contains `<` or `>`
5. ❌ No `<multi-col>` used → ✅ MUST use for two-column layouts
6. ❌ No `<ls-u>` used → ✅ MUST use for bulleted lists
7. ❌ No super sections → ✅ MUST wrap each topic in parent `<section>`
8. ❌ Missing `custom.css` link → ✅ MUST include in `<head>`
9. ❌ Missing `data-auto-animate` → ✅ MUST add to sections
10. ❌ Section dividers wrong → ✅ MUST use section headers inside super sections

## Output Directory

Slides must be saved in the reveal-cpvbcdd repository:

```
/home/openclaw/.openclaw/workspace/reveal-cpvbcdd-202501/
├── bdd1/        ← Banco de Dados 1
├── bdd2/        ← Banco de Dados 2
└── iot/         ← IoT
```

After creating slides, always commit and push:
```bash
cd /home/openclaw/.openclaw/workspace/reveal-cpvbcdd-202501
git add .
git commit -m "feat: <descricao>"
git push
```

## HTML Boilerplate (EXACT — copy from references/template.md)

Every slide file MUST have this exact structure:

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
  <link rel="stylesheet" href="../plugin/highlight/monokai.css" />
</head>

<body>

  <div id="app" class="reveal">
    <div class="slides">

      <!-- SLIDES HERE (4-space indentation inside <div class="slides">) -->

    </div>
  </div>

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
  <script src="../components/md.js"></script>
  <script src="../components/components.js"></script>
  <script src="../slides_template/init.js"></script>

  <script>
    window.app = mountSlideApp();
  </script>

</body>

</html>
```

**CRITICAL: The `init.js` script and `mountSlideApp()` call are required in EVERY slide file. `init.js` handles:**
1. Creating a Vue app and mounting it on `#app`
2. Registering all custom components via `initializeComponents(app)` and `initializeHeader(app)`
3. Initializing Reveal.js with all plugins
4. Handling `.fragment.auto` elements that auto-advance on slide change

## Slide Structure Patterns

### Indentation
ALL content inside `<div class="slides">` uses **4-space indentation**. Each nested level adds 4 spaces.

### Cover Slide (always first)
```html
      <!-- SLIDE 1: Capa -->
      <section data-auto-animate>
        <header1 aula="{NUM}" curso="{CURSO}" title-size="24"
                 title="{TITULO COMPLETO}">
          <!-- Optional: mermaid diagram or image as slot content -->
        </header1>
      </section>
```

### Super Sections (REQUIRED for every major topic)
Wrap each major topic/phase in a parent `<section>` element:

```html
      <!-- ============================================================
         SEÇÃO: {NOME DA SEÇÃO}
         ============================================================ -->
      <section>

        <!-- SLIDE: Seção header -->
        <section data-auto-animate>
          <h2 style="color: #8be9fd;">Seção: {TÍTULO}</h2>
          <!-- intro content for this section -->
        </section>

        <!-- More slides in this section... -->

      </section><!-- fim {NOME} -->
```

Rules:
- Cover slide stays OUTSIDE super sections (top-level)
- Each major topic gets its own super section
- First slide inside super section should be a header/intro slide
- Close with `<!-- fim {NOME} -->` comment

### Code Slide (USE code-block)
```html
      <section data-auto-animate>
        <h2>{TITULO}</h2>
        <!-- Use <textarea> when code contains < or > characters -->
        <code-block lang="sql" data-trim>
        <textarea>SELECT * FROM orders;</textarea>
        </code-block>
      </section>
```

### Two-Column Layout (USE multi-col)
```html
      <section data-auto-animate>
        <h2>{TITULO}</h2>
        <multi-col style="gap:15px">
          <div style="flex: 1;">
            <ul>
              <li>Point 1</li>
              <li>Point 2</li>
            </ul>
          </div>
          <div style="flex: 1; text-align: center;">
            <img src="{URL}" alt="{ALT TEXT}" />
          </div>
        </multi-col>
      </section>
```

### Bulleted List (USE ls-u for progressive reveal, ul for static)
```html
      <ls-u font-size="22pt">
        <li>Item 1</li>
        <li>Item 2</li>
      </ls-u>
```

### Mermaid Diagram
```html
      <section data-auto-animate>
        <h2>{TITULO}</h2>
        <div class="mermaid" data-id="{unique-id}">
          <pre>
graph TD
  A["Label A"] -->|"edge label"| B["Label B"]
  style A fill:#44475a,color:#f8f8f2
  style B fill:#ff5555,color:#f8f8f2
          </pre>
        </div>
      </section>
```

### Table with Copy Button
```html
      <section data-auto-animate>
        <h2>{TITULO}</h2>
        <table>
          <thead>
            <tr><th>Col 1</th><th>Col 2</th></tr>
          </thead>
          <tbody>
            <tr><td>Val 1</td><td>Val 2</td></tr>
          </tbody>
        </table>
        <copy-btn></copy-btn>
      </section>
```

## Available Vue Components

| Component | Usage | When to Use |
|-----------|-------|-------------|
| `<header1>` | Cover slide | Always first slide |
| `<code-block>` | Code with copy | All code examples |
| `<multi-col>` | Two-column layouts | Concept + image, code + explanation |
| `<ls-u>` | Bulleted lists with animation | Exercise steps, summary, recap only |
| `<ul>` | Static bulleted lists | Definitions, "when to use", info lists |
| `<copy-btn>` | Copy button for tables | After any `<table>` |
| `<md>` | Markdown rendering | For markdown content |
| `<leader-line>` | Arrow between elements | With `from` and `to` IDs |

## Critical Rules

1. **ALWAYS use `<header1>` for title slide** — not plain h2 + p
2. **ALWAYS include `custom.css`** in head
3. **ALWAYS call `initializeComponents(app)` and `initializeHeader(app)`** before mounting
4. **ALWAYS handle `.fragment.auto`** in slidechanged event
5. **ALWAYS use `<code-block>`** for code — not raw `<pre><code>`
6. **ALWAYS use `<multi-col>`** for two-column layouts — not raw flex divs
7. **ALWAYS wrap each major topic in a super section** with header child
8. **ALWAYS use `data-auto-animate` on sections** for smooth transitions

## Dracula Color Palette

- `#282a36` — Background (dark)
- `#44475a` — Secondary background (cards, boxes)
- `#6272a4` — Muted text, borders
- `#f8f8f2` — Primary text
- `#ff5555` — Red (errors, warnings)
- `#ffb86c` — Orange (accent)
- `#50fa7b` — Green (success, positive)
- `#bd93f9` — Purple (highlights)
- `#ff79c6` — Pink (important notes)
- `#8be9fd` — Cyan (neutral info)

## Code Block with Synchronized Line Highlighting

For code explanations that need to highlight specific lines in sync with a list:

### Structure: Two-column layout (code + list)

```html
<section data-auto-animate>
  <h2>{TITLE}</h2>
  <multi-col style="gap: 30px;">
    <div style="flex: 1;">
      <code-block lang="r" data-line-numbers="FIRST-LINES|STEP1|STEP2|STEP3|STEP4" data-fragment-index="1">
# Complete code here - all lines visible initially
code_line_1
code_line_2
code_line_3
...      </code-block>
    </div>
    <div style="flex: 1;">
      <ol>
        <li class="fragment" data-fragment-index="1">Step 1 description</li>
        <li class="fragment" data-fragment-index="2">Step 2 description</li>
        <li class="fragment" data-fragment-index="3">Step 3 description</li>
        <li class="fragment" data-fragment-index="4">Step 4 description</li>
      </ol>
    </div>
  </multi-col>
</section>
```

### data-line-numbers format:
- **Format**: `"all-lines|F1|F2|F3|F4"` where F1-F4 are the lines highlighted for each fragment
- **First value**: ALL lines shown when slide loads (no fragment active yet)
- **Subsequent values**: Lines highlighted when corresponding fragment index is active
- **Separator**: Pipe `|` between values

### Example for 14-line code:
```html
data-line-numbers="1-14|2|5|8-11|14"
```
- `1-14` = All 14 lines shown initially (active by default)
- `2` = When fragment 1 shows, highlight line 2
- `5` = When fragment 2 shows, highlight line 5
- `8-11` = When fragment 3 shows, highlight lines 8-11
- `14` = When fragment 4 shows, highlight line 14

### data-fragment-index rules:
- **Start at 1** (not 0) — fragment 0 is the initial state (all lines)
- List items use `<ol>` (ordered) with `<li class="fragment" data-fragment-index="N">`
- Index N corresponds to the Nth value after the first in data-line-numbers

### IMPORTANT:
- **Code stays in ONE code-block** — never split into multiple code-blocks
- **Use `<ol>` not `<ul>`** for numbered steps
- **First data-line-numbers value is always active** — no fragment-index="0"
- **Max 80 characters per line** of code

---

## Fragment Guidelines

**Use fragments SPARINGLY. Only when:**
1. Introducing concepts step-by-step
2. Code explanation synced with line numbers
3. Exercise steps (revealing requirements one at a time)

**Do NOT use fragments for:**
- Results/output of code examples
- Informational lists (definitions, "when to use")
- Concept definition slides

**ls-u vs ul decision:**
- `<ls-u>` ONLY for: motivation intro, exercise steps, final summary/recap
- Plain `<ul>` for: definitions, "when to use", informational bullet points

## After Creating Slides

1. Copy to both locations:
   - Repo: `reveal-cpvbcdd-202501/{bdd1,bdd2,iot}/`
   - Lesson dir: `bdd2/aulas/{date}-{slug}/slides/aula-slides-final.html`
2. Commit and push to repo
3. Report completion to user with summary of what was created