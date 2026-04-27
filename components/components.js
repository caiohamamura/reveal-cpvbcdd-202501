const codeInlineComponent = {
  props: ['lang', 'size'],
  setup(props) {
    let classNames = {};
    classNames[props.lang || 'sql'] = true;
    return { classNames };
  },
  /* html */
  template: `
  <pre class="code-inline"><code :class="classNames" :style="{fontSize: (size || 20) + 'pt'}" data-trim><slot></slot></code></pre>
        `,
};

const multiColComponent = {
  template: `<div class="multi-col" :style="{ '--col-count': cols }"><slot></slot></div>`,
  props: { cols: { type: Number, default: 2 } }
};

const highlightBoxComponent = {
  template: `<div class="fragment highlight-box" :data-fragment-index="index"><slot></slot></div>`,
  props: ['index']
};

const lsUComponent = {
  props: ['fontSize'],
  mounted() {
    // Initialize the list component
    this.$el.querySelectorAll("li").forEach((li) => {
      li.classList.add("fragment");
      li.classList.add("fade-in-then-semi-out"); 
      li.style.fontSize = this.fontSize || "24pt";
    });
  },
  /*html*/
  template: `
  <ul>
    <slot></slot>
  </ul>
        `,
}

// Global store for raw code-block HTML, populated before Vue mounts
window.__codeBlockRaw = {};
window.__codeBlockCounter = 0;

// Strip common leading whitespace from all non-empty lines
function stripIndentation(text) {
  const lines = text.split('\n');
  let minIndent = Infinity;
  for (const line of lines) {
    if (line.trim().length === 0) continue;
    const indent = line.match(/^(\s*)/)[1].length;
    if (indent < minIndent) minIndent = indent;
  }
  if (minIndent === Infinity || minIndent === 0) return text.trim();
  return lines.map(line => line.substring(minIndent)).join('\n').trim();
}

// HTML-escape text so v-html renders it as-is (prevents <Arduino.h> → <arduino.h>)
function escapeHtml(text) {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

// Capture raw content of all <code-block> elements before Vue processes them
(function captureCodeBlocks() {
  document.querySelectorAll('code-block').forEach(el => {
    const id = '__cb_' + (window.__codeBlockCounter++);
    // Prefer <script type="text/plain"> child to avoid HTML parser mangling
    // (e.g. #include <Arduino.h> becomes <arduino.h>)
    const plain = el.querySelector('script[type="text/plain"]');
    const raw = plain ? plain.textContent : el.textContent;
    window.__codeBlockRaw[id] = escapeHtml(stripIndentation(raw));
    el.setAttribute('data-cb-id', id);
  });
})();

const codeBlockComponent = {
  props: {
    lang: { type: String, default: '' },
  },
  setup(props, { attrs }) {
    const btnMsg = Vue.ref('Copiar');
    const pre = Vue.useTemplateRef('pre');
    const root = Vue.useTemplateRef('root');
    const rawCode = Vue.ref('');

    Vue.onMounted(() => {
      const id = root.value?.getAttribute('data-cb-id');
      if (id && window.__codeBlockRaw[id]) {
        rawCode.value = window.__codeBlockRaw[id];
      }
    });

    function copiar() {
      const conteudo = pre.value?.textContent;
      navigator.clipboard.writeText(conteudo || '')
        .then(() => {
          btnMsg.value = 'Copiado!';
          setTimeout(() => { btnMsg.value = 'Copiar'; }, 2000);
        })
        .catch(err => console.error('Erro ao copiar:', err));
    }
    const codeClass = props.lang ? `lang-${props.lang} code-wrapper` : 'code-wrapper';
    return { copiar, btnMsg, codeClass, attrs, rawCode };
  },
  /*html*/
  template: `
  <div ref="root" style="display:none" v-bind="attrs"><slot></slot></div>
  <div style="position: relative; margin: 0; padding: 0;display:block; width: min-content;">
  <pre ref="pre" class="code-wrapper" style="min-width: max-content; padding:0; margin: 0;"><code :class="codeClass" data-trim v-bind="attrs" v-html="rawCode"></code></pre>
  <button class="copy-button" style="position:absolute; top:5px; right:5px;" @click=copiar>{{btnMsg}}</button>
  </div>
  `,
}

const copyBtnComponent = {
  setup() {
    const btn = Vue.ref('btn');

    Vue.onMounted(function () {
      let anterior = btn.value?.previousSibling;
      console.log(anterior);
      anterior.insertBefore(btn.value, anterior.firstChild);


    });

    async function copiar() {
      const conteudo = btn.value?.nextSibling;

      // Process each row into a tab-separated string
      let rows = Array.from(conteudo.querySelectorAll('tr'));


      if (rows.length === 0) {
        text = conteudo.textContent || '';
      }
      else {
        let firstRow = '';
        let remove = false;
        for (row of rows) {
          if (firstRow === '') {
            firstRow = row.textContent;
          } else if (row.textContent === firstRow) {
            let index = rows.indexOf(row);
            console.log(index);
            while (rows.length > index) {
              rows.pop();
            }
          }
        }
        console.log(rows);
        text = rows.map(row => {
          const cells = Array.from(row.querySelectorAll('td, th'));
          return cells.map(cell => cell.innerText).join('');
        });
        text = text.join('\n');
      }

      // Copy to clipboard
      try {
        await navigator.clipboard.writeText(text);
        btn.value.textContent = 'Copiado!';
        setTimeout(() => {
          btn.value.textContent = 'Copiar';
        }, 2000);
      } catch (err) {
        console.error('Erro ao copiar:', err);
      };
    }

    return { copiar, btn };

  },
  /*html*/
  template: `
  <button ref="btn" class="copy-button btn color-black" @click=copiar>Copiar</button>
  `
};

const mdComponent = {
  props: ["md"],
  /*html*/
  template: `
  <p data-markdown>
    <textarea data-template v-text="md"></textarea>
</p>
        `,
};

const leaderLineComponent = {
  props: {
    from: { type: String, required: true },
    to: { type: String, required  : true },
    color: { type: String, default: '#ff79c6' },
    size: { type: Number, default: 3 },
    path: { type: String, default: 'fluid' },
    startSocket: { type: String },
    endSocket: { type: String },
    startLabel: { type: String },
    endLabel: { type: String },
    middleLabel: { type: String },
    dash: { type: Boolean, default: false },
    animated: { type: Boolean, default: true },
  },
  setup(props, { attrs }) {
    const root = Vue.ref(null);
    let line = null;

    // Is this component itself marked as a fragment?
    function isFragment() {
      return root.value?.classList.contains('fragment');
    }

    // Is this fragment revealed by Reveal?
    function isRevealed() {
      return !isFragment() || root.value?.classList.contains('visible');
    }

    function makeLabel(text) {
      if (!text) return undefined;
      return typeof LeaderLine.captionLabel === 'function'
        ? LeaderLine.captionLabel(text)
        : text;
    }

    function ensureLine() {
      if (line) return line;
      if (typeof LeaderLine === 'undefined') return null;
      const startEl = document.getElementById(props.from);
      const endEl = document.getElementById(props.to);
      if (!startEl || !endEl) return null;

      const opts = {
        color: props.color,
        size: props.size,
        path: props.path,
        hide: true,
      };
      if (props.startSocket) opts.startSocket = props.startSocket;
      if (props.endSocket) opts.endSocket = props.endSocket;
      if (props.startLabel) opts.startLabel = makeLabel(props.startLabel);
      if (props.endLabel) opts.endLabel = makeLabel(props.endLabel);
      if (props.middleLabel) opts.middleLabel = makeLabel(props.middleLabel);
      if (props.dash) opts.dash = true;

      line = new LeaderLine(startEl, endEl, opts);
      return line;
    }

    function show() {
      if (!isRevealed()) return;
      const l = ensureLine();
      if (!l) return;
      props.animated ? l.show('draw') : l.show();
    }

    function hide() {
      if (!line) return;
      props.animated ? line.hide('draw') : line.hide();
    }

    let observer = null;

    function setup() {
      // Not a fragment — show immediately
      if (root.value?.closest("section")?.classList?.contains("present")) {
        show();
        return;
      } else {
        line?.remove();
      }
      // Already visible — show now
      if (root.value.classList.contains('visible')) {
        show();
      }
      // Watch this component's own element for .visible being added by Reveal
      observer = new MutationObserver(() => {
        if (root.value.closest("section").classList.contains("present")) {
          if (root.value.classList.contains('visible') || (
            root.value.classList.contains('fragment') == false && 
            (
              (root.value.closest(".fragment.visible") ?? false) ||
              (root.value.closest(".fragment") === null)
            ))
          ) {
            show();
          } else {
            hide();
          }
          return;
        } else {
          line?.remove();
          line = null;
        }
      });
      observer.observe(root.value.closest("section"), { attributes: true, attributeFilter: ['class'] });
    }

    function cleanup() {
      if (observer) { observer.disconnect(); observer = null; }
      if (line) { line.remove(); line = null; }
    }

    Vue.onMounted(() => Vue.nextTick(setup));
    Vue.onBeforeUnmount(cleanup);

    return { root };
  },
  template: `<span ref="root" style="display:none"></span>`,
};

function initializeComponents(app) {
  app.component('copy-btn', copyBtnComponent);
  app.component('code-block', codeBlockComponent);
  app.component("code-inline", codeInlineComponent);
  app.component('multi-col', multiColComponent);
  app.component('highlight-box', highlightBoxComponent);
  app.component("ls-u", lsUComponent);
  app.component("md", mdComponent);
  app.component("leader-line", leaderLineComponent);
}


if (window.app?.component) {
  initializeComponents(app);
}

