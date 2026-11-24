# Vue Components & Slide Layout Patterns

Complete reference for custom Vue components (`components/components.js`, `slides_template/header1.js`) and CSS helpers (`dist/custom.css`).

## Vue Component Reference

| Component | Purpose | Key Props (always kebab-case in HTML) |
|-----------|---------|---------------------------------------|
| `<header1>` | Cover slide (top-level slide 1) | `aula`, `curso`, `title`, `title-size` |
| `<section-banner>` | IFSP green-striped chapter divider (`img/fundo.png`) | `title`, `subtitle`, `eyebrow`, `align` (`right`/`left`), `title-size`, `bg` |
| `<paper-card>` | Academic paper citation card with optional abstract | `title`, `authors`, `venue`, `year`, `url`, `compact` (boolean) |
| `<multi-col>` | CSS Grid multi-column layout | `cols` (`2`, `3`, `"1.3fr 1fr"`), `gap` or `style="gap:20px"` |
| `<ls-u>` | Auto-fragmenting bullet list (`fade-in-then-semi-out`) | `font-size` (default `24`) |
| `<code-block>` | Syntax-highlighted code with copy button | `lang`, `data-trim`, `data-line-numbers` |
| `<code-inline>` | Inline highlighted snippet | `lang`, `size` |
| `<highlight-box>` | Purple callout box (fragment by default) | `index`, `instant` (present = no fragment) |
| `<copy-btn>` | Copies preceding sibling (`<table>` or text) | — |
| `<md>` | Renders Markdown string | `md` |
| `<leader-line>` | SVG arrow between two DOM elements (**must close with `</leader-line>`**) | `from`, `to`, `color`, `size`, `path`, `start-socket`, `end-socket`, `start-label`, `middle-label`, `end-label`, `dash`, `animated`, `start-plug`, `end-plug` |
| `<poll-question>` | Live student poll (wrap in parent `<section>`, 1 per child slide) | `id`, `title`, `question`, `answer`, `answer-text`, `:options` |
| `<reveald3-plot>` | Interactive RevealD3 + Plotly iframe figure | `file`, `width`, `height`, `scroll` |
| `<plotly-figure>` | Legacy inline Plotly chart (prefer `<reveald3-plot>` for new decks) | `:traces`, `:layout` |

## Illustrated-Style CSS Classes (`dist/custom.css`)

- `.figure-card` — White rounded frame (`#fefefe`) with subtle elevation shadow for cropped paper diagrams, equations, and light-background plots.
- `.figure-stage` — Relative wrapper around `<img>` for percentage-based overlays.
- `.annotate-box` + `--yellow` / `--pink` / `--green` / `--cyan` / `--orange` — Translucent highlight box positioned over `.figure-stage` (`left`, `top`, `width`, `height` in `%`). Combine with `class="fragment"`.
- `.annotate-svg` — Full-overlay SVG layer over `.figure-stage` for crisp vector arrows and markers.
- `.paper-mark` (optional `--pink`) — Yellow/pink translucent text highlighter inside `<paper-card>` abstract slots; with `class="fragment"` text stays visible while highlight illuminates on step.
- `.title-with-paper` — Flex header row placing `<h2>` on the left and `<paper-card compact>` on the right.
- `.formula-stage`, `.formula-term` (`--yellow`/`--pink`/`--cyan`/`--green`), `.formula-captions`, `.formula-caption` — Step-by-step KaTeX equation deconstruction with plain-Portuguese intuition directly below each term.
- `.slide-takeaway` — Short centered 1–2 line takeaway directly below a hero visual.
- `.colab-pill` — Clickable pill link for Colab/Jupyter notebooks placed right where the concept finishes.
- `.reveal p.source` — Standardized `11pt` attribution caption (links inside inherit `11pt`).

## Common Slide Recipes

### Cover Slide

```html
      <!-- SLIDE 1: Capa -->
      <section data-auto-animate>
        <header1 aula="11" curso="Inteligência Artificial" title-size="28"
                 title="IAs Generativas: do VAE ao Stable Diffusion">
          <img src="images/aula11/logo-1.png" alt="Logo ferramenta 1" height="180" style="border-radius: 8px;" />
          <img src="images/aula11/logo-2.png" alt="Logo ferramenta 2" height="180" style="border-radius: 8px;" />
        </header1>
      </section>
```

### Synced Code Walkthrough (`data-line-numbers` + fragments)

```html
        <section data-auto-animate>
          <h2>{TITULO}</h2>
          <multi-col style="gap: 28px;">
            <div>
              <code-block lang="python" data-trim
                data-line-numbers="1-12|1-3|5-8|10-12"
                data-fragment-index="1">
# código completo em um único code-block
              </code-block>
            </div>
            <div>
              <ol>
                <li class="fragment" data-fragment-index="1"><strong>Passo 1:</strong> explicação</li>
                <li class="fragment" data-fragment-index="2"><strong>Passo 2:</strong> explicação</li>
                <li class="fragment" data-fragment-index="3"><strong>Passo 3:</strong> explicação</li>
              </ol>
            </div>
          </multi-col>
        </section>
```

Keep all code in ONE `<code-block>` and start `data-fragment-index` at `1` (`0` = initial full-code state).

### Interactive Quiz (`<poll-question>`)

```html
      <section>
        <section>
          <h2>Quiz Interativo</h2>
          <p>Conecte-se à sala e vote!</p>
        </section>

        <section>
          <poll-question
            id="q1"
            title="Questão 1: Espaço Latente"
            question="Por que o Stable Diffusion aplica ruído no espaço latente do VAE?"
            answer="b"
            answer-text="O espaço latente tem muito menos dimensões que a imagem em pixels, acelerando treino e geração."
            :options="[
              { value: 'a', label: 'Para aumentar o número de pixels da saída' },
              { value: 'b', label: 'Para reduzir drasticamente a dimensionalidade e o custo computacional' },
              { value: 'c', label: 'Para dispensar redes neurais na decodificação' }
            ]" />
        </section>
      </section>
```

### Practical Exercise Slide (when applicable to lab courses)

```html
        <section data-auto-animate>
          <h2>Exercício Prático</h2>
          <div class="green-box">
            <p><strong>Objetivo:</strong> {DESCRICAO}</p>
            <ls-u>
              <li>Passo 1</li>
              <li>Passo 2</li>
            </ls-u>
          </div>
          <code-block lang="sql" data-trim>
CREATE OR REPLACE FUNCTION nome_funcao() RETURNS void AS $$
BEGIN
    -- sua lógica aqui
END;
$$ LANGUAGE plpgsql;
          </code-block>
        </section>
```

### Closing Summary & References

```html
      <section data-auto-animate>
        <h2>Resumo da Aula</h2>
        <ls-u font-size="20">
          <li>Ponto-chave 1</li>
          <li>Ponto-chave 2</li>
        </ls-u>
        <p class="slide-takeaway fragment">Próxima aula: <strong>{PROXIMO TOPICO}</strong></p>
      </section>

      <section data-auto-animate>
        <h2>Referências</h2>
        <ul style="font-size: 17pt;">
          <li><a href="https://arxiv.org/abs/..." target="_blank" rel="noopener">Autor et al. — Título (Ano)</a></li>
        </ul>
      </section>
```
