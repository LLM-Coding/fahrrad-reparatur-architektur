#!/usr/bin/env python3
"""Verlinkt Zeitmarken (mm:ss) in der arc42-Doku auf die Podcast-MP3s der Folgen 111 bis 113
und bettet je Datei und Folge einen Player ("Hoerprobe") ein.

Die Zeitmarken stammen aus genau diesen MP3s (transcription/audio/11x.mp3), deshalb ist kein
Versatz noetig. Link-Form: link:<mp3-url>#t=<sekunden>[16:46,role=ts f111]; Spannen bekommen
#t=<start>,<ende>. Ein Klick oeffnet die MP3 an der Stelle (Media Fragment); mit JavaScript
(src/docs/microsite/assets/js/hoerprobe.js) springt der Player auf der Seite dorthin.

Aufruf:  python3 transcription/analysis/link_timestamps.py [--dry-run] [--verbose]
Idempotent: bereits gesetzte Links bleiben, der Hoerprobe-Block wird je Lauf neu erzeugt.
Aeltere YouTube-Zeitmarken-Links (link:https://www.youtube.com/watch?v=..&t=..s[mm:ss]) werden
in die MP3-Form umgeschrieben.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOC_GLOBS = ["src/docs/arc42/chapters/*.adoc", "src/docs/arc42/adr/_ADR-*.adoc"]

MP3_URLS = {
    "111": "https://1evriw.podcaster.de/software-architektur-im-stream/media/WirBauenEineSoftwareArchitektur-xcf.mp3",
    "112": "https://1evriw.podcaster.de/software-architektur-im-stream/media/WirBauenEineSoftwareArchitekturStrukturDerLoesung.mp3",
    "113": "https://1evriw.podcaster.de/software-architektur-im-stream/media/Qualitaeten_nicht-funktionale_Anforderungen_umsetzen_-_Wir_bauen_eine_Software-Architektur.mp3",
}
EPISODE_PAGES = {
    "111": "https://software-architektur.tv/2022/02/25/folge111.html",
    "112": "https://software-architektur.tv/2022/03/11/folge112.html",
    "113": "https://software-architektur.tv/2022/03/25/folge113.html",
}
YOUTUBE_IDS = {"111": "-FCkp1aJzRY", "112": "K512HtCbb2Q", "113": "oteC-_RZzPk"}
# Gemessener Versatz Video-Zeit minus MP3-Zeit in Sekunden (Kreuzkorrelation der Huellkurven, NCC > 0.9
# an fuenf Stellen je Folge, per Whisper bestaetigt, 2026-09-18). Fuer die MP3-Links nicht noetig,
# nur fuer YouTube-Links mit Zeitmarke: t_video = t_mp3 + OFFSET.
VIDEO_OFFSETS = {"111": -24.99, "112": -26.60, "113": -25.98}
ADR_REF_RE = re.compile(r"adr-(\d{3})")
# "Folge 113, 08:24" in der Quelle-Zeile, auch wenn die Zeitmarke schon verlinkt ist
QUELLE_TS_RE = re.compile(r"Folge (11[123]), (?:link:\{mp3-11[123]\}#t=[0-9,]+\[)?\d{1,3}:\d{2}")


def quelle_episodes(line: str):
    """Folgen, denen in der Quelle-Zeile Zeitmarken folgen (nicht blosse Board-Verweise)."""
    return sorted(set(QUELLE_TS_RE.findall(line)))
# Kapitel, in denen Zeitmarken ohne Folgenangabe Folge 111 meinen (steht so im Kapitelkopf)
DEFAULT_EPISODE_FILES = {
    "01_introduction_and_goals.adoc": "111",
    "02_architecture_constraints.adoc": "111",
    "03_context_and_scope.adoc": "111",
}
SCRIPT_TAG = '<script src="/js/hoerprobe.js" defer></script>'  # Theme schreibt src="/ auf rootpath um
MARK_BEGIN, MARK_END = "// hoerprobe:begin (generiert von transcription/analysis/link_timestamps.py)", "// hoerprobe:end"

TS = r"(?<![\d:])(\d{1,3}):(\d{2})(?![\d:])"
TS_RE = re.compile(TS + r"(?:( bis )" + TS + r")?")
FOLGE_RE = re.compile(r"Folge (11[123])\b")
LINK_RE = re.compile(r"link:\S+?\[[^\]]*\]")  # auch link:{mp3-111}#t=..[..]
URL_RE = re.compile(r"https?://\S+")
OLD_MP3_RE = re.compile(r"link:(https?://\S+?\.mp3)#t=")
OLD_YT_RE = re.compile(r"link:https://www\.youtube\.com/watch\?v=([^&\[]+)&t=\d+s\[([^\]]*)\]")
MP3_LINK_RE = re.compile(r"link:(https?://\S+?\.mp3)#t=")
SENT_SPLIT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-ZÄÖÜ\"„(])")


def to_seconds(mm: str, ss: str) -> int:
    return int(mm) * 60 + int(ss)


def mp3_link(episode: str, text: str, start: int, end=None) -> str:
    # URL als Attribut: Asciidoctor wendet die Kursiv-Substitution (_..._) vor der Makro-Substitution an,
    # die Unterstriche in der MP3-URL wuerden sonst zu <em> im href. Attribute werden erst danach ersetzt.
    frag = f"{start}" if end is None else f"{start},{end}"
    return f"link:{{mp3-{episode}}}#t={frag}[{text},role=ts f{episode}]"


ATTR_RE = re.compile(r"^ifndef::mp3-11[123]\[")


def attribute_lines(episodes):
    return [f"ifndef::mp3-{ep}[:mp3-{ep}: {MP3_URLS[ep]}]" for ep in sorted(episodes)]


def insert_attributes(lines, episodes):
    """Definiert {mp3-11x} im Kopf der Datei (nach ifndef::imagesdir, sonst nach dem Attributblock)."""
    lines = [l for l in lines if not ATTR_RE.match(l)]
    if not episodes:
        return lines
    at = next((i + 1 for i, l in enumerate(lines) if l.startswith("ifndef::imagesdir")), None)
    if at is None:
        at = 0
        while at < len(lines) and (lines[at].startswith(":") or lines[at].startswith("ifndef::")):
            at += 1
    lines[at:at] = attribute_lines(episodes)
    return lines


def masked(text: str) -> str:
    """Blendet bestehende Links und URLs aus, damit ihre Zahlen nicht als Zeitmarke zaehlen."""
    out = text
    for rx in (LINK_RE, URL_RE):
        out = rx.sub(lambda m: " " * len(m.group(0)), out)
    return out


def paragraphs(lines):
    """(start, end) der Absaetze: Bloecke ohne Leerzeile; Tabellenzellen (Zeilen mit '|') einzeln."""
    blocks, start = [], None
    for i, line in enumerate(lines + [""]):
        is_cell = line.startswith("|")
        if line.strip() == "" or is_cell:
            if start is not None:
                blocks.append((start, i))
                start = None
            if is_cell:
                blocks.append((i, i + 1))
        elif start is None:
            start = i
    return blocks


def preceding_mention(text: str, pos: int):
    hits = [m for m in FOLGE_RE.finditer(text) if m.end() <= pos]
    return hits[-1].group(1) if hits else None


def sentence_span(line: str, pos: int):
    start = 0
    for m in SENT_SPLIT_RE.finditer(line):
        if m.end() <= pos:
            start = m.end()
        else:
            return start, m.start()
    return start, len(line)


def adr_episodes():
    """ADR-Nummer -> Folge aus der Quelle-Zeile des ADR (nur wenn dort genau eine Folge Zeitmarken hat)."""
    out = {}
    for path in ROOT.glob("src/docs/arc42/adr/_ADR-*.adoc"):
        num = path.name[5:8]
        for l in path.read_text(encoding="utf-8").split("\n"):
            if l.startswith("| Quelle"):
                eps = quelle_episodes(l)
                if len(eps) == 1:
                    out[num] = eps[0]
    return out


ADR_EPISODES = adr_episodes()


def previous_paragraph(lines, para, blocks):
    prev = [b for b in blocks if b[1] <= para[0]]
    return prev[-1] if prev else None


def episode_for(lines, para, li, pos, default, quelle_eps, blocks):
    """Folge fuer eine Zeitmarke: Satz, Quelle-Zeile (ADR), Absatz/Zelle, ADR-Verweis im Absatz,
    vorhergehender Absatz (nur Kapitel ohne Standard), Kapitel-Standard."""
    line = masked(lines[li])
    s0, s1 = sentence_span(line, pos)
    ep = preceding_mention(line[s0:s1], pos - s0)
    if ep:
        return ep, "satz"
    if len(quelle_eps) == 1:
        return quelle_eps[0], "quelle"
    para_text = "\n".join(masked(l) for l in lines[para[0]:para[1]])
    abs_pos = sum(len(masked(l)) + 1 for l in lines[para[0]:li]) + pos
    para_eps = sorted(set(FOLGE_RE.findall(para_text)))
    ep = preceding_mention(para_text, abs_pos)
    if default:
        if ep and len(para_eps) == 1:
            return ep, "absatz"
        return default, "standard"
    if ep:
        return ep, "absatz"
    adr_eps = sorted({ADR_EPISODES[n] for n in ADR_REF_RE.findall(para_text) if n in ADR_EPISODES})
    if len(adr_eps) == 1:
        return adr_eps[0], "adr-verweis"
    prev = previous_paragraph(lines, para, blocks)
    if prev:
        prev_eps = sorted(set(FOLGE_RE.findall("\n".join(masked(l) for l in lines[prev[0]:prev[1]]))))
        if len(prev_eps) == 1:
            return prev_eps[0], "vorabsatz"
    return None, "mehrdeutig"


def convert_old_youtube_links(line: str) -> str:
    id_to_ep = {v: k for k, v in YOUTUBE_IDS.items()}

    def repl(m):
        ep, text = id_to_ep.get(m.group(1)), m.group(2)
        t = TS_RE.fullmatch(text)
        if not ep or not t:
            return m.group(0)
        start = to_seconds(t.group(1), t.group(2))
        end = to_seconds(t.group(4), t.group(5)) if t.group(3) else None
        return mp3_link(ep, text, start, end)

    line = OLD_YT_RE.sub(repl, line)
    url_to_ep = {v: k for k, v in MP3_URLS.items()}
    return OLD_MP3_RE.sub(lambda m: f"link:{{mp3-{url_to_ep[m.group(1)]}}}#t=" if m.group(1) in url_to_ep else m.group(0), line)


def strip_block(lines):
    """Entfernt einen frueher erzeugten Hoerprobe-Block (Markerzeilen inklusive)."""
    out, skip = [], False
    for l in lines:
        if l.strip() == MARK_BEGIN:
            skip = True
            continue
        if skip and l.strip() == MARK_END:
            skip = False
            continue
        if not skip:
            out.append(l)
    while out and out[-1].strip() == "":
        out.pop()
    return out


def hoerprobe_block(episodes, with_script: bool):
    block = [MARK_BEGIN]
    for ep in sorted(episodes):
        # Passthrough statt audio::-Makro: preload="none", damit die Player nichts vorladen; im
        # Passthrough gibt es keine Substitution, die URL darf also wörtlich stehen.
        block += [
            "",
            "++++",
            '<figure class="hoerprobe">',
            f"<figcaption>Hörprobe Folge {ep}</figcaption>",
            f'<audio src="{MP3_URLS[ep]}" controls preload="none" class="player f{ep}"></audio>',
            "</figure>",
            "++++",
            "",
            f"link:{EPISODE_PAGES[ep]}[Folge {ep} auf software-architektur.tv] und "
            f"link:https://www.youtube.com/watch?v={YOUTUBE_IDS[ep]}[Video auf YouTube]. "
            "Die Zeitmarken im Text springen im Player an die Stelle.",
        ]
    if with_script:
        block += ["", "++++", SCRIPT_TAG, "++++"]
    block += ["", MARK_END]
    return block


def process_file(path: Path, dry_run: bool):
    lines = strip_block(path.read_text(encoding="utf-8").split("\n"))
    lines = [convert_old_youtube_links(l) for l in lines]
    default = DEFAULT_EPISODE_FILES.get(path.name)
    quelle_eps = []
    for l in lines:
        if l.startswith("| Quelle"):
            quelle_eps = quelle_episodes(l)
    para_of = {}
    blocks = paragraphs(lines)
    for p in blocks:
        for i in range(p[0], p[1]):
            para_of[i] = p
    count, ambiguous, samples = 0, [], []
    for li, line in enumerate(lines):
        m_line = masked(line)
        if not TS_RE.search(m_line):
            continue
        pieces, last = [], 0
        for m in TS_RE.finditer(m_line):
            ep, rule = episode_for(lines, para_of.get(li, (li, li + 1)), li, m.start(), default, quelle_eps, blocks)
            text = line[m.start():m.end()]
            if ep is None:
                ambiguous.append(f"{path.name}:{li + 1}: {text}  |  {line.strip()[:90]}")
                continue
            start = to_seconds(m.group(1), m.group(2))
            end = to_seconds(m.group(4), m.group(5)) if m.group(3) else None
            pieces += [line[last:m.start()], mp3_link(ep, text, start, end)]
            last = m.end()
            count += 1
            samples.append((ep, rule, text))
        pieces.append(line[last:])
        lines[li] = "".join(pieces)
    episodes = set(re.findall(r"role=ts f(11[123])\]", "\n".join(lines)))
    is_chapter = path.parent.name == "chapters"
    if is_chapter:
        # alle drei Attribute, weil eingebundene ADR-Partials (Kapitel 09) andere Folgen zitieren koennen
        lines = insert_attributes(lines, set(MP3_URLS) if episodes or any(l.startswith("include::") for l in lines) else set())
    if episodes:
        block = hoerprobe_block(episodes, with_script=is_chapter)
        first_include = next((i for i, l in enumerate(lines) if l.startswith("include::")), None)
        if is_chapter and first_include is not None:
            lines[first_include:first_include] = block + [""]
        else:
            lines += [""] + block
        lines.append("")
        if not dry_run:
            path.write_text("\n".join(lines), encoding="utf-8")
    return count, ambiguous, samples, sorted(episodes)


def main():
    dry_run, verbose = "--dry-run" in sys.argv, "--verbose" in sys.argv
    total, all_ambiguous = 0, []
    for glob in DOC_GLOBS:
        for path in sorted(ROOT.glob(glob)):
            n, amb, samples, eps = process_file(path, dry_run)
            total += n
            all_ambiguous += amb
            if n or amb or eps:
                print(f"{path.relative_to(ROOT)}: {n} neue Links, {len(amb)} mehrdeutig, Player: {', '.join(eps)}")
                if verbose:
                    for ep, rule, text in samples:
                        print(f"    {ep} ({rule}) {text}")
    print(f"gesamt: {total} Links gesetzt{' (dry-run)' if dry_run else ''}")
    if all_ambiguous:
        print("nicht verlinkt (Folge nicht eindeutig):")
        for a in all_ambiguous:
            print("  " + a)


if __name__ == "__main__":
    main()
