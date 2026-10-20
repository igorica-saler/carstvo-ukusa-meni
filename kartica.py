# Kartice za sto sa QR kodom: 4 x A6 na A4 listu (za sečenje) + samostalni QR (PNG/SVG)
#   1) QR za meni (carstvoukusa.rs/meni/)
#   2) QR za Google recenzije
import pathlib, subprocess
import qrcode, qrcode.constants

ROOT = pathlib.Path(__file__).parent
URL = "https://carstvoukusa.rs/meni/"  # živi sajt od 2026-10-20 (ranije GitHub Pages)
# Google recenzije: Place ID profila "Carstvo Ukusa, Hercegovačka 37, Pančevo"
# (Maps feature id 0x475a7efc1b8f8397:0xaf9a36d73269b9dd, ludocid 12653486400942488029), proveren 2026-10-20
REVIEW_URL = "https://search.google.com/local/writereview?placeid=ChIJl4OPG_x-WkcR3blpMtc2mq8"
PHONE = "063/821-66-78"
SITE = "carstvoukusa.rs"
INK, PAPER, SAGE = "#1E3328", "#F6F1E7", "#9CC3B1"


def make_qr(url, name):
    """SVG (kvadratni moduli, bez mirne zone — nju daje okvir u CSS-u) + PNG, oba u docs/."""
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, border=0)
    qr.add_data(url)
    qr.make(fit=True)
    m = qr.get_matrix()
    n = len(m)
    rects = "".join(f'<rect x="{x}" y="{y}" width="1" height="1"/>' for y, row in enumerate(m) for x, v in enumerate(row) if v)
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {n} {n}" shape-rendering="crispEdges"><g fill="{INK}">{rects}</g></svg>'
    (ROOT / "docs" / f"{name}.svg").write_text(svg, encoding="utf-8")
    qr.border = 4
    qr.make_image(fill_color=INK, back_color=PAPER).resize((1600, 1600), 0).save(ROOT / "docs" / f"{name}.png")
    print(f"QR {name}: {n}x{n} modula, {url}")
    return svg


def card_html(qr_svg, kicker, hint, extra="", cls=""):
    return f'''<div class="card {cls}">
  <div class="frame"></div>
  <img class="logo" src="assets/logo-cream.png" alt="Carstvo Ukusa">
  <p class="kicker">{kicker}</p>{extra}
  <div class="qr">{qr_svg}</div>
  <p class="hint">{hint}</p>
  <p class="site">{SITE}</p>
  <p class="phone">{PHONE}</p>
</div>'''


STARS = '\n  <p class="stars">★★★★★</p>'
CARDS = {
    # ime PDF-a: (ime QR fajla u docs/, url, kicker, hint, dodatak iznad QR-a)
    "QR kartica za sto (4 x A6).pdf": ("qr", URL, "Skenirajte za meni",
        "Uperite kameru telefona u kod<br>i otvorite meni — bez aplikacije.", "", ""),
    "QR kartica Google recenzije (4 x A6).pdf": ("qr-recenzije", REVIEW_URL, "Ocenite nas na Google-u",
        "Uperite kameru telefona u kod<br>i ostavite recenziju — traje minut.<br>Vaše mišljenje nam mnogo znači.", STARS, "rev"),
}


def sheet_html(card):
    return f'''<!doctype html><html lang="sr-Latn"><head><meta charset="utf-8"><title>QR kartica za sto</title>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..700;1,9..144,300..700&family=Manrope:wght@500;600;700&display=block&subset=latin-ext" rel="stylesheet">
<style>
@page {{ size: A4; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: "Manrope", sans-serif; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.sheet {{ width: 210mm; height: 297mm; position: relative; display: grid; grid-template-columns: 105mm 105mm; grid-template-rows: 148.5mm 148.5mm; }}
.sheet::before, .sheet::after {{ content: ""; position: absolute; background: #bbb; }}
.sheet::before {{ left: 105mm; top: 0; width: 0.2mm; height: 100%; }}
.sheet::after {{ top: 148.5mm; left: 0; height: 0.2mm; width: 100%; }}
.card {{ position: relative; width: 105mm; height: 148.5mm; overflow: hidden; color: {PAPER}; text-align: center;
  padding: 11mm 10mm 9mm; display: flex; flex-direction: column; align-items: center;
  background: radial-gradient(120% 70% at 50% 0%, #2A4A3A 0%, transparent 60%), {INK}; }}
.frame {{ position: absolute; inset: 5mm; border: 0.3mm solid rgba(156,195,177,.45); border-radius: 2.5mm; pointer-events: none; }}
.logo {{ width: 42mm; }}
.kicker {{ margin-top: 7mm; font-size: 8pt; letter-spacing: .32em; text-transform: uppercase; color: {SAGE}; font-weight: 700; }}
.stars {{ margin-top: 2mm; font-size: 12pt; letter-spacing: .2em; color: {SAGE}; }}
.rev .logo {{ width: 36mm; }}
.rev .kicker {{ margin-top: 5mm; }}
.rev .qr {{ margin-top: 2.5mm; width: 50mm; height: 50mm; padding: 4mm; }}
.rev .hint {{ margin-top: 3mm; }}
.qr {{ margin-top: 3.5mm; width: 56mm; height: 56mm; padding: 4.5mm; background: {PAPER}; border-radius: 3mm; }}
.qr svg {{ width: 100%; height: 100%; display: block; }}
.hint {{ margin-top: 4mm; font-size: 8.5pt; line-height: 1.5; color: rgba(246,241,231,.75); }}
.site {{ margin-top: 2.5mm; font-family: "Fraunces", serif; font-size: 13pt; }}
.phone {{ margin-top: auto; font-family: "Fraunces", serif; font-size: 19pt; font-weight: 400; }}
</style></head><body><div class="sheet">{card * 4}</div></body></html>'''


chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
for pdf_name, (qr_name, url, kicker, hint, extra, cls) in CARDS.items():
    card = card_html(make_qr(url, qr_name), kicker, hint, extra, cls)
    out = ROOT / f"kartica-{qr_name}.html"
    out.write_text(sheet_html(card), encoding="utf-8")
    pdf = ROOT / pdf_name
    subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=15000",
                    f"--print-to-pdf={pdf}", out.as_uri()], check=True, capture_output=True)
    print("PDF:", pdf)
