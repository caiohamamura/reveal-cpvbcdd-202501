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

const codeBlockComponent = {
  setup(props) {
    const btnMsg = Vue.ref('Copiar');
    const pre = Vue.useTemplateRef('pre');
    function copiar() {
      const conteudo = pre.value?.textContent;

      navigator.clipboard.writeText(conteudo || '')
        .then(() => {
          btnMsg.value = 'Copiado!';
          setTimeout(() => {
            btnMsg.value = 'Copiar';
          }, 2000);
        })
        .catch(err => {
          console.error('Erro ao copiar:', err);
        });
    }
    return { copiar, btnMsg };
  },
  style: {
    width: 'max-content',
  },
  /*html*/
  template: `
  <div style="position: relative; margin: 0; padding: 0;display:block; width: min-content;">
  <pre ref="pre" class="code-wrapper" style="min-width: max-content; padding:0; margin: 0;"><code data-trim v-bind="$attrs" v-html="$slots.default().map(el=>el.children).join('')"></code></pre>
  <button class="copy-button" @click=copiar>{{btnMsg}}</button>
  </div>
  `,
}

const copyBtnComponent = {
  setup() {
    const btn = Vue.ref('btn');

    Vue.onMounted(function() {
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

function initializeComponents(app) {
  app.component('copy-btn', copyBtnComponent);
  app.component('code-block', codeBlockComponent);
  app.component("code-inline", codeInlineComponent);
  app.component('multi-col', multiColComponent);
  app.component('highlight-box', highlightBoxComponent);
  app.component("ls-u", lsUComponent);
  app.component("md", mdComponent);
}


if (window.app?.component) {
  initializeComponents(app);
}

