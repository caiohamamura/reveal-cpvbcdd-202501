# Ecossistema Reveal-CPVBCDD 2025

## Visão Geral

Este repositório é um **framework de apresentação educacional** construído sobre o Reveal.js, extensivamente customizado para suportar aulas interativas de programação, banco de dados e IoT no IFSP Capivari. O ecossistema integra múltiplas bibliotecas para criar slides com código destacado, componentes Vue.js, animações, e suporte a SQL animado.

---

## Pilha Tecnológica

| Camada | Tecnologia | Versão | Propósito |
|--------|-----------|--------|-----------|
| **Framework principal** | Reveal.js | 5.2.1 | Motor de slides |
| **Templates** | Vue.js (ESM Browser) | 3.x | Componentes reativos |
| **Código** | highlight.js + reveal-code-focus | 11.x / 1.1.0 | Syntax highlighting |
| **Markdown** | marked + reveal.js markdown plugin | - | Slides via MD |
| **Matemática** | KaTeX + MathJax | - | Equações |
| **Animações** | CSS fragments + data-auto-animate | - | Transições |
| **Estilização** | CSS customizado + temas Reveal.js | - | Visual temático |
| **Linhas conectoras** | LeaderLine | - | Setas/linhas entre elementos |

---

## Arquitetura do Projeto

```
reveal-cpvbcdd-202501/
├── dist/                    # Reveal.js core + bibliotecas bundled
│   ├── reveal.js            # Motor principal
│   ├── reveal.css           # Estilos base
│   ├── reset.css            # Normalização
│   ├── custom.css           # Estilos customizados CPVBCDD
│   ├── vue.js / vue.esm-browser.js  # Vue 3 (UMD + ESM)
│   ├── theme/               # 12 temas Reveal.js
│   └── highlight/           # Temas de syntax highlighting
├── plugin/                  # Plugins Reveal.js
│   ├── highlight/           # Syntax highlighting
│   ├── markdown/            # Suporte Markdown
│   ├── math/                # KaTeX + MathJax
│   ├── notes/               # Speaker notes
│   ├── search/              # Busca no slide
│   ├── zoom/                # Zoom
│   └── leader-line.min.js   # Biblioteca LeaderLine (linhas conectoras)
├── components/              # Componentes Vue.js customizados
│   ├── components.js        # Componentes de UI
│   └── md.js                # (legacy/incompleto)
├── slides_template/         # Templates reutilizáveis
│   └── header1.js           # Componente header de aula
├── bdd1/                    # Módulo Banco de Dados I
│   ├── aula15.html
│   └── aula16.html
├── bdd2/                    # Módulo Banco de Dados II
│   ├── aula-rtc-deep-sleep.html
│   ├── exemplo_animado.html
│   ├── materialized_views.html
│   ├── slides_blocks_functions_procedures.html
│   ├── snapshot_materialized_views.html
│   ├── roteiro_aula_materialized_views.md
│   ├── pratica_materialized_views.md
│   └── *.sql                # Scripts SQL para aula
├── iot/                     # Módulo IoT
│   └── aula-rtc-deep-sleep.html
├── img/                     # Assets visuais
│   ├── fundo.png            # Background do header
│   └── Artboard 1 copy 2.png  # Logo IFSP
├── package.json             # Dependência: reveal-code-focus
└── docs/                    # Esta documentação
```

---

## Integração Reveal.js + Vue.js

### Padrão de Inicialização

As apresentações seguem este padrão HTML:

```html
<body>
  <div id="app" class="reveal">
    <div class="slides">
      <section>
        <!-- Componentes Vue dentro dos slides -->
      </section>
    </div>
  </div>

  <script type="module">
    import Reveal from './dist/reveal.js';
    import Vue from './dist/vue.esm-browser.js';

    // 1. Criar app Vue ANTES de inicializar Reveal
    const app = Vue.createApp({});

    // 2. Importar e registrar componentes customizados
    import './components/components.js';
    import './slides_template/header1.js';

    // 3. Montar Vue (sem el, porque Reveal controlled)
    app.mount('#app');

    // 4. Inicializar Reveal.js
    Reveal.initialize({
      hash: true,
      plugins: [
        RevealMarkdown,
        RevealHighlight,
        // ...
      ]
    });
  </script>
</body>
```

### Ponto Crítico de Integração

**Ordem de inicialização é crucial:**
1. `Vue.createApp()` — Vue é criado primeiro
2. `app.mount('#app')` — Vue assume o DOM
3. `Reveal.initialize()` — Reveal é inicializado depois

Os componentes `components.js` e `header1.js` detectam `window.app` e se auto-registram via `initializeComponents(app)` e `initializeHeader(app)`.

---

## Sistema de Componentes

### Componentes Disponíveis

#### `header1` — Header de Aula
```html
<header1 aula="08" curso="Banco de Dados" title-size="30"
         title="Materialized Views - Performance com Cache">
  <img src="https://i.imgur.com/Z53uKac.png" height="120">
</header1>
```

**Props:**
- `aula` — Número da aula
- `curso` — Nome do curso/disciplina
- `title` — Título principal
- `titleSize` — Tamanho da fonte do título (pt)

**Funcionalidades:**
- Background com `img/fundo.png`
- Logo IFSP + dados do professor no rodapé
- Slot para imagens extras
- Atualiza `<title>` da página automaticamente

#### `code-inline` — Bloco de Código Inline
```html
<code-inline lang="sql" size="18">
SELECT * FROM orders;
</code-inline>
```

#### `code-block` — Bloco de Código com Botão Copiar
```html
<code-block class="lang-sql">
SELECT * FROM orders;
</code-block>
```
**Funcionalidades:**
- Botão "Copiar" que copia o conteúdo
- Feedback visual "Copiado!" por 2s

#### `multi-col` — Layout Multi-Coluna
```html
<multi-col :cols="3">
  <div>Coluna 1</div>
  <div>Coluna 2</div>
  <div>Coluna 3</div>
</multi-col>
```

#### `highlight-box` — Caixa de Destaque
```html
<highlight-box :index="0">
  Conteúdo destacado...
</highlight-box>
```

#### `ls-u` — Lista com Animação de Entrada
```html
<ls-u font-size="24pt">
  <li>Item 1</li>
  <li>Item 2</li>
</ls-u>
```

#### `md` — Markdown Renderizado
```html
<md :md="'<strong>Texto</strong>'"></md>
```

#### `copy-btn` — Botão Copiar Genérico
```html
<table>...</table>
<copy-btn></copy-btn>
```
**Funcionalidades:**
- Detecta o irmão anterior (tabela, bloco de texto) e copia seu conteúdo
- Para tabelas: extrai células em texto separado por tabulação, remove linhas duplicadas do header
- Feedback visual "Copiado!" por 2s

#### `leader-line` — Linhas Conectoras entre Elementos
```html
<div id="el1">Elemento A</div>
<div id="el2">Elemento B</div>

<!-- Sempre visível -->
<leader-line from="el1" to="el2"></leader-line>

<!-- Aparece como fragment step -->
<leader-line from="el1" to="el2" class="fragment"></leader-line>

<!-- Com índice de fragmento -->
<leader-line from="el1" to="el2" class="fragment" data-fragment-index="3"></leader-line>
```

> **Importante:** Use tag com fechamento explícito `</leader-line>`. Tag auto-fechada `<leader-line />` causa problemas no parser HTML do browser (consome elementos subsequentes como filhos).

**Props:**
| Prop | Tipo | Default | Descrição |
|------|------|---------|-----------|
| `from` | String | *obrigatório* | ID do elemento de origem |
| `to` | String | *obrigatório* | ID do elemento de destino |
| `color` | String | `'#ff79c6'` | Cor da linha |
| `size` | Number | `3` | Espessura da linha |
| `path` | String | `'fluid'` | Tipo de caminho (`fluid`, `straight`, `arc`, `grid`, `magnet`) |
| `startSocket` | String | auto | Socket de saída (`top`, `bottom`, `left`, `right`) |
| `endSocket` | String | auto | Socket de chegada |
| `startLabel` | String | — | Texto no início da linha |
| `middleLabel` | String | — | Texto no meio da linha |
| `endLabel` | String | — | Texto no fim da linha |
| `dash` | Boolean | `false` | Linha tracejada |
| `animated` | Boolean | `true` | Animação `draw` ao mostrar/esconder |

**Comportamento com Reveal.js Fragments:**
- **Sem `class="fragment"`:** a linha aparece imediatamente quando a seção se torna `present`
- **Com `class="fragment"`:** a linha só aparece quando Reveal adiciona `.visible` ao componente, e desaparece ao navegar de volta (quando `.visible` é removido)
- O componente monitora mudanças de classe na `<section>` pai via `MutationObserver`, garantindo que a linha seja removida ao sair do slide e recriada ao retornar

**Dependência:** Requer `plugin/leader-line.min.js` carregado via `<script>` antes do módulo principal.

---

## Sistema de Plugins

### Plugin Markdown
Permite escrever slides em Markdown dentro de `<section>`:
```html
<section data-markdown>
  <textarea data-template>
    ## Título
    - Item 1
    - Item 2
  </textarea>
</section>
```

### Plugin Highlight
Syntax highlighting com suporte a:
- Linhas específicas com `data-line-numbers="3-6"`
- Foco em linhas com `data-line-focus`
- Temas: `panda-syntax-dark.min.css`, `dracula.css`, `monokai.css`, `zenburn.css`

### Plugin Math
Suporte a KaTeX e MathJax 3 para equações matemáticas.

### Plugin Animate
Reveal.js Auto-Animate para transições suaves entre estados de código:
```html
<pre data-id="code"><code data-line-numbers="3-6">...</code></pre>
<pre data-id="code"><code data-line-numbers="2-3">...</code></pre>
```
Otimizado para mostrar mudanças graduais em código SQL.

---

## Convenções de Estilo CSS

### Classes Utilitárias (definidas em `custom.css` e nos próprios HTMLs)

| Classe | Efeito |
|--------|--------|
| `.two-cols` | Layout flex com 2 colunas |
| `.highlight-box` | Fundo semi-transparente roxo |
| `.red-box` | Fundo vermelho com borda esquerda |
| `.green-box` | Fundo verde com borda esquerda |
| `.yellow-box` | Fundo amarelo com borda esquerda |
| `.big-number` | Número grande verde (2.5em) |
| `.red-number` | Número grande vermelho (2.5em) |
| `.comparison-table` | Tabela estilizada |
| `.step-number` | Número em círculo roxo |

### Temas Disponíveis
Os 12 temas do Reveal.js estão em `dist/theme/`:
`beige.css`, `black-contrast.css`, `black.css`, `blood.css`, `dracula.css`, `league-gothic/`, `league.css`, `moon.css`, `night.css`, `serif.css`, `simple.css`, `sky.css`, `solarized.css`, `white-contrast.css`, `white.css`, `white_contrast_compact_verbatim_headers.css`

---

## Padrões de Conteúdo por Módulo

### BDD1 — Banco de Dados I
Aulas introdutórias de SQL:
- `aula15.html`, `aula16.html`
- Sem componentes Vue avançados
- CSS inline no próprio HTML

### BDD2 — Banco de Dados II
Aulas avançadas com dados sintéticos:
- `materialized_views.html` — View + Animated SQL examples
- `slides_blocks_functions_procedures.html` — Blocos, Functions, Procedures
- `exemplo_animado.html` — Animações de query plans
- Scripts SQL: `01northwind.sql` → `04.sql`
- Roteiros MD: `roteiro_aula_*.md`, `pratica_*.md`

### IoT — Internet das Coisas
Slides sobre hardware embarcado:
- `aula-rtc-deep-sleep.html` — NodeMCU ESP8266

---

## Build e Deploy

### Estrutura Estática
O projeto é **100% estático** — não há bundler (Webpack/Vite). Todos os assets são servidos diretamente.

**Para deploy:**
1. Copiar toda a estrutura de diretórios para um servidor web
2. Não requer Node.js no servidor (só para desenvolvimento opcional)
3. Funciona com GitHub Pages, Netlify, Apache, Nginx

### Servidor de Desenvolvimento
```bash
npx serve .
# ou
python -m http.server 8000
```

---

## Extensibilidade

### Criando Novo Componente

1. **Definir o componente Vue** em `components/`:
```javascript
const meuComponente = {
  props: ['msg'],
  template: `<div class="meu-estilo">{{ msg }}</div>`
};
```

2. **Registrar no `initializeComponents`:**
```javascript
function initializeComponents(app) {
  app.component('meu-componente', meuComponente);
  // ... outros componentes
}
```

3. **Usar no HTML:**
```html
<meu-componente msg="Olá"></meu-componente>
```

### Criando Novo Slide

1. Copiar um HTML existente como base
2. Adicionar `<section>` dentro de `<div class="slides">`
3. Usar componentes Vue disponíveis
4. Incluir `data-markdown` para conteúdo em Markdown

### Adicionando Plugin

1. Baixar/copiar arquivos do plugin para `plugin/<nome>/`
2. Importar no `<script type="module">`:
```javascript
import RevealPlugin from './plugin/zoom/plugin.js';
```
3. Adicionar à array `plugins` em `Reveal.initialize()`

---

## Fluxo de Dados dos Módulos

```
┌─────────────────────────────────────────────────────────────┐
│                     index.html principal                    │
├─────────────────────────────────────────────────────────────┤
│  dist/reveal.js ──── motor de slides                         │
│  dist/vue.esm-browser.js ─── sistema de componentes         │
│  components/components.js ─── componentes de UI              │
│  slides_template/header1.js ─── template de header           │
│  plugin/* ─── plugins Reveal.js                             │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
    ┌────────┐          ┌──────────┐          ┌────────┐
    │  BDD1  │          │   BDD2   │          │   IoT  │
    │  aula  │          │materiali │          │  aula  │
    │  15/16 │          │zed_views │          │  rtc   │
    └────────┘          └──────────┘          └────────┘
                              │
                              ▼
                      ┌──────────────┐
                      │ SQL Scripts  │
                      │ *.sql        │
                      └──────────────┘
```

---

## Notas Técnicas

### Por que Vue 3 via ESM Browser?
Permite usar Composition API diretamente no browser sem build step. O `vue.esm-browser.js` é a versão "runtime-only" otimizada para módulos ES.

### Por que não usa reveal.js via npm?
Os arquivos em `dist/` são cópias manuais do Reveal.js para:
1. Evitar dependência de bundler
2. Permitir customização direta dos arquivos
3. Simplificar deploy (estrutura 100% estática)

### Leader-Line.js
Biblioteca `plugin/leader-line.min.js` para desenhar linhas/setas SVG entre elementos DOM. Integrada ao ecossistema via componente Vue `<leader-line>`, com suporte a fragments do Reveal.js. Não é um plugin Reveal — é carregada como script standalone e consumida pelo componente.

---

*Documentação gerada em 2026-04-24*
