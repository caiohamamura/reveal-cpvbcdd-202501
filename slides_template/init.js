/**
 * Shared Reveal.js + Vue initialization for all slide decks.
 *
 * Usage in any slide HTML file — replace the inline <script> block with:
 *
 *   <script>
 *     window.app = mountSlideApp();
 *   </script>
 *
 * Optional plugins (auto-detected when their <script> tags are included):
 *   - RevealSeminar + RevealPoll + RevealCustomControls + RevealChalkboard + RevealChart
 *   - Requires socket.io loaded before seminar plugin
 *   - Seminar config is hardcoded here (same server/room for all decks)
 */

window.inTransition = false;

// Default seminar config (used by all decks — same server, room derived from path)
// Override window.seminarConfig BEFORE calling mountSlideApp() to customize room
window.seminarConfig = {
  server: 'https://seminar.hamacorps.work/',
  room: window.seminarConfig?.room || location.pathname,
};
window.pollConfig = {};

// Seminar panel HTML (injected by injectSeminarPanel)
const SEMINAR_PANEL_HTML = `
<button class="seminar-toggle" id="seminarToggleBtn" onclick="document.getElementById('seminarPanel').classList.toggle('open');document.getElementById('seminarPassword').focus()">&#9776;</button>
<div id="seminarPanel" class="seminar-panel">
  <div id="seminarHost">
    <label><strong>Host (apresentador)</strong></label>
    <form action="" onsubmit="event.preventDefault();RevealSeminar.open_or_join_room(document.getElementById('seminarPassword').value);setTimeout(() => {document.getElementById('seminarPanel').classList.toggle('open');}, 1000)">
      <input type="password" id="seminarPassword" placeholder="Senha do host"/>
    </form>
    <button class="btn-host"
            onclick="RevealSeminar.open_or_join_room(document.getElementById('seminarPassword').value)">Host</button>
    <button class="btn-leave"
            onclick="RevealSeminar.close_room(document.getElementById('seminarPassword').value)">Fechar sala</button>
  </div>
  <hr style="border-color: #44475a; margin: 12px 0;" />
  <div class="seminar-status" id="seminarStatus">Desconectado</div>
</div>
`;

function injectSeminarPanel() {
  document.body.insertAdjacentHTML('afterbegin', SEMINAR_PANEL_HTML);
  document.addEventListener('seminar', function (e) {
    if (!e.detail) return;
    const el = document.getElementById('seminarStatus');
    if (el) {
      el.textContent = e.detail.connected
        ? 'Conectado como ' + (e.detail.isHost ? 'host' : 'participante')
        : 'Desconectado';
      el.style.color = e.detail.connected ? '#50fa7b' : '#ff5555';
    }
  });
}

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
  injectSeminarPanel();
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
