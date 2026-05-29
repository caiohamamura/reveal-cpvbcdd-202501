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

> **Design visual:** Aplique também a skill local `.opencode/skills/slide-design/SKILL.md` ao criar ou revisar decks. Ela adapta princípios de frontend design para slides: direção visual intencional, uso de artefatos reais, layouts legíveis, assets locais, e validação visual.

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
          <!-- Optional: prefer a real local image/logo/asset when it represents the topic better than a diagram -->
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
        <code-block lang="{lang}" data-trim>
{CODE HERE}
</code-block>
      </section>
```
- Use `lang="sql"` for SQL, `lang="cpp"` or `lang="c"` for Arduino/C++, `lang="python"` for Python, `lang="r"` for R
- Do not use `<script>` tags inside `<code-block>`; Vue treats them as side-effect tags and logs template compilation warnings.
- Use raw text directly for ordinary code. Use `<textarea>` only when the code actually contains `<` or `>` that the browser would parse as HTML.

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
          <code-block lang="sql">
CREATE OR REPLACE FUNCTION nome_funcao(
    -- parâmetros
) RETURNS tipo AS $$
BEGIN
    -- sua lógica aqui
END;
$$ LANGUAGE plpgsql;
</code-block>
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
- Prefer local, versioned assets for course slides; official logos, real screenshots, generated outputs, file trees, and query results are usually better than generic decorative diagrams.
- Mermaid should clarify a flow or structure, not be default cover decoration.

### Slide Design Quality
- Pick a visual direction from the lesson purpose and audience before building slides.
- Keep one dominant visual idea per slide: a diagram, code+output, table, screenshot, image, or exercise prompt.
- Preserve the user's pedagogical sequence unless explicitly asked to redesign the narrative.
- Fit content inside the Reveal logical slide canvas; avoid overlap with headers, footers, logos, and IFSP branding.
- Use fragments only when they serve teaching: staged reasoning, code walkthroughs, or exercise steps.
- Show actual executed output near teaching code when it helps students interpret formats/results.
- Prefer practical, concrete examples connected to students' reality over decorative visuals.

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
- Never use `<script>` tags inside `<code-block>`; Vue ignores side-effect tags and emits warnings.
- Use direct text inside `<code-block>` for ordinary code.
- Use `<textarea>` inside `<code-block>` only when the code actually contains `<` or `>` that would be parsed as HTML, such as `#include <Arduino.h>`.
- In Python examples that index a SciPy sparse matrix with a pandas boolean mask, convert the mask first: `X[mask.to_numpy()]`. Recent pandas/scipy combinations can fail on `X[mask]`.
- For SQL/Cypher/Mongo examples that show a result table, include enough seed data earlier in the deck so the query actually returns the displayed rows.
- When introducing acronyms such as OLTP/OLAP, expand the English term and explain the origin before using the acronym as shorthand.
- For lessons comparing SQL with DataFrame tools, include a non-trivial side-by-side example where SQL combines `WHERE`, `GROUP BY`, aggregate functions, `HAVING`, window functions, or joins in one readable query, and contrast that with the more imperative multi-step pandas version.
- For DuckDB/file analytics decks, include real-file workflows beyond a single CSV: CSV vs Parquet performance tradeoffs, `read_parquet()`/`read_csv_auto()` with glob patterns over many files, data-lake/big-data parallels, and DuckDB as a staging/cleaning bridge before loading into PostgreSQL or another DBMS.
- Do not use one of the student task options as the fully worked example in the same lesson; choose a separate domain so the example does not solve a proposed activity.

#### Converting Google Slides with gogcli
- If `gog slides list-slides/read-slide` fails with `403 accessNotConfigured`, enable Google Slides API for the OAuth project shown in the error URL, then retry after propagation.
- Fallback path: export with `gog slides export <presentationId> --format pptx/pdf`, extract text from `ppt/slides/slide*.xml`, and extract images from `ppt/media/`.
- Prefer committing only selected reusable assets, not source PPTX/PDF, unzip folders, or per-slide JSON dumps.

#### HTML section nesting (Reveal.js)
- Reveal.js uses nested `<section>` elements for vertical navigation. A misplaced closing `</section>` can cause slides to be nested incorrectly, making them invisible or out of order.
- Use comment markers like `<!-- fim Fase N -->` to track section boundaries.
- If `FASE N` starts before `fim Fase N-1`, Reveal can mix the first slides of the next phase and render following slides blank.
- Run `python .opencode/skills/validate-slides/scripts/validate_slide_deck.py <slide-file.html>` after edits to catch unclosed phase comments.
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

#### Windows install commands with winget
- `winget search` may return no useful output on first use unless `--accept-source-agreements` is included.
- For Windows machines without WSL/Docker Desktop, `winget install Redis.Redis --accept-source-agreements --accept-package-agreements` installs the archived Windows Redis port and creates a `Redis` service. It is old, but works for basic classroom `redis-py` examples.
- `winget install Memurai.MemuraiDeveloper` can fail with MSI `1603` on some machines; do not use it as the primary classroom path unless tested on that lab image.

#### Researching tool deprecation status
- Always check deprecation/EOL status before mentioning tools in slides. MongoDB Atlas Data API was deprecated (End-of-Life) and should not be recommended to students. Verify via official docs release notes.

#### Using MDI icons for section headers
- `https://cdn.jsdelivr.net/npm/@mdi/svg@latest/svg/<icon>.svg` is a reliable source for Material Design Icons on jsDelivr CDN. Good for section header illustrations when Wikimedia Commons doesn't have relevant images.

#### Package compatibility in comparisons
- When comparing ecosystems (e.g., PostgreSQL vs MongoDB), verify that tools actually support the target database in their current version. Strapi v4+ dropped MongoDB support — a fact that invalidates comparisons using older docs.

This is cleaner than creating a separate Vue app, using globalProperties globally, or building a scoped component — the data lives only in the app instance that drives that specific slide deck.

#### Default Plotly integration: RevealD3 iframe plots
- For new Plotly charts, prefer a standalone HTML file loaded with RevealD3 instead of embedding all plot state in the deck HTML.
- Load the plugin in the deck: `<script src="../plugin/reveald3/reveald3.js"></script>` before `init.js`; `slides_template/init.js` auto-detects `window.Reveald3`.
- Put the chart container in the slide:
  ```html
  <reveald3-plot file="aulas/my-plot.html" width="780px" height="460px"></reveald3-plot>
  ```
- Raw RevealD3 markup is also valid: `<div data-file="aulas/my-plot.html" data-scroll="no"></div>`.
- Put Plotly.js, data, layout, and animation code inside `aulas/my-plot.html`; this keeps the deck small and prevents Vue/globalProperties issues.
- To export from Python or notebooks, use `.opencode/skills/export-plots/scripts/export_reveald3_plotly.py` or import `export_reveald3_plotly()`.
- If a RevealD3 plot container is visible but no iframe is created, check that the rendered element has class `fig-container`; the plugin discovers plots with `document.getElementsByClassName('fig-container')`.
- For fragments, add visible labels in the slide and define `_transitions` inside the iframe HTML with matching zero-based `index` values:
  ```js
  var _transitions = [
    {
      index: 0,
      transitionForward: () => animateStep(1),
      transitionBackward: () => animateStep(0)
    }
  ];
  ```
- Use `Plotly.react()` for initial render. Use `Plotly.animate()` for step transitions that should move points, resize markers, or update positions naturally. Keep trace order stable and set `uid` values on traces; adding/removing traces may require `frame.redraw: true`.
- Color changes can still feel more abrupt than numeric changes because Plotly does not interpolate every marker style like D3. If fully interpolated style morphing is required, use native D3 inside the same RevealD3 iframe pattern.

#### PlotlyFigure component
- A global `plotlyFigureComponent` is available in `components/components.js` for rendering simple Plotly.js charts inline in slides.
- It includes a Plotly guard (`typeof Plotly === 'undefined'`) so decks without the Plotly CDN don't break.
- Use it for static charts or lightweight reactive charts only. For new step-by-step teaching plots, prefer RevealD3 iframe plots above.
- Do not add new `<plotly-figure>` usage unless maintaining an existing deck.
- When using fragment sync with inline charts, scope your check (e.g. `.my-step-class`) to avoid responding to ALL fragments in the deck.

#### Plotly 6.x API changes
- `colorbar.titlefont` is **removed** — use `colorbar=dict(title=dict(text='...', font=dict(color='...')))` instead
- `symbol='x'` still works for marker symbols
- When exporting Plotly JSON from Python (`fig.to_dict()`), clean `None` values before embedding in JS — they cause issues

#### Notebook → Slides Plotly pipeline
1. Generate Plotly figures in Jupyter notebook
2. Export as JSON: `json.dump(fig.to_dict(), f)`
3. Convert to data/constants consumed by a standalone plot HTML file under `aulas/` or `images/plotly/`
4. Load the plot into the slide with RevealD3: `<div data-file="aulas/plot_name.html" data-scroll="no"></div>`
5. Define `_transitions` in the plot HTML when fragments should update the figure step by step
6. Only for legacy inline `<plotly-figure>` charts: Vue 3 does NOT resolve bare `window` globals in templates. You MUST either:
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
7. Reference in `<plotly-figure>`: `:traces="PLOT_NAME_TRACES" :layout="PLOT_NAME_LAYOUT"`

#### Legacy interactive Plotly with Vue reactivity
For existing inline step-by-step demos (K-Means, etc.), use Vue reactivity; for new plots, prefer RevealD3 iframe plots:
1. Create `Vue.reactive({ step: 0 })` outside the app for shared mutable state
2. Use `Vue.computed()` to derive traces from reactive state
3. Use `<plotly-figure :traces="computedTraces" :layout="computedLayout">` component
4. Use visible fragments with descriptive labels (NOT empty invisible divs): `<div class="fragment fade-in-then-out kmeans-step" data-fragment-index="N">`
5. Do NOT add a separate `<p id="step-label">` — the fragment labels already show one at a time via `fade-in-then-out`. A duplicate label creates visual clutter and goes out of sync.
6. Listen to `window.deck.on('fragmentshown'/'fragmenthidden')` scoped by class name
7. Avoid `Plotly.animate()` in the inline Vue component path when traces are added/removed; it can silently ignore new traces. Inside standalone RevealD3 iframe plots, `Plotly.animate()` is the preferred method for smooth numeric transitions.
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

#### Side-by-side code comparisons need vertical formatting
- When two `code-block`s share a `multi-col` row, even moderately long expressions can overflow or feel cramped.
- Prefer one item per line for `SELECT` lists, dict/list literals, boolean filters, and long `COPY`/`FROM` paths.
- If the comparison still feels tight, reduce the font size only on those two blocks instead of shrinking the whole deck.

#### `ul > li` font-size inheritance causes compounding overflow
- The global CSS rule `.reveal .slides section ul li, .reveal .slides section ol li` sets a fixed `font-size` (e.g. `0.52em`). When inline `style="font-size: X.em"` is added on a `<ul>` element, the nested `<li>` elements inherit from that scaled value, causing text to become too small or overflow unpredictably.
- **Fix**: Adjust the global `ul li / ol li` font-size in the `<style>` block to a reasonable baseline (e.g. `0.82em`) rather than shrinking individual `<ul>` elements further. Typical working values: `ul li` at `0.82em`, `code-block` at `0.88em`, colored box `p` at `0.88em`, colored box `ul li` at `0.82em`.

#### AsyncTelegram2 (IoT slides reference)
- Library: `cotestatnt/AsyncTelegram2 @ ^2.3.4`, JSON: `bblanchon/ArduinoJson @ ^6.21.5` (v6, NOT v7)
- Use `enableInsecureFallback()` for simpler teaching code (not full BearSSL cert validation)
- Key API: `bot.getNewMessage(msg)` returns bool, `msg.messageType` is `MessageText` or `MessageQuery`, `msg.callbackQueryData` for button data, `bot.endQuery(msg, text)` required for callbacks
- `bot.sendTo(chat_id, text)` for proactive messages (takes `int64_t chat_id`)

#### express-restify-mongoose URL pattern
- Routes are registered at `/api/v1/<modelName>` (singular), e.g. `Produto` → `/api/v1/Produto`
- The library uses `model.modelName` directly — it does NOT pluralize automatically
- Default prefix: `/api`, default version: `/v1`
- Slide comments saying `GET /Produtos` (plural) are incorrect — the actual route is singular

#### MongoDB conda-forge limitations
- `mongodb` from conda-forge provides `mongod` but NOT `mongosh`
- Install `mongosh` separately via `npm install -g mongosh` for a complete test environment

#### Redis Python teaching setup
- For Python/IPython Redis examples, create the client with `redis.Redis(host="localhost", port=6379, decode_responses=True)` so string outputs are readable.
- On Ubuntu 24.04+, avoid teaching `pip install --user redis` for the system Python; PEP 668 blocks it. Use `sudo apt install redis-server python3-redis ipython3` for a simple classroom setup.
- `redis-py` may display membership checks like `r.sismember(...)` as `1` instead of `True`; both indicate membership.
- The archived Windows `Redis.Redis` package is Redis 3.0 and does not support multi-field `HSET`; use repeated `r.hset(key, field, value)` calls instead of `r.hset(key, mapping={...})`.

---
# IMPORTANT!!!!!
---

### Final Testing

- Never skip testing, specially images status 200 and MIME type image, valid binary data (not placeholders <=1KB)
- Run deterministic static checks with `python .opencode/skills/validate-slides/scripts/validate_slide_deck.py <slide-file.html>` instead of recreating ad hoc commands.
- Test other links for 200
- Double-check spelling for correct Portuguese (Brazilian) never Chinese characters only technical english terms
are acceptable
