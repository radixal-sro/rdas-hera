# 🔍 16. Hloubkové review: Identifikace mezer a přidání další strategické hodnoty

Tento dokument představuje **kritické inženýrské a strategické review** celého našeho konceptu. Identifikuje 6 klíčových oblastí, které jsme doposud nepokryli, a které posunou naše návrhy z kategorie *„velmi dobré“* do kategorie *„naprosto bezkonkurenční a neodmítnutelné“*.

---

## 🎯 6 strategických prvků, které posunou návrh na absolutní špičku

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                   6 NOVÝCH HODNOTOVÝCH PRVKŮ PRO PROPOSALS                       │
├──────────────────────────────────────────────────────────────────────────────────┤
│ 1. 🛡️ **Softwarová radiační odolnost (SIFT / TMR na proměnných):**               │
│    - Ochrana proti překlopení bitů kosmickým zářením (Single Event Upsets - SEU).│
│                                                                                  │
│ 2. 🖥️ **Dodávka pozemního dekodéru a vizualizéru (Ground Segment Tooling):**    │
│    - Webový / Python dashboard pro operátory ESOC k okamžitému zobrazení dat.   │
│                                                                                  │
│ 3. 🎛️ **Za-letu konfigurovatelný blok parametrů (64B Telecommand Patching):**    │
│    - Možnost operátorů ladit prahy algoritmů bez nutnosti re-kompilace binárky. │
│                                                                                  │
│ 4. 📐 **Multimodální senzorická fúze (Kamera AFC + Laserový dálkoměr PALT):**    │
│    - Výpočet absolutního metrického měřítka kráterů fúzí fotonů a laseru.       │
│                                                                                  │
│ 5. 🔬 **Formální verifikace kódu (Frama-C / MISRA-C Compliance Matrix):**        │
│    - Matematický důkaz nepřítomnosti běhových chyb (Zero Runtime Exceptions).    │
│                                                                                  │
│ 6. 🌍 **Veřejný outreach a vzdělávací přesah (Czech Space Week & EU Schools):**  │
│    - Zapojení evropských studentů a amatérských astronomů do analýzy dat.        │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Detailní rozpracování jednotlivých prvků:

### 1. Softwarová radiační odolnost (Software-Implemented Fault Tolerance – SIFT):
- **Problém:** V meziplanetárním prostoru za magnetosférou Země zasahuje procesor kosmické záření. Přestože je čip GR712RC radiačně odolný, v registrech Core 1 může dojít k překlopení bitu (Single Event Upset – SEU).
- **Naše přidaná hodnota:** Do C kódu integrujeme **TMR (Triple Modular Redundancy)** pro klíčové navigační proměnné a **CRC32 kontrolní součty** pro váhy neuronových sítí v `TensorAreně`. Pokud software detekuje poškození vah v RAM, automaticky obnoví intaktní váhy ze záložního ROM bloku.
- **Dopad na komisi:** Jorge López (ESTEC FDIR) bude nadšen – prokážeme hluboké povědomí o kosmickém prostředí.

### 2. Pozemní vizualizační a dekódovací dashboard (Ground Segment Tooling):
- **Problém:** Operátoři v ESOCu a vědci nemají čas psát vlastní dekodéry pro surové hexadecimální PUS Science pakety.
- **Naše přidaná hodnota:** Jako součást dodávky Fáze 2 dodáme **otevřený pozemní software (R-DAS Ground Station Visualizer)** v Pythonu / Web UI, který automaticky:
  - Přebírá PUS pakety ze stanic Estrack,
  - Dekóduje komprimované vlnky a detekované krátery,
  - V reálném čase vykresluje 3D polohu sondy a mapu asteroidu.
- **Dopad na komisi:** Obrovská úleva pro letové operátory ESOCu – ušetříme jim týdny práce.

### 3. Za-letu laditelný konfigurační blok (In-Flight Telecommand Patching):
- **Problém:** Co když se světelné podmínky u asteroidu budou lišit od simulace a citlivost detektoru bude potřeba upravit?
- **Naše přidaná hodnota:** Vyhradíme pevný 64bajtový blok paměti (`0x40001000`) pro **konfigurační parametry** (citlivost prahování, kompresní poměr, expoziční offset). Operátoři mohou poslat drobný telekomand (PUS Service 128) a upravit chování softwaru bez nutnosti re-kompilace celého 100KB binárního souboru.

### 4. Multimodální senzorická fúze (Kamera AFC + Laser PALT):
- **Problém:** Samotná kamera vidí kráter pouze v pixelech (neví, zda má 5 metrů nebo 50 metrů).
- **Naše přidaná hodnota:** Software v C načítá z Mission Data Poolu výšku z laserového výškoměru **PALT** (`PALT_ALTITUDE_VAL`, vzorkování 10 Hz) a fúzuje ji s optickým obrazem kamery **AFC**. Výsledkem je **přesný metrický průměr a hloubka kráteru v metrech přímo na palubě sondy**.

### 5. Formální verifikace kódu (Frama-C & Zero-Warning Policy):
- **Naše přidaná hodnota:** Kód nebude pouze splňovat normu MISRA-C:2012, ale projde **formální matematickou verifikací pomocí nástroje Frama-C (ACSL anotace)**, která matematicky dokazuje:
  - Nulové riziko dělení nulou,
  - Nulové riziko přetečení bufferu (Buffer Overflow),
  - Nulové riziko uvíznutí v nekonečné smyčce (Worst-Case Execution Time guarantee).

### 6. Evropský veřejný outreach a vzdělávání (Public Engagement):
- **Naše přidaná hodnota:** Propojíme výsledky experimentu s festivalem **Czech Space Week** (organizovaným Ministerstvem dopravy ČR a agenturou CzechInvest) a připravíme vzdělávací balíček pro střední a vysoké školy v Evropě, kde si studenti budou moci na reálných datech z Hery vyzkoušet běh našeho algoritmu.

---

## 🏆 Co tato zjištění znamenají pro naše návrhy:

Tyto body zapracujeme do všech 6 proposals do kapitol *Technical Feasibility*, *Safety & Sandbox*, *Operational Concept* a *Benefits*. 

Návrhy radixalu tím získají punc **naprosté inženýrské dokonalosti**, jaká se v soutěžích OSIP prakticky nevyskytuje.
