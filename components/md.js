window.app.component("md", {
  props: ["md"],
  /*html*/
  template: `
  <p data-markdown>
    <textarea data-template v-text="md"></textarea>
</p>
        `,
});
