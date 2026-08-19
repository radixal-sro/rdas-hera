# 🏢 14. Firemní portrét radixal s.r.o. – Zkušenosti, portfolio a positioning

Tento dokument shrnuje kompletní historii reálných zakázek a referencí společnosti **radixal s.r.o.** a na jejich základě staví **autoritativní, průmyslově vyzrálý portrét firmy** pro potřeby výběrové komise ESA a mezinárodních kosmických projektů.

---

## 🏛️ 1. Kdo je radixal s.r.o. (The Corporate Identity)

Společnost **radixal s.r.o.** (založena v červnu 2016, sídlo Brno, základní kapitál 900 000 Kč) je zavedená softwarová a inženýrská společnost specializující se na **návrh, vývoj a dlouhodobý provoz mission-critical systémů, vestavného softwaru s vysokými nároky na bezpečnost a spolehlivost (Safety-Critical Systems) a velkých distribuovaných architektur**.

### 👥 Řídicí a realizační tým společnosti (The Core Leadership Team)

Projekty pro ESA jsou vedeny osvědčeným týmem tří společníků a jednatelů s jasnou dělbou odpovědnosti:

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                   REALIZAČNÍ A ŘÍDICÍ TRIÁDA SPOLEČNOSTI RADIXAL                 │
├──────────────────────────────────────────────────────────────────────────────────┤
│ 🔹 **Bc. Viktor Lošťák** – Lead Architect & Principal Investigator (PI)          │
│    - Návrh systémové a algoritmické architektury pro hluboký vesmír              │
│    - Vědecko-operační koncepty, AI & TinyML modely, koordinace s ESA OSIP        │
│                                                                                  │
│ 🔹 **Ing. Petr Slepička** – Engineering Lead & Delivery Director                 │
│    - Přímá exekuce a řízení softwarové dodávky (Implementation & Delivery)      │
│    - MISRA-C compliance, statická analýza, QEMU integrační harness, QA (ECSS)   │
│                                                                                  │
│ 🔹 **Mgr. David Riedl** – Executive Director & Operations Governance             │
│    - Operační a smluvní řízení projektu (ESA Contract Management & Compliance)   │
│    - Právní rámec, IPR ochrana, alokace inženýrských kapacit a harmonogram       │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🧭 2. Čtyři inženýrské pilíře radixalu postavené na reálných zakázkách

Prozkoumáním kompletní historie zakázek jsme identifikovali 4 klíčové technologické domény, které přímo korelují s požadavky ESA na software pro sondu Hera:

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                   ČTYŘI TECHNOLOGICKÉ PILÍŘE RADIXAL S.R.O.                      │
├────────────────────────────────────────┬─────────────────────────────────────────┤
│ 1. 🛡️ **Safety-Critical & Embedded**   │ 2. 🛰️ **Space, Satellite & Optics**     │
│    - Drážní zabezpečovací systémy (SIL)│    - Satelitní zpracování v C (Norsko)  │
│    - Průmyslová automatizace           │    - Fyzikální a meteorologická pole    │
│    - Reference: **AK Signal, Schneider**│    - 3D CAD/Rendering: **HiStruct/Shade**│
├────────────────────────────────────────┼─────────────────────────────────────────┤
│ 3. 🔒 **Air-Gapped & Defense Systems** │ 4. ⚡ **Real-Time Telemetry & SCADA**   │
│    - Autonomní agenti bez internetu    │    - Distribuované energetické sítě     │
│    - Kritická státní infrastruktura    │    - Real-Time Pub-Sub notifikace       │
│    - Reference: **URC Systems, CENDIS** │    - Reference: **E.ON, Swiss Life**    │
└────────────────────────────────────────┴─────────────────────────────────────────┘
```

---

## 📂 3. Detailní zmapování referenčních projektů radixalu

### Pilíř 1: Bezpečnostně-kritické a vestavné systémy (Safety-Critical & Deterministic C/C++)
- **AK Signal Brno (Drážní zabezpečovací systémy):**
  - Vývoj a refaktoring řídicího a integračního softwaru pro železniční zabezpečovací techniku podléhající přísným normám funkční bezpečnosti (SIL).
  - Deterministická C/C++ jádra, cross-platformní abstrakční vrstvy (Linux/Windows), přísné integrační a regresní testování.
- **Schneider Electric:**
  - Vývoj a konzultace pro globálního lídra v oblasti průmyslové automatizace a řízení energetických celků.

### Pilíř 2: Zpracování satelitních, optických a fyzikálních dat (Space & Remote Sensing)
- **Komerční reference v C (Norsko – Earth Observation):**
  - Zakázkový vývoj nízkoúrovňových C algoritmů pro reálný čas: filtrace, rektifikace a sémantické zpracování družicových a radarových snímků.
- **Meteo & Oekoplan (Fyzikální a meteorologické modely):**
  - Zpracování surových senzorických toků z meteorologických a energetických čidel, predikční matematické modely a termální audity.
- **Shade / HiStruct (CAD Rendering Server):**
  - Vývoj nízkoúrovňového grafického serveru a geometrického jádra pro manipulaci s 3D geometrií v reálném čase.

### Pilíř 3: Izolované, vysoce zabezpečené a národní systémy (Air-Gapped & Critical Infrastructure)
- **URC Systems (Obranné a bezpečnostní technologie):**
  - Návrh distribuovaného systému autonomních agentů (Controller-Worker) pro bezpečné instalace a aktualizace v izolovaných (air-gapped) prostředích s jednosměrnými datovými diodami a nulovou dostupností internetu (přesný analog hlubokého vesmíru!).
- **CENDIS s.p. (Centrum dopravních informačních systémů – Ministerstvo dopravy ČR):**
  - Dlouhodobý vývoj a údržba národních dopravních agendových systémů (OneTicket, dálnice, mýto) s garancí 24/7/365 dostupnosti a zpracováním milionů transakcí denně.
- **Strabag:**
  - Zakázkový logistický a skladový systém pro nadnárodní stavební korporaci.

### Pilíř 4: Distribuovaná telemetrie, energetika a Real-Time Pub-Sub
- **E.ON (Distribuce & Energetická flexibilita):**
  - Vývoj HMI rozhraní a telemetrických integračních modulů pro řízení distribuční energetické sítě v reálném čase (SCADA integrace).
- **Swiss Life Select (DACH Region / ČR):**
  - Zakázkový vývoj distribuovaných pub-sub notifikačních komponent, transakčních enginů a velkých ERP platforem s vysokou datovou integritou.
- **SolSol & Schlieger:**
  - Komplexní řídicí a dohledové portály pro fotovoltaické elektrárny, bateriová úložiště a střídače.

---

## 🎯 4. Oficiální profil společnosti pro návrh ESA OSIP (The Executive Pitch)

V návrzích pro ESA budeme firmu prezentovat tímto neprůstřelným profilem:

> **„radixal s.r.o. is an established European mission-critical software engineering company with a decade-long track record of delivering high-reliability embedded systems, safety-critical railway controls, defense-grade air-gapped architectures, and real-time remote sensing software across ESA Member States (including Norway, Germany, Switzerland, and the Czech Republic).**
>
> **The company is steered by a dedicated executive and engineering leadership triad: Lead Architect Bc. Viktor Lošťák (System Architecture & Mission Concept), Engineering Director Ing. Petr Slepička (Software Implementation, MISRA-C & Delivery Execution), and Executive Director Mgr. David Riedl (Operations, Project Governance & Compliance).**
>
> **Combining rigorous industrial quality standards (MISRA-C, SIL functional safety compliance, zero-heap deterministic execution) with deep expertise in bare-metal systems, distributed telemetry, and edge computing, radixal guarantees the on-time and verified delivery of all mission deliverables according to ECSS-E-ST-40C Category D standards.“**

---

## 🏆 Proč je tento týmový profil dokonalý pro hodnotitele ESA:

1. **Eliminace personálního rizika (No Single-Point-of-Failure):** Komise vidí stabilní řídicí trojici společníků, kde architektura (Bc. Viktor Lošťák), exekuce vývoje (Ing. Petr Slepička) i operační řízení (Mgr. David Riedl) mají jasného garanta.
2. **Průmyslová a bezpečnostní zkušenost:** Reálné reference z drážních systémů (AK Signal), energetiky (E.ON, Schneider) a obranného průmyslu (URC Systems).
3. **Prověřená schopnost mezinárodních dodávek:** Zakázky pro komerční partnery v Norsku a DACH regionu.
