#!/usr/bin/env python3
"""Belegt die Zeitmarken-Links der arc42-Doku mit dem Transkript-Wortlaut, rein statisch.

Laeuft nach link_timestamps.py. Zwei Ergaenzungen je Link link:{mp3-11x}#t=..[..,role=ts f11x]:

1. Tooltip: title="<Wortlaut>" im Attributlist. Einzelstelle t nimmt die Segmente, die [t-3, t+20]
   ueberlappen (max. 280 Zeichen), Spanne a,b die Segmente ueber [a, b] (max. 400 Zeichen).
2. Auszug: Steht ein Spannen-Link in einem normalen Absatz (auch NOTE:-Absatz), folgt dem Absatz
   ein aufklappbarer Block [%collapsible.auszug] mit dem ungekuerzten Wortlaut, eingerahmt von
   // auszug:begin <folge> <a> <b> ... // auszug:end. Spannen in Tabellen, Listen, Block-Titeln und
   Quell-/Passthrough-Bloecken bekommen nur den Tooltip.

3. Startpunkt: Die Wiedergabe beginnt am Anfang des ersten zitierten Segments, nicht an der Zeitmarke,
   damit man hoert, was der Tooltip zeigt. Das Media Fragment #t= zeigt auf die volle Sekunde davor
   (ohne JavaScript), die Rolle start-<sekunden> traegt den genauen Wert fuer hoerprobe.js. Die Zeitmarke
   selbst bleibt als Linktext (14:25) stehen; aus ihr liest ein erneuter Lauf die Belegstelle.

Quelle: transcription/api/11x-whisper1.json (OpenAI whisper-1 verbose_json, Segmente in MP3-Sekunden).
Aufruf:  python3 transcription/analysis/transcript_excerpts.py [--dry-run] [--verbose]
Idempotent: vorhandene title-Attribute werden ersetzt, alte Auszug-Bloecke neu erzeugt; der zweite Lauf
meldet 0 Aenderungen.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOC_GLOBS = ["src/docs/arc42/chapters/*.adoc", "src/docs/arc42/adr/_ADR-*.adoc"]
TRANSCRIPTS = {ep: ROOT / "transcription" / "api" / f"{ep}-whisper1.json" for ep in ("111", "112", "113")}

SINGLE_BEFORE, SINGLE_AFTER = 3, 20
MAX_SINGLE, MAX_SPAN = 280, 400
MARK_BEGIN, MARK_END = "// auszug:begin", "// auszug:end"

# Link ohne oder mit bereits gesetztem title-Attribut; der Tooltip enthaelt weder " noch ]
LINK_RE = re.compile(r'link:\{mp3-(11[123])\}#t=(\d+)(?:,(\d+))?\[([^\]"]*?)(?:,title="[^"\]]*")?\]')
# Belegstelle aus dem Linktext ("14:25" oder "14:25 bis 15:10"), Startpunkt-Rolle eines frueheren Laufs
EVIDENCE_RE = re.compile(r"^(\d+):(\d{2})(?![:\d])")
START_ROLE_RE = re.compile(r" start-[\d.]+")
LIST_RE = re.compile(r"^(?:[*\-.]+ |\d+\. |[^\s].*?:: )")
DELIMITERS = ("----", "++++", "....", "====", "|===")
BAD_CHARS_RE = re.compile(r"[*_`^~{}#\\]")


# Hoerfehler von whisper-1, die im Auszug sinnentstellend waeren. Die Rohdaten bleiben unveraendert.
KORREKTUREN = {
    "112": [
        ("Feinde", "Pfeile"),  # 58:21 "sind die Pfeile eher als Richtung des Informationsflusses"
        ("verbaut die Frage", "beantwortet die Frage"),  # 58:21 und kurz davor, zweimal gleich verhoert
    ],
}


def korrigiert(ep: str, text: str) -> str:
    for falsch, richtig in KORREKTUREN.get(ep, []):
        text = text.replace(falsch, richtig)
    return text


def load_segments():
    segs = {}
    for ep, path in TRANSCRIPTS.items():
        data = json.loads(path.read_text(encoding="utf-8"))
        segs[ep] = [(float(s["start"]), float(s["end"]), korrigiert(ep, s["text"])) for s in data["segments"]]
    return segs


def quoted(segments, lo: float, hi: float):
    """Segmente, die [lo, hi] ueberlappen."""
    return [(start, text) for start, end, text in segments if end > lo and start < hi]


def wording(segments, lo: float, hi: float) -> str:
    """Wortlaut aller Segmente, die [lo, hi] ueberlappen, mit normalisiertem Whitespace."""
    text = re.sub(r"\s+", " ", " ".join(text for _, text in quoted(segments, lo, hi))).strip()
    return BAD_CHARS_RE.sub("", text)


def segment_start(segments, lo: float, hi: float):
    """Beginn des ersten zitierten Segments, None ohne Treffer."""
    found = quoted(segments, lo, hi)
    return found[0][0] if found else None


def shorten(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    cut = text.rfind(" ", 0, limit)
    return text[: cut if cut > 0 else limit].rstrip(" ,;:") + "…"


def tooltip_text(text: str) -> str:
    return text.replace('"', "'").replace("]", ")").replace("[", "(")


def mmss(seconds: int) -> str:
    return f"{seconds // 60:02d}:{seconds % 60:02d}"


def link_with_tooltip(segments, ep: str, start: int, end, attrs: str) -> str:
    """start ist die Belegstelle; Fragment und Rolle zeigen auf den Beginn des zitierten Wortlauts."""
    lo, hi = (start - SINGLE_BEFORE, start + SINGLE_AFTER) if end is None else (start, end)
    text = shorten(wording(segments[ep], lo, hi), MAX_SINGLE if end is None else MAX_SPAN)
    play = segment_start(segments[ep], lo, hi)
    attrs = START_ROLE_RE.sub("", attrs)
    if play is None:
        play = start
    else:
        role = f"role=ts f{ep}"
        if role not in attrs:
            sys.exit(f"Folge {ep}, {mmss(start)}: Rolle '{role}' fehlt im Link [{attrs}]")
        attrs = attrs.replace(role, f"{role} start-{play:.2f}".rstrip("0").rstrip("."), 1)
    frag = str(int(play)) if end is None else f"{int(play)},{end}"
    title = f',title="{tooltip_text(text)}"' if text else ""
    return f"link:{{mp3-{ep}}}#t={frag}[{attrs}{title}]"


def evidence(m) -> int:
    """Belegstelle eines Links aus dem Linktext. Das Fragment taugt nicht: es ist schon verschoben."""
    ev = EVIDENCE_RE.match(m.group(4))
    if not ev:
        sys.exit(f"Linktext ohne Zeitmarke mm:ss: {m.group(0)[:80]}")
    return int(ev.group(1)) * 60 + int(ev.group(2))


def add_tooltips(lines, segments):
    count = 0

    def repl(m):
        nonlocal count
        count += 1
        end = int(m.group(3)) if m.group(3) else None
        return link_with_tooltip(segments, m.group(1), evidence(m), end, m.group(4))

    return [LINK_RE.sub(repl, line) for line in lines], count


def strip_blocks(lines):
    """Entfernt alte Auszug-Bloecke samt der Leerzeile davor, die der Generator gesetzt hat."""
    out, skipping = [], False
    for line in lines:
        if line.startswith(MARK_BEGIN):
            skipping = True
            if out and out[-1] == "":
                out.pop()
            continue
        if skipping:
            if line.startswith(MARK_END):
                skipping = False
            continue
        out.append(line)
    return out


def excerpt_block(segments, ep: str, start: int, end: int):
    text = wording(segments[ep], start, end)
    text = re.sub(r"^[^\wÄÖÜäöü]+", "", text)  # kein AsciiDoc-Sonderzeichen am Zeilenanfang
    title_link = link_with_tooltip(segments, ep, start, end, f"{mmss(start)} bis {mmss(end)},role=ts f{ep}")
    return [
        "",
        f"{MARK_BEGIN} {ep} {start} {end}",
        f".Transkript Folge {ep}, {title_link}",
        "[%collapsible.auszug]",
        "====",
        text,
        "====",
        MARK_END,
    ]


def paragraph_bounds(lines, li: int):
    start = li
    while start > 0 and lines[start - 1].strip() != "":
        start -= 1
    end = li + 1
    while end < len(lines) and lines[end].strip() != "":
        end += 1
    return start, end


def classify(lines, li: int, open_delims) -> str:
    """'absatz' oder der Grund, warum die Spanne nur einen Tooltip bekommt."""
    if open_delims:
        return f"in Block {open_delims[-1]}"
    line = lines[li]
    if line.startswith("|") or " |" in line:
        return "in Tabellenzelle"
    if line.startswith(".") and not line.startswith(". "):
        return "in Block-Titel"
    start, end = paragraph_bounds(lines, li)
    first = start
    while first < end and (lines[first].startswith("[") or lines[first].startswith(".")):
        first += 1
    if first >= end or LIST_RE.match(lines[first]):
        return "in Listenpunkt"
    if any(l.startswith("|") or " |" in l for l in lines[start:end]):
        return "in Tabellenzelle"
    if start >= 1 and lines[start - 1].strip() == "+" or (start >= 2 and lines[start - 2].strip() == "+"):
        return "in Listenpunkt (Fortsetzung)"
    return "absatz"


def add_excerpts(lines, segments, verbose: bool, name: str):
    """Fuegt je Spannen-Link in einem normalen Absatz einen Auszug-Block nach dem Absatz ein."""
    inserts, skipped, open_delims = {}, {}, []
    for li, line in enumerate(lines):
        if line.rstrip() in DELIMITERS:
            delim = line.rstrip()
            if open_delims and open_delims[-1] == delim:
                open_delims.pop()
            else:
                open_delims.append(delim)
            continue
        spans = [(m.group(1), evidence(m), int(m.group(3))) for m in LINK_RE.finditer(line) if m.group(3)]
        if not spans:
            continue
        kind = classify(lines, li, open_delims)
        if kind != "absatz":
            skipped[kind] = skipped.get(kind, 0) + len(spans)
            if verbose:
                print(f"  {name}:{li + 1}: nur Tooltip ({kind}) fuer {len(spans)} Spanne(n)")
            continue
        _, end = paragraph_bounds(lines, li)
        inserts.setdefault(end, []).extend(spans)
    out, count = [], 0
    for li, line in enumerate(lines + [None]):
        for ep, start, end in inserts.get(li, []):
            out += excerpt_block(segments, ep, start, end)
            count += 1
        if line is not None:
            out.append(line)
    return out, count, skipped


def process_file(path: Path, segments, dry_run: bool, verbose: bool):
    original = path.read_text(encoding="utf-8")
    lines = strip_blocks(original.split("\n"))
    lines, tooltips = add_tooltips(lines, segments)
    lines, blocks, skipped = add_excerpts(lines, segments, verbose, path.name)
    result = "\n".join(lines)
    changed = result != original
    if changed and not dry_run:
        path.write_text(result, encoding="utf-8")
    return tooltips, blocks, skipped, changed


def main():
    dry_run, verbose = "--dry-run" in sys.argv, "--verbose" in sys.argv
    segments = load_segments()
    total_tooltips = total_blocks = total_changed = 0
    total_skipped = {}
    for glob in DOC_GLOBS:
        for path in sorted(ROOT.glob(glob)):
            tooltips, blocks, skipped, changed = process_file(path, segments, dry_run, verbose)
            if tooltips or blocks:
                print(f"{path.relative_to(ROOT)}: {tooltips} Tooltips, {blocks} Auszuege"
                      f"{', geaendert' if changed else ', unveraendert'}")
            total_tooltips += tooltips
            total_blocks += blocks
            total_changed += changed
            for k, v in skipped.items():
                total_skipped[k] = total_skipped.get(k, 0) + v
    print(f"gesamt: {total_tooltips} Tooltips, {total_blocks} Auszuege, {total_changed} Dateien geaendert"
          f"{' (dry-run)' if dry_run else ''}")
    for k, v in sorted(total_skipped.items()):
        print(f"  Spannen nur mit Tooltip, {k}: {v}")


if __name__ == "__main__":
    main()
