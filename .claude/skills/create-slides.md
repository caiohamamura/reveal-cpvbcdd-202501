# Skill: create-slides

Create a new Reveal.js slide file for the CPVBCDD educational framework.

## Trigger
When the user asks to create slides, a new lesson, a new presentation, or says "create slides for..." / "nova aula..." / "slides para..."

## Instructions

You will be given a topic and course context. Generate a complete `.html` slide file following the patterns below exactly. Ask the user for: course name, lesson number, and topic if not provided.

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
  <link rel="stylesheet" href="../dist/theme/night.css" />
  <link rel="stylesheet" href="../dist/custom.css" />
  <link rel="stylesheet" href="../plugin/highlight/monokai.css" />
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
  <script src="../components/md.js"></script>
  <script src="../components/components.js"></script>
  <!-- Plugin scripts (local for chalkboard — NOT CDN) -->
  <script src="../plugin/poll/plugin.js"></script>
  <script src="../plugin/customcontrols/plugin.js"></script>
  <script src="../plugin/chalkboard/plugin.js"></script>

  <script type="module">
    import { mountSlideApp } from '../slides_template/init.js';
    mountSlideApp();
  </script>

</body>
</html>
```

Theme: use `night.css` for IoT, `dracula.css` for BDD.

**CRITICAL: Use `mountSlideApp()` from `slides_template/init.js`.** This:
1. Injects the seminar connect panel into `<body>` (host button + status display)
2. Sets `window.seminarConfig` automatically (server is shared, room defaults to `location.pathname`)
3. To override the room, set `window.seminarConfig = { room: 'my-room' }` BEFORE calling `mountSlideApp()`
4. Creates Vue app, registers components, initializes Reveal.js with all plugins
5. Do NOT call `new Reveal()` or set `window.seminarConfig` yourself

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
6. **Summary** — Recap + preview of next lesson

### Language
- All slide content in **Portuguese (Brazilian)**
- Technical terms can stay in English (WiFi, Deep Sleep, MQTT, etc.)
- Code comments in Portuguese
