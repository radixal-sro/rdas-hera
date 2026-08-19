# 🧠 02. Psychologie hodnotitelů, jejich skutečné motivace a vítězná strategie

Tento dokument analyzuje klíčové osoby a týmy v hodnoticí komisi ESA (OSIP), jejich skutečné profesní incentivy, vnitřní obavy, hodnoticí systém a konkrétní formulace (rétoriku), které v návrhu očekávají.

---

## 👥 1. Složení hodnoticí komise a profil aktérů

Hodnocení na platformě OSIP v rámci výzvy *Operations Innovations* provádí komise složená ze 3 hlavních zájmových skupin:

```
                  ┌─────────────────────────────────────────────────────────┐
                  │              HODNOTICÍ PANEL ESA (OSIP)                 │
                  └─────────────────────────────────────────────────────────┘
                                   │
         ┌─────────────────────────┼─────────────────────────┐
         ▼                         ▼                         ▼
┌───────────────────┐    ┌───────────────────┐    ┌───────────────────┐
│ 1. Jorge López    │    │ 2. ESOC Flight    │    │ 3. Ian Carnelli   │
│    Trescastro     │    │    Control Team   │    │    & Vedení mise │
│ (ESTEC / TEC-SW)  │    │ (Darmstadt, ESOC) │    │ (Planetary Def.)  │
│ ➔ Technický filtr │    │ ➔ Bezpečnostní    │    │ ➔ Strategický a   │
│    a "Gatekeeper" │    │    veto a klid    │    │    PR dopad       │
└───────────────────┘    └───────────────────┘    └───────────────────┘
```

---

## 🎭 2. Deklarovaná vs. Skutečná motivace a vnitřní obavy

| Aktér | Deklarovaná motivace (Oficiální PR) | SKUTEČNÁ interní motivace (Proč to dělají) | Vnitřní obava / Alergie (Čeho se děsí) |
| :--- | :--- | :--- | :--- |
| **Jorge López Trescastro** *(Inženýr palubního SW, ESTEC)* | *„Hledáme inovativní myšlenky pro autonomii a AI v hlubokém vesmíru.“* | **Chce dokázat, že jím navržená architektura LEON3 sandboxu funguje bezchybně.** Úspěch experimentu je pro něj profesním a publikačním triumfem (články na konferencích EDHPC / DASIA). | **„AI Buzzword Hand-waving“:** Nesnáší naivní akademické návrhy, které slibují hluboké neuronové sítě / LLM, ale autor neví, co je to 50MHz CPU, SPARC architektura a statická paměť. |
| **ESOC Flight Control** *(Operátoři řízení letu, Darmstadt)* | *„Podporujeme otevřenost platformy a nové operační postupy.“* | **Chtějí „ZERO DRAMA“ a maximální provozní klid.** Každý cizí software na sondě za 300+ mil. EUR je pro ně provozní riziko. Nechtějí noční pohotovost ani řešení zahlcené paměti. | **Pád do Safe Mode:** Že experiment způsobí CPU lockup, zaplní Mass Memory nebo spustí lavinu falešných poplachů, kvůli čemuž by museli svolávat mimořádnou směnu. |
| **Ian Carnelli** *(Hera Mission Manager)* | *„Otevíráme hluboký vesmír evropským univerzitám a firmám.“* | **Hledá silný technologický odkaz mise (Legacy) a politický kapitál pro ESA.** Potřebuje letem prověřené technologie pro připravovanou misi **Ramses (Apophis 2029)**. | **Nezajímavý pokus nebo trapas:** Že vybraný experiment selže na banální chybě, nebo že půjde o triviální kód bez hmatatelného přínosu pro budoucí planetární obranu. |

---

## 📊 3. Systém a kritéria hodnocení na platformě OSIP

Hodnocení probíhá podle pevné bodovací matice ESA:

1. **Novelty & Innovation (25 %):** Originalita přístupu. Zda jde o skutečnou autonomii a přidanou hodnotu, nikoli jen základní RLE kompresi.
2. **Scientific & Operational Value (25 %):** Kvantifikovatelný provozní přínos (např. *„Ušetří 80 % objemu downlinku a zkrátí reakční dobu z 40 minut na 2 sekundy“*).
3. **Technical Credibility & Feasibility (30 % – NEJTVRDŠÍ FILTR):** Realističnost návrhu v C na 50MHz procesoru LEON3 s pevnou pamětí.
4. **Safety & Sandbox Compliance (20 %):** Dodržení izolace Core 1, limitu 12 MB, PUS standardů a bezstavové architektury (stateless execution).

---

## 🎯 4. Co přesně chtějí slyšet (Vítězná rétorika a klíčové výrazy)

### A. Pro Jorgeho (Technický inženýrský jazyk):
- **Striktní embedded realismus:** Používat termíny *MISRA-C compliant, zero dynamic allocation, static buffer pooling, deterministic worst-case execution time (WCET), LibmCS adherence, ECSS-E-ST-40C Category D*.
- **Konkrétní čísla namísto vágních slibů:**
  - ❌ *Nevhodné:* „Použijeme pokročilou AI síť pro detekci kráterů.“
  - ✔️ *Vítězné:* „Využijeme 8-bit kvantizovanou mikro-konvoluční síť (INT8 Micro-CNN) o velikosti vah 38,4 kB, která při taktu 50 MHz vyžaduje 1,2 milionu MAC operací (~24 ms na patch), s celkovým statickým paměťovým otiskem 185 kB RAM včetně 64KB stacku.“
- **Důkaz připravenosti:** Explicitně uvést, že algoritmus je **již validován na dodaném archivu `AFC_images.tar.gz` a kompilován pod `sparc-gaisler-elf-gcc` v emulátoru QEMU LEON3**.

### B. Pro ESOC (Operátory řízení letu):
- **„Stateless“ & Asynchronní architektura:**
  - Zdůraznit: *„Software je navržen jako striktně bezstavový (stateless) mezi jednotlivými dny. Pokud Core 0 experiment kdykoliv násilně ukončí (např. při Safe Mode), nedojde k žádnému poškození dat ani nekonzistenci stavu.“*
- **Telemetrická ukázněnost:**
  - Zdůraznit: *„Striktní dodržení PUS standardu: Housekeeping (Service 3) generován pouze 1× za 10 minut (128 B, hluboko pod limitem 256 B / 5 min), Eventy (Service 5) výhradně při klíčové detekci (max 3 eventy za 3 hodiny). Celkový vědecký downlink nepřekročí 2,1 MB (pouze 17,5 % povoleného 12MB limitu).“*

### C. Pro Iana Carnelliho (Strategický a politický dopad):
- **Vazba na budoucí mise ESA:**
  - Přímo propojit experiment s misí **ESA Ramses (Apophis 2029)** a **Comet Interceptor**:
  - Formulace: *„Tento experiment poskytne první letem ověřenou demonstraci (TRL 8) plně autonomního palubního vyhodnocování snímků pro evropskou planetární obranu, která je přímo aplikovatelná pro nadcházející misi ESA Ramses k asteroidu Apophis.“*
- **Evropská technologická suverenita:**
  - Zdůraznit, že řešení staví na čistě evropském ekosystému (LEON3 / GR712RC, LibmCS, evropské standardy ECSS).
