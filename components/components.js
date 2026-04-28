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
  props: {
    cols: {
      type: [Number, String, Array],
      default: '1fr 1fr'
    },
    gap: Number
  },
  computed: {
    template() {
      const c = this.cols;
      if (Number(c) > 0) {
        return `repeat(${c}, 1fr)`
      }

      return Array.isArray(c)
        ? c.join(' ')
        : c
    }
  },
  template: `
    <div
      class="multi-col"
      :style="{ gridTemplateColumns: template, gap: gap }"
    >
      <slot></slot>
    </div>
  `
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
      li.style.fontSize = (this.fontSize || "24") + "pt";
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
    const raw = el.textContent;
    window.__codeBlockRaw[id] = escapeHtml(stripIndentation(raw));
    el.setAttribute('data-cb-id', id);
  });
})();

function getCodeWithLineBreaks(preEl) {
  const lines = preEl.querySelectorAll('.hljs-ln-code')
  if (lines.length) {
    return Array.from(lines)
      .map(line => line.textContent)
      .join('\n')
  }
  return preEl.textContent;
}

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
      const conteudo = getCodeWithLineBreaks(pre.value);

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
    const btn = Vue.ref(null)

    function extractCode(codeEl) {
      if (!codeEl) return ''

      // Case 1: highlight.js with line numbers (table)
      const lines = codeEl.querySelectorAll('tr')
      if (lines.length > 0) {
        return [...lines]
          .map(line => [...line.querySelectorAll("td,th")].map(e => e.innerHTML).join('\t'))
          .join('\n')
      }

      // Case 2: normal <code>
      return codeEl.textContent || ''
    }

    async function copiar() {
      const container = btn.value?.previousSibling
      const codeEl = container
      console.log(codeEl);

      const text = extractCode(codeEl)

      try {
        await navigator.clipboard.writeText(text)

        btn.value.textContent = 'Copiado!'
        setTimeout(() => {
          btn.value.textContent = 'Copiar'
        }, 2000)

      } catch (err) {
        console.error('Erro ao copiar:', err)
      }
    }

    return { copiar, btn }
  },

  template: `
    <button
      ref="btn"
      class="copy-button btn color-black"
      @click="copiar"
    >
      Copiar
    </button>
  `
}

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
    to: { type: String, required: true },
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
    let animations = [];
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
      const startEl = document.querySelector(props.from);
      const endEl = document.querySelector(props.to);
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
      animations.push(setTimeout(() => {
        if (!isRevealed()) return;
        const l = ensureLine();
        if (!l) return;
        props.animated ? l.show('draw') : l.show();
      }, 100));
    }

    function hide() {
      if (!line) return;
      props.animated ? line.hide('draw') : line.hide();
    }

    let observer = null;

    function hasOutInTree(el) {
      while (el) {
        if (
          el.classList &&
          [...el.classList].some(cls => cls.endsWith('out'))
        ) {
          return true;
        }
        el = el.parentElement;
      }
      return false;
    }

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
        for (animation of animations) {
          clearTimeout(animation); 
        }
        animations = [];
        
        const section = root.value.closest("section");

        if (!section.classList.contains("present")) {
          line?.remove();
          line = null;
          return;
        }

        const isCurrent = root.value.classList.contains('current-fragment');
        const hasOut = hasOutInTree(root.value);

        // 🔴 THE RULE YOU WANT
        if (hasOut && !isCurrent) {
          hide();
          return;
        }

        // fallback (your original behavior)
        const isVisible = root.value.classList.contains('visible');
        if (isVisible || !root.value.closest(".fragment")) {
          show();
        } else {
          hide();
        }
      });
      observer.observe(root.value.closest("section"), {
        attributes: true,
        attributeFilter: ['class']
      });
      const fragmentEl = root.value.closest(".fragment");

      if (fragmentEl) {
        observer.observe(fragmentEl, {
          attributes: true,
          attributeFilter: ['class']
        });
      }
    }

    function cleanup() {
      if (observer) { observer.disconnect(); observer = null; }
      if (line) { line.remove(); line = null; }
    }

    Vue.onMounted(() => {
      Vue.nextTick(setup)
    });
    Vue.onBeforeUnmount(cleanup);

    return { root };
  },
  template: `<span ref="root" style="display:none"></span>`,
};

const pollQuestionComponent = {
  props: {
    id: { type: String, required: true },
    title: { type: String, default: '' },
    question: { type: String, default: '' },
    options: { type: Array, required: true },
    answer: { type: String, default: '' },
    answerText: { type: String, default: '' },
  },
  mounted() {
    const el = this.$el;
    const results = el.querySelector('.poll-results');
    const pollEl = el.querySelector('.poll');

    const highlightAnswer = () => {
      if (!this.answer || !pollEl) return;
      // Highlight the correct button
      pollEl.querySelectorAll('button').forEach(btn => {
        btn.style.outline = '';
        btn.style.fontWeight = '';
      });
      const correctBtn = pollEl.querySelector(`button[data-value="${this.answer}"]`);
      if (correctBtn) {
        correctBtn.style.outline = '3px solid #50fa7b';
        correctBtn.style.fontWeight = 'bold';
      }
      // Highlight the correct bar
      if (results) {
        results.querySelectorAll('.poll-bar-fill').forEach(bar => {
          const span = bar.querySelector('[data-value]');
          if (span && span.getAttribute('data-value') === this.answer) {
            bar.style.background = '#50fa7b';
          }
        });
      }
    };

    if (results) {
      const updateBars = () => {
        const bars = results.querySelectorAll('.poll-bar-fill');
        let total = 0;
        const counts = [];
        bars.forEach(bar => {
          const span = bar.querySelector('[data-value]');
          const count = parseInt(span.textContent) || 0;
          counts.push(count);
          total += count;
        });
        bars.forEach((bar, i) => {
          const pct = total > 0 ? Math.round(counts[i] / total * 100) : 0;
          bar.style.height = Math.max(pct, 8) + '%';
          bar.style.background = pct > 0 && counts[i] === Math.max(...counts) ? '#50fa7b' : '#bd93f9';
        });
      };

      const observer = new MutationObserver(updateBars);
      results.querySelectorAll('[data-value]').forEach(span => {
        observer.observe(span, { childList: true, characterData: true, subtree: true });
      });
    }

    // Watch answer fragment for "visible" class to highlight correct answer
    const answerRef = this.$refs.answerRef;
    if (answerRef) {
      const answerObserver = new MutationObserver(() => {
        if (answerRef.classList.contains('visible')) {
          highlightAnswer();
        } else {
          // De-highlight
          if (pollEl) {
            pollEl.querySelectorAll('button').forEach(btn => {
              btn.style.outline = '';
              btn.style.fontWeight = '';
            });
          }
          if (results) {
            results.querySelectorAll('.poll-bar-fill').forEach(bar => {
              bar.style.background = '#bd93f9';
            });
          }
        }
      });
      answerObserver.observe(answerRef, { attributes: true, attributeFilter: ['class'] });
    }
  },
  /*html*/
  template: `
  <div>
      <h3 v-if="title">{{ title }}</h3>
      <p v-if="question">{{ question }}</p>
      <multi-col>
      <div class="poll" :data-poll="id">
        <button v-for="opt in options" :data-value="opt.value">
          {{ String(opt.value).toUpperCase() }}) {{ opt.label }}
        </button>
      </div>
      <div class="results poll-results" :data-poll="id" style="display:flex;justify-content:space-evenly;align-items:end;height:100%">
        <div class="poll-bar" v-for="opt in options" style="display:flex;flex-flow:column;">
          <div class="poll-bar-track">
            <div class="poll-bar-fill" :style="{height:'0%'}">
              <span :data-value="opt.value">0</span>
            </div>
          </div>
          <span class="poll-bar-label">{{ String(opt.value).toUpperCase() }}</span>
        </div>
      </div> 
      </multi-col>
      <p>Total: <span class="voters" :data-poll="id">0</span> votos</p>
      
      <div v-if="answer" ref="answerRef" class="fragment" data-fragment-index="1" style="background: #50fa7b20; border: 1px solid #50fa7b; padding: 8px; margin-top: 8px; border-radius: 8px;">
        <span style="color: #50fa7b;">
          Resposta: <strong>{{ String(answer).toUpperCase() }}</strong><span v-if="answerText"> — {{ answerText }}</span>
        </span>
      </div>
    </div>
  `,
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
  app.component('poll-question', pollQuestionComponent);
}


if (window.app?.component) {
  initializeComponents(app);
}

