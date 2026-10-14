# Carstvo Ukusa — katalog 2026 i QR meni

## Kako se gradi
- `python build.py` — iz liste `SECTIONS` pravi `katalog.html` → `Katalog Carstvo Ukusa 2026 - novi dizajn.pdf` (A4, 6 strana) i mobilni meni `docs/index.html` (+ `docs/katalog.pdf`, `docs/logo.png`).
- `python kartica.py` — QR kod za `URL` → `docs/qr.svg`, `docs/qr.png` i `QR kartica za sto (4 x A6).pdf` (A4 list, 4 kartice za sečenje).
- Izmena cene/jela: samo u `SECTIONS` u `build.py`, pa oba skripta.

## Stanje 2026-10-14
- Dodato: „Sendvič u domaćoj kroasan kifli" 2.200 din/kg (Finger food), „Kroasan kifle" 1.500 din/kg (Pecivo).
- Mobilni meni i QR kartica GOTOVI lokalno. QR pokazuje na `https://igorica-saler.github.io/carstvo-ukusa-meni/`.
- ✅ OBJAVLJENO 2026-10-14: javni repo `igorica-saler/carstvo-ukusa-meni` (remote `origin`), GitHub Pages iz `/docs`. Meni živ na `https://igorica-saler.github.io/carstvo-ukusa-meni/`, QR testiran. Izmena menija: `python build.py` → `git push`, Pages se osveži za ~1 min. Ako se promeni hosting/domen → promeniti `URL` u `kartica.py` i ponovo štampati kartice.
- 2026-10-14: git repo bio oštećen (ref main i index nule, prekinut upis) — popravljen iz object store-a, ništa izgubljeno.

## Flajer (2026-10-14)
- `python flajer.py` → `Flajer Carstvo Ukusa 2026.pdf` (pregled, 297×210, 2 strane); `python flajer.py --bleed` → `... za stampu (bleed 3mm).pdf` (303×216, crop + fold marke).
- `python provera_flajera.py` — proverava da unutrašnji paneli ne prelivaju (exit 1 = preliva).
- Format: A4 vodoravno, **roll fold** 100 | 100 | 97 mm. Spolja: flap (Kako radimo) | zadnja (QR) | prednja. Unutra: 01–02 | 03–05 | 06–08.
- Koncept: „Trpeza po vašoj meri" + fina karirana (stolnjak) tekstura, terakota traka na hrbatu, kremaste salate kao jedna cenovna traka.
- Za štampariju: 2/2 boje, papir 170–200 g mat, bleed 3 mm, roll fold (unutrašnji panel 97 mm). Referentni skenovi u `skenirani flyer/`.
- Sledeće: digitalna verzija flajera (korisnik najavio), objava GitHub Pages (vidi gore).
