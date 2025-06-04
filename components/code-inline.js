window.app.component("code-inline", {
  props: ['lang', 'size'],
  setup(props) {
    let classNames = {};
    classNames[props.lang || 'sql'] = true;
    return {classNames};
  },
  /* html */
  template: `
  <pre class="code-inline"><code :class="classNames" :style="{fontSize: (size || 20) + 'pt'}" data-trim><slot></slot></code></pre>
        `,
});

// Columns wrapper (supports 2-3 columns)
app.component('multi-col', {
  template: `<div class="multi-col" :style="{ '--col-count': cols }"><slot></slot></div>`,
  props: { cols: { type: Number, default: 2 } }
});

// Highlight box component
app.component('highlight-box', {
  template: `<div class="fragment highlight-box" :data-fragment-index="index"><slot></slot></div>`,
  props: ['index']
});