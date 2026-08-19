# 🛰️ ESA Hera Space Probe Code Contest (2026_026)

Tento projekt obsahuje kompletní podklady, technické analýzy, strategii a návrhy experimentálního softwaru pro soutěž Evropské vesmírné agentury (**ESA**) v rámci platformy **OSIP (Open Space Innovation Platform)**: *Call for Ideas: Autonomous Software Experiments on Hera*.

---

## 📌 Rychlý přehled mise a příležitosti

- **Sonda:** ESA Hera (vlajková mise planetární obrany u binárního asteroidu Didymos / Dimorphos).
- **Lokalita běhu kódu:** Hluboký vesmír (cca 150 milionů km od Země).
- **Termín provozu na sondě:** Srpen 2027 (4týdenní kampaň v prodloužené fázi mise).
- **Architektura:** Dvoujádrový procesor **GR712RC (LEON3 SPARC V8)**. Jádro **Core 1** je vyhrazeno jako hardwarově izolovaný "sandbox" pro hostování externího experimentálního softwaru (ESW).
- **Operační systém:** **Core 0** běží na **RTEMS** (Hard Real-Time OS), zatímco **Core 1** je **100% Bare-metal C** (bez OS) pro maximální výkon a bezpečnost.
- **Časové okno běhu:** 2 až 3 hodiny denně (stateless, asynchronní, deterministický C kód).
- **Předkladatel a řídicí triáda (radixal s.r.o.):**
  - **Bc. Viktor Lošťák** – *Lead Architect & Principal Investigator (PI)*
  - **Ing. Petr Slepička** – *Engineering Lead & Delivery Director*
  - **Mgr. David Riedl** – *Executive Director & Operations Governance*
- **Reference a historie:** Safety-critical vestavné systémy (AK Signal / drážní normy SIL), obranné air-gapped technologie (URC Systems), komerční zpracování satelitních snímků v C (Norsko), státní infrastruktura (CENDIS / MD ČR) a energetická telemetrie (E.ON, Schneider Electric).
- **Portfolio R-DAS:** Kompletní sada **6 samostatných anglických návrhů** pokrývajících všech 6 soutěžních kategorií ESA.
- **Financování a IPR:** Vývoj je plně financován přímým inovačním kontraktem ESA (z programu Operations Innovations a české národní obálky Geo-Return), 100 % duševního vlastnictví (IPR) zůstává společnosti radixal s.r.o.

---

## 🗂️ Kompletní portfolio 6 pracovních návrhů (Sada R-DAS)

Ve složce [`navrhy/`](file:///c:/Users/vikto/Disk%20Google/Radixal/Zakázky/2026_026%20Hera%20Space%20Probe%20Code%20Contest/navrhy/) jsou připraveny kompletní 10stránkové návrhy v angličtině:

1. 🚀 **[ARGOS-AI (Kat. 4 – Edge AI / Vlajková loď)](file:///c:/Users/vikto/Disk%20Google/Radixal/Zakázky/2026_026%20Hera%20Space%20Probe%20Code%20Contest/navrhy/ESA-OSIP-HERA-2026-RDAS-EDGE-ARGOS-AI_Working_Draft.md)** – Autonomní detekce kráterů a morfologie po DARTu přes INT8 Micro-CNN a PALT fúzi.
2. 🌊 **[DEEP-WAVE (Kat. 2 – Komprese dat)](file:///c:/Users/vikto/Disk%20Google/Radixal/Zakázky/2026_026%20Hera%20Space%20Probe%20Code%20Contest/navrhy/ESA-OSIP-HERA-2026-RDAS-COMP-DEEP-WAVE_Working_Draft.md)** – Deterministická vlnková komprese (CDF 5/3) šetřící 82 % downlinkového pásma.
3. 🧭 **[AURA-GNC (Kat. 1 – Autonomie a navigace)](file:///c:/Users/vikto/Disk%20Google/Radixal/Zakázky/2026_026%20Hera%20Space%20Probe%20Code%20Contest/navrhy/ESA-OSIP-HERA-2026-RDAS-NAV-AURA-GNC_Working_Draft.md)** – Optická relativní navigace, sledování orientačních bodů (Tiny-ORB) a 9stavový EKF.
4. 🛡️ **[AEGIS-FDIR (Kat. 5 – Odolnost a FDIR)](file:///c:/Users/vikto/Disk%20Google/Radixal/Zakázky/2026_026%20Hera%20Space%20Probe%20Code%20Contest/navrhy/ESA-OSIP-HERA-2026-RDAS-FDIR-AEGIS-FDIR_Working_Draft.md)** – Telemetrický Isolation Forest (in-flight realizace výzkumu Jorgeho Lópeze z ESTECu).
5. ⏱️ **[ARES-Planner (Kat. 3 – Operační optimalizace)](file:///c:/Users/vikto/Disk%20Google/Radixal/Zakázky/2026_026%20Hera%20Space%20Probe%20Code%20Contest/navrhy/ESA-OSIP-HERA-2026-RDAS-OPS-ARES-PLANNER_Working_Draft.md)** – Autonomní řešič CSP pro plánování pozorování a optimalizaci energetického rozpočtu.
6. 🔭 **[CHRONOS-Photometry (Kat. 6 – Otevřená věda)](file:///c:/Users/vikto/Disk%20Google/Radixal/Zakázky/2026_026%20Hera%20Space%20Probe%20Code%20Contest/navrhy/ESA-OSIP-HERA-2026-RDAS-ASTRO-CHRONOS_Working_Draft.md)** – Palubní aperturová fotometrie a měření periody Dimorphosu navazující na výzkum v Ondřejově.

---

## 📁 Struktura složek v projektu

```
2026_026 Hera Space Probe Code Contest/
├── README.md                                      # Tento hlavní rozcestník
├── .gitignore                                     # Ignorování velkých archivů a binárek
│
├── 📁 navrhy/                                     # 6 kompletních anglických návrhů pro OSIP
│   ├── ESA-OSIP-HERA-2026-RDAS-EDGE-ARGOS-AI_Working_Draft.md
│   ├── ESA-OSIP-HERA-2026-RDAS-COMP-DEEP-WAVE_Working_Draft.md
│   ├── ESA-OSIP-HERA-2026-RDAS-NAV-AURA-GNC_Working_Draft.md
│   ├── ESA-OSIP-HERA-2026-RDAS-FDIR-AEGIS-FDIR_Working_Draft.md
│   ├── ESA-OSIP-HERA-2026-RDAS-OPS-ARES-PLANNER_Working_Draft.md
│   └── ESA-OSIP-HERA-2026-RDAS-ASTRO-CHRONOS_Working_Draft.md
│
├── 📁 media/                                      # Grafické podklady a vizuální identita
│   └── rdas_mission_patch.jpg                     # Oficiální mezinárodní emblém mise R-DAS
│
├── 📁 analyza/                                    # Kompletní 21kapitolová strategická knihovna
│   ├── 01_technicke_mantinely_a_architektura.md až 21_master_harmonogram_kroku_a_roadmapa_do_letu.md
│
└── 📁 podklady/                                   # Oficiální zadávací materiály ESA a simulátor v C
```

---

## 📅 Časová osa soutěže (Závazná data z OSIP)

| Fáze | Termín | Popis a výstupy |
| :--- | :--- | :--- |
| **Phase 1: Submission Deadline** | **15. září 2026** | Podání všech 6 návrhů (Ideas, max. 10 stran v angličtině) přes OSIP formulář. |
| **Discussion Phase** | **od 15. září 2026** | Expertní a komunitní diskuze nápadů na platformě OSIP. |
| **Evaluation Phase (Výběr vítězů)** | **od 15. října 2026** | Vyhodnocení komisí ESA a vyhlášení vybraných experimentů. |
| **Phase 2: Implementation Delivery** | **do 31. května 2027** | Dodání kompletního C kódu, DDF, SUM, ICD a V&V testovacího reportu. |
| **In-Flight Execution Campaign** | **Srpen 2027 (4 týdny)** | Nahrání na sondu a reálné spuštění v hlubokém vesmíru u asteroidu Didymos. |
