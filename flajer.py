# Flajer Carstvo Ukusa 2026 — A4 vodoravno, roll fold na 3 panela (100 | 100 | 97 mm)
# Koncept „Vaga": sve je po kilogramu, pa je i dizajn po meri — skala vage na naslovnoj,
# pravi milimetarski lenjir uz gornju ivicu unutrašnjosti, tabela „koliko treba" za planiranje.
# Strana 1 (spolja): [flap 97 | zadnja korica 100 | prednja korica 100]
# Strana 2 (unutra): [unutra-levo 100 | unutra-sredina 100 | unutra-desno 97]
# Čitanje: korica → (unutra-levo + flap) → cela unutrašnjost 01→08
import math
import subprocess
import sys

from meni_data import *  # noqa

TERRA, PAPER2, LINE, MUTED = "#B8552E", "#EEE7D7", "#CFC4AE", "#5F6B63"
HAIR = "rgba(30,51,40,.22)"
BLEED = 3 if "--bleed" in sys.argv else 0
QR_SVG = (ROOT / "docs" / "qr.svg").read_text(encoding="utf-8")

# Orijentacione količine po osobi (grama) — PROVERITI SA VLASNIKOM pre štampe (meso/riba 350 g potvrdio vlasnik 2026-10-15)
PLAN = [
    ("Predjelo", 80, "g"),
    ("Finger food", 120, "g"),
    ("Meso ili riba", 350, "g"),
    ("Prilozi", 150, "g"),
    ("Salate", 150, "g"),
    ("Pecivo", 2, "kom"),
]
GUESTS = (10, 30, 50)


# ---------- vektorski elementi ----------
def dial(fg, accent, bg):
    """Skala kuhinjske vage 0–1 kg: podeok na svakih 10 g, kazaljka na 1 kg (gore)."""
    cx = cy = 100
    R = 94
    out = []
    for i in range(100):
        a = math.radians(-90 + i * 3.6)
        major, mid = i % 10 == 0, i % 5 == 0
        L = 10 if major else (6.5 if mid else 3.2)
        w = 1.5 if major else (0.9 if mid else 0.55)
        x1, y1 = cx + R * math.cos(a), cy + R * math.sin(a)
        x2, y2 = cx + (R - L) * math.cos(a), cy + (R - L) * math.sin(a)
        out.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{fg}" stroke-width="{w}"/>')
    labels = []
    for k in range(10):
        a = math.radians(-90 + k * 36)
        r = R - 20
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        txt = "1 kg" if k == 0 else f"{k * 100}"
        labels.append(f'<text x="{x:.2f}" y="{y + 2.6:.2f}" text-anchor="middle" font-size="{8.5 if k else 9.5}" '
                      f'font-weight="{700 if k == 0 else 500}">{txt}</text>')
    return f'''<svg class="dial" viewBox="0 0 200 200" aria-label="Vaga, 1 kg">
  <circle cx="{cx}" cy="{cy}" r="{R + 4.5}" fill="none" stroke="{fg}" stroke-width="1.1"/>
  <circle cx="{cx}" cy="{cy}" r="{R + 1}" fill="{bg}"/>
  {"".join(out)}
  <g fill="{fg}" font-family="Schibsted Grotesk, sans-serif" letter-spacing=".02em">{"".join(labels)}</g>
  <polygon points="{cx - 2.6},{cy} {cx + 2.6},{cy} {cx + 0.5},{cy - 69} {cx - 0.5},{cy - 69}" fill="{accent}"/>
  <polygon points="{cx - 2.2},{cy} {cx + 2.2},{cy} {cx},{cy + 10}" fill="{accent}"/>
  <circle cx="{cx}" cy="{cy}" r="4.6" fill="{accent}"/>
  <circle cx="{cx}" cy="{cy}" r="1.6" fill="{bg}"/>
</svg>'''


def ruler(width_mm, fg):
    """Pravi metrički lenjir: podeok svaki mm, broj na svaki cm. Štampa 1:1 → može se meriti."""
    parts = []
    for i in range(int(width_mm) + 1):
        h = 3.2 if i % 10 == 0 else (2 if i % 5 == 0 else 1.1)
        w = 0.22 if i % 10 == 0 else 0.14
        parts.append(f'<line x1="{i}" y1="0" x2="{i}" y2="{h}" stroke="{fg}" stroke-width="{w}"/>')
        if i % 10 == 0 and i < width_mm:
            parts.append(f'<text x="{i + 0.9}" y="3.1" font-size="2.3" font-weight="500">{i // 10}</text>')
    return (f'<svg class="ruler" viewBox="0 0 {width_mm} 4.2" width="{width_mm}mm" height="4.2mm" preserveAspectRatio="none">'
            f'<g font-family="Schibsted Grotesk, sans-serif" fill="{fg}">{"".join(parts)}</g></svg>')


# ---------- stavke ----------
def row(name, desc, p, unit, tag):
    t = f'<i class="tag">{e(tag)}</i>' if tag else ""
    d = f'<p class="d">{e(desc)}</p>' if desc else ""
    return f'<div class="it"><div class="r"><span class="n">{e(name)}{t}</span><span class="p">{price(p)}<small>{unit}</small></span></div>{d}</div>'


def head(i, note=""):
    title, sub, items = SECTIONS[i]
    return (f'<header class="h"><div class="hl"><span class="num">{i + 1:02d}</span><h2>{e(title)}</h2></div>'
            f'<div class="hr"><p>{e(sub)}</p>{note}</div></header>')


def sec(i):
    title, sub, items = SECTIONS[i]
    return f'<section class="s">{head(i)}{"".join(row(*it) for it in items)}</section>'


def sec_predjelo():
    cards = ""
    for name, desc, p, unit, tag in SECTIONS[0][2]:
        cards += (f'<div class="plate {tag.lower()}"><div class="pt"><b>{e(name)}</b><span class="p">{price(p)}<small>{unit}</small></span></div>'
                  f'<p>{e(desc)}</p></div>')
    return f'<section class="s">{head(0)}<div class="plates">{cards}</div></section>'


def sec_kremaste():
    i = 6
    title, sub, items = SECTIONS[i]
    p0 = items[0][2]
    assert all(it[2] == p0 for it in items), "kremaste salate više nemaju istu cenu — vrati sec(6)"
    names = ' <span class="sep">/</span> '.join(
        e(n) + (f'<i class="tag">{e(t)}</i>' if t else "") for n, _, _, _, t in items)
    note = f'<span class="p big">{price(p0)}<small>din/kg</small></span>'
    return f'<section class="s">{head(i, note)}<p class="flow">{names}</p></section>'


def panel(cls, inner):
    return f'<div class="panel {cls}">{inner}</div>'


def plan_table():
    hdr = "".join(f"<th>{g}</th>" for g in GUESTS)
    rows = ""
    for name, per, unit in PLAN:
        cells = ""
        for g in GUESTS:
            tot = per * g
            if unit == "g":
                kg = tot / 1000
                txt = f"{kg:g}".replace(".", ",") + " kg"
            else:
                txt = f"{tot} kom"
            cells += f"<td>{txt}</td>"
        rows += f'<tr><th scope="row">{e(name)}<small>{per} {unit} po osobi</small></th>{cells}</tr>'
    return f'<table class="plan"><thead><tr><th>Gostiju</th>{hdr}</tr></thead><tbody>{rows}</tbody></table>'


# ---------- spolja ----------
front = panel("front", f'''
  <div class="kick"><span>Ketering</span><span>Katalog jela</span><span>2026</span></div>
  <div class="dialwrap">{dial(INK, TERRA, PAPER)}<img class="dial-logo" src="assets/logo-ink.png" alt="Carstvo Ukusa"></div>
  <h1>Trpeza<br>po vašoj<br><em>meri.</em></h1>
  <p class="lede">Predjela, finger food, meso, riba, salate i prilozi — sve po kilogramu. Vi odredite koliko, mi odmerimo i spremimo.</p>
  <div class="bottom"><div><span class="lbl">Porudžbine</span><a class="tel" href="tel:{PHONE_TEL}">{PHONE}</a></div><span class="lbl r">Slave · Proslave<br>Poslovni događaji</span></div>
''')

back = panel("back", f'''
  <img class="logo-s" src="assets/logo-cream.png" alt="Carstvo Ukusa">
  <div class="mid">
    <p class="bk">Ceo meni na telefonu</p>
    <div class="qrbox">{QR_SVG}</div>
    <p class="hint">Uperite kameru u kod. Bez aplikacije,<br>na iPhone-u i Androidu.</p>
  </div>
  <div class="bbot">
    <div class="bline"><span class="lbl">Porudžbine</span><a class="tel" href="tel:{PHONE_TEL}">{PHONE}</a></div>
    <div class="fine"><div>{seal(PAPER, INK, "seal seal-back")}</div><p>Sva jela pripremamo po HACCP standardu bezbednosti hrane. Cene su u dinarima po kilogramu, osim gde je drugačije navedeno, i važe za 2026. godinu.</p></div>
  </div>
''')

flap = panel("flap", f'''
  <p class="fk">Vodič za planiranje</p>
  <h3>Koliko<br>treba?</h3>
  <p class="ft">Orijentaciono, po osobi. Za tačan broj gostiju i prilike pozovite nas — odmerićemo zajedno.</p>
  {plan_table()}
  <ol class="steps">
    <li><b>Izaberite jela</b><span>iz osam odeljaka ovog menija</span></li>
    <li><b>Pozovite ili pišite nam</b><span>{PHONE} — dogovorimo količine i termin</span></li>
    <li><b>Mi spremamo</b><span>sveže, po HACCP standardu bezbednosti hrane</span></li>
  </ol>
  <dl class="contact">
    <dt>Mejl</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd>
    <dt>Instagram</dt><dd><a href="{INSTAGRAM_URL}">{INSTAGRAM}</a></dd>
    <dt>Facebook</dt><dd><a href="{FACEBOOK_URL}">{FACEBOOK}</a></dd>
    <dt>Web</dt><dd><a href="{SITE_URL}">{SITE}</a></dd>
  </dl>
  <div class="legend"><i class="tag">posno</i><span>posna jela i posne opcije su označene</span></div>
''')

# ---------- unutra ----------
left = panel("in first", sec_predjelo() + sec(1))
mid = panel("in", sec(2) + sec(3) + sec(4))
right = panel("in narrow", sec(5) + sec_kremaste() + sec(7)
              + f'<p class="foot">Cene u dinarima po kilogramu, osim gde je drugačije navedeno. <b style="white-space:nowrap">Porudžbine {PHONE}</b></p>')

W, H = 297, 210
B = BLEED
css = f'''
@page {{ size: {W + 2 * B}mm {H + 2 * B}mm; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: "Schibsted Grotesk", sans-serif; color: {INK}; -webkit-print-color-adjust: exact; print-color-adjust: exact;
  font-feature-settings: "lnum", "kern"; background: #777; }}
.tel {{ font-feature-settings: "lnum", "tnum"; }}
.sheet {{ position: relative; width: {W + 2 * B}mm; height: {H + 2 * B}mm; overflow: hidden; page-break-after: always; background: {PAPER}; }}
.sheet:last-child {{ page-break-after: auto; }}
.panel {{ position: absolute; top: 0; height: {H + 2 * B}mm; padding-top: {B}mm; padding-bottom: {B}mm; overflow: hidden; }}
.flap  {{ left: 0; width: {97 + B}mm; padding-left: {B}mm; }}
.back  {{ left: {B + 97}mm; width: 100mm; }}
.front {{ left: {B + 197}mm; width: {100 + B}mm; padding-right: {B}mm; }}
.sheet.inside .panel:nth-child(1) {{ left: 0; width: {100 + B}mm; padding-left: {B}mm; }}
.sheet.inside .panel:nth-child(2) {{ left: {B + 100}mm; width: 100mm; }}
.sheet.inside .panel:nth-child(3) {{ left: {B + 200}mm; width: {97 + B}mm; padding-right: {B}mm; }}

h1, h2, h3, .n, .plate b, .flow, .tel, .num, .steps b {{ font-family: "Newsreader", serif; }}
.lbl, .kick, .fk, .bk {{ font-size: 6pt; letter-spacing: .28em; text-transform: uppercase; font-weight: 700; }}

/* ---- prednja korica: vaga ---- */
.front {{ padding: {11 + B}mm {10 + B}mm {10 + B}mm 11mm; display: flex; flex-direction: column; }}
.kick {{ display: flex; justify-content: space-between; color: {INK}; border-bottom: 0.5mm solid {INK}; padding-bottom: 2.2mm; }}
.dialwrap {{ position: relative; width: 74mm; height: 74mm; margin: 9mm auto 0; }}
.dial {{ width: 100%; height: 100%; display: block; }}
.dial-logo {{ position: absolute; left: 50%; top: 57%; width: 17mm; transform: translateX(-50%); }}
.front h1 {{ margin-top: 10mm; font-weight: 400; font-variation-settings: "opsz" 72; font-size: 33pt; line-height: .96; letter-spacing: -.02em; }}
.front h1 em {{ font-style: italic; color: {TERRA}; }}
.lede {{ margin-top: 5mm; font-size: 7.6pt; line-height: 1.55; color: {MUTED}; max-width: 70mm; }}
.bottom {{ margin-top: auto; display: flex; justify-content: space-between; align-items: flex-end; border-top: 0.5mm solid {INK}; padding-top: 2.6mm; }}
.lbl {{ display: block; color: {TERRA}; margin-bottom: 1mm; }}
.lbl.r {{ text-align: right; color: {INK}; line-height: 1.6; margin: 0; font-weight: 600; letter-spacing: .18em; }}
.tel {{ font-size: 16.5pt; font-weight: 500; color: inherit; text-decoration: none; white-space: nowrap; letter-spacing: -.01em; line-height: 1; }}

/* ---- zadnja korica: QR ---- */
.back {{ background: {INK}; color: {PAPER}; padding: {11 + B}mm 10mm {10 + B}mm; display: flex; flex-direction: column; align-items: center; text-align: center; }}
.back .logo-s {{ width: 36mm; margin-top: 2mm; }}
.back .mid {{ margin: auto 0; display: flex; flex-direction: column; align-items: center; }}
.bk {{ color: {SAGE}; }}
.qrbox {{ margin-top: 4mm; width: 50mm; height: 50mm; padding: 3.5mm; background: {PAPER}; }}
.qrbox svg {{ width: 100%; height: 100%; display: block; }}
.hint {{ margin-top: 4mm; font-size: 7pt; line-height: 1.5; color: rgba(246,241,231,.72); }}
.bbot {{ width: 100%; }}
.bline {{ text-align: left; border-top: 0.4mm solid rgba(246,241,231,.45); padding-top: 2.6mm; }}
.bline .lbl {{ color: {SAGE}; }}
.fine {{ margin-top: 5mm; display: flex; gap: 3mm; align-items: center; text-align: left; }}
.fine p {{ font-size: 5.6pt; line-height: 1.5; color: rgba(246,241,231,.6); }}
.seal-back {{ width: 15mm; height: 15mm; flex: none; opacity: .85; }}

/* ---- flap: koliko treba ---- */
.flap {{ background: {PAPER2}; padding-top: {12 + B}mm; padding-right: 9mm; padding-bottom: {10 + B}mm; padding-left: {10 + B}mm; display: flex; flex-direction: column; }}
.fk {{ color: {TERRA}; }}
.flap h3 {{ margin-top: 3mm; font-weight: 400; font-variation-settings: "opsz" 72; font-size: 27pt; line-height: .96; letter-spacing: -.02em; }}
.ft {{ margin-top: 4mm; font-size: 7.2pt; line-height: 1.5; color: {MUTED}; }}
.plan {{ width: 100%; border-collapse: collapse; margin-top: 5mm; font-size: 7.2pt; }}
.plan th, .plan td {{ text-align: right; padding: 1.7mm 0 1.6mm; border-top: 0.18mm solid {HAIR}; vertical-align: baseline; white-space: nowrap; }}
.plan thead th {{ font-size: 5.6pt; letter-spacing: .14em; text-transform: uppercase; color: {TERRA}; border-top: 0; padding-top: 0; font-weight: 700; }}
.plan thead th:first-child {{ text-align: left; }}
.plan tbody th {{ text-align: left; font-family: "Newsreader", serif; font-weight: 500; font-size: 8.2pt; }}
.plan tbody th small {{ display: block; font-family: "Schibsted Grotesk", sans-serif; font-weight: 400; font-size: 5.4pt; color: {MUTED}; margin-top: .3mm; }}
.plan td {{ font-weight: 600; font-size: 7.6pt; padding-left: 2mm; }}
.plan td:last-child {{ color: {TERRA}; }}
.plan tbody tr:last-child td, .plan tbody tr:last-child th {{ border-bottom: 0.45mm solid {INK}; }}
.steps {{ list-style: none; counter-reset: k; margin-top: 7mm; }}
.steps li {{ counter-increment: k; display: grid; grid-template-columns: 8mm 1fr; column-gap: 1.5mm; padding: 2.4mm 0; border-top: 0.18mm solid {HAIR}; }}
.steps li:first-child {{ border-top: 0; padding-top: 0; }}
.steps li::before {{ content: counter(k, decimal-leading-zero); font-family: "Newsreader", serif; font-style: italic; font-size: 13pt; color: {TERRA}; line-height: 1; grid-row: 1 / span 2; }}
.steps b {{ display: block; font-weight: 500; font-size: 9pt; }}
.steps span {{ display: block; font-size: 6.6pt; color: {MUTED}; margin-top: .5mm; }}
.contact {{ margin-top: 5mm; display: grid; grid-template-columns: 13mm 1fr; column-gap: 1.5mm; row-gap: 0; border-top: 0.45mm solid {INK}; padding-top: 2.2mm; }}
.contact dt {{ font-size: 5.2pt; letter-spacing: .14em; text-transform: uppercase; color: {TERRA}; font-weight: 700; align-self: baseline; padding-top: 1mm; }}
.contact dd {{ font-family: "Newsreader", serif; font-weight: 500; font-size: 8.2pt; line-height: 1.15; padding: .6mm 0 .7mm; border-top: 0.18mm solid {HAIR}; font-variation-settings: "opsz" 14; }}
.contact dd:first-of-type {{ border-top: 0; }}
.contact a {{ color: inherit; text-decoration: none; }}
.legend {{ margin-top: 5mm; display: flex; align-items: center; gap: 2mm; font-size: 6.4pt; color: {MUTED}; }}

/* ---- unutra: ledger ---- */
.in {{ background: {PAPER}; padding-top: {10 + B}mm; padding-bottom: {7 + B}mm; padding-left: 8mm; padding-right: 7mm; }}
.sheet.inside .panel:nth-child(1) {{ padding-left: {8 + B}mm; }}
.sheet.inside .panel:nth-child(3) {{ padding-right: {8 + B}mm; }}
.ruler {{ position: absolute; left: {B}mm; top: {B + 4}mm; }}
.s {{ position: relative; }}
.s + .s {{ margin-top: 3.4mm; }}
.h {{ display: flex; justify-content: space-between; align-items: flex-end; padding-bottom: 1mm; border-bottom: 0.55mm solid {INK}; margin-bottom: .4mm; }}
.hl {{ display: flex; align-items: baseline; gap: 1.6mm; }}
.num {{ font-style: italic; font-size: 19pt; line-height: .75; color: {TERRA}; font-weight: 400; letter-spacing: -.02em; }}
.h h2 {{ font-weight: 500; font-size: 12pt; line-height: .9; letter-spacing: -.012em; font-variation-settings: "opsz" 36; }}
.hr {{ text-align: right; }}
.hr p {{ font-size: 5.6pt; letter-spacing: .12em; text-transform: uppercase; color: {MUTED}; font-weight: 600; max-width: 34mm; line-height: 1.3; }}
.hr .big {{ display: block; margin-top: .8mm; font-size: 10pt; }}
.it {{ padding: .78mm 0; border-top: 0.16mm solid {HAIR}; }}
.it:first-of-type {{ border-top: 0; }}
.r {{ display: flex; justify-content: space-between; align-items: baseline; gap: 2mm; }}
.n {{ font-weight: 500; font-size: 8pt; line-height: 1.15; font-variation-settings: "opsz" 14; }}
.p {{ font-weight: 700; font-size: 7.6pt; white-space: nowrap; letter-spacing: -.01em; }}
.p small {{ font-weight: 500; font-size: 4.6pt; letter-spacing: .06em; text-transform: uppercase; color: {MUTED}; margin-left: .7mm; }}
.d {{ font-size: 5.8pt; line-height: 1.35; color: {MUTED}; margin-top: .35mm; padding-right: 10mm; }}
.tag {{ display: inline-block; font-style: normal; font-family: "Schibsted Grotesk", sans-serif; font-weight: 700; font-size: 4.5pt; letter-spacing: .1em; text-transform: uppercase; color: {TERRA}; border: 0.18mm solid {TERRA}; padding: .25mm 1mm .15mm; margin-left: 1.4mm; vertical-align: .3mm; line-height: 1; }}
.first .it {{ padding: 1.35mm 0; }}
.first .n {{ font-size: 8.6pt; }}
.first .d {{ font-size: 5.9pt; }}
.plates {{ margin-top: 1.2mm; }}
.plate {{ padding: 2.4mm 0 2.6mm; border-top: 0.16mm solid {HAIR}; }}
.plate:first-child {{ border-top: 0; }}
.pt {{ display: flex; justify-content: space-between; align-items: baseline; }}
.plate b {{ font-weight: 500; font-style: italic; font-size: 11pt; letter-spacing: -.01em; }}
.plate .p {{ font-size: 10pt; }}
.plate.lux b {{ color: {TERRA}; }}
.plate p {{ margin-top: 1.2mm; font-size: 6.2pt; line-height: 1.4; color: {MUTED}; padding-right: 6mm; }}
.flow {{ font-weight: 500; font-size: 8pt; line-height: 1.75; margin-top: 1.6mm; font-variation-settings: "opsz" 14; }}
.sep {{ color: {TERRA}; padding: 0 .3mm; font-weight: 300; }}
.foot {{ position: absolute; left: 8mm; right: {8 + B}mm; bottom: {7 + B}mm; font-size: 5.6pt; color: {MUTED}; border-top: 0.16mm solid {HAIR}; padding-top: 1.4mm; }}

.mark {{ position: absolute; background: #000; }}
'''


def marks():
    """Crop marks u uglovima trim zone, van nje."""
    if not B:
        return ""
    m = []
    for x in (B, B + W):
        for y in (B, B + H):
            ty = y - B if y == B else y + 1
            tx = x - B if x == B else x + 1
            m.append(f'<div class="mark" style="left:{x}mm;top:{ty}mm;width:0.15mm;height:{B - 1}mm"></div>')
            m.append(f'<div class="mark" style="top:{y}mm;left:{tx}mm;height:0.15mm;width:{B - 1}mm"></div>')
    return "".join(m)


def fold_marks(xs):
    if not B:
        return ""
    return "".join(f'<div class="mark" style="left:{B + x}mm;top:{t}mm;width:0.15mm;height:{B - 1}mm;opacity:.6"></div>'
                   for x in xs for t in (0, B + H + 1))


doc = f'''<!doctype html><html lang="sr-Latn"><head><meta charset="utf-8"><title>Carstvo Ukusa — flajer 2026</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,300..800;1,6..72,300..800&family=Schibsted+Grotesk:ital,wght@0,400..900;1,400..900&family=Barlow+Condensed:wght@700;800&display=block&subset=latin-ext" rel="stylesheet">
<style>{css}</style></head><body>
<div class="sheet outside">{flap}{back}{front}{marks()}{fold_marks([97, 197])}</div>
<div class="sheet inside">{left}{mid}{right}{ruler(W, INK)}{marks()}{fold_marks([100, 200])}</div>
</body></html>'''

out = ROOT / "flajer.html"
out.write_text(doc, encoding="utf-8")
chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
pdf = ROOT / ("Flajer Carstvo Ukusa 2026 - za stampu (bleed 3mm).pdf" if B else "Flajer Carstvo Ukusa 2026.pdf")
subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=20000",
                "--run-all-compositor-stages-before-draw", f"--print-to-pdf={pdf}", out.as_uri()], check=True, capture_output=True)
print("PDF:", pdf)
