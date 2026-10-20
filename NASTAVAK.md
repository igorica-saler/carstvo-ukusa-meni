# Carstvo Ukusa — katalog 2026 i QR meni

## Kako se gradi
- `python build.py` — iz liste `SECTIONS` pravi mobilni meni `docs/index.html` (stil u `meni.css`), pa TU ISTU stranicu štampa u `Katalog Carstvo Ukusa 2026 - novi dizajn.pdf` (A4, kopija u `docs/katalog.pdf`). Katalog i QR meni su identični po konstrukciji; razlike samo pod `@media print` u `meni.css`.
- `python kartica.py` — QR kod za `URL` → `docs/qr.svg`, `docs/qr.png` i `QR kartica za sto (4 x A6).pdf` (A4 list, 4 kartice za sečenje).
- Izmena cene/jela: samo u `SECTIONS` u `meni_data.py`, pa sva tri skripta.
- 2026-10-14: stari samostalni generator kataloga (`katalog.html`, `katalog.css`, `raspored.js`, korice sa sadržajem, dve kolone) uklonjen na zahtev korisnika — u git istoriji do commita 067e080.

## Stanje 2026-10-14
- Dodato: „Sendvič u domaćoj kroasan kifli" 2.200 din/kg (Finger food), „Kroasan kifle" 1.500 din/kg (Pecivo).
- Mobilni meni i QR kartica GOTOVI lokalno. QR pokazuje na `https://igorica-saler.github.io/carstvo-ukusa-meni/`.
- ✅ OBJAVLJENO 2026-10-14: javni repo `igorica-saler/carstvo-ukusa-meni` (remote `origin`), GitHub Pages iz `/docs`. Meni živ na `https://igorica-saler.github.io/carstvo-ukusa-meni/`, QR testiran. Izmena menija: `python build.py` → `git push`, Pages se osveži za ~1 min. Ako se promeni hosting/domen → promeniti `URL` u `kartica.py` i ponovo štampati kartice.
- 2026-10-14: git repo bio oštećen (ref main i index nule, prekinut upis) — popravljen iz object store-a, ništa izgubljeno.

## Flajer (2026-10-14)
- `python flajer.py` → `Flajer Carstvo Ukusa 2026.pdf` (pregled, 297×210, 2 strane); `python flajer.py --bleed` → `... za stampu (bleed 3mm).pdf` (303×216, crop + fold marke).
- `python provera_flajera.py` — proverava da unutrašnji paneli ne prelivaju (exit 1 = preliva).
- Format: A4 vodoravno, **roll fold** 100 | 100 | 97 mm. Spolja: flap (Koliko treba?) | zadnja (QR) | prednja (vaga). Unutra: 01–02 | 03–05 | 06–08.
- Koncept v2 „Vaga" (2026-10-14, redizajn po briefu „state of the art, ne sme ličiti na AI"): sve je po kilogramu → skala kuhinjske vage 0–1 kg na naslovnoj (SVG, `dial()`), pravi milimetarski lenjir 0–29 cm uz gornju ivicu unutrašnjosti (`ruler()`, štampa 1:1), tabela „Koliko treba?" za 10/30/50 gostiju na flapu (`PLAN`, `plan_table()`). Tipografija: Newsreader (nazivi, naslovi) + Schibsted Grotesk (cene, opisi), bez tačkastih vođica, tanke linije između redova. Boje nepromenjene: zelena INK + terakota, krem papir.
- `PLAN` (grama po osobi: predjelo **100** (vlasnik 2026-10-20), finger food 120, meso/riba **350** (vlasnik tražio 2026-10-15), prilozi 150, salate 150, pecivo 2 kom) — ostale vrednosti su i dalje pretpostavka. Menja se samo u `flajer.py`.
- v1 (karirani stolnjak, Fraunces/Manrope) je u git istoriji: commit 953fb10.
- Za štampariju: 2/2 boje, papir 170–200 g mat, bleed 3 mm, roll fold (unutrašnji panel 97 mm). Referentni skenovi u `skenirani flyer/`.
- Sledeće: digitalna verzija flajera (korisnik najavio).

## Kontakti (2026-10-15)
- Mejl `carstvo.ukusa@gmail.com` (ZVANIČNI, potvrdio korisnik 2026-10-20 — isti i na sajtu), sajt `carstvoukusa.rs` (bez www; na flajeru pod QR-om i uz telefon, na katalogu u heroju i futeru, na QR kartici), Instagram `@carstvoukusa`, Facebook `CarstvoUkusaCatering` — konstante `EMAIL`, `SITE`, `SITE_URL`, `INSTAGRAM(_URL)`, `FACEBOOK(_URL)` u `meni_data.py` (ne zvati `WEB` — sudara se sa `WEB = ROOT/'docs'` u build.py).
- Prikazani: flajer flap (blok `.contact` ispod koraka 01–03, korak 02 = „Pozovite ili pišite nam"), katalog/QR meni hero (`.links` ispod dugmeta) i futer („Ili nam pišite" + `.links`). Na webu su linkovi, u PDF-u tekst.
- Sajt `carstvoukusa.rs` je ŽIV od 2026-10-20 (kod u `C:\dev\carstvo-ukusa`, hosting unlimited.rs).

## QR → živi sajt (2026-10-20)
- `URL` u `kartica.py` = `https://carstvoukusa.rs/meni/` (jelovnik na novom sajtu). Regenerisani: `docs/qr.svg`, `docs/qr.png`,
  `QR kartica za sto (4 x A6).pdf`, oba flajer PDF-a (QR na zadnjoj korici) i katalog. Provera flajera OK.
- Stari QR (GitHub Pages) i dalje radi: `build.py` u `docs/index.html` ubacuje skript koji na `*.github.io` preusmerava na
  `https://carstvoukusa.rs/meni/` (lokalni print iz `file://` ne preusmerava). GitHub Pages meni je sada samo most — izvor
  cena za sajt ostaje `meni_data.py` (`npm run menu` u sajtu).
- Štampane kartice/flajeri pre ovog datuma nose stari QR — rade preko preusmerenja, ali za novu štampu koristiti nove PDF-ove.
