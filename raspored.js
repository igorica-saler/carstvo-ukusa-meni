// Raspoređuje prazan prostor strane na redove artikala, da svaka strana bude ravnomerno popunjena.
(function () {
  const MM = 96 / 25.4;
  function layout() {
    document.querySelectorAll('.page.inner').forEach(page => {
      const foot = page.querySelector('.runfoot');
      const blocks = page.querySelectorAll('.sec, .cta');
      const last = blocks[blocks.length - 1];
      const free = foot.getBoundingClientRect().top - last.getBoundingClientRect().bottom - 8 * MM;
      if (free <= 0) return;
      const secs = page.querySelectorAll('.sec');
      let rows = 0;
      page.querySelectorAll('.items').forEach(g => rows += g.children.length);
      // deo prostora ide u razmak između sekcija, ostatak u redove
      const gapExtra = Math.min(free * 0.25 / secs.length, 10 * MM);
      const perRow = Math.min((free - gapExtra * secs.length) / Math.max(rows, 1), 4 * MM);
      secs.forEach(s => s.style.marginTop = `calc(7mm + ${gapExtra}px)`);
      page.querySelectorAll('.items .item').forEach(it => {
        it.style.paddingTop = `calc(1.8mm + ${perRow / 2}px)`;
        it.style.paddingBottom = `calc(1.8mm + ${perRow / 2}px)`;
      });
      const cta = page.querySelector('.cta');
      if (cta) cta.style.marginTop = `calc(7mm + ${gapExtra}px)`;
    });
  }
  document.addEventListener('DOMContentLoaded', () => document.fonts.ready.then(layout));
})();
