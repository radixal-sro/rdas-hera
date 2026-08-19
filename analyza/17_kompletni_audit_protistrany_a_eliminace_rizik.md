# 🎯 17. Kompletní audit protistrany: Co přesně chtějí, kdo může „hodit vidle“ a jak je získat

Tento dokument provádí **nemilosrdně upřímný 360stupňový audit všech klíčových aktérů v ESA**, kteří budou sedět v hodnoticí komisi nebo mají právo veta. Analyzuje jejich skutečné (neveřejné) zájmy, skryté obavy a definuje, jak jsme v našem návrhu ošetřili každou jednotlivou překážku.

---

## 👥 1. Mapa rozhodovacího stolu ESA (Kdo rozhoduje a co skutečně chtějí)

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                   ROZHODOVACÍ STŮL ESA PRO VÝBĚR EXPERIMENTŮ HERA                │
├──────────────────────────────────────────────────────────────────────────────────┤
│ 1. 🛡️ **ESOC Letové řízení (Darmstadt) – „Strážce bezpečnosti a nulového rizika“**│
│ 2. 🔬 **ESTEC Flight Software (Noordwijk) – Jorge López Trescastro – „Technik a ego“**│
│ 3. 🚀 **Vedení mise a Planetární obrana – Ian Carnelli – „PR sláva a mise Ramses“** │
│ 4. 🔭 **Vědecký tým mise – Patrick Michel & Michael Kueppers – „Vědecká data“**  │
│ 5. 🏢 **Průmyslový Prime dodavatel sondy – OHB / Spacebel – „Potenciální veto“**  │
│ 6. 💳 **Finanční a smluvní sekce ESA – „Geo-Return a bezproblémové papíry“**      │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔍 2. Detailní rentgen jednotlivých aktérů:

### 1. ESOC Letové řízení v Darmstadtu (Spacecraft Operations Manager)
- **Co chtějí:** **Absolutní klid a nulovou zátěž.** Nechtějí ve 3 ráno řešit, že cizí kód shodil sondu do Safe Mode, ani psát složité dekódovací skripty pro novou telemetrii.
- **Jejich noční můra:** Program uvízne v nekonečné smyčce, sežere baterie nebo zahltí komunikační okno.
- **Jak jsme to vyřešili v našem návrhu:**
  - Plně **bezstavový (stateless) běh** v pevném 2–3h okně. Pokud dojde k přerušení, kód okamžitě a čistě skončí.
  - Žádný přímý přístup k hardwarovým registrům (izolace přes MMU na Core 1).
  - **DODÁVKA POZEMNÍHO DEKODÉRU:** Zdarma dodáme Python/Web dashboard, který jejich operátorům okamžitě dekóduje telemetrii bez jakékoliv práce navíc.

### 2. Jorge López Trescastro a ESTEC Flight Software Systems (Noordwijk)
- **Co chce:** **Uznání, citace a letové ověření jeho vlastního výzkumu.** Jorge léta publikuje o projektu *HERA-IoD* (TinyML pro detekci anomálií na LEON3). Chce vidět firmu, která jeho práci dotáhne k reálnému letu a napíše s ním prestižní vědecký článek pro konferenci EDHPC/DASIA 2028.
- **Jeho noční můra:** Amatérský kód s `malloc`, dynamickou pamětí a chybějící statickou analýzou, který porušuje standardy ECSS.
- **Jak jsme to vyřešili v našem návrhu:**
  - Přímá citace jeho práce z ADCSS 2023 u konceptu *AEGIS-FDIR* a *ARGOS-AI*.
  - Striktní **MISRA-C:2012 Zero-Heap architektura** s `TensorArenou` a formální verifikací přes **Frama-C**.
  - Formální pozvání jeho týmu do **Advisory Boardu** pro společné publikování výsledků.

### 3. Ian Carnelli a vedení Planetární obrany ESA
- **Co chce:** **PR triumf, publicitu v médiích a technologický most pro misi RAMSES (Apophis 2029).** Ian potřebuje v roce 2027 ukázat generálnímu řediteli a ministrům: *„Hera dokázala jako první v historii autonomně analyzovat asteroid pomocí AI. Naše technologie fungují a mise Ramses k Apophisu je připravena!“*
- **Jeho noční můra:** Nudný, neviditelný experiment, který v médiích nikoho nezajímá.
- **Jak jsme to vyřešili v našem návrhu:**
  - Vlajkový koncept **ARGOS-AI** (autonomní detekce kráterů po dopadu DART) a **CHRONOS-Photometry** (světelné křivky Didymosu).
  - Přímé zarámování jako **TRL 8 In-Flight Demonstrator pro misi Ramses (2029)**.

### 4. Vědecký tým mise (Patrick Michel / Observatoire de la Côte d'Azur & Ondřejov)
- **Co chtějí:** **Nová vědecká data navíc**, aniž by jim experiment sebral přenosové pásmo pro hlavní přístroje (TIRI, HyperScout).
- **Jak jsme to vyřešili v našem návrhu:**
  - Naše vlnková a sémantická komprese **DEEP-WAVE** ušetří 80 % pásma, takže jim zbude více kapacity pro vědecká data.
  - Vědecké napojení na fotometrické modely Dr. Petra Pravce z Ondřejova.

---

## 🚫 3. Kdo by mohl „hodit vidle“ a jak jsme to ošetřili?

| Potenciální překážka / Aktér | Důvod proč by mohl protestovat | Jak jsme to v návrhu eliminovali |
| :--- | :--- | :--- |
| **OHB Bremen / Spacebel (Prime dodavatelé FSW)** | Obava, že cizí software zasahuje do jejich letového jádra Core 0. | Explicitně deklarujeme, že R-DAS běží **výhradně na Core 1 sandboxu**, plně respektuje jejich rozhraní `hera_interface.h` a nesahá na Core 0. |
| **Finanční a právní oddělení ESA** | Obavy z nejasného IPR, drahého rozpočtu nebo neznámé firmy. | 10 let prověřená historie radixal s.r.o. (kapitál 900k Kč), akceptace standardního pevného rozpočtu EISI a financování přes český Geo-Return. |
| **Zastánci tradičních západních velkých firem** | Tlak, aby zakázku dostal francouzský nebo německý dodavatel. | Podpora generálního ředitele Josefa Aschbachera pro SME diverzitu + ucelený příběh české účasti (OHB Czechspace struktura + Ondřejov věda + radixal software). |

---

## 📜 4. Ideologie a oficiální „Wording“ ESA (Náš slovník)

Návrhy jsou protkány přesnou terminologií a ideologií, kterou hodnotitelé ESA milují:

- **„European Digital Sovereignty & Non-Dependence“** *(Evropská digitální suverenita a nezávislost na proprietárním software)*
- **„Deterministic Zero-Heap Embedded AI“** *(Deterministická umělá inteligence bez dynamické paměti)*
- **„In-Orbit Demonstration (IOD) at TRL 8“** *(Letová demonstrace technologické zralosti)*
- **„Faster, Cheaper, Better through Open Standards“** *(Rychlejší a levnější vývoj díky otevřeným standardům)*
- **„Technology De-risking for ESA Ramses (Apophis 2029)“** *(Snížení rizik pro misi Ramses)*
- **„ECSS-E-ST-40C Category D Compliance“** *(Přísný soulad s evropskými kosmickými standardy)*

---

## 🏆 Závěr auditu:

V návrhu **nikdo nechybí, nikdo není opomenut a každá zájmová skupina dostává přesně to, po čem touží**:
1. **ESOC:** Nulové riziko, žádnou práci navíc a hotový pozemní dekodér.
2. **ESTEC (Jorge):** Citace, respekt k jeho výzkumu HERA-IoD a společný vědecký článek.
3. **Vedení (Ian Carnelli):** Skvělé PR, fotky kráterů pro tisk a technologie pro misi Ramses.
4. **Vědci (Ondřejov/Patrick Michel):** Bonusová fotometrická a obrazová data.
5. **Vedení ESA (Aschbacher):** Úspěšný příběh středoevropského SME inovátora financovaný z české obálky.
