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
  room: (window.seminarConfig && window.seminarConfig.room) || location.pathname,
  hash: '$2b$10$03JZ.k23reA7h65I.CB8/.JUgmfuNiz8J9ltfxtV0HzRi1QnlHT0W',
  autoJoin: true,
};
window.pollConfig = window.pollConfig || {};

// Default chalkboard config — customize via window.chalkboardConfig before mountSlideApp()
window.chalkboardConfig = window.chalkboardConfig || {
  readOnly: false,
  toggleReadOnly: true,
  toggleNotesButton: { left: "70px", bottom: "50px" },
  boardmarkerWidth: 3,
  chalkboardWidth: 3,
  color: '#8be9fd',
  backgroundColor: '#282a36',
  src: null
};

// Default custom controls config
window.customControlsConfig = window.customControlsConfig || {
  toggle: true,
  toggleClass: 'toggled',
  width: 48,
  height: 48,
  offset: 12
};

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
      const el = document.getElementById('seminarStatus');
      const labels = { 1: 'Conectado', 2: 'Aguardando sala...', 3: 'Conectado como participante', 4: 'Conectado como host', 5: 'Conectado como chair' };
      el.textContent = labels[e.status] || 'Desconectado';
      el.style.color = e.status >= 3 ? '#50fa7b' : e.status >= 1 ? '#f1fa8c' : '#6272a4';
    });
}

function initializeReveal() {
  const plugins = [];

  if (window.RevealMarkdown) plugins.push(window.RevealMarkdown);
  if (window.RevealNotes) plugins.push(window.RevealNotes);
  if (window.RevealZoom) plugins.push(window.RevealZoom);
  if (window.RevealHighlight) plugins.push(window.RevealHighlight);
  if (window.RevealMath && window.RevealMath.KaTeX) plugins.push(window.RevealMath.KaTeX);
  if (window.RevealMermaid) plugins.push(window.RevealMermaid);

  // Auto-detect optional plugins
  if (window.RevealSeminar) plugins.push(window.RevealSeminar);
  if (window.RevealPoll) plugins.push(window.RevealPoll);
  if (window.RevealChart) plugins.push(window.RevealChart);
  if (window.RevealCustomControls) plugins.push(window.RevealCustomControls);
  if (window.RevealChalkboard) plugins.push(window.RevealChalkboard);
  if (window.Reveald3) plugins.push(window.Reveald3);

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
  if (window.reveald3Config) config.reveald3 = window.reveald3Config;

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
