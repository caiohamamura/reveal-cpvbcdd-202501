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
 *
 * Optional plugins (auto-detected when their <script> tags are included):
 *   - RevealSeminar + RevealPoll + RevealCustomControls
 *   - Requires socket.io loaded before seminar plugin
 *   - Configure via window.seminarConfig, window.pollConfig, etc.
 */

window.inTransition = false;

function initializeReveal() {
  const plugins = [RevealMarkdown, RevealNotes, RevealZoom, RevealHighlight, RevealMath.KaTeX, RevealMermaid];

  // Auto-detect optional plugins
  if (window.RevealSeminar) plugins.push(RevealSeminar);
  if (window.RevealPoll) plugins.push(RevealPoll);
  if (window.RevealChart) plugins.push(RevealChart);
  if (window.RevealCustomControls) plugins.push(RevealCustomControls);
  if (window.RevealChalkboard) plugins.push(RevealChalkboard);

  const config = {
    controls: true,
    controlsLayout: 'edges',
    hash: true,
    respondToHashChanges: true,
    history: true,
    keyboardCondition: 'focused',
    slideNumber: 'h.v',
    navigationMode: 'linear',
    plugins: plugins,
  };

  // Merge optional plugin configs from HTML
  if (window.seminarConfig) config.seminar = window.seminarConfig;
  if (window.pollConfig) config.poll = window.pollConfig;
  if (window.customControlsConfig) config.customcontrols = window.customControlsConfig;
  if (window.chartConfig) config.chart = window.chartConfig;
  if (window.chalkboardConfig) config.chalkboard = window.chalkboardConfig;

  window.deck = new Reveal(document.querySelector('.reveal'), config);
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
