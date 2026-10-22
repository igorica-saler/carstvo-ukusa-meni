# Zajednički podaci menija Carstvo Ukusa 2026 — jedini izvor istine za katalog, flajer i mobilni meni
import html, pathlib

ROOT = pathlib.Path(__file__).parent
PHONE = "063/821-66-78"
PHONE_TEL = "+381638216678"
EMAIL = "carstvo.ukusa@gmail.com"
SITE = "carstvoukusa.rs"
SITE_URL = "https://carstvoukusa.rs"
INSTAGRAM = "@carstvoukusa"
INSTAGRAM_URL = "https://www.instagram.com/carstvoukusa/"
FACEBOOK = "Carstvo Ukusa"
FACEBOOK_URL = "https://www.facebook.com/CarstvoUkusaCatering/"

# (naziv, opis, cena, jedinica, oznaka)
KG, KOM = "din/kg", "din/kom"
SECTIONS = [
    ("Predjelo", "Hladne plate", [
        ("Mix predjelo lux", "beli kravlji sir, bajuval, brie, mocarela, gorgonzola, dimljeni kačkavalj, suvo meso, kulen, goveđa, zimska, biber blok, kobasica u parmezanu", 3500, KG, "Lux"),
        ("Mix predjelo standard", "edamer kačkavalj, beli kravlji sir, feta sir, zimska kobasica, kulen, suvo meso, suvi vrat", 3000, KG, "Standard"),
    ]),
    ("Finger food", "Zalogaji za koktel i proslave", [
        ("Kanapei mrsni lux", "na bavarskoj kifli, sa različitim namazima i kulenom, zimskom kobasicom, suvim mesom, goveđom kobasicom, kobasicom u parmezanu, biber blokom", 2500, KG, ""),
        ("Kanapei mrsni standard", "na bavarskoj kifli, sa različitim namazima i kulenom, zimskom kobasicom, suvim mesom, goveđom kobasicom", 2000, KG, ""),
        ("Posni kanapei", "na bavarskoj kifli, sa različitim namazima i plodovima mora, lososom, inćunima", 2000, KG, "posno"),
        ("Punjene korpice", "gorgonzola sos, kikiriki sos, ruska, urnebes, pileća, susam salata", 2000, KG, ""),
        ("Rolati, slana torta", "spanać, ajvar", 1500, KG, ""),
        ("Snack sticks", "beli kravlji sir, cherry paradajz, suvo meso, crne masline, baby corn", 2000, KG, ""),
        ("Brusketi 3 vrste", "dimljeni losos, caprese, gorgonzola i suvo meso", 2000, KG, ""),
        ("Rolovani štapići sa pršutom", "", 3500, KG, ""),
        ("Trouglići sa kajmakom i suvim mesom", "", 3000, KG, ""),
        ("Mini burger", "juneće meso, edamer, pavlaka, puterica", 1500, KG, ""),
        ("Mini sendviči", "šunka, rendani kačkavalj, pavlaka, puterica", 1200, KG, ""),
        ("Sendvič u domaćoj puter kroasan kifli", "", 2200, KG, ""),
        ("Slane pohovane palačinke", "pileći file, kačkavalj, gorgonzola sos", 1500, KG, ""),
        ("Piletina u tortilji", "", 1500, KG, ""),
    ]),
    ("Pecivo", "Domaće, iz naše kuhinje", [
        ("Naan bread", "", 1000, KG, ""),
        ("Somuni", "", 50, KOM, ""),
        ("Domaće kiflice, projice sa sirom", "", 1000, KG, ""),
        ("Kroasan puter kifle", "", 1500, KG, ""),
        ("Zemičke sa peršunom i belim lukom", "", 1000, KG, ""),
        ("Mini pice", "", 1000, KG, ""),
        ("Domaće pite, gibanica sa sirom", "pite sa sirom, mesom ili krompirom", 1300, KG, ""),
    ]),
    ("Specijaliteti od mesa", "Sa roštilja, iz sača i pušnice", [
        ("Roštilj standard", "ćevapi, leskovački uštipci, rolovano belo meso, svinjski ražnjić, gurmanska kobasica, pileći file, batak na žaru", 1800, KG, ""),
        ("Pileći ražnjići sa povrćem", "", 1800, KG, ""),
        ("Dimljena vešalica", "", 2000, KG, ""),
        ("Dimljeni vrat", "", 2000, KG, ""),
        ("Dimljene butkice ispod sača", "", 1800, KG, ""),
        ("Dimljeni batak", "", 1900, KG, ""),
        ("Domaće kobasice, ćevapi, uštipci", "", 2000, KG, ""),
        ("Svinjska rebra u BBQ sosu", "", 2000, KG, ""),
        ("Medaljoni u sosu od pečuraka", "", 2000, KG, ""),
        ("Piletina u sosu od kikirikija", "", 2000, KG, ""),
        ("Piletina u gorgonzola sosu", "", 2000, KG, ""),
        ("Karađorđeva šnicla", "", 2000, KG, ""),
        ("Plava traka", "", 2000, KG, ""),
        ("Bečka šnicla", "", 1800, KG, ""),
        ("Pileći štapići u susamu", "", 1800, KG, ""),
    ]),
    ("Riblji specijalitet", "Sa žara i iz tiganja", [
        ("Panirani oslić / oslić na žaru", "", 1200, KG, ""),
        ("Skuša na žaru", "", 1600, KG, ""),
        ("Pastrmka na žaru", "", 1800, KG, ""),
        ("Dimljena pastrmka fileti", "", 2800, KG, ""),
        ("Šaran šnicle", "", 2200, KG, ""),
        ("Panirani bakalar, panirani kolutići lignje, panirani losos", "", 2000, KG, ""),
    ]),
    ("Sveže salate", "Sezonsko povrće, spremljeno istog dana", [
        ("Paradajz salata", "", 600, KG, ""),
        ("Srpska salata", "", 600, KG, ""),
        ("Šopska salata", "", 600, KG, ""),
        ("Grčka salata", "", 600, KG, ""),
        ("Vitaminska salata", "", 700, KG, ""),
        ("Mix zelene salate", "lollo rosso, lollo bianco, iceberg, puterica", 800, KG, ""),
        ("Kupus salata", "", 600, KG, ""),
        ("Kiseli kupus", "", 600, KG, "sezonski"),
        ("Cvekla", "", 600, KG, ""),
        ("Cezar salata", "", 1200, KG, ""),
        ("Salata sa tunjevinom", "", 900, KG, ""),
        ("Salata sa pečurkama", "", 900, KG, ""),
    ]),
    ("Kremaste salate", "Klasici svake trpeze", [
        ("Ruska salata", "", 900, KG, "posna opcija"),
        ("Pileća salata", "", 900, KG, ""),
        ("Susam salata", "", 900, KG, ""),
        ("Mimoza salata", "", 900, KG, ""),
        ("Šampinjoni salata", "", 900, KG, "posna opcija"),
        ("Urnebes salata", "", 900, KG, ""),
        ("Goveđa salata", "", 900, KG, ""),
        ("Kukuruz salata", "", 900, KG, "posna opcija"),
        ("Tunjevina salata", "", 900, KG, "posno"),
        ("Tartar sos", "", 900, KG, ""),
    ]),
    ("Prilozi", "Topli dodaci glavnim jelima", [
        ("Pomfrit", "", 800, KG, ""),
        ("Grilovano povrće", "", 1400, KG, ""),
        ("Grilovane pečurke", "", 1400, KG, ""),
        ("Aromatizovani krompir", "", 900, KG, ""),
        ("Pohovani kačkavalj", "", 2000, KG, ""),
        ("Pirinač sa povrćem", "", 800, KG, ""),
        ("Pekarski krompir", "", 800, KG, ""),
        ("Krompir sa blitvom", "", 800, KG, ""),
    ]),
]

INK, PAPER, SAGE = "#1E3328", "#F6F1E7", "#9CC3B1"

e = html.escape


def price(n):
    return f"{n:,}".replace(",", ".")


def stavki(n):
    if n % 10 == 1 and n % 100 != 11:
        return f"{n} stavka"
    if n % 10 in (2, 3, 4) and n % 100 not in (12, 13, 14):
        return f"{n} stavke"
    return f"{n} stavki"


def seal(fg, bg, cls="seal"):
    """HACCP pečat kao vektor (isti raspored kao original: dva prstena, tekst u luku, HACCP preko sredine)."""
    uid = cls.split()[-1]
    return f'''<svg class="{cls}" viewBox="0 0 200 200" aria-label="HACCP">
  <defs>
    <path id="{uid}-top" d="M 31,100 A 69,69 0 0 1 169,100"/>
    <path id="{uid}-bot" d="M 16,100 A 84,84 0 0 0 184,100"/>
  </defs>
  <circle cx="100" cy="100" r="93" fill="none" stroke="{fg}" stroke-width="5"/>
  <circle cx="100" cy="100" r="61" fill="none" stroke="{fg}" stroke-width="3.2"/>
  <g fill="{fg}" font-family="Barlow Condensed, sans-serif" font-weight="700" letter-spacing="1.2">
    <text font-size="17"><textPath href="#{uid}-top" startOffset="50%" text-anchor="middle">Hazard • Analysis</textPath></text>
    <text font-size="17"><textPath href="#{uid}-bot" startOffset="50%" text-anchor="middle">Critical • Control • Point</textPath></text>
  </g>
  <rect x="6" y="80" width="188" height="40" fill="{bg}"/>
  <text x="100" y="116" text-anchor="middle" fill="{fg}" font-family="Barlow Condensed, sans-serif" font-weight="800" font-size="50" letter-spacing="2">HACCP</text>
</svg>'''


