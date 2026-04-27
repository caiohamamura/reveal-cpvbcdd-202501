/**
 * Shared Reveal.js + Vue initialization for all slide decks.
 *
 * Usage in any slide HTML file — replace the inline <script> block with:
 *
 *   <script>
 *     const app = Vue.createApp({ setup() { Vue.onMounted(() => { initializeReveal(); }); return {}; } });
 *     initializeComponents(app);
 *     initializeHeader(app);
 *     app.mount("#app");
 *   </script>
 *
 * Or simply:
 *
 *   <script>
 *     window.app = mountSlideApp();
 *   </script>
 */

window.inTransition = false;

function initializeReveal() {
  window.deck = new Reveal(document.querySelector('.reveal'), {
    controls: true,
    controlsLayout: 'edges',
    hash: true,
    respondToHashChanges: true,
    history: true,
    keyboardCondition: 'focused',
    slideNumber: 'h.v',
    navigationMode: 'linear',
    plugins: [RevealMarkdown, RevealNotes, RevealZoom, RevealHighlight, RevealMath.KaTeX, RevealMermaid],
  });
  deck.initialize();

  let animations = [];
  deck.on('slidetransitionend', event => {
    for (let animation of animations) {
      clearTimeout(animation);
    }
    animations = [];

    const auto = event.currentSlide.querySelectorAll('.fragment.auto');
    for (const el of auto) {
      animations.push(setTimeout(() => deck.nextFragment(), 100));
    }
  });
}

function mountSlideApp() {
  const app = Vue.createApp({
    setup() {
      Vue.onMounted(() => {
        initializeReveal();
      });
      return {};
    },
  });
  initializeComponents(app);
  initializeHeader(app);
  app.mount('#app');
  return app;
}
