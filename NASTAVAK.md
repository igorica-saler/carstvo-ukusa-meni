# Carstvo Ukusa — katalog 2026 i QR meni

## Kako se gradi
- `python build.py` — iz liste `SECTIONS` pravi `katalog.html` → `Katalog Carstvo Ukusa 2026 - novi dizajn.pdf` (A4, 6 strana) i mobilni meni `docs/index.html` (+ `docs/katalog.pdf`, `docs/logo.png`).
- `python kartica.py` — QR kod za `URL` → `docs/qr.svg`, `docs/qr.png` i `QR kartica za sto (4 x A6).pdf` (A4 list, 4 kartice za sečenje).
- Izmena cene/jela: samo u `SECTIONS` u `build.py`, pa oba skripta.

## Stanje 2026-10-14
- Dodato: „Sendvič u domaćoj kroasan kifli" 2.200 din/kg (Finger food), „Kroasan kifle" 1.500 din/kg (Pecivo).
- Mobilni meni i QR kartica GOTOVI lokalno. QR pokazuje na `https://igorica-saler.github.io/carstvo-ukusa-meni/`.
- ⏳ OTVORENO: objaviti meni — javni GitHub repo `carstvo-ukusa-meni` + Pages iz `/docs` (kreiranje javnog repoa je tražilo dozvolu korisnika):
  ```
  gh repo create carstvo-ukusa-meni --public --source=. --remote=origin --push
  gh api -X POST repos/igorica-saler/carstvo-ukusa-meni/pages -f source[branch]=main -f source[path]=/docs
  ```
  Posle objave: otvoriti link na telefonu i skenirati karticu. Ako se promeni hosting/domen → promeniti `URL` u `kartica.py` i ponovo štampati kartice.
