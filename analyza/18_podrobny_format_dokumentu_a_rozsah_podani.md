# 📑 18. Podrobný formát dokumentů, rozsah a struktura podání na ESA OSIP

Tento dokument přesně specifikuje **formáty souborů, rozsahové limity, jazyk a strukturu balíčků**, které se odevzdávají do **1. fáze (do 15. září 2026)** a následně do **2. fáze (do 31. května 2027)**.

---

## 📅 1. FÁZE 1: Co přesně posíláme do 15. září 2026

Podání probíhá elektronicky přes portál **ESA OSIP (ideas.esa.int)** v rámci výzvy *„Call for Ideas: Autonomous Software Experiments on Hera“*.

Pro každou z našich 6 kategorií odevzdáváme **jeden ucelený podávací balík (Submission Package)**:

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                   STRUKTURA PODÁVACÍHO BALÍKU PRO FÁZI 1 (OSIP)                  │
├──────────────────────────────────────────────────────────────────────────────────┤
│ 1. 🌐 **Textová pole ve webovém formuláři OSIP (Web Submission Form):**         │
│    - Vyplnění povinných polí (Problem, Solution, Feasibility, Benefits, Team).   │
│                                                                                  │
│ 2. 📄 **Hlavní přiložený dokument (Main Idea Proposal):**                        │
│    - **Formát:** Formátované **PDF** (Portable Document Format).                 │
│    - **Rozsah:** **Striktně maximálně 10 stran A4** (včetně schémat a tabulek). │
│    - **Jazyk:** Výhradně **Angličtina (English)**.                               │
│    - **Struktura:** Hlavička s emblémem R-DAS, Executive Box, schémata, rozpočty.│
│                                                                                  │
│ 3. 📎 **Doprovodné technické přílohy (Optional Technical Attachments):**         │
│    - Zdrojový prototyp v C (`hera_app.c` / `hera_app.h`),                       │
│    - Protokol ze statické analýzy MISRA-C (Zero Warnings),                       │
│    - Výstupy z testovacího běhu v emulátoru QEMU LEON3.                          │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🗂️ 2. Přehled 6 odevzdávaných PDF dokumentů (Sada R-DAS)

Do systému OSIP vložíme 6 samostatných přihlášek s těmito názvy souborů:

| Kód a kategorie | Název odevzdávaného PDF souboru | Rozsah | Jazyk |
| :--- | :--- | :--- | :--- |
| **Kat. 1 (Auton.)** | `ESA-OSIP-HERA-2026-RDAS-NAV-AURA-GNC.pdf` | max. 10 stran | Angličtina |
| **Kat. 2 (Data)** | `ESA-OSIP-HERA-2026-RDAS-COMP-DEEP-WAVE.pdf` | max. 10 stran | Angličtina |
| **Kat. 3 (Ops)** | `ESA-OSIP-HERA-2026-RDAS-OPS-ARES-PLANNER.pdf` | max. 10 stran | Angličtina |
| **Kat. 4 (Edge AI)** | `ESA-OSIP-HERA-2026-RDAS-EDGE-ARGOS-AI.pdf` *(VLAJKA)* | max. 10 stran | Angličtina |
| **Kat. 5 (Resil.)** | `ESA-OSIP-HERA-2026-RDAS-FDIR-AEGIS-FDIR.pdf` | max. 10 stran | Angličtina |
| **Kat. 6 (Open)** | `ESA-OSIP-HERA-2026-RDAS-ASTRO-CHRONOS.pdf` | max. 10 stran | Angličtina |

---

## 🛠️ 3. FÁZE 2: Co se odevzdává po výběru (do 31. května 2027)

Vítězné experimenty odevzdávají do 31. května 2027 kompletní **letový balík (Experiment Implementation Package)**:

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│              LETOVÝ IMPLEMENTAČNÍ BALÍK PRO FÁZI 2 (DO 31. 5. 2027)              │
├──────────────────────────────────────────────────────────────────────────────────┤
│ 1. 💻 **Full Source Code & Makefile:**                                           │
│    - 100% MISRA-C kompatibilní zdrojové kódy kompilovatelné přes BCC LEON3.      │
│                                                                                  │
│ 2. 📘 **DDF (Design Definition File):**                                          │
│    - PDF (20–40 stran): Kompletní architektonická specifikace a matematický popis│
│                                                                                  │
│ 3. 📗 **SUM (Software User Manual):**                                            │
│    - PDF (15–25 stran): Operační příručka pro operátory ESOC v Darmstadtu.      │
│                                                                                  │
│ 4. 📙 **ICD (Interface Control Document):**                                      │
│    - PDF (10–20 stran): Bytová struktura PUS paketů a telekomandů.               │
│                                                                                  │
│ 5. 📕 **V&V Test Plan & Test Report:**                                           │
│    - PDF (20–30 stran): Protokoly z automatizovaných testů v QEMU simulátoru.    │
│                                                                                  │
│ 6. 🖥️ **R-DAS Ground Segment Decoder:**                                         │
│    - Python balíček s webovým dashboardem pro okamžité dekódování telemetrie.    │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🎯 4. Formátovací a vizuální standard pro Fázi 1 (Design PDF):

Každý z našich 6 dokumentů pro Fázi 1 bude vysázen podle nejvyšších evropských standardů:
- **Písmo:** Formální profesionální typografie (Georgia / Helvetica / Arial),
- **Hlavička:** Logo radixal s.r.o. a oficiální **Mission Patch R-DAS**,
- **Grafika:** Vektorová schémata architektury, toky dat a stavové diagramy,
- **Zvýraznění:** Callout boxy s klíčovými inženýrskými čísly (CPU %, RAM, Bandwidth).
