# 🗓️ 21. Master harmonogram: Od přípravy přes podání až po letový provoz v hlubokém vesmíru

Tento dokument představuje **kompletní časovou a exekuční mapu projektu**. Obsahuje podrobný rozpis kroků od dnešního dne (srpen 2026) přes uzávěrku podání (15. září 2026), smluvní vyjednávání a inženýrský vývoj až po samotný letový provoz na sondě Hera u asteroidu Didymos v srpnu 2027 a následnou vědeckou sklizeň.

---

## 🧭 1. Celkový přehled pěti fází projektu

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                   ČASOVÁ OSA PROJEKTU RADIXAL R-DAS / ESA HERA                   │
├──────────────────────────────────────────────────────────────────────────────────┤
│ 🟢 **FÁZE I: Příprava a kompletace 6 proposals**       (19. 8. – 5. 9. 2026)     │
│ 🟢 **FÁZE II: Interní revize a podání na OSIP**        (5. 9. – 14. 9. 2026)     │
│ 🟡 **FÁZE III: Discussion Phase a výběr vítězů**       (15. 9. – 15. 10. 2026)   │
│ 🔵 **FÁZE IV: Kontrakt ESA, vývoj C a letový balík**   (Listopad 2026 – Květen 27│
│ 🔴 **FÁZE V: In-Flight letová kampaň u asteroidu**     (Srpen 2027)              │
│ 🟣 **FÁZE VI: Vědecké publikace a transfer pro Ramses**(Podzim 2027 – 2028)      │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

## 📅 2. Detailní rozpis kroků do uzávěrky podání (19. 8. – 15. 9. 2026)

### 🔹 Týden 1: Dokončení textů a simulace v QEMU (19. – 26. srpna 2026)
- **Krok 1 (Dokončení proposals):** Dopracovat zbývajících 5 anglických návrhů podle vzoru vlajkového *ARGOS-AI* (DEEP-WAVE, AURA-GNC, AEGIS-FDIR, ARES-Planner, CHRONOS).
- **Krok 2 (QEMU ověření):** Zkompilovat C prototypy přes `sparc-gaisler-elf-gcc` a provést testovací běh nad 2 400+ AFC snímky v emulátoru QEMU LEON3.
- **Krok 3 (Registrace OSIP):** Zaregistrovat oficiální profil na portálu **[ideas.esa.int](https://ideas.esa.int)** pro **Bc. Viktora Lošťáka** (`viktor.lostak@radixal.net`) za společnost **radixal s.r.o.**

### 🔹 Týden 2: Technická diplomacie a sazba dokumentů (27. srpna – 4. září 2026)
- **Krok 4 (Odborný dotaz na ESTEC):** Odeslat promyšlený technický dotaz (Clarification Request) týmu Jorgeho Lópeze Trescastra ohledně fragmentace PUS paketů a WCET na Core 1.
- **Krok 5 (Briefing Ministerstva dopravy ČR):** Odeslat diskrétní informační dopis řediteli Odboru kosmických aktivit Ing. Václavu Koberovi o naší účasti v soutěži.
- **Krok 6 (Sazba PDF):** Převést všech 6 návrhů do finálních reprezentativních PDF (max. 10 stran A4) s Mission Patchem, schématy a tabulkami rozpočtů.

### 🔹 Týden 3: Finální review a nahrání přihlášek (5. – 14. září 2026)
- **Krok 7 (Vedení review):** Společné schválení řídicí triádou (**Lošťák, Slepička, Riedl**).
- **Krok 8 (Podání na OSIP s předstihem):** Ve dnech **11.–14. září 2026** (s bezpečnou rezervou před přetížením serverů) nahrát všech 6 přihlášek na portál OSIP.
- **15. září 2026:** **OFICIÁLNÍ DEADLINE OSIP (Uzávěrka Fáze 1).**

---

## 📢 3. Co se děje po podání: Od diskuze k výběru (Září – Říjen 2026)

### 🔹 16. září – 14. října 2026: Discussion Phase na OSIP & Odborná publicita
- **Aktivita na OSIP:** Aktivně odpovídat na dotazy hodnotitelů a komunity pod našimi nápady.
- **Odborný článek pro Kosmonautix.cz:** Vydání článku představujícího českou sadu experimentů R-DAS (čímž vytvoříme silný komunitní buzz).
- **Podpora české delegace:** Český zástupce v ESA (MD ČR) vstupuje do jednání s vědomím, že radixal s.r.o. má špičkový, veřejně podpořený projekt.

### 🔹 15. října 2026: Vyhlášení vítězů ESA
- Zasedání hodnoticí komise ESA v ESTECu a oficiální výběr vítězných experimentů pro sondu Hera.

---

## 🛠️ 4. Fáze 2: Kontrakt, inženýrský vývoj a dodání (Listopad 2026 – Květen 2027)

```
┌───────────────────────────┬───────────────────┬──────────────────────────────────────────────────┐
│ Období                    │ Milník / Událost  │ Popis a dodávky                                  │
├───────────────────────────┼───────────────────┼──────────────────────────────────────────────────┤
│ **Listopad 2026**         │ esa-star & Smlouva│ Registrace v esa-star, podpis inovačního         │
│                           │                   │ kontraktu s ESA, vyplacení zálohy (Advance).     │
│ **Listopad 2026**         │ Czech Space Week  │ Oficiální prezentace vítězného projektu na       │
│                           │                   │ národním festivalu kosmických aktivit v ČR.      │
│ **Prosinec 26 – Únor 27** │ PDR & CDR         │ Dopracování C kódu, statická analýza Frama-C,    │
│                           │                   │ dodání DDF (Design Definition File) a ICD.       │
│ **Březen – Duben 2027**   │ V&V Qualification │ Automatizované testy v QEMU, V&V Test Report,    │
│                           │                   │ dokončení R-DAS Ground Segment Decoderu.         │
│ **15.–31. května 2027**   │ Final Delivery    │ **Finální odevzdání letového balíku do ESA**     │
│                           │                   │ (Zdrojový C kód, DDF, SUM, ICD, V&V report).     │
└───────────────────────────┴───────────────────┴──────────────────────────────────────────────────┘
```

---

## 🛰️ 5. Letová kampaň v hlubokém vesmíru a následná sklizeň (Srpen 2027+)

1. **Červenec 2027 (Příprava uplinku):** Operátoři v ESOCu (Darmstadt) provádějí validaci binárního souboru na pozemním testbedu sondy.
2. **Srpen 2027 (In-Flight Execution):**
   - Binární kód je uplinkován na vzdálenost 150 milionů km přes síť Estrack.
   - Po dobu **4 týdnů běží náš software 2–3 hodiny denně** přímo na palubě sondy Hera u asteroidu Didymos.
   - PUS Science pakety jsou stahovány na Zemi a v reálném čase dekódovány naším **R-DAS Ground Segment Decoderem**.
3. **Podzim 2027 – 2028 (Vědecká a komerční sklizeň):**
   - Tisková konference ESA s prvními autonomně detekovanými snímky kráterů po dopadu DARTu.
   - Společná publikace vědeckého a inženýrského článku s Jorge Lópezem Trescastrem na konferencích **DASIA 2028** a **EDHPC 2028**.
   - **Technologický transfer:** Certifikovaný C kód je přímo integrován do letového softwaru připravované evropské mise **ESA Ramses (Apophis 2029)**.
   - Komerční licencování algoritmů pro družice dálkového průzkumu Země a pozemské průmyslové IoT.
