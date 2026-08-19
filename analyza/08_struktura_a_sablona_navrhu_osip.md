# 📋 08. Struktura a šablona návrhu pro ESA OSIP (Industrial Framework)

Tento dokument definuje závaznou strukturu a obsahovou šablonu pro všech 6 návrhů (Idea Submissions) v rámci sady **Radixal Deep-Space Autonomy Suite (R-DAS)**. Šablona je postavena na principu **průmyslového softwarového inženýrství** a striktního realismu.

---

## 🏛️ 1. Hlavní filozofie návrhu: „Průmyslový embedded systém“

Každý návrh musí od prvního odstavce komunikovat jasné poselství:
- **Nejsme akademičtí teoretici:** Nezkoušíme nerealistické hluboké sítě ani experimentální runtimy.
- **Kosmický software je specifický průmyslový software:** Staví na determinismu, statické alokaci paměti, pravidlech MISRA-C a přísném dodržení časových rozpočtů.
- **Průmyslová reference:** Opíráme se o komerční zkušenost s vývojem nízkoúrovňového C kódu pro zpracování satelitních dat pro partnera v Norsku.

---

## 📑 2. Unifikovaná šablona návrhu (Max. 10 stran v angličtině)

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│             STRUKTURA FORMULÁŘE ESA OSIP (RADIXAL R-DAS FRAMEWORK)              │
└──────────────────────────────────────────────────────────────────────────────────┘
```

### Kapitola 1: The Problem (Definice operačního problému)
- **Obsah:** Popis úzkého hrdla současného průzkumu hlubokého vesmíru:
  - Zpoždění signálu 15–20 minut v jednom směru (40 min round-trip) znemožňuje řízení ze Země v reálném čase.
  - Úzké pásmo downlinku (Deep Space Network / Estrack) a omezení objemu přenášených dat na sondě Hera (max. 12 MB na 3h okno).
  - Přetížení pozemních operátorů rutinní kontrolou a manuálním vyhodnocováním snímků.

### Kapitola 2: The Solution (Architektura a algoritmické řešení)
- **Obsah:** Detailní popis navrženého algoritmu v C:
  - Matematický model a princip fungování (např. *Bio-Inspired Saliency Engine*, *Integer Wavelet Transform*, *INT8 Quantized Micro-CNN v TensorAreně*, *9stavový EKF*).
  - Vstupní data (AFC snímky 1020×1020, laserový dálkoměr PALT, telemetrie Data Poolu).
  - Výstupní produkty a jejich struktura.

### Kapitola 3: Technical Feasibility & Constraints (Technická proveditelnost)
- **Obsah:** Důkaz zvládnutí limitů platformy:
  - Cílový procesor: **GR712RC Dual-Core LEON3 (SPARC V8)**, takt 50 MHz.
  - Běhové prostředí: **100% Bare-metal C (bez OS)**, zákaz `malloc`/`free`.
  - Paměťový model: Pevně vyhrazená statická paměť (TensorArena / static pools), stack 64 KB (`0x40010000`), celkový otisk RAM pod 250 kB.
  - Soulad se standardy: **MISRA-C:2012** a **ECSS-E-ST-40C Category D**. Použití ESA knihovny `LibmCS`.

### Kapitola 4: Safety & Sandbox Compliance (Bezpečnost a izolace)
- **Obsah:** Garance nulového rizika pro primární misi:
  - Asynchronní, plně bezstavový (stateless) běh – kód nevyžaduje ukládání stavu mezi dny.
  - Okamžitá a bezpečná přerušitelnost v případě anomálie na sondě nebo přechodu do Safe Mode (žádný poškozený stav).
  - Striktní hardwarová izolace paměti (MMU na Core 1) – nulový přístup k I/O registrům a paměti Core 0.

### Kapitola 5: Compliance with Interfaces & Telemetry (Rozhraní a PUS)
- **Obsah:** Soulad s dodanými Annexy:
  - Volání platformových funkcí z [`hera_interface.h`](file:///c:/Users/vikto/Disk%20Google/Radixal/Zakázky/2026_026%20Hera%20Space%20Probe%20Code%20Contest/podklady/ANNEX_A_-_Hera_interface_API_documentation.pdf) (Annex A).
  - Seznam čtených telemetrických parametrů z Mission Data Poolu (Annex B).
  - Telemetrická disciplína: **PUS Service 3** (HK 1× za 10 min, 128 B), **PUS Service 5** (Eventy max. 3 za okno), **Science Reports** (celkem < 2,5 MB na 3h slot).

### Kapitola 6: Quantified Benefits (Kvantifikovaný přínos pro ESA)
- **Obsah:** Měřitelné přínosy podložené čísly:
  - Snížení objemu přenášených dat o 75–85 % (u komprese).
  - Zkrácení reakční doby na dynamické jevy z 40 minut na < 2 sekundy (u autonomního agenta).
  - Zvýšení hustoty navigačních bodů 4× bez zátěže pozemního střediska.
  - Strategický technologický transfer pro misi **ESA Ramses (Apophis 2029)**.

### Kapitola 7: Operational Concept (Operační profil 2–3h okna)
- **Obsah:** Přesný časový a stavový diagram denního běhu:
  1. *Boot & Initialization (t = 0–5 s):* Nastavení registrů SPARC, inicializace statických ukazatelů, odeslání úvodního HK reportu.
  2. *Data Ingestion (t = 5–20 s):* Čtení stavu z Data Poolu, vyžádání snímku z kamery AFC (`Hera_AFC_AcquireSingleImage`).
  3. *Deterministic Processing (t = 20–120 s):* Běh jádra algoritmu v C, vyhodnocení, generování vědeckých dat.
  4. *Telemetry Packaging (t = 120–180 s):* Zabalení výstupů do PUS paketů a uložení do Mass Memory.
  5. *Graceful Idle / Sleep:* Přechod do spánku (`Hera_Sleep`) nebo ukončení.

### Kapitola 8: Maturity & Verification Evidence (Zralost a ověření)
- **Obsah:** Důkaz, že nejde o hypotetický nápad na papíře:
  - Algoritmus je již v rámci přípravy návrhu naimplementován v ANSI C.
  - Úspěšně zkompilován toolchainem `sparc-gaisler-elf-gcc` (`-mcpu=leon3 -O2`).
  - Plně ověřen a otestován na reálném datasetu 2 400+ kalibračních snímků kamery AFC v emulátoru **QEMU LEON3**.

### Kapitola 9: Industrial Implementation Plan & Quality Assurance
- **Obsah:** Garance dodávky Fáze 2 do 31. května 2027:
  - Projektové milníky a Stage-Gate review proces.
  - Závazek dodat kompletní balík: **Full Source Code, DDF, SUM, ICD a V&V Test Report**.
  - Zavedené procesy QA a statické analýzy kódu podle standardu ECSS-E-ST-40C pro software Kategorie D.

### Kapitola 10: Proposing Organisation, Heritage & Team Profile
- **Obsah:** Představení společnosti a týmu:
  - **radixal s.r.o.:** Etablovaná softwarová společnost se zaměřením na vývoj spolehlivých průmyslových systémů.
  - **Průmyslová reference:** Vývoj nízkoúrovňového C kódu pro zpracování satelitních snímků a obrazových dat pro komerčního partnera v Norsku.
  - **Klíčový personál:** **Bc. Viktor Lošťák** (Chief Architect & Project Lead) + C embedded inženýři.
  - **Navržená poradní rada (Advisory Board):** Formální nabídka konzultací a společného review pro ESTEC Flight Software Section (**Jorge López Trescastro / HERA-IoD**), operátory ESOC a českou vědeckou obec (Astronomický ústav AV ČR Ondřejov).
