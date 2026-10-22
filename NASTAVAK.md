# Carstvo Ukusa — katalog 2026 i QR meni

## Kako se gradi
- `python build.py` — iz liste `SECTIONS` pravi mobilni meni `docs/index.html` (stil u `meni.css`), pa TU ISTU stranicu štampa u `Katalog Carstvo Ukusa 2026 - novi dizajn.pdf` (A4, kopija u `docs/katalog.pdf`). Katalog i QR meni su identični po konstrukciji; razlike samo pod `@media print` u `meni.css`.
- `python kartica.py` — QR kod za `URL` → `docs/qr.svg`, `docs/qr.png` i `QR kartica za sto (4 x A6).pdf` (A4 list, 4 kartice za sečenje).
- Isti `kartica.py` pravi i **QR karticu za Google recenzije** (2026-10-20): `REVIEW_URL` = `search.google.com/local/writereview?placeid=ChIJl4OPG_x-WkcR3blpMtc2mq8` (Place ID Google profila „Carstvo Ukusa, Hercegovačka 37", izveden iz Maps feature id-a `0x475a7efc1b8f8397:0xaf9a36d73269b9dd`, link proveren u browseru) → `docs/qr-recenzije.svg/png` i `QR kartica Google recenzije (4 x A6).pdf`. Varijante su u rečniku `CARDS`; kartica recenzija ima klasu `rev` (manji logo i QR, jer ima zvezdice + 3 reda teksta — inače preliva telefon).
- Na Google profilu stoji sajt `carstvoukusa.com` i telefon 013 314825 — vlasnik treba da promeni sajt na `carstvoukusa.rs` u Google Business profilu (nije urađeno).
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
- `PLAN` (grama po osobi: predjelo **100** (vlasnik 2026-10-20), finger food 120, meso/riba **350** (vlasnik 2026-10-15, potvrđeno 2026-10-21; sajt usklađen na 350), prilozi 150, salate 150, pecivo 2 kom) — ostale vrednosti su i dalje pretpostavka. Menja se samo u `flajer.py`.
- v1 (karirani stolnjak, Fraunces/Manrope) je u git istoriji: commit 953fb10.
- Za štampariju: 2/2 boje, papir 170–200 g mat, bleed 3 mm, roll fold (unutrašnji panel 97 mm). Referentni skenovi u `skenirani flyer/`.
- Sledeće: digitalna verzija flajera (korisnik najavio).

## Kontakti (2026-10-15)
- Mejl `carstvo.ukusa@gmail.com` (ZVANIČNI, potvrdio korisnik 2026-10-20 — isti i na sajtu), sajt `carstvoukusa.rs` (bez www; na flajeru pod QR-om i uz telefon, na katalogu u heroju i futeru, na QR kartici), Instagram `@carstvoukusa`, Facebook prikaz „Carstvo Ukusa" (link ostaje `facebook.com/CarstvoUkusaCatering`, korisnik 2026-10-20) — konstante `EMAIL`, `SITE`, `SITE_URL`, `INSTAGRAM(_URL)`, `FACEBOOK(_URL)` u `meni_data.py` (ne zvati `WEB` — sudara se sa `WEB = ROOT/'docs'` u build.py).
- Prikazani: flajer flap (blok `.contact` ispod koraka 01–03, korak 02 = „Pozovite ili pišite nam"), katalog/QR meni hero (`.links` ispod dugmeta) i futer („Ili nam pišite" + `.links`). Na webu su linkovi, u PDF-u tekst.
- Sajt `carstvoukusa.rs` je ŽIV od 2026-10-20 (kod u `C:\dev\carstvo-ukusa`, hosting unlimited.rs).

## QR → živi sajt (2026-10-20)
- `URL` u `kartica.py` = `https://carstvoukusa.rs/meni/` (jelovnik na novom sajtu). Regenerisani: `docs/qr.svg`, `docs/qr.png`,
  `QR kartica za sto (4 x A6).pdf`, oba flajer PDF-a (QR na zadnjoj korici) i katalog. Provera flajera OK.
- Stari QR (GitHub Pages) i dalje radi: `build.py` u `docs/index.html` ubacuje skript koji na `*.github.io` preusmerava na
  `https://carstvoukusa.rs/meni/` (lokalni print iz `file://` ne preusmerava). GitHub Pages meni je sada samo most — izvor
  cena za sajt ostaje `meni_data.py` (`npm run menu` u sajtu).
- Štampane kartice/flajeri pre ovog datuma nose stari QR — rade preko preusmerenja, ali za novu štampu koristiti nove PDF-ove.
- 2026-10-20: `build.py` kopira katalog PDF i u `C:/dev/carstvo-ukusa/frontend/public/katalog-carstvo-ukusa-2026.pdf`
  (dugme „Preuzmi jelovnik (PDF)" na sajtu /meni/). Posle izmene menija: `python build.py` → u sajtu `npm run build` + prenos `out/`.

## 2026-10-22
- Nazivi (vlasnik): „Sendvič u domaćoj puter kroasan kifli", „Kroasan puter kifle", „Panirani bakalar, panirani kolutići lignje, panirani losos" — samo u `meni_data.py`; regenerisani flajer (oba PDF-a), katalog, QR meni i sajt (id u `lib/engine/suggest.ts` sajta promenjen na `pecivo--kroasan-puter-kifle`). Objavljeno na carstvoukusa.rs.
