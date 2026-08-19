# 💰 07. Financování, smluvní model, rozpočty a duševní vlastnictví (IPR)

Tento dokument detailně popisuje finanční a smluvní mechanismus soutěže ESA OSIP, způsoby úhrady vývojových nákladů, princip geografické návratnosti (Geo-Return) pro Českou republiku a podmínky ochrany duševního vlastnictví (IPR).

---

## 1. Zdroje financování vývoje (Kdo a jak projekt zaplatí)

Vývoj experimentálního softwaru neplatí dodavatel z vlastních zdrojů. Celý inženýrský cyklus je financován **Evropskou vesmírnou agenturou (ESA)** na základě mezinárodního smluvního rámce:

```
                  ┌─────────────────────────────────────────────────────────┐
                  │                 FINANČNÍ TOKY PROJEKTU                  │
                  └─────────────────────────────────────────────────────────┘
                                   │
         ┌─────────────────────────┴─────────────────────────┐
         ▼                                                   ▼
┌─────────────────────────────────┐         ┌─────────────────────────────────┐
│ 1. ESA OSIP Inovační Kontrakt   │         │ 2. Česká národní obálka v ESA   │
│    (Program Operations Innov.)  │         │    (Princip Geo-Return)         │
│ ➔ Přímá fixní platba od ESA     │         │ ➔ Finance z Ministerstva        │
│    za splnění milníků vývoje    │         │    dopravy ČR vyhrazené pro     │
│    (typicky 50 000–100 000+ EUR)│         │    český kosmický průmysl       │
└─────────────────────────────────┘         └─────────────────────────────────┘
```

### A. Přímý inovační kontrakt ESA (EISI / Fixed-Price Innovation Agreement)
- **Mechanismus:** Po schválení návrhu v 1. fázi (v polovině října 2026) obdrží úspěšná komerční firma od ESA návrh smlouvy (**Firm Fixed Price Contract**).
- **Alokace:** Kontrakt pokrývá náklady na inženýrskou práci, adaptaci algoritmů do MISRA-C, verifikaci v QEMU simulátoru a sepsání letové dokumentace (DDF, SUM, ICD, V&V report).
- **Struktura milníkových plateb:**
  1. **Advance Payment (Záloha):** Vyplacena ihned po podpisu smlouvy (podzim 2026).
  2. **Mid-Term Payment (Průběžná platba):** Vyplacena po dokončení architektury a testů v simulátoru (jaro 2027).
  3. **Final Delivery Payment (Doplatek):** Vyplacena po odevzdání a schválení finálního letového balíku do 31. května 2027.

### B. Česká národní alokace v ESA a princip „Geo-Return“
- Česká republika (přes Ministerstvo dopravy ČR – Odbor kosmických aktivit) platí roční příspěvky do volitelných a povinných programů ESA.
- Podle pravidel ESA platí princip **geografické návratnosti (Geo-Return)**: Peníze, které ČR odvede do rozpočtu ESA, se **musí vrátit formou zakázek pro české firmy a výzkumné instituce**.
- Když česká společnost (**radixal s.r.o.**) uspěje ve výzvě OSIP, ESA kontrakt profinancuje z české národní obálky, což plní národní kvóty návratnosti ČR.

---

## 🛰️ 2. Hodnota letového provozu zdarma (In-Kind plnění od ESA)

Kromě přímého financování vývojových prací poskytuje ESA vítězným týmům bezplatně veškerou letovou a komunikační infrastrukturu:

| Složka letové podpory | Popis a komerční hodnota |
| :--- | :--- |
| **Komunikační síť Estrack** | Využití tří 35metrových hlubokovesmírných antén (Malargüe, New Norcia, Cebreros) pro downlink dat z asteroidu. Hodnota v řádu **desítek tisíc EUR za hodinu spojení**. |
| **Letové středisko ESOC (Darmstadt)** | Čas letových operátorů a inženýrů letové dynamiky v meziplanetárním sále. |
| **Letová validace v hlubokém vesmíru** | Získání nejvyššího technologického stupně zralosti **TRL 8/9 (Flight Proven)** ve vzdálenosti 150 milionů km od Země. |

---

## 🔒 3. Ochrana duševního vlastnictví (IPR)

Podle oficiálních všeobecných podmínek OSIP (*General Conditions of Participation, Článek VII*):

- **100 % duševního vlastnictví (IPR), know-how a zdrojových kódů zůstává společnosti radixal s.r.o.**
- ESA získává pouze bezplatnou, nevýhradní licenci k tomu, aby:
  1. Zkompilovaný binární software nahrála (uplinkovala) na palubní počítač sondy Hera.
  2. Spustila kód v průběhu letové kampaně v srpnu 2027.
  3. Publikovala shrnující vědecké zprávy o výsledcích demonstrace.
- **Komerční využití:** radixal s.r.o. může vyvinuté knihovny pro kompresi, autonomní navigaci a detekci anomálií následně volně prodávat, komerčně licencovat nebo nabízet dalším vesmírným misím (např. mise Ramses, komerční družicové konstelace na oběžné dráze Země).

---

## 📋 4. Shrnutí obchodních a finančních výhod pro radixal s.r.o.

1. **Nulové finanční riziko:** Náklady na vývoj v C jsou hrazeny fixním kontraktem ESA.
2. **Globální technologická reference:** Status dodavatele letového softwaru pro vlajkovou meziplanetární misi ESA.
3. **Plné vlastnictví vyvinutého kódu a AI modelů** pro komerční monetizaci.
