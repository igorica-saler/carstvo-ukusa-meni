# Generator menija Carstvo Ukusa 2026: podaci -> docs/index.html (mobilni meni za QR)
# -> isti HTML štampan u PDF (Chrome headless) = katalog. Jedan izvor, dva formata.
import shutil
import subprocess

from meni_data import *  # noqa: F401,F403

WEB = ROOT / "docs"  # GitHub Pages služi iz /docs
WEB.mkdir(exist_ok=True)
shutil.copy(ROOT / "assets" / "logo-cream.png", WEB / "logo.png")


def web_item(name, desc, p, unit, tag):
    t = f'<span class="tag">{e(tag)}</span>' if tag else ""
    d = f'<p class="desc">{e(desc)}</p>' if desc else ""
    return f'<li><div class="row"><span class="name">{e(name)}{t}</span><span class="price">{price(p)}<small>{unit}</small></span></div>{d}</li>'


nav = "".join(f'<a href="#s{i + 1}">{e(t)}</a>' for i, (t, _, _) in enumerate(SECTIONS))
secs = "".join(f'''<section id="s{i + 1}">
<header><span class="num">{i + 1:02d}</span><div><h2>{e(t)}</h2><p>{e(sub)}</p></div></header>
<ul>{"".join(web_item(*it) for it in items)}</ul>
</section>''' for i, (t, sub, items) in enumerate(SECTIONS))

WEB_CSS = (ROOT / "meni.css").read_text(encoding="utf-8")
web = f'''<!doctype html>
<html lang="sr-Latn"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="{INK}">
<meta name="robots" content="noindex">
<title>Carstvo Ukusa — Meni 2026</title>
<!-- Stari QR kodovi (štampani pre 2026-10-20) vode na GitHub Pages: preusmeri na živi sajt. Lokalni print (file://) ostaje. -->
<script>if(/github\.io$/.test(location.hostname))location.replace("https://carstvoukusa.rs/meni/");</script>
<link rel="icon" href="logo.png">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..700;1,9..144,300..700&family=Manrope:wght@400;500;600;700&display=swap&subset=latin-ext" rel="stylesheet">
<style>{WEB_CSS}</style></head>
<body>
<header class="hero">
  <img src="logo.png" alt="Carstvo Ukusa">
  <h1><em>Meni</em> 2026</h1>
  <p>Ketering · predjela, finger food, meso, riba, salate i prilozi</p>
  <p class="site"><a href="{SITE_URL}">{SITE}</a></p>
  <a class="call" href="tel:{PHONE_TEL}">Pozovite {PHONE}</a>
  <p class="links"><a href="mailto:{EMAIL}">{EMAIL}</a><a href="{INSTAGRAM_URL}">Instagram {INSTAGRAM}</a><a href="{FACEBOOK_URL}">Facebook {FACEBOOK}</a></p>
</header>
<nav class="nav"><div>{nav}</div></nav>
<main>{secs}</main>
<footer>
  <p>Cene su izražene u dinarima po kilogramu, osim gde je drugačije navedeno.</p>
  <p>Sva jela pripremamo po HACCP standardu bezbednosti hrane.</p>
  <a class="call" href="tel:{PHONE_TEL}">Poručite · {PHONE}</a>
  <p class="site"><a href="{SITE_URL}">{SITE}</a></p>
  <p class="write">Ili nam pišite</p>
  <p class="links"><a href="mailto:{EMAIL}">{EMAIL}</a><a href="{INSTAGRAM_URL}">Instagram {INSTAGRAM}</a><a href="{FACEBOOK_URL}">Facebook {FACEBOOK}</a></p>
  <a class="pdf" href="katalog.pdf">Katalog u PDF-u</a>
</footer>
</body></html>'''
index = WEB / "index.html"
index.write_text(web, encoding="utf-8")
print("WEB:", index)

# katalog = ista stranica štampana u A4 (pravila u meni.css pod @media print)
chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
pdf = ROOT / "Katalog Carstvo Ukusa 2026 - novi dizajn.pdf"
subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                "--virtual-time-budget=15000", "--run-all-compositor-stages-before-draw",
                f"--print-to-pdf={pdf}", index.as_uri()], check=True, capture_output=True)
shutil.copy(pdf, WEB / "katalog.pdf")
# Isti PDF se nudi i na sajtu (dugme „Preuzmi jelovnik (PDF)" na /meni/) — kopiraj ako repo sajta postoji.
SITE_PDF = pathlib.Path(r"C:/dev/carstvo-ukusa/frontend/public/katalog-carstvo-ukusa-2026.pdf")
if SITE_PDF.parent.exists():
    shutil.copy(pdf, SITE_PDF)
    print("SAJT:", SITE_PDF, "(posle toga: npm run build + prenos out/ na server)")
print("PDF:", pdf)

# Verzija za štampariju: ista A4 strana + 3 mm bleed sa svih strana (pozadina produžena rubnim pikselima)
# + crop marke u uglovima, kao kod flajera. Trim = 210 x 297, list = 216 x 303 mm.
import pymupdf  # noqa: E402

BLEED = 3
MM = 72 / 25.4
src = pymupdf.open(pdf)
dst = pymupdf.open()
for page in src:
    w, h = page.rect.width, page.rect.height
    b = BLEED * MM
    out_pg = dst.new_page(width=w + 2 * b, height=h + 2 * b)
    e = 0.3  # širina rubne trake (pt) koja se razvlači preko bleed zone
    edges = [  # (isečak strane u pt, odredište na listu u pt)
        ((0, 0, w, e), (b, 0, b + w, b)), ((0, h - e, w, h), (b, b + h, b + w, 2 * b + h)),      # gore, dole
        ((0, 0, e, h), (0, b, b, b + h)), ((w - e, 0, w, h), (b + w, b, 2 * b + w, b + h)),      # levo, desno
        ((0, 0, e, e), (0, 0, b, b)), ((w - e, 0, w, e), (b + w, 0, 2 * b + w, b)),              # uglovi
        ((0, h - e, e, h), (0, b + h, b, 2 * b + h)), ((w - e, h - e, w, h), (b + w, b + h, 2 * b + w, 2 * b + h)),
    ]
    o = 1  # trake ulaze 1 pt ispod sadržaja strane (koji se crta preko) — bez šava na liniji reza
    for clip, (x0, y0, x1, y1) in edges:
        strip = page.get_pixmap(dpi=300, clip=pymupdf.Rect(*clip))
        rect = pymupdf.Rect(x0 - (o if x0 >= b + w else 0), y0 - (o if y0 >= b + h else 0),
                            x1 + (o if x1 <= b else 0), y1 + (o if y1 <= b else 0))
        out_pg.insert_image(rect, pixmap=strip, keep_proportion=False)
    out_pg.show_pdf_page(pymupdf.Rect(b, b, b + w, b + h), src, page.number)  # vektorski sadržaj, bez rasterizacije
    # crop marke: 2 mm dugačke, 1 mm od trim linije, van trim zone
    for x in (b, b + w):
        for y in (b, b + h):
            ty = (y - b, y - 1 * MM) if y == b else (y + 1 * MM, y + b)
            tx = (x - b, x - 1 * MM) if x == b else (x + 1 * MM, x + b)
            out_pg.draw_line((x, ty[0]), (x, ty[1]), color=(0, 0, 0), width=0.15 * MM)
            out_pg.draw_line((tx[0], y), (tx[1], y), color=(0, 0, 0), width=0.15 * MM)
print_pdf = ROOT / "Katalog Carstvo Ukusa 2026 - za stampu (bleed 3mm).pdf"
dst.save(print_pdf, garbage=3, deflate=True)
print("PDF (štampa):", print_pdf)
