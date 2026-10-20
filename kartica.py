# Kartica za sto sa QR kodom: 4 x A6 na A4 listu (za sečenje) + samostalni QR (PNG/SVG)
import pathlib, subprocess
import qrcode, qrcode.constants

ROOT = pathlib.Path(__file__).parent
URL = "https://carstvoukusa.rs/meni/"  # živi sajt od 2026-10-20 (ranije GitHub Pages)
PHONE = "063/821-66-78"
INK, PAPER, SAGE = "#1E3328", "#F6F1E7", "#9CC3B1"

qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, border=0)
qr.add_data(URL)
qr.make(fit=True)
m = qr.get_matrix()
n = len(m)

# SVG: kvadratni moduli (najsigurnije za skeniranje), bez mirne zone — nju daje okvir u CSS-u
rects = "".join(f'<rect x="{x}" y="{y}" width="1" height="1"/>' for y, row in enumerate(m) for x, v in enumerate(row) if v)
qr_svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {n} {n}" shape-rendering="crispEdges"><g fill="{INK}">{rects}</g></svg>'
(ROOT / "docs" / "qr.svg").write_text(qr_svg, encoding="utf-8")
qr.border = 4
qr.make_image(fill_color=INK, back_color=PAPER).resize((1600, 1600), 0).save(ROOT / "docs" / "qr.png")
print(f"QR: {n}x{n} modula, {URL}")

card = f'''<div class="card">
  <div class="frame"></div>
  <img class="logo" src="assets/logo-cream.png" alt="Carstvo Ukusa">
  <p class="kicker">Skenirajte za meni</p>
  <div class="qr">{qr_svg}</div>
  <p class="hint">Uperite kameru telefona u kod<br>i otvorite meni — bez aplikacije.</p>
  <p class="phone">{PHONE}</p>
</div>'''

html = f'''<!doctype html><html lang="sr-Latn"><head><meta charset="utf-8"><title>QR kartica za sto</title>
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
.qr {{ margin-top: 4mm; width: 62mm; height: 62mm; padding: 5mm; background: {PAPER}; border-radius: 3mm; }}
.qr svg {{ width: 100%; height: 100%; display: block; }}
.hint {{ margin-top: 5mm; font-size: 8.5pt; line-height: 1.5; color: rgba(246,241,231,.75); }}
.phone {{ margin-top: auto; font-family: "Fraunces", serif; font-size: 19pt; font-weight: 400; }}
</style></head><body><div class="sheet">{card * 4}</div></body></html>'''
out = ROOT / "kartica.html"
out.write_text(html, encoding="utf-8")

chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
pdf = ROOT / "QR kartica za sto (4 x A6).pdf"
subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=15000",
                f"--print-to-pdf={pdf}", out.as_uri()], check=True, capture_output=True)
print("PDF:", pdf)
