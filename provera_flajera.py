# Proverava da sadržaj unutrašnjih panela ne ulazi u donju marginu (prelivanje) — renderuje PDF i gleda piksele
import sys, pymupdf
from PIL import Image
pdf = sys.argv[1] if len(sys.argv) > 1 else "Flajer Carstvo Ukusa 2026.pdf"
page = pymupdf.open(pdf)[1]
dpi = 100
pix = page.get_pixmap(dpi=dpi)
im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples).convert("L")
mm = dpi / 25.4
H = pix.height
ok = True
for name, x0, x1 in (("levo", 8, 98), ("sredina", 108, 193), ("desno", 208, 289)):
    # donjih 6 mm panela (iznad bottom paddinga od 7mm ostavljamo 1mm tolerancije)
    strip = im.crop((int(x0 * mm), int(H - 6.5 * mm), int(x1 * mm), int(H - 1 * mm)))
    dark = sum(1 for v in strip.getdata() if v < 150)
    # pronađi najnižu tamnu liniju piksela u panelu
    col = im.crop((int(x0 * mm), 0, int(x1 * mm), H))
    w, h = col.size
    px = col.load()
    low = max((y for y in range(h) for x in range(0, w, 3) if px[x, y] < 150), default=0)
    print(f"{name}: najniži tekst na {low / mm:.1f} mm od {H / mm:.0f} mm; tamnih piksela u donjoj zoni: {dark}")
    if dark > 30:
        ok = False
print("OK — ništa ne preliva" if ok else "PRELIVA!")
sys.exit(0 if ok else 1)
