# Framework & Course Gotchas

Consolidated technical pitfalls collected across decks in this repository. Check this before debugging odd Reveal.js, Vue, CSS, or course-tool behavior.

## Reveal.js & HTML Structure

- **Nested `<section>` boundaries**: Misplaced `</section>` tags cause slides to nest unexpectedly or render blank. Always pair `<!-- Etapa N: ... -->` with `<!-- fim Etapa N -->` and run `validate_slide_deck.py`. Quiz and References sections must be top-level siblings of super sections.
- **No `<script>` inside `<code-block>`**: Vue ignores side-effect `<script>` tags in templates and logs compilation warnings (and `validate_slide_deck.py` flags it as an ERROR). Put ordinary code as raw text inside `<code-block>`; wrap in `<textarea>` only when angle brackets (`<`, `>`) would be parsed as HTML (e.g., `#include <Arduino.h>`).
- **Explicit `</leader-line>` close tag**: Self-closing `<leader-line />` breaks HTML parsing and swallows following elements as children.
- **Vue DOM templates require kebab-case props**: Browsers lowercase HTML attributes (`startSocket` → `startsocket`), breaking Vue prop binding. Always write `start-socket`, `end-socket`, `middle-label`, `start-plug`, `end-plug`, `title-size`, `answer-text`, `font-size`.
- **Per-slide Vue reactive state**: Override `mountSlideApp()` before calling it rather than creating a second Vue app:
  ```js
  const _originalMount = mountSlideApp;
  mountSlideApp = function () {
    const app = _originalMount();
    app.config.globalProperties.myState = Vue.reactive({ step: 0 });
    return app;
  };
  window.app = mountSlideApp();
  ```
- **Chalkboard plugin must be local**: Always load `../plugin/chalkboard/plugin.js`, never jsDelivr CDN (CDN lacks custom keyboard shortcuts `B`, `C`, `E`, `=`, `-`, `1`–`7`).

## CSS, Layout & Diagrams

- **LeaderLine labels on dark themes**: Rendered as SVG text; white outline is an SVG stroke (neutralized globally via `body svg text { stroke: none !important; }` in `dist/custom.css`).
- **Mermaid syntax**:
  - Do NOT wrap edge labels in quotes: use `A -->|texto| B`, NOT `A -->|"texto"| B`.
  - Use **0 spaces** indentation for graph content inside `<pre>`.
  - Always give each `.mermaid` div a unique `data-id`.
- **Long code/URLs inside `<multi-col>`**: `custom.css` sets `.multi-col > * { min-width: 0 }` and horizontal scroll for `pre.code-wrapper`. For long inline URLs inside `<code>`, add `overflow-wrap: break-word`. For side-by-side code blocks, format vertically (one field/argument per line).
- **Avoid inline `font-size` on `<ul>` directly**: `.reveal .slides section li` sets relative `em` sizing; shrinking `<ul>` compounds on nested `<li>`. Adjust `<li>` or local styles instead.
- **Centering orphan cards**: Use `display: flex; flex-flow: row wrap; justify-content: center; gap: 12px;` with card `max-width` instead of fixed-column CSS Grid when rows are uneven.
- **Background logo opacity on Dracula**: Start at `data-background-opacity="0.20"`–`0.25` (below `0.10` dark/blue logos disappear against `#282a36`).
- **Multi-line `.terminal` blocks under Vue**: Vue's DOM template compiler collapses newlines inside `<div class="terminal">`; use `<pre class="terminal" style="width: auto; box-shadow: none;">` to preserve line breaks.
- **`.figure-stage` + `.annotate-box` alignment**: Reveal's default `.reveal section img { max-width: 95%; max-height: 95%; }` can shrink images relative to `.figure-stage` and offset percentage overlays. Override `.figure-stage > img { max-width: none !important; max-height: none !important; }` and size ultra-wide figures by `width="..."` (not `height="..."`) to avoid horizontal overflow.
- **Wikimedia Commons SVGs**: Link directly to `https://upload.wikimedia.org/wikipedia/commons/X/XX/Filename.svg`; `/thumb/.../Filename.svg.png` frequently returns 400/404.

## Plotly & RevealD3

- Prefer standalone RevealD3 iframe HTML plots (`<reveald3-plot file="aulas/plot.html">`) via `export-plots` skill over legacy inline `<plotly-figure>`.
- Container MUST keep class `fig-container` (handled automatically by `<reveald3-plot>`).
- Use `Plotly.react()` for initial state and `Plotly.animate()` for `_transitions` (keep trace order stable with explicit `uid`).
- **Plotly 6.x**: `colorbar.titlefont` was removed — use `colorbar=dict(title=dict(text='...', font=dict(color='...')))`. Clean `None` values from `fig.to_dict()`.
- **SciPy sparse + pandas mask**: Use `X[mask.to_numpy()]` instead of `X[mask]`.

## Course-Specific Technical Notes

- **General pedagogy**: Always expand acronyms (e.g., OLTP/OLAP, VAE, DDPM, IoU, NMS) on first use; verify tool deprecation/EOL status before recommending (e.g., MongoDB Atlas Data API is EOL; Strapi v4+ dropped MongoDB); do not use a student assignment option as the worked class example.
- **IoT (ESP8266/ESP32)**: `cotestatnt/AsyncTelegram2 @ ^2.3.4` pairs with `bblanchon/ArduinoJson @ ^6.21.5` (v6, not v7). Use `enableInsecureFallback()`, check `msg.messageType` (`MessageText` / `MessageQuery`), call `bot.endQuery(msg, text)` for callbacks, `bot.sendTo(chat_id, text)` for proactive messages.
- **BDD2 / Node (`express-restify-mongoose`)**: Registers routes at singular `/api/v1/<modelName>` (e.g., `/api/v1/Produto`, never pluralized automatically).
- **BDD2 / MongoDB**: `mongodb` from conda-forge provides `mongod` but NOT `mongosh` (install `mongosh` separately via `npm install -g mongosh`).
- **BDD2 / Redis**: Initialize `redis.Redis(host="localhost", port=6379, decode_responses=True)`. On Ubuntu 24.04+, prefer `sudo apt install redis-server python3-redis ipython3` (avoids PEP 668 `pip install --user` failure). Archived Windows `Redis.Redis` (`winget install Redis.Redis --accept-source-agreements --accept-package-agreements`) is Redis 3.0 and does not support multi-field `HSET mapping={...}` — use repeated `r.hset(key, field, value)`.
- **BDD2 / DuckDB**: Cover real multi-file workflows (`read_parquet('dados/**/*.parquet')`, CSV vs Parquet tradeoffs, staging/cleaning bridge into PostgreSQL) and non-trivial SQL vs pandas comparisons (`WHERE`, `GROUP BY`, `HAVING`, window functions/joins).
- **BDD2 / SQL/Cypher/Mongo**: Always seed enough data earlier in the deck so every shown query actually produces the displayed result table.
- **Web research**: `npmjs.com` blocks automated fetches with 403; check GitHub repo pages instead.
