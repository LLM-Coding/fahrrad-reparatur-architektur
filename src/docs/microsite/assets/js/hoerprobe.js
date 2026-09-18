/* Hörprobe: Klick auf einen Zeitstempel-Link (a.ts, href = MP3-URL#t=Sekunden) springt im
 * eingebetteten Player derselben Seite an die Stelle. Ohne JavaScript öffnet der Link die MP3
 * direkt an der Stelle (Media Fragment). Progressive Enhancement, kein Rendering von Inhalt. */
(function () {
  if (window.hoerprobeInstalled) { return; }
  window.hoerprobeInstalled = true;
  var active = null;

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
    var t = parseFloat(m[2]);
    // Zweiter Klick auf dieselbe Zeitmarke pausiert, der Player kann außer Sicht sein.
    if (!player.paused && player.dataset.hoerprobeAt === m[2]) { player.pause(); return; }
    pauseOthers(player);
    active = player;
    player.dataset.hoerprobeAt = m[2];
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

  // Nur ein Player läuft: startet einer (per Klick oder Controls), pausieren die anderen.
  function pauseOthers(current) {
    var audios = document.querySelectorAll('audio');
    for (var i = 0; i < audios.length; i++) {
      if (audios[i] !== current && !audios[i].paused) { audios[i].pause(); }
    }
  }
  document.addEventListener('play', function (ev) {
    if (ev.target && ev.target.tagName === 'AUDIO') { active = ev.target; pauseOthers(ev.target); }
  }, true);
})();
