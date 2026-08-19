# 🤝 19. Registrace na OSIP, esa-star a strategie navázání kontaktů přes dotazy

Tento dokument detailně popisuje **administrativní proces registrace**, ověřování totožnosti a především **taktickou strategii, jak se předem obrátit na hodnotitele s odbornými dotazy**, zanechat perfektní první dojem a vybudovat si u nich jméno ještě před uzávěrkou 15. září 2026.

---

## 💻 1. Jak funguje registrace a ověření totožnosti (OSIP vs. esa-star)

V ekosystému ESA existují dvě úrovně registrace:

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                   DVOJÚROVŇOVÝ SYSTÉM REGISTRACE V ESA                           │
├────────────────────────────────────────┬─────────────────────────────────────────┤
│ ÚROVEŇ 1: FÁZE 1 (Do 15. září 2026)    │ ÚROVEŇ 2: FÁZE 2 (Po výběru v říjnu)    │
├────────────────────────────────────────┼─────────────────────────────────────────┤
│ 🌐 **Portál ESA OSIP (ideas.esa.int)** │ 🏢 **Portál dodavatelů (esa-star)**     │
│ ➔ Blesková registrace zdarma online    │ ➔ Oficiální registr dodavatelů ESA      │
│ ➔ Pouze pracovní e-mail a jméno firmy  │ ➔ Vyplnění IČO, DIČ, banky a statutárů │
│ ➔ ŽÁDNÁ složitá byrokracie ani poplatky│ ➔ Přidělení „ESA Entity Code“ pro smlouvu│
│ ➔ Účet je aktivní během 2 minut.       │ ➔ Potřeba až pro podpis inovační smlouvy│
└────────────────────────────────────────┴─────────────────────────────────────────┘
```

### Postup pro Fázi 1 (Teď):
1. Přejdeme na **[ideas.esa.int](https://ideas.esa.int)**,
2. Klikneme na *Register*, zadáme jméno (**Bc. Viktor Lošťák**), organizaci (**radixal s.r.o.**) a e-mail (`viktor.lostak@radixal.net`),
3. Potvrdíme aktivační odkaz v e-mailu a máme plný přístup pro nahrávání všech 6 návrhů.

---

## 🎯 2. Jak si předem udělat známé a oslovit hodnotitele přes odborné dotazy

V ESA je **zasílání technických dotazů (Clarification Requests) naprosto běžnou a vysoce ceněnou praxí**. Nejde o „otravování“, ale o **důkaz seriózního inženýrského zájmu**.

Máme 3 synergické kanály, jak se zapsat do povědomí klíčových lidí:

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                   TŘI STRATEGICKÉ KANÁLY PRO NAVÁZÁNÍ KONTAKTŮ                   │
├──────────────────────────────────────────────────────────────────────────────────┤
│ 1. 📬 **Oficiální technický dotaz na kampaň Hera OSIP (Campaign Managers):**     │
│    - Cílený dotaz na chování Core 1 v simulátoru ESTECu.                         │
│                                                                                  │
│ 2. 🔬 **Odborné oslovení Jorgeho Lópeze Trescastra (ESTEC TEC-SW):**             │
│    - Technický dotaz navazující na jeho výzkum HERA-IoD a měření WCET na LEON3.  │
│                                                                                  │
│ 3. 🇨🇿 **Informování České kosmické delegace (Ministerstvo dopravy ČR):**        │
│    - Představení projektu českému delegátovi v Radě ESA (Václav Kobera).         │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

## ✉️ 3. Konkrétní návrh textace dotazu pro Jorgeho a tým ESTECu

Položíme dotaz, který okamžitě ukáže, že jsme **jediní, kdo reálně do hloubky studuje simulační vrstvu v C a rozumí procesoru LEON3**:

### Návrh technického dotazu (Odeslat přes kontaktní formulář OSIP / e-mail kampaně):

> **Subject:** Technical Clarification on GR712RC Core 1 Register Windows and Memory Boundary Enforcement for Hera ESW
>
> **Dear Hera Campaign Technical Team / Flight Software Section,**
>
> In preparation for our submission under the *Call for Ideas: Autonomous Software Experiments on Hera*, our engineering team at **radixal s.r.o.** has been setting up the emulation workflow using the provided simulation layer (`hera_client_stub.c`) alongside QEMU for the LEON3 architecture.
>
> We would like to clarify two specific operational boundaries to ensure our deterministic bare-metal architecture matches the flight harness exactly:
>
> 1. **Worst-Case Execution Time (WCET) & Register Windows:** For deterministic algorithms executed on Core 1 without dynamic allocation, does the onboard watchdog on Core 0 monitor execution continuously via heartbeats, or is the timeout enforced strictly at the expiration of the 2–3 hour session window?
> 2. **PUS Science Telemetry Fragmentation:** When calling `Hera_Science_Report` with payloads approaching the 2048-byte limit, does the Core 0 RTEMS telemetry broker handle CCSDS source packet fragmentation automatically, or is packetization within a single application process identifier (APID) strictly managed per single call?
>
> Thank you very much for providing such a clear technical baseline and interface documentation.
>
> Best regards,  
> **Bc. Viktor Lošťák**  
> Lead Architect & Co-Founder, radixal s.r.o.  
> *Purkyňova 649/127, 612 00 Brno, Czech Republic*

---

## 🇨🇿 4. Zapojení České kosmické kanceláře (Ministerstvo dopravy ČR)

Paralelně pošleme krátký informační e-mail na **Odbor kosmických aktivit Ministerstva dopravy ČR** (Václav Kobera / Michal Reinöhl):

> *„Vážený pane řediteli / vážený pane inženýre,*  
> *dovolujeme si vás informovat, že společnost **radixal s.r.o.** připravuje ucelenou sadu 6 návrhů do mezinárodní výzvy ESA OSIP: Autonomous Software Experiments on Hera (R-DAS suite pro autonomní AI kód na sondě Hera).*  
> *Rádi bychom vám v případě zájmu zaslali stručné shrnutí našich konceptů a budeme rádi za podporu české účasti při nadcházejícím hodnocení.“*

---

## 🏆 Co tím získáme:

1. **V ESTECu (Jorge):** Budou vědět, že v Brně sedí inženýři, kteří reálně ladí kód na procesorové úrovni. Když v říjnu uvidí náš proposal, řeknou si: *„Aha, to je ten Lošťák z radixalu, co se ptal na ty SPARC register windows a PUS fragmentaci – ti to mají zmáknuté!“*
2. **V České delegaci:** Český zástupce v ESA bude vědět, že v soutěži máme silné želízko v ohni, a může náš projekt při jednáních komise aktivně podpořit.
