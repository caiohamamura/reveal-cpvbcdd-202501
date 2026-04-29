# Boilerplate — Script Block

## Script Block CORRETO

A partir de agora, toda a inicialização é feita por `init.js`. O inline script é mínimo:

```html
  <!-- Scripts na ordem EXATA abaixo -->
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
```

## Ordem dos Scripts

1. `../dist/reveal.js`
2. `../plugin/notes/notes.js`
3. `../plugin/math/math.js`
4. `../plugin/markdown/markdown.js`
5. `../plugin/highlight/highlight.js`
6. `../plugin/zoom/zoom.js`
7. `https://cdn.jsdelivr.net/npm/reveal.js-mermaid-plugin@11.6.0/plugin/mermaid/mermaid.js`
8. `../plugin/leader-line.min.js`
9. `../dist/vue.js`
10. `../slides_template/header1.js`
11. `../components/md.js`
12. `../components/components.js`
13. `../slides_template/init.js`
14. **Inline `mountSlideApp()``**

## O que `init.js` faz

- `initializeReveal()` — configura Reveal.js com plugins, controls, hash, etc.
- `mountSlideApp()` — cria Vue app, registra componentes, monta em `#app`, chama `initializeReveal()` no `onMounted`
- Handler de `.fragment.auto` — avança fragmentos automaticamente no `slidechanged`

## Code Block with Synchronized Line Highlighting

For code explanations that need to highlight specific lines in sync with a list:

```html
<code-block lang="r" data-line-numbers="1-14|2|5|8-11|14" data-fragment-index="1">
# Complete code - all lines visible initially
code_line_1
code_line_2
...
</code-block>
```

**data-line-numbers format:** `all-lines|F1|F2|F3|F4`
- First value = all lines shown initially (active by default)
- Subsequent values = lines highlighted when fragment N is active
- Separator: pipe `|`

**data-fragment-index:** Start at 1, use `<ol>` not `<ul>`

---

## Erros a Evitar

### ❌ ERRADO (inicialização inline duplicada)
```javascript
// NÃO repita a lógica de inicialização em cada slide
const app = Vue.createApp({ ... });
initializeComponents(app);
initializeHeader(app);
function initializeReveal() { ... }
app.mount("#app");
```

### ✅ CORRETO (uma linha)
```javascript
window.app = mountSlideApp();
```

### ❌ ERRADO (multiple code-blocks for stepwise)
```html
<!-- NÃO FAÇA ISSO - código fragmentado em múltiplos code-block -->
<code-block lang="r" data-line-numbers="1">...</code-block>
<code-block lang="r" data-line-numbers="2">...</code-block>
```

### ✅ CORRETO (one code-block with synchronized highlighting)
```html
<!-- FAÇA ISSO - código em uma célula com highlight sequencial -->
<code-block lang="r" data-line-numbers="1-14|2|5|8-11|14" data-fragment-index="1">
...all code...
</code-block>
```
