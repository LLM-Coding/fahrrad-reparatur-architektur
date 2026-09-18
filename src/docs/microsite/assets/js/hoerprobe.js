/* Hörprobe: Klick auf einen Zeitstempel-Link (a.ts, href = MP3-URL#t=Sekunden) springt im
 * eingebetteten Player derselben Seite an die Stelle. Ohne JavaScript öffnet der Link die MP3
 * direkt an der Stelle (Media Fragment). Progressive Enhancement, kein Rendering von Inhalt.
 *
 * Läuft ein Player, zeigt eine feste Leiste am unteren Rand Folge und Position und bietet
 * Pause und Stopp. Es läuft immer nur ein Player. */
(function () {
  if (window.hoerprobeInstalled) { return; }
  window.hoerprobeInstalled = true;

  var active = null;      // Player, der zuletzt gestartet wurde
  var activeLink = null;  // Zeitmarke, die ihn gestartet hat
  var bar = null, barText = null, barPause = null;

  var css =
    '.hoerprobe-bar{position:fixed;right:1rem;bottom:1rem;z-index:1050;display:flex;' +
    'align-items:center;gap:.6rem;padding:.5rem .8rem;background:#334E68;color:#fff;' +
    'border-radius:.5rem;box-shadow:0 .25rem .75rem rgba(0,0,0,.3);font-size:.95rem;' +
    'font-variant-numeric:tabular-nums}' +
    '.hoerprobe-bar button{border:0;border-radius:.3rem;padding:.25rem .6rem;cursor:pointer;' +
    'background:#F59E0B;color:#1a2a3a;font-weight:600;font-size:.9rem}' +
    '.hoerprobe-bar button.stop{background:transparent;color:#fff;font-size:1.1rem;padding:.1rem .4rem}' +
    'a.ts.ts-active{background:#FDE68A;border-radius:.2rem;padding:0 .2rem}' +
    '@media print{.hoerprobe-bar{display:none}}';

  function episode(el) {
    var m = (el.className || '').match(/\bf(\d{3})\b/);
    return m ? 'Folge ' + m[1] : 'Player';
  }

  function fmt(sec) {
    sec = Math.floor(sec || 0);
    var h = Math.floor(sec / 3600), m = Math.floor(sec % 3600 / 60), s = sec % 60;
    var ms = (m < 10 && h ? '0' : '') + m + ':' + (s < 10 ? '0' : '') + s;
    return h ? h + ':' + ms : ms;
  }

  function ensureBar() {
    if (bar) { return; }
    var style = document.createElement('style');
    style.textContent = css;
    document.head.appendChild(style);
    bar = document.createElement('div');
    bar.className = 'hoerprobe-bar';
    bar.setAttribute('role', 'status');
    bar.hidden = true;
    barText = document.createElement('span');
    barPause = document.createElement('button');
    barPause.type = 'button';
    barPause.addEventListener('click', function () {
      if (!active) { return; }
      if (active.paused) { active.play(); } else { active.pause(); }
    });
    var stop = document.createElement('button');
    stop.type = 'button';
    stop.className = 'stop';
    stop.textContent = '×';
    stop.title = 'Stopp';
    stop.setAttribute('aria-label', 'Stopp');
    stop.addEventListener('click', stopAll);
    bar.appendChild(barText);
    bar.appendChild(barPause);
    bar.appendChild(stop);
    document.body.appendChild(bar);
  }

  function render() {
    if (!bar) { return; }
    if (!active) { bar.hidden = true; return; }
    bar.hidden = false;
    var state = active.paused ? 'pausiert' : 'läuft';
    barText.textContent = episode(active) + ' · ' + fmt(active.currentTime) + ' · ' + state;
    barPause.textContent = active.paused ? 'Weiter' : 'Pause';
  }

  function markLink(link) {
    if (activeLink) { activeLink.classList.remove('ts-active'); }
    activeLink = link;
    if (link) { link.classList.add('ts-active'); }
  }

  function pauseOthers(current) {
    var audios = document.querySelectorAll('audio');
    for (var i = 0; i < audios.length; i++) {
      if (audios[i] !== current && !audios[i].paused) { audios[i].pause(); }
    }
  }

  function stopAll() {
    if (active) { active.pause(); }
    active = null;
    markLink(null);
    render();
  }

  function findPlayer(link, src) {
    var audios = document.querySelectorAll('audio');
    var before = null;
    for (var i = 0; i < audios.length; i++) {
      var a = audios[i];
      if (a.getAttribute('src') !== src) { continue; }
      if (link.compareDocumentPosition(a) & Node.DOCUMENT_POSITION_FOLLOWING) { return a; }
      before = a;
    }
    return before;
  }

  document.addEventListener('click', function (ev) {
    var link = ev.target.closest ? ev.target.closest('a.ts') : null;
    if (!link) { return; }
    var m = (link.getAttribute('href') || '').match(/^(.*\.mp3)#t=([\d.]+)/);
    if (!m) { return; }
    var player = findPlayer(link, m[1]);
    if (!player) { return; }
    ev.preventDefault();
    ensureBar();
    var t = parseFloat(m[2]);
    // Zweiter Klick auf dieselbe laufende Zeitmarke pausiert.
    if (!player.paused && link === activeLink) { player.pause(); return; }
    pauseOthers(player);
    active = player;
    markLink(link);
    player.dataset.hoerprobeAt = m[2];
    render();
    // Bei preload="none" kommen die Metadaten erst nach dem Klick. Hat der Hörer inzwischen
    // einen anderen Player gestartet, verfällt der alte Sprung.
    var seek = function () {
      if (active !== player || player.dataset.hoerprobeAt !== m[2]) { return; }
      player.currentTime = t; player.play();
    };
    if (player.readyState >= 1) { seek(); } else {
      player.addEventListener('loadedmetadata', seek, { once: true });
      player.load();
    }
  });

  // Start über die Controls eines Players: gleiche Regeln, Leiste erscheint.
  document.addEventListener('play', function (ev) {
    var el = ev.target;
    if (!el || el.tagName !== 'AUDIO') { return; }
    ensureBar();
    if (active !== el) { markLink(null); }
    active = el;
    pauseOthers(el);
    render();
  }, true);

  document.addEventListener('pause', function (ev) {
    if (ev.target === active) { render(); }
  }, true);

  document.addEventListener('ended', function (ev) {
    if (ev.target === active) { stopAll(); }
  }, true);

  document.addEventListener('timeupdate', function (ev) {
    if (ev.target === active) { render(); }
  }, true);
})();
