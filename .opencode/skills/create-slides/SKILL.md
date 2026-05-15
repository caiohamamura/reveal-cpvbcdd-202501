---
name: create-slides
description: Create Reveal.js slide files for the CPVBCDD educational framework (IoT, BDD1, BDD2 courses)
---

Create a new Reveal.js slide file for the CPVBCDD educational framework.

## Trigger
When the user asks to create slides, a new lesson, a new presentation, or says "create slides for..." / "nova aula..." / "slides para..."

## Instructions

You will be given a topic and course context. Generate a complete `.html` slide file following the patterns below exactly. Ask the user for: course name, lesson number, and topic if not provided.

> **Fonte de consulta:** Consulte `docs/ECOSSISTEMA.md` para documentação completa do ecossistema — componentes Vue (`<header1>`, `<code-block>`, `<multi-col>`, `<ls-u>`, `<md>`, `<poll-question>`, `<leader-line>`, `<copy-btn>`), plugins (chalkboard, chart, poll, seminar, customcontrols), convenções CSS (classes utilitárias, paleta Dracula, estilos de `<h2>`/`<h3>`/`<h4>`/`<li>`), arquitetura do projeto, e padrões de inicialização Vue + Reveal.js.

### File location
Place files in the appropriate subfolder: `iot/`, `bdd1/`, `bdd2/`, or a new folder as instructed.

### HTML Boilerplate (EXACT structure)

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
  <!-- Optional plugins -->
  <link rel="stylesheet" href="../plugin/poll/style.css" />
  <link rel="stylesheet" href="../plugin/customcontrols/style.css" />
  <link rel="stylesheet" href="../plugin/chalkboard/style.css" />
</head>

<body>

  <div id="app" class="reveal">
    <div class="slides">

      <!-- SLIDES HERE (4-space indentation inside <div class="slides">) -->

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
  <!-- Plugin scripts (local — NOT CDN) -->
  <script src="../plugin/poll/plugin.js"></script>
  <script src="../plugin/customcontrols/plugin.js"></script>
  <script src="../plugin/chalkboard/plugin.js"></script>
  <!-- socket.io required by seminar plugin — must load before init.js -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.7.5/socket.io.min.js"></script>
  <script src="../slides_template/init.js"></script>
  <script src="../plugin/seminar/plugin.js"></script>

  <script>
    window.app = mountSlideApp();
  </script>

</body>
</html>
```

Theme: use `dracula.css` for all courses (IoT, BDD, Ciência de Dados).

**CRITICAL: Use `mountSlideApp()` from `slides_template/init.js` loaded as a regular script.** This:
1. Sets default configs for chalkboard, customcontrols, poll, and seminar
2. Injects the seminar connect panel into `<body>` (host button + status display)
3. Sets `window.seminarConfig` automatically (server is shared, room defaults to `location.pathname`)
4. To override the room, set `window.seminarConfig = { room: 'my-room' }` BEFORE the `<script src="../slides_template/init.js">` tag
5. Creates the Vue app, registers components, initializes Reveal.js with all auto-detected plugins
6. Load init.js as a **regular `<script>` tag** (NOT `<script type="module">`) — init.js defines `mountSlideApp()` as a global function
7. Must include `socket.io` (CDN) **before** `init.js` and `seminar/plugin.js` **after** `init.js` for seminar to work
8. Call `window.app = mountSlideApp();` in a regular `<script>` block after all plugins are loaded

### Slide Structure Patterns

#### Indentation
ALL content inside `<div class="slides">` uses **4-space indentation**. Each nested level adds 4 spaces. This is critical.

#### Cover Slide (always first)
```html
      <!-- SLIDE 1: Capa -->
      <section data-auto-animate>
        <header1 aula="{NUM}" curso="{CURSO}" title-size="24"
                 title="{TITULO COMPLETO}">
          <!-- Optional: mermaid diagram or image as slot content -->
          <div class="mermaid" data-id="cover-diagram" style="width:450px">
            <pre>
graph LR
  A["Node A"] --> B["Node B"]
            </pre>
          </div>
        </header1>
      </section>
```

#### Super Sections (REQUIRED for every major topic)
Wrap each major topic/phase in a parent `<section>` element. This groups related slides into logical sections visible in the slide overview and enables vertical navigation. Always include a header slide as the first child.

```html
      <!-- ============================================================
         FASE N: {NOME DA SEÇÃO}
         ============================================================ -->
      <section>

        <!-- SLIDE: Fase N header -->
        <section data-auto-animate>
          <h2 style="color: #8be9fd;">Fase N: {TÍTULO}</h2>
          <!-- intro content for this section -->
        </section>

        <!-- More slides in this section... -->

      </section><!-- fim Fase N -->
```

Rules:
- Cover slide and review slides stay OUTSIDE super sections (top-level)
- Each major topic (e.g. "Pipeline Completo", "Random Forest", "Ética") gets its own super section
- The first slide inside a super section should be a header/intro slide with a colored h2
- Close with `<!-- fim {NOME} -->` comment for clarity
- Comment dividers (`<!-- ============ -->`) go BEFORE the opening `<section>` tag, not inside

#### Review slide (when continuing a course)
```html
      <!-- SLIDE: Revisão -->
      <section data-auto-animate data-background-image="https://i.imgur.com/A62GI4n.png" data-background-opacity="0.3">
        <h2>Revisão: Aula Passada</h2>
        <ls-u>
          <li>Topic 1</li>
          <li>Topic 2</li>
          <li>Topic 3</li>
        </ls-u>
      </section>
```

#### Concept + Image (two-column)
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
            <img src="{URL}" alt="{CONCISE ALT TEXT}" />
          </div>
        </multi-col>
      </section>
```

#### Code Slide
```html
      <section data-auto-animate>
        <h2>{TITULO}</h2>
        <code-block lang="{lang}" data-trim><script type="text/plain">
{CODE HERE - raw code, angle brackets preserved}
</script></code-block>
      </section>
```
- Use `lang="sql"` for SQL, `lang="cpp"` or `lang="c"` for Arduino/C++, `lang="python"` for Python, `lang="r"` for R
- **ALWAYS** wrap code content in `<script type="text/plain">` — this prevents the browser's HTML parser from mangling angle brackets (e.g. `#include <Arduino.h>` would become `#include <arduino.h>` without it)
- The `<script type="text/plain">` is invisible to the browser and acts as a raw text container

#### Challenge / "Desafio" slide
```html
      <section data-auto-animate>
        <h2>{TITULO} 🔋</h2>
        <multi-col style="gap:15px">
          <div id="element1" style="flex:1;">
            <ls-u>
              <li>Data point 1</li>
              <li>Data point 2</li>
            </ls-u>
          </div>
          <div id="element2" class="fragment" style="flex:1; text-align:center;">
            <!-- diagram or visual -->
          </div>
        </multi-col>
        <div class="fragment" style="text-align: center; margin-top: 15px;">
          <p style="font-size: 26pt; color: #ff79c6;">Provocative question?</p>
        </div>
      </section>
```

#### Practical Exercise slide
```html
      <section data-auto-animate>
        <h2>Exercício Prático</h2>
        <div style="background: #282a36; border-left: 4px solid #50fa7b; padding: 20px;">
          <p><strong>Objetivo:</strong> {DESCRICAO}</p>
          <ls-u>
            <li>Step 1</li>
            <li>Step 2</li>
          </ls-u>
        </div>
        <div>
          <code-block lang="sql"><script type="text/plain">
CREATE OR REPLACE FUNCTION nome_funcao(
    -- parâmetros
) RETURNS tipo AS $$
BEGIN
    -- sua lógica aqui
END;
$$ LANGUAGE plpgsql;
</script></code-block>
        </div>
      </section>
```
- Exercise slides should include a **starter code template** with `-- sua lógica aqui` placeholder
- Templates show only the bare structure (`CREATE ... AS $$ BEGIN END; $$ LANGUAGE plpgsql`), NOT parameter names or types
- Use `ls-u` for exercise steps (progressive reveal of requirements)

#### Mermaid diagram slide
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
- Always use `data-id` on mermaid divs with unique values
- Graph content indented with **0 spaces** inside the `<pre>` (mermaid is whitespace-sensitive)

#### Table slide
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

#### Closing / Summary slide
```html
      <!-- SLIDE: Encerramento -->
      <section data-auto-animate>
        <h2>Resumo da Aula</h2>
        <ls-u>
          <li>Topic covered 1</li>
          <li>Topic covered 2</li>
        </ls-u>
        <div class="fragment" style="text-align: center; margin-top: 20px;">
          <p style="font-size: 22pt;">Próxima aula: <strong>{TOPICO PROXIMA AULA}</strong></p>
        </div>
      </section>
```

### Available Vue Components

| Component | Usage | Notes |
|-----------|-------|-------|
| `<header1>` | Cover slide only | Props: `aula`, `curso`, `title`, `title-size` |
| `<multi-col>` | Two-column layouts | Prop: `cols` (default 2), use `style="gap:15px"` |
| `<ls-u>` | Bulleted lists | Each `<li>` becomes a `fragment fade-in-then-semi-out` automatically |
| `<code-block>` | Code with copy button | Raw code in slot, use `lang=""` attr |
| `<code-inline>` | Inline code | Props: `lang`, `size` |
| `<highlight-box>` | Callout boxes | Prop: `index` (fragment index) |
| `<copy-btn>` | Copy button for tables | Place after `<table>` |
| `<md>` | Markdown rendering | Prop: `md` (markdown string) |
| `<leader-line>` | Arrow between elements | **Must use explicit close `</leader-line>`** |
| `<poll-question>` | Interactive poll (live voting) | Wrap in `<section>` parent, each question is a child slide |
| `<md>` | Markdown rendering | Prop: `md` (markdown string) |

### Poll Questions — `poll-question` Pattern

Each question is a **separate slide** wrapped in a parent `<section>`:

```html
<section>
  <!-- SLIDE: Instructions (shown first) -->
  <section>
    <h2>Quiz Interativo</h2>
    <p>Conecte-se à sala e vote!</p>
  </section>

  <!-- SLIDE: Question 1 -->
  <section>
    <poll-question
      id="q1"
      title="Questão 1: Data Leakage"
      question="Se você escala TODOS os dados ANTES do split, qual problema pode ocorrer?"
      answer="b"
      answer-text="Escalar antes do split causa data leakage!"
      :options="[
        { value: 'a', label: 'O modelo treina mais rápido' },
        { value: 'b', label: 'Data leakage — info do teste vaza para treino' },
        { value: 'c', label: 'Accuracy melhora automaticamente' },
      ]" />
  </section>

  <!-- SLIDE: Question 2 -->
  <section>
    <poll-question
      id="q2"
      title="Questão 2: AUC"
      question="Um modelo tem AUC = 0.45. O que isso significa?"
      answer="c"
      answer-text="AUC < 0.5 significa previsões invertidas!"
      :options="[
        { value: 'a', label: 'Modelo excelente' },
        { value: 'b', label: 'Modelo razoável' },
        { value: 'c', label: 'Pior que aleatório — inverteu as previsões!' },
        { value: 'd', label: 'Modelo perfeito!' },
      ]" />
  </section>
</section>
```

**Props:** `id` (unique identifier), `title` (e.g. "Questão 1: Topic"), `question` (the question text), `answer` (correct value, e.g. `"b"`), `answer-text` (explanation shown after answering), `:options` (array of `{value, label}` — **must use `:options` binding**).

**Note:** Poll server is shared with seminar (`https://seminar.hamacorps.work/`). `mountSlideApp()` already sets `window.pollConfig = {}` — no additional config needed.

### Styling Conventions (from custom.css and user's manual edits)

- `<h2>` titles: `42pt`, Impact font, left-aligned
- `<h3>`: `32pt`, color `#359830`, green with white text-shadow
- `<h4>`: `24pt`, `margin: 10px 0`
- Body text, `<li>`: `22pt`, left-aligned, `margin: 5px 40px`
- Code font size: default `20pt` (overridable via `size` prop)
- All text is LEFT-aligned (not centered)
- Dracula color palette accents: `#ff79c6` (pink), `#8be9fd` (cyan), `#ff5555` (red), `#50fa7b` (green), `#f1fa8c` (yellow), `#44475a` (dark bg), `#6272a4` (muted)
- Use inline `style=""` for one-off styling, not CSS classes
- Background images: `data-background-image="..." data-background-opacity="0.3"`
- Emojis are welcome in slide content (titles, diagrams, emphasis)

### Fragment Patterns

**Use fragments SPARINGLY.** Only add fragments when:

1. **Introducing new concepts step-by-step** — e.g., first bullet appears, then next concept builds on it
2. **Code explanation synced with highlighting** — `data-fragment-index` paired with `data-line-numbers` to walk through code line by line
3. **Exercise steps** — revealing task requirements one at a time

**Do NOT use fragments for:**
- Results/output of code examples (show immediately)
- Informational lists (definitions, "when to use" bullet points)
- "Quando usar X?" slides — these are reference lists, show all at once
- Concept definition slides (e.g., "O que são Procedures?") — show all bullets at once

**ls-u vs ul decision:**
- Use `<ls-u>` (auto-fragmenting) ONLY for: motivation intro slides, exercise step slides, final summary/recap
- Use plain `<ul>` for: definitions, "when to use" lists, informational bullet points, comparison lists
- When in doubt, use `<ul>` — fragments should be the exception, not the default

Technical details:
- `<ls-u>` auto-fragments each `<li>` with `fade-in-then-semi-out`
- Use `data-fragment-index="N"` to control ordering when syncing with code highlighting
- `<leader-line class="fragment">` makes arrow appear as a fragment step
- `data-auto-animate` on `<section>` for smooth transitions between slides with same elements

### Image Rules
- ALL `<img>` tags MUST have concise `alt` text describing the image content
- Use `width` or `height` to constrain size, not both
- Center images with parent `style="text-align: center"` or `<center>`

### Content Flow (per lesson)
1. **Cover** — `<header1>` with title, course, lesson number
2. **Review** — Quick recap of previous lesson (if applicable)
3. **Motivation** — Why this topic matters, real-world scenario
4. **Concept sections** — 2-5 slides per concept, with code + explanation
5. **Practical exercise** — Hands-on task
6. **Summary**

### Language
- All slides content in **Portuguese (Brazilian)** NEVER write Chinese letters!
- Technical terms can stay in English (WiFi, Deep Sleep, MQTT, ...)
- Code comments in pt-BR


### Gotchas & Tips

#### Mermaid syntax
- **Edge labels: do NOT use inner quotes.** Use `|text|`, NOT `|"text"|`. Inner quotes break rendering.
- Mermaid is whitespace-sensitive — graph content inside `<pre>` should have **0 spaces** of indentation.
- Node labels with emojis and accents (e.g. `["🤖 Bot"]`) are fine.

#### Code blocks with angle brackets
- **Always** use `<script type="text/plain">` (not `<textarea>`) to wrap code in `<code-block>`.
- This prevents the HTML parser from interpreting `#include <Arduino.h>` as an HTML tag and mangling it.

#### HTML section nesting (Reveal.js)
- Reveal.js uses nested `<section>` elements for vertical navigation. A misplaced closing `</section>` can cause slides to be nested incorrectly, making them invisible or out of order.
- Use comment markers like `<!-- fim Fase N -->` to track section boundaries.
- Quiz/references sections must be siblings of other super-sections, NOT nested inside them.

#### mountSlideApp() override pattern (per-slide Vue reactive state)
When a slide needs its own Vue reactive data (e.g. interactive demos, Plotly charts), override `mountSlideApp()` before calling it:

```js
const _originalMount = mountSlideApp;
mountSlideApp = function () {
    const app = _originalMount();
    // Add reactive state on the app instance
    app.config.globalProperties.myState = Vue.reactive({ counter: 0 });
    return app;
};
window.app = mountSlideApp();
```

#### npm registry blocks webfetch
- `npmjs.com` URLs return **403 Forbidden** to `webfetch`. Use GitHub repository pages, `winget.run`, or `github.com/search?q=<package>` instead for package research.

#### Researching tool deprecation status
- Always check deprecation/EOL status before mentioning tools in slides. MongoDB Atlas Data API was deprecated (End-of-Life) and should not be recommended to students. Verify via official docs release notes.

#### Using MDI icons for section headers
- `https://cdn.jsdelivr.net/npm/@mdi/svg@latest/svg/<icon>.svg` is a reliable source for Material Design Icons on jsDelivr CDN. Good for section header illustrations when Wikimedia Commons doesn't have relevant images.

#### Package compatibility in comparisons
- When comparing ecosystems (e.g., PostgreSQL vs MongoDB), verify that tools actually support the target database in their current version. Strapi v4+ dropped MongoDB support — a fact that invalidates comparisons using older docs.

This is cleaner than creating a separate Vue app, using globalProperties globally, or building a scoped component — the data lives only in the app instance that drives that specific slide deck.

#### PlotlyFigure component
- A global `plotlyFigureComponent` is available in `components/components.js` for rendering Plotly.js charts inside slides.
- It includes a Plotly guard (`typeof Plotly === 'undefined'`) so decks without the Plotly CDN don't break.
- For interactive demos (e.g. K-Means), combine with the `mountSlideApp()` override pattern and `window.deck` (the Reveal instance) for fragment-synced step-by-step visualization.
- When using fragment sync, scope your check (e.g. `.my-step-class`) to avoid responding to ALL fragments in the deck.

#### Plotly 6.x API changes
- `colorbar.titlefont` is **removed** — use `colorbar=dict(title=dict(text='...', font=dict(color='...')))` instead
- `symbol='x'` still works for marker symbols
- When exporting Plotly JSON from Python (`fig.to_dict()`), clean `None` values before embedding in JS — they cause issues

#### Notebook → Slides Plotly pipeline
1. Generate Plotly figures in Jupyter notebook
2. Export as JSON: `json.dump(fig.to_dict(), f)`
3. Convert to JS constants: `const PLOT_NAME_TRACES = [...]; const PLOT_NAME_LAYOUT = {...};`
4. Load in slide HTML: `<script src="images/plotly/plot_name.js"></script>`
5. **CRITICAL:** Vue 3 does NOT resolve bare `window` globals in templates. You MUST either:
   - **Option A (simple — static charts only):** Intercept `Vue.createApp` to inject constants as `globalProperties`:
     ```js
     var _createApp = Vue.createApp;
     Vue.createApp = function(opts) {
       var app = _createApp(opts);
       Object.assign(app.config.globalProperties, { PLOT_NAME_TRACES, PLOT_NAME_LAYOUT });
       return app;
     };
     window.app = mountSlideApp();
     Vue.createApp = _createApp;
     ```
   - **Option B (required for interactive charts):** Replace `mountSlideApp()` entirely with a custom app that includes both static constants AND reactive state in `setup()`:
     ```js
     var kmeansState = Vue.reactive({ step: 0 });
     injectSeminarPanel();
     var app = Vue.createApp({
       setup() {
         var kmTraces = Vue.computed(() => buildTraces(kmeansState.step));
         var kmLayout = Vue.computed(() => ({ /* ... */ }));
         Vue.onMounted(() => {
           initializeReveal();
           window.deck.on('fragmentshown', (e) => {
             if (e.fragment.classList.contains('kmeans-step'))
               kmeansState.step = +e.fragment.dataset.fragmentIndex + 1;
           });
         });
         return { kmTraces, kmLayout, PLOT_NAME_TRACES, PLOT_NAME_LAYOUT, /* all statics */ };
       }
     });
     initializeComponents(app); initializeHeader(app); app.mount('#app');
     ```
6. Reference in `<plotly-figure>`: `:traces="PLOT_NAME_TRACES" :layout="PLOT_NAME_LAYOUT"`

#### Interactive Plotly with Vue reactivity
For step-by-step demos (K-Means, etc.), you MUST use Vue reactivity — raw DOM approaches fail:
1. Create `Vue.reactive({ step: 0 })` outside the app for shared mutable state
2. Use `Vue.computed()` to derive traces from reactive state
3. Use `<plotly-figure :traces="computedTraces" :layout="computedLayout">` component
4. Use visible fragments with descriptive labels (NOT empty invisible divs): `<div class="fragment fade-in-then-out kmeans-step" data-fragment-index="N">`
5. Do NOT add a separate `<p id="step-label">` — the fragment labels already show one at a time via `fade-in-then-out`. A duplicate label creates visual clutter and goes out of sync.
6. Listen to `window.deck.on('fragmentshown'/'fragmenthidden')` scoped by class name
7. **NEVER use `Plotly.animate()`** — it silently ignores new traces. **NEVER use raw DOM** — empty fragment divs don't fire events reliably.
8. Color centroid markers to match their cluster colors (e.g. `['#8be9fd', '#ff79c6']`) so students can visually track which centroid owns which group. Use red `#ff5555` for both before any assignment happens.

#### `multi-col` grid overflow with long inline content
- `<multi-col>` uses CSS `gridTemplateColumns`. Even with `cols="1fr 1fr"`, columns can expand past slide boundaries if child elements contain unbreakable inline text (e.g., long URLs in `<span class="mini-code">` or `<code>`).
- **Fix**: Add `word-break: break-all` or `overflow-wrap: break-word` to the inline element's CSS class. Without this, the grid cell grows to fit the unbreakable text and pushes the other column off-screen.

#### Background-image opacity on dark themes
- For `data-background-image` logos on Dracula dark backgrounds (`#282a36`), start opacity at **0.20–0.25**, not below 0.10. Blue logos especially (#0078d4) need higher opacity to contrast against dark backgrounds.
- Position via `data-background-position="top 160px right 70px"` to place it below the title but out of the way of content.

#### Wikimedia Commons SVG reliability
- Use direct SVG URLs: `https://upload.wikimedia.org/wikipedia/commons/X/XX/Filename.svg`
- The `/thumb/.../Filename.svg.png` conversion often returns **400/404** for SVGs. Don't rely on it.
- **Alternative CDN**: `https://cdn.jsdelivr.net/npm/@mdi/svg@latest/svg/<icon>.svg` (Material Design Icons on jsDelivr) is a reliable fallback for simple SVG icons.

#### Diagnosing layout overflow
- Text descriptions of layout issues are often insufficient. **Ask the user for a screenshot** when a slide column or element is reported as overflowing or misaligned. Screenshots reveal exact overflow boundaries that descriptions miss.

#### Long command lines in code blocks overflow slide width
- Shell commands with long URLs or paths can exceed the code block width, hiding the copy button and cutting off content.
- **Fix**: Add `overflow-x: auto; max-width: 100%` to `code-block` and `code-block pre` in the deck's `<style>` block. This enables horizontal scrolling instead of breaking lines or clipping content.
  ```css
  .reveal .slides section code-block { overflow-x: auto; max-width: 100%; }
  .reveal .slides section code-block pre { overflow-x: auto; max-width: 100%; }
  ```

#### `ul > li` font-size inheritance causes compounding overflow
- The global CSS rule `.reveal .slides section ul li, .reveal .slides section ol li` sets a fixed `font-size` (e.g. `0.52em`). When inline `style="font-size: X.em"` is added on a `<ul>` element, the nested `<li>` elements inherit from that scaled value, causing text to become too small or overflow unpredictably.
- **Fix**: Adjust the global `ul li / ol li` font-size in the `<style>` block to a reasonable baseline (e.g. `0.82em`) rather than shrinking individual `<ul>` elements further. Typical working values: `ul li` at `0.82em`, `code-block` at `0.88em`, colored box `p` at `0.88em`, colored box `ul li` at `0.82em`.

#### `r-stack` fragment synchronization
- When using `div.r-stack` with paired fragments (image + overlay div), **both elements MUST share the same `data-fragment-index`** so they trigger simultaneously.
- Without matching indices, Reveal.js advances them on separate steps — image fades first, then text appears on the next click — creating a jarring two-step transition.
- Pattern: `<img class="fragment semi-fade-out" data-fragment-index="N" src="..." /><div class="fragment" data-fragment-index="N">...</div>`
- Each r-stack pair in the same deck should use a **unique index** (0, 1, 2, ...) to avoid cross-pair conflicts.

#### `semi-fade-out` vs `fade-in-then-semi-out`
- Both classes exist in `reveal.css` but differ in final opacity: `semi-fade-out` drops to ~30%, `fade-in-then-semi-out` drops to ~50%.
- Prefer `semi-fade-out` for r-stack overlays — makes the background image more subdued so overlay text is more readable.

#### `init.js` hardcodes `RevealMermaid`
- `slides_template/init.js` line 79 hardcodes `RevealMermaid` in the plugins array: `const plugins = [RevealMarkdown, RevealNotes, RevealZoom, RevealHighlight, RevealMath.KaTeX, RevealMermaid];`
- **Every slide deck MUST load the mermaid script** (`https://cdn.jsdelivr.net/npm/reveal.js-mermaid-plugin@11.6.0/plugin/mermaid/mermaid.js`) even if it doesn't use mermaid diagrams.
- Omitting it causes `ReferenceError: RevealMermaid is not defined` at runtime.

#### `r-stack` for project showcase slides
- Use `div.r-stack` to layer content: first child appears, then fades to semi-transparent watermark while next child overlays on top.
- Pattern: `<div class="r-stack"><img class="fragment semi-fade-out" data-fragment-index="N" src="..." /><div class="fragment" data-fragment-index="N"><p>explanation text</p></div></div>`
- **CRITICAL**: Both the image and overlay div MUST share the same `data-fragment-index` (see `r-stack fragment synchronization` gotcha above).
- Image appears solo after title, then fades semi-transparent, explanation text appears over it.
- Works great for project showcase slides where you want to highlight the finished project photo.

#### Image validation — always test URLs
- Many Random Nerd Tutorials URLs return **404** — the site has restructured/renamed files over time.
- Wikimedia Commons returns **403 Forbidden** to HEAD requests from scripts.
- Instructables cover images are often tiny placeholder thumbnails (~8KB) — not useful for slides.
- **Always validate** with HEAD/GET: status 200, Content-Type starts with `image/`, size > 1KB.
- Use the `extract_images.py` script for deterministic extraction and validation from tutorial pages.

#### Image selection for project slides
- **Prefer photos of complete DIY projects** (assembled devices, installed setups, real-world usage).
- **Avoid**: single component photos, breadboard circuits, Fritzing wiring diagrams, stock photos, product catalog images.
- Best sources: Instructables project pages, Hackster.io project pages, personal tech blogs with build photos.
- Use `site:` search queries on educational/DIY sites, then run `extract_images.py` on the most promising URLs.

#### Follow instruction documents exactly
When the user provides a detailed slide-by-slide instructions document (e.g., `instrucoes-codex-aula-XX.md`), **follow the proposed structure exactly** — do not improvise, add extra slides, remove proposed slides, or change the content flow. Treat the document as a specification, not a suggestion. Verify each slide against the proposed structure as you build.

#### Checklist verification script for slide creation
After generating slides, run a quick script to verify all requirements from the instructions document are met:
```python
checks = {
    'Aula N title': 'aula="N"' in html,
    'DBSCAN connection': 'DBSCAN' in html,
    'Code blocks': 'code-block' in html,
    'Poll questions': 'poll-question' in html,
    # ... add checks specific to the lesson
}
for check, result in checks.items():
    status = 'PASS' if result else 'FAIL'
    print(f'[{status}] {check}')
```

#### `metric-card` reusable CSS pattern
For side-by-side comparison blocks with colored left borders, use this inline style pattern:
```html
<div class="metric-card" style="border-left-color: #8be9fd;">
  <h4 style="color: #8be9fd;">Title</h4>
  <p>Description content.</p>
</div>
```
Combine with `<multi-col>` for comparison layouts. Dracula colors: `#8be9fd` (cyan), `#ff79c6` (pink), `#50fa7b` (green), `#ff5555` (red), `#f1fa8c` (yellow), `#bd93f9` (purple).

#### `step-pill` for inline sequential steps
Show sequential steps as inline badges:
```html
<span class="step-pill">Step 1</span>
<span class="step-pill">Step 2</span>
<span class="step-pill">Step 3</span>
```
Useful for algorithm walkthroughs, pipeline stages, or process flows. Pairs well with `data-auto-animate` for progressive reveal.

#### Concept-heavy data science slides don't need Plotly
For topics focused on algorithms, comparisons, and code walkthroughs (e.g., anomaly detection, feature engineering), skip Plotly figures entirely. Use:
- `<code-block>` for code examples
- `<table>` for method comparisons
- `<multi-col>` + `metric-card` for side-by-side concepts
- Mermaid diagrams for process flows
Only use Plotly when the topic requires visualizing data distributions, model outputs, or interactive step-by-step demos.

#### Notebook structure for data science hands-on
Consistent notebook pattern for practical exercises:
1. Imports + Dracula theme helper
2. Dataset generation (synthetic or loaded)
3. Initial visualization
4. Method 1 (code + visualization)
5. Method 2 (code + visualization)
6. Method N (code + visualization)
7. Comparison table + bar chart
8. Discussion questions
Each method section follows: explanation → code → result visualization.

#### `code-block` without `<script type="text/plain">` for safe languages
For Python, R, SQL code that doesn't contain `<` or `>` characters, raw text inside `<code-block>` works fine:
```html
<code-block lang="python">
z = (x - x.mean()) / x.std()
</code-block>
```
For C/C++/Arduino code with `#include <Arduino.h>`, **always** use `<script type="text/plain">` to prevent HTML parser mangling.

#### Two-notebook pattern for data science slides
Separate figure generation from student exercises:
- **Figure gen notebook** (`aula13-gerar-figuras.ipynb`): generates all Plotly figures, exports to JS. Not for students.
- **Hands-on notebook** (`aula13-deteccao-anomalias.ipynb`): student-facing, with exercises, discussion, and code to fill in.
This keeps the slide figures stable while allowing the hands-on notebook to evolve independently.

#### Plotly CDN required for `<plotly-figure>` component
When using `<plotly-figure>` in slides, you **must** include the Plotly CDN script before `reveal.js`:
```html
<script src="https://cdn.plot.ly/plotly-2.32.0.min.js"></script>
```
The `plotlyFigureComponent` has a guard (`typeof Plotly === 'undefined'`) so the deck won't crash without it, but charts won't render.

#### Figure naming convention for exports
Use `AULA{N}_{DESCRIPTIVE_NAME}` for exported figure constants:
```python
figures = {
    'AULA13_MOTIVACAO': fig_motivacao,
    'AULA13_DBSCAN': fig_dbscan,
    'AULA13_COMPARACAO': fig_comparacao,
}
```
This avoids collisions when multiple decks share the same `images/plotly/` directory.

#### `clean_none` is mandatory for Plotly 6.x exports
Plotly 6.x `fig.to_dict()` includes `None` values that break JavaScript when embedded. Always apply a recursive `clean_none` before `json.dumps`:
```python
def clean_none(obj):
    if isinstance(obj, dict):
        return {k: clean_none(v) for k, v in obj.items() if v is not None}
    if isinstance(obj, list):
        return [clean_none(v) for v in obj]
    return obj
```
Without this, the JS file will contain `null` values that cause `ReferenceError` or silent render failures.

---
# IMPORTANT!!!!!
---

### Final Testing

- Never skip testing, specially images status 200 and MIME type image, valid binary data (not placeholders <=1KB)
- Test other links for 200
- Double-check spelling for correct Portuguese (Brazilian) never Chinese characters only technical english terms
are acceptable


