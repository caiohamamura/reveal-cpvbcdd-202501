// Evaluate inside a loaded Reveal.js slide deck to verify zero 960x700 overflow
// and zero broken images across every horizontal and vertical slide.
(() => {
  const deck = window.deck;
  if (!deck) return { error: 'window.deck not initialized' };
  const cw = 960;
  const ch = 700;
  const indices = [];

  document.querySelectorAll('.slides > section').forEach((h, hi) => {
    const verts = h.querySelectorAll(':scope > section');
    if (verts.length) verts.forEach((_, vi) => indices.push([hi, vi]));
    else indices.push([hi, 0]);
  });

  const results = [];
  for (const [h, v] of indices) {
    deck.slide(h, v);
    const s = deck.getCurrentSlide();
    const sRect = s.getBoundingClientRect();
    const scale = deck.getScale();
    let maxRight = 0;
    let maxBottom = 0;

    s.querySelectorAll('img, table, pre, div, ul, ol, p, blockquote').forEach((el) => {
      const r = el.getBoundingClientRect();
      if (!r.width || !r.height) return;
      maxRight = Math.max(maxRight, (r.right - sRect.left) / scale);
      maxBottom = Math.max(maxBottom, (r.bottom - sRect.top) / scale);
    });

    results.push({
      h,
      v,
      title: (s.querySelector('h2, h1') || {}).textContent?.trim().slice(0, 45) || '(sem título)',
      maxRight: Math.round(maxRight),
      maxBottom: Math.round(maxBottom),
    });
  }

  deck.slide(0, 0);

  const brokenImages = [...document.querySelectorAll('img')]
    .filter((img) => img.complete && !img.naturalWidth)
    .map((img) => img.getAttribute('src'));

  return {
    total: results.length,
    over: results.filter((r) => r.maxBottom > ch + 10 || r.maxRight > cw + 10),
    brokenImages,
  };
})();
