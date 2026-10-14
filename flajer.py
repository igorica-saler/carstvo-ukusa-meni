# Flajer Carstvo Ukusa 2026: A4 vodoravno, roll fold na 3 panela (100 | 100 | 97 mm)
# Strana 1 (spolja): [flap 97 | zadnja korica 100 | prednja korica 100]
# Strana 2 (unutra): [unutra-levo 100 | unutra-sredina 100 | unutra-desno 97]
# Čitanje: korica → (unutra-levo + flap) → cela unutrašnjost 01→08
import subprocess, sys
from meni_data import *  # noqa

TERRA, PAPER2, LINE, MUTED = "#B5663A", "#ECE4D3", "#D8CDB8", "#6E7A70"
BLEED = 3 if "--bleed" in sys.argv else 0
QR_SVG = (ROOT / "docs" / "qr.svg").read_text(encoding="utf-8")


def row(name, desc, p, unit, tag):
    t = f'<i class="tag">{e(tag)}</i>' if tag else ""
    d = f'<p class="d">{e(desc)}</p>' if desc else ""
    return f'<div class="it"><div class="r"><span class="n">{e(name)}{t}</span><span class="l"></span><span class="p">{price(p)}<small>{unit}</small></span></div>{d}</div>'


def head(i, note=""):
    title, sub, items = SECTIONS[i]
    return f'<header class="h"><span class="num">{i + 1:02d}</span><div><h2>{e(title)}</h2><p>{e(sub)}</p></div>{note}</header>'


def sec(i):
    title, sub, items = SECTIONS[i]
    return f'<section class="s">{head(i)}{"".join(row(*it) for it in items)}</section>'


def sec_predjelo():
    cards = ""
    for name, desc, p, unit, tag in SECTIONS[0][2]:
        cards += (f'<div class="plate {tag.lower()}"><div class="r"><b>{e(name)}</b>'
                  f'<span class="p">{price(p)}<small>{unit}</small></span></div><p>{e(desc)}</p></div>')
    return f'<section class="s">{head(0)}{cards}</section>'


def sec_kremaste():
    i = 6
    title, sub, items = SECTIONS[i]
    p0 = items[0][2]
    assert all(it[2] == p0 for it in items), "kremaste salate više nemaju istu cenu — vrati sec(6)"
    names = ' <span class="sep">·</span> '.join(
        e(n) + (f'<i class="tag">{e(t)}</i>' if t else "") for n, _, _, _, t in items)
    note = f'<span class="p">{price(p0)}<small>din/kg</small></span>'
    return f'<section class="s">{head(i, note)}<p class="flow">{names}</p></section>'


def panel(cls, inner):
    return f'<div class="panel {cls}">{inner}</div>'


# ---------- spolja ----------
front = panel("front", f'''
  <div class="frame"></div>
  <div class="kick"><span>Ketering</span><i></i><span>Katalog jela</span><i></i><span>2026</span></div>
  <img class="logo" src="assets/logo-cream.png" alt="Carstvo Ukusa">
  <h1>Trpeza<br><em>po vašoj</em><br>meri.</h1>
  <p class="lede">Predjela, finger food, meso, riba, salate i prilozi — za slave, proslave i poslovne događaje. Sve po kilogramu: vi birate koliko.</p>
  <div class="bottom"><div><span class="lbl">Porudžbine</span><a class="tel" href="tel:{PHONE_TEL}">{PHONE}</a></div>{seal(SAGE, INK, "seal seal-front")}</div>
''')

back = panel("back", f'''
  <div class="frame"></div>
  <img class="logo-s" src="assets/logo-cream.png" alt="Carstvo Ukusa">
  <div class="mid"><p class="bk">Ceo meni na telefonu</p>
  <div class="qrbox">{QR_SVG}</div>
  <p class="hint">Uperite kameru u kod —<br>bez aplikacije, na iPhone-u i Androidu.</p></div>
  <div class="bottom"><div><span class="lbl">Porudžbine</span><a class="tel" href="tel:{PHONE_TEL}">{PHONE}</a></div></div>
  <p class="fine">Sva jela pripremamo po HACCP standardu bezbednosti hrane. Cene su izražene u dinarima po kilogramu, osim gde je drugačije navedeno.</p>
''')

flap = panel("flap", f'''
  <p class="fk">Kako radimo</p>
  <h3>Sve je<br>po kilogramu.</h3>
  <p class="ft">Umesto porcija i paketa, naš meni je cenovnik po kilogramu. Sastavite trpezu od onoga što volite, u količini koja vam treba — za 10 ili za 100 gostiju.</p>
  <ol class="steps">
    <li><b>Izaberite jela</b><span>iz osam odeljaka ovog menija</span></li>
    <li><b>Pozovite nas</b><span>{PHONE} — dogovorimo količine i termin</span></li>
    <li><b>Mi spremamo</b><span>sveže, po HACCP standardu bezbednosti hrane</span></li>
  </ol>
  <p class="occ"><b>Za svaku priliku</b>Slave · Krštenja · Rođendani<br>Venčanja · Poslovni događaji</p>
  <div class="legend"><i class="tag">posno</i><span>posna jela i posne opcije su označene</span></div>
  <div class="fseal">{seal(INK, PAPER2, "seal seal-flap")}</div>
''')

# ---------- unutra ----------
left = panel("in airy", sec_predjelo() + sec(1))
mid = panel("in", sec(2) + sec(3) + sec(4))
right = panel("in narrow", sec(5) + sec_kremaste() + sec(7)
              + f'<p class="foot">Cene u dinarima po kilogramu, osim gde je drugačije navedeno. · {PHONE}</p>')

W, H = 297, 210
B = BLEED
css = f'''
@page {{ size: {W + 2 * B}mm {H + 2 * B}mm; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: "Manrope", sans-serif; color: {INK}; -webkit-print-color-adjust: exact; print-color-adjust: exact; font-feature-settings: "lnum", "tnum"; background: #777; }}
.sheet {{ position: relative; width: {W + 2 * B}mm; height: {H + 2 * B}mm; overflow: hidden; page-break-after: always; background: {PAPER}; }}
.sheet:last-child {{ page-break-after: auto; }}
.panel {{ position: absolute; top: 0; height: {H + 2 * B}mm; padding-top: {B}mm; padding-bottom: {B}mm; overflow: hidden; }}
/* spolja: flap | back | front  — krajnji paneli idu u bleed */
.flap  {{ left: 0; width: {97 + B}mm; padding-left: {B}mm; }}
.back  {{ left: {B + 97}mm; width: 100mm; }}
.front {{ left: {B + 197}mm; width: {100 + B}mm; padding-right: {B}mm; }}
/* unutra: levo | sredina | desno(97) */
.sheet.inside .panel:nth-child(1) {{ left: 0; width: {100 + B}mm; padding-left: {B}mm; }}
.sheet.inside .panel:nth-child(2) {{ left: {B + 100}mm; width: 100mm; }}
.sheet.inside .panel:nth-child(3) {{ left: {B + 200}mm; width: {97 + B}mm; padding-right: {B}mm; }}

/* karirani stolnjak — fina tekstura (originalni motiv) */
.gingham {{ position: absolute; inset: 0; pointer-events: none;
  background-image: repeating-linear-gradient(0deg, rgba(156,195,177,.09) 0 5mm, transparent 5mm 14mm), repeating-linear-gradient(90deg, rgba(156,195,177,.09) 0 5mm, transparent 5mm 14mm); }}
.gingham-dark {{ position: absolute; inset: 0; pointer-events: none;
  background-image: repeating-linear-gradient(0deg, rgba(246,241,231,.035) 0 5mm, transparent 5mm 14mm), repeating-linear-gradient(90deg, rgba(246,241,231,.035) 0 5mm, transparent 5mm 14mm); }}

/* ---- korice ---- */
.front, .back {{ color: {PAPER}; background: radial-gradient(120% 60% at 50% 0%, #2A4A3A 0%, transparent 60%), {INK}; display: flex; flex-direction: column; align-items: center; text-align: center; }}
.front {{ padding: {12 + B}mm {10 + B}mm {10 + B}mm 10mm; }}
.back {{ padding: {12 + B}mm 10mm {10 + B}mm; }}
.frame {{ position: absolute; inset: {6 + B}mm; border: 0.3mm solid rgba(156,195,177,.45); border-radius: 2.5mm; }}
.front .frame {{ left: 6mm; right: {6 + B}mm; }} .back .frame {{ left: 6mm; right: 6mm; }}
.frame::after {{ content: ""; position: absolute; inset: 1.4mm; border: 0.18mm solid rgba(156,195,177,.2); border-radius: 1.6mm; }}
.kick {{ display: flex; align-items: center; gap: 2.6mm; font-size: 6.2pt; letter-spacing: .3em; text-transform: uppercase; color: {SAGE}; font-weight: 600; }}
.kick i {{ width: 1mm; height: 1mm; border-radius: 50%; background: {SAGE}; opacity: .7; }}
.front .logo {{ width: 58mm; margin-top: 14mm; }}
.front h1 {{ margin-top: 12mm; font-family: "Fraunces", serif; font-weight: 300; font-variation-settings: "opsz" 144; font-size: 31pt; line-height: 1.02; letter-spacing: -.01em; }}
.front h1 em {{ font-style: italic; color: {SAGE}; }}
.lede {{ margin-top: 6mm; font-size: 7.4pt; line-height: 1.6; color: rgba(246,241,231,.72); max-width: 72mm; }}
.bottom {{ margin-top: auto; width: 100%; display: flex; justify-content: space-between; align-items: flex-end; text-align: left; padding: 0 2mm; }}
.lbl {{ display: block; font-size: 6pt; letter-spacing: .3em; text-transform: uppercase; color: {SAGE}; font-weight: 600; margin-bottom: 1mm; }}
.tel {{ font-family: "Fraunces", serif; font-size: 17pt; color: {PAPER}; text-decoration: none; white-space: nowrap; }}
.seal-front {{ width: 24mm; height: 24mm; transform: rotate(-12deg); }}
.back .logo-s {{ width: 34mm; margin-top: 6mm; }}
.back .mid {{ margin: auto 0; display: flex; flex-direction: column; align-items: center; }}
.bk {{ margin-top: 0; font-size: 6.2pt; letter-spacing: .3em; text-transform: uppercase; color: {SAGE}; font-weight: 600; }}
.qrbox {{ margin-top: 4mm; width: 46mm; height: 46mm; padding: 4mm; background: {PAPER}; border-radius: 2.5mm; }}
.qrbox svg {{ width: 100%; height: 100%; display: block; }}
.hint {{ margin-top: 4mm; font-size: 7pt; line-height: 1.5; color: rgba(246,241,231,.72); }}
.back .bottom {{ justify-content: center; text-align: center; margin-top: 0; }}
.fine {{ margin-top: 6mm; font-size: 5.6pt; line-height: 1.5; color: rgba(246,241,231,.5); max-width: 70mm; }}

/* ---- flap (kako radimo) ---- */
.flap {{ background: {PAPER2}; padding-top: {14 + B}mm; padding-right: 10mm; padding-bottom: {10 + B}mm; padding-left: {11 + B}mm; display: flex; flex-direction: column; }}
.fk {{ font-size: 6.2pt; letter-spacing: .3em; text-transform: uppercase; color: {TERRA}; font-weight: 700; }}
.flap h3 {{ margin-top: 4mm; font-family: "Fraunces", serif; font-weight: 300; font-variation-settings: "opsz" 144; font-size: 24pt; line-height: 1.02; }}
.ft {{ margin-top: 5mm; font-size: 7.6pt; line-height: 1.6; color: #3d4a42; }}
.steps {{ list-style: none; counter-reset: k; margin-top: 8mm; }}
.steps li {{ counter-increment: k; display: grid; grid-template-columns: 9mm 1fr; column-gap: 2mm; padding: 3.2mm 0; border-top: 0.2mm solid {LINE}; }}
.steps li::before {{ content: counter(k, decimal-leading-zero); font-family: "Fraunces", serif; font-style: italic; font-size: 14pt; color: {SAGE}; line-height: 1; grid-row: 1 / span 2; }}
.steps b {{ display: block; font-family: "Fraunces", serif; font-weight: 500; font-size: 9.5pt; }}
.steps span {{ display: block; font-size: 6.8pt; color: {MUTED}; margin-top: .6mm; }}
.occ {{ margin-top: 7mm; font-family: "Fraunces", serif; font-weight: 500; font-size: 8.6pt; line-height: 1.6; color: {INK}; }}
.occ b {{ display: block; font-family: "Manrope", sans-serif; font-weight: 700; font-size: 6.2pt; letter-spacing: .3em; text-transform: uppercase; color: {TERRA}; margin-bottom: 1.5mm; }}
.legend {{ margin-top: 5mm; display: flex; align-items: center; gap: 2mm; font-size: 6.6pt; color: {MUTED}; }}
.fseal {{ margin-top: auto; display: flex; justify-content: flex-end; }}
.seal-flap {{ width: 20mm; height: 20mm; transform: rotate(8deg); opacity: .9; }}

/* ---- unutra ---- */
.in {{ background: {PAPER}; padding-top: {7.5 + B}mm; padding-bottom: {7 + B}mm; padding-left: 8mm; padding-right: 7mm; }}
.sheet.inside .panel:nth-child(1) {{ padding-left: {8 + B}mm; }}
.sheet.inside .panel:nth-child(3) {{ padding-right: {8 + B}mm; }}
.sheet.inside .panel:nth-child(2) {{ border-left: 0.18mm solid {LINE}; border-right: 0.18mm solid {LINE}; }}
.s {{ position: relative; }}
.s + .s {{ margin-top: 3.6mm; }}
.h {{ display: flex; align-items: flex-end; gap: 2.4mm; padding-bottom: 1.4mm; border-bottom: 0.45mm solid {INK}; margin-bottom: .6mm; }}
.h .num {{ font-family: "Fraunces", serif; font-style: italic; font-size: 16pt; line-height: .78; color: {SAGE}; }}
.h h2 {{ font-family: "Fraunces", serif; font-weight: 500; font-size: 11.5pt; line-height: 1; letter-spacing: -.005em; }}
.h p {{ font-family: "Fraunces", serif; font-style: italic; font-size: 6.6pt; color: {MUTED}; margin-top: 1mm; }}
.h > .p {{ margin-left: auto; align-self: flex-end; }}
.it {{ padding: .95mm 0 .95mm; }}
.airy .it {{ padding: 1.4mm 0; }}
.airy .s + .s {{ margin-top: 5mm; }}
.airy .plate {{ margin-top: 2.4mm; padding: 2.8mm 3mm; }}
.r {{ display: flex; align-items: baseline; gap: 1.5mm; }}
.n {{ font-family: "Fraunces", serif; font-weight: 500; font-size: 7.7pt; line-height: 1.15; }}
.l {{ flex: 1; border-bottom: 0.18mm dotted rgba(30,51,40,.35); transform: translateY(-0.9mm); min-width: 3mm; }}
.p {{ font-family: "Fraunces", serif; font-weight: 600; font-size: 8pt; white-space: nowrap; }}
.p small {{ font-family: "Manrope", sans-serif; font-weight: 600; font-size: 4.6pt; letter-spacing: .05em; text-transform: uppercase; color: {MUTED}; margin-left: .8mm; }}
.d {{ font-size: 5.7pt; line-height: 1.35; color: {MUTED}; margin-top: .4mm; padding-right: 4mm; }}
.tag {{ display: inline-block; font-style: normal; font-family: "Manrope", sans-serif; font-weight: 700; font-size: 4.6pt; letter-spacing: .08em; text-transform: uppercase; color: {TERRA}; background: {PAPER2}; padding: .3mm 1.3mm; border-radius: 2mm; margin-left: 1.4mm; vertical-align: middle; }}
.plate {{ margin-top: 1.8mm; padding: 2.2mm 2.8mm 2.4mm; border-radius: 2mm; background: {PAPER2}; }}
.plate.lux {{ background: {INK}; color: {PAPER}; }}
.plate .r {{ justify-content: space-between; }}
.plate b {{ font-family: "Fraunces", serif; font-weight: 500; font-style: italic; font-size: 9pt; }}
.plate p {{ margin-top: 1mm; font-size: 5.7pt; line-height: 1.4; opacity: .8; }}
.plate.lux .p small {{ color: {SAGE}; }}
.flow {{ font-family: "Fraunces", serif; font-weight: 500; font-size: 7.7pt; line-height: 1.65; margin-top: 1.2mm; }}
.sep {{ color: {SAGE}; padding: 0 .4mm; }}
.foot {{ position: absolute; left: 8mm; right: {8 + B}mm; bottom: {7 + B}mm; font-size: 5.6pt; color: {MUTED}; }}

.spine {{ position: absolute; top: 0; bottom: 0; left: {B + 197 - 1.2}mm; width: 2.4mm; background: {TERRA}; }}

/* oznake za sečenje i savijanje (samo bleed verzija) */
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
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..700;1,9..144,300..700&family=Manrope:wght@400;500;600;700&family=Barlow+Condensed:wght@700;800&display=block&subset=latin-ext" rel="stylesheet">
<style>{css}</style></head><body>
<div class="sheet outside">{flap}{back}{front}<div class="gingham-dark"></div><div class="spine"></div>{marks()}{fold_marks([97, 197])}</div>
<div class="sheet inside">{left}{mid}{right}<div class="gingham"></div>{marks()}{fold_marks([100, 200])}</div>
</body></html>'''

out = ROOT / "flajer.html"
out.write_text(doc, encoding="utf-8")
chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
pdf = ROOT / ("Flajer Carstvo Ukusa 2026 - za stampu (bleed 3mm).pdf" if B else "Flajer Carstvo Ukusa 2026.pdf")
subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=15000",
                "--run-all-compositor-stages-before-draw", f"--print-to-pdf={pdf}", out.as_uri()], check=True, capture_output=True)
print("PDF:", pdf)
