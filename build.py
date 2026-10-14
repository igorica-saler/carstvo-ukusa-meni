# Generator kataloga Carstvo Ukusa 2026: podaci -> katalog.html -> PDF (Chrome headless)
import subprocess, pathlib

from meni_data import *  # noqa: F401,F403

# raspored sekcija po stranama (indeksi u SECTIONS)
PAGES = [[0, 1], [2, 3], [4, 5], [6, 7]]

def item_html(name, desc, p, unit, tag):
    t = f'<span class="tag">{e(tag)}</span>' if tag else ""
    d = f'<p class="desc">{e(desc)}</p>' if desc else ""
    return f'''<div class="item">
  <div class="name-row"><h3>{e(name)}{t}</h3><span class="lead"></span><span class="price">{price(p)}<small>{unit}</small></span></div>
  {d}
</div>'''


def feature_html(name, desc, p, unit, tag):
    chips = "".join(f"<li>{e(x.strip())}</li>" for x in desc.split(","))
    return f'''<article class="feature {'lux' if tag == 'Lux' else ''}">
  <div class="feature-top"><span class="kicker">{e(tag)}</span><span class="price big">{price(p)}<small>{unit}</small></span></div>
  <h3>{e(name)}</h3>
  <ul class="chips">{chips}</ul>
</article>'''


def section_html(i):
    title, sub, items = SECTIONS[i]
    num = f"{i + 1:02d}"
    if i == 0:
        body = f'<div class="features">{"".join(feature_html(*it) for it in items)}</div>'
    else:
        body = f'<div class="items">{"".join(item_html(*it) for it in items)}</div>'
    return f'''<section class="sec">
  <header class="sec-head"><span class="num">{num}</span><div><h2>{e(title)}</h2><p class="sub">{e(sub)}</p></div><span class="count">{stavki(len(items))}</span></header>
  {body}
</section>'''


def cta():
    return f'''<aside class="cta">
  <div><p class="cta-k">Poručite svoj meni</p><a class="cta-phone" href="tel:{PHONE_TEL}">{PHONE}</a></div>
  {seal(SAGE, INK, "seal cta-seal")}
</aside>'''


def inner_page(secs, pno, last=False):
    return f'''<div class="page inner">
  <div class="runhead"><img src="assets/logo-ink.png" alt="Carstvo Ukusa"><span>Katalog <em>2026</em></span><span class="rh-phone">{PHONE}</span></div>
  {"".join(section_html(i) for i in secs)}
  {cta() if last else ""}
  <div class="runfoot"><span>Cene su izražene u dinarima po kilogramu, osim gde je drugačije navedeno.</span><span class="pno">{pno:02d}</span></div>
</div>'''


def toc():
    rows = []
    for pi, secs in enumerate(PAGES):
        for i in secs:
            rows.append(f'<li><span class="tn">{i + 1:02d}</span><span class="tt">{e(SECTIONS[i][0])}</span><span class="tp">str. {pi + 2:02d}</span></li>')
    return "".join(rows)


cover = f'''<div class="page cover">
  <div class="frame"></div>
  <div class="cover-top"><span>Ketering</span><span class="dot"></span><span>Katalog jela</span><span class="dot"></span><span>2026</span></div>
  <img class="cover-logo" src="assets/logo-cream.png" alt="Carstvo Ukusa">
  <h1><span class="k">Katalog</span><span class="y">2026</span></h1>
  <p class="lede">Predjela, finger food, specijaliteti od mesa i ribe, salate i prilozi — za proslave, slave i poslovne događaje.</p>
  <ol class="toc">{toc()}</ol>
  <div class="cover-bottom">
    <div><span class="lbl">Porudžbine</span><a class="phone" href="tel:{PHONE_TEL}">{PHONE}</a></div>
    {seal(SAGE, INK, "seal cover-seal")}
  </div>
</div>'''

back = f'''<div class="page back">
  <div class="frame"></div>
  <img class="back-logo" src="assets/logo-cream.png" alt="Carstvo Ukusa">
  <p class="back-kicker">Poručite svoj meni</p>
  <a class="back-phone" href="tel:{PHONE_TEL}">{PHONE}</a>
  <p class="back-note">Sva jela pripremamo po HACCP standardu bezbednosti hrane.</p>
  {seal(SAGE, INK, "seal back-seal")}
</div>'''

pages = [cover] + [inner_page(s, n + 2, n == len(PAGES) - 1) for n, s in enumerate(PAGES)] + [back]

CSS = (ROOT / "katalog.css").read_text(encoding="utf-8")
JS = (ROOT / "raspored.js").read_text(encoding="utf-8")
doc = f'''<!doctype html>
<html lang="sr-Latn"><head><meta charset="utf-8">
<title>Carstvo Ukusa — Katalog 2026</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..700;1,9..144,300..700&family=Manrope:wght@400;500;600;700&family=Barlow+Condensed:wght@700;800&display=block&subset=latin-ext" rel="stylesheet">
<style>{CSS}</style><script>{JS}</script></head>
<body>{"".join(pages)}</body></html>'''

out = ROOT / "katalog.html"
out.write_text(doc, encoding="utf-8")
print("HTML:", out)

chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
pdf = ROOT / "Katalog Carstvo Ukusa 2026 - novi dizajn.pdf"
subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                "--virtual-time-budget=15000", "--run-all-compositor-stages-before-draw",
                f"--print-to-pdf={pdf}", out.as_uri()], check=True, capture_output=True)
print("PDF:", pdf)

# ---------- mobilni meni (za QR kod na stolu) ----------
import shutil
WEB = ROOT / "docs"  # GitHub Pages služi iz /docs
WEB.mkdir(exist_ok=True)
shutil.copy(ROOT / "assets" / "logo-cream.png", WEB / "logo.png")
shutil.copy(pdf, WEB / "katalog.pdf")


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
<link rel="icon" href="logo.png">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..700;1,9..144,300..700&family=Manrope:wght@400;500;600;700&display=swap&subset=latin-ext" rel="stylesheet">
<style>{WEB_CSS}</style></head>
<body>
<header class="hero">
  <img src="logo.png" alt="Carstvo Ukusa">
  <h1><em>Meni</em> 2026</h1>
  <p>Ketering · predjela, finger food, meso, riba, salate i prilozi</p>
  <a class="call" href="tel:{PHONE_TEL}">Pozovite {PHONE}</a>
</header>
<nav class="nav"><div>{nav}</div></nav>
<main>{secs}</main>
<footer>
  <p>Cene su izražene u dinarima po kilogramu, osim gde je drugačije navedeno.</p>
  <p>Sva jela pripremamo po HACCP standardu bezbednosti hrane.</p>
  <a class="call" href="tel:{PHONE_TEL}">Poručite · {PHONE}</a>
  <a class="pdf" href="katalog.pdf">Katalog u PDF-u</a>
</footer>
</body></html>'''
(WEB / "index.html").write_text(web, encoding="utf-8")
print("WEB:", WEB / "index.html")
