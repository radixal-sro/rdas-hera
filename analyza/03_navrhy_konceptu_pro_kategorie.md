# 🚀 03. Návrhy konceptů pro jednotlivé soutěžní kategorie (se zaměřením na AI)

Tento dokument představuje rozpracované koncepty pro všech **6 oficiálně vypsaných kategorií ESA**, včetně matematického aparátu, odhadů výpočetních zdrojů a doporučeného hybridního vítězného konceptu.

---

## 1. Přehled 6 oficiálních kategorií ESA

| # | Oficiální kategorie ESA | Navržený koncept experimentu | Hlavní použitá technologie / AI |
| :- | :--- | :--- | :--- |
| **1** | **Onboard Image Processing & Feature Tracking** | **Tiny-ORB & Micro-CNN Crater Tracker** | Kvantizovaná INT8 Micro-CNN + kruhový Hough/FAST detektor |
| **2** | **Autonomous Decision Logic** | **Opportunistic Science & Multi-Instrument Agent** | Rozhodovací strom + detektor rozptylu světla na horizontu |
| **3** | **Advanced GNC (Guidance, Nav & Control)** | **Horizon-PALT Sensor Fusion EKF** | Rozšířený Kalmanův filtr (EKF) s fúzí laseru PALT a těžiště AFC |
| **4** | **Data Compression, Security & Prioritisation** | **AI Saliency-Based Adaptive ROI Compressor** | Sémantická segmentace + Wavelet/RLE s prioritizací balíků |
| **5** | **Inference for Anomaly Detection / Classification**| **TinyML Telemetry Isolation Forest & Regolith Classifier**| Multivarietní detekce anomálií v Data Poolu + texturový klasifikátor |
| **6** | **New Deep-Space Operational Concepts** | **Goal-Oriented Autonomous Mission Executive** | Cílově orientovaný plánovač na bázi stavového automatu |

---

## 2. Detailní rozpracování jednotlivých konceptů

---

### 🟢 Kategorie 1: Onboard Image Processing and Feature Tracking
*Název konceptu:* **Tiny-ORB & Micro-CNN: Palubní autonomní detekce kráterů a optické trasování povrchu**

#### Princip a algoritmus:
1. **Subsampling a detekce:** Snímek 1020×1020 je zmenšen na 256×256 pro rychlou detekci kandidátních oblastí pomocí FAST/Sobel operátoru v pevné řádové čárce.
2. **Micro-CNN klasifikace:** Kolem každého kandidáta je vyříznut patch 32×32 pixelů, který je předán mikro-konvoluční síti (2 konvoluční vrstvy + 1 plně propojená, 8-bitové kvantizované váhy INT8, celkem 38,4 kB). Síť potvrdí přítomnost kráteru nebo balvanu s jistotou > 85 %.
3. **Feature Tracking:** Polohy detekovaných útvarů jsou porovnány se snímkem pořízeným o 60 sekund dříve (Optical Flow v celočíselné aritmetice), čímž je vypočten vektor zdánlivého posunu a rotace.

#### Odhad zdrojů:
- **RAM:** 185 kB (včetně 64KB stacku a mezilehlých bufferů).
- **CPU zátěž:** ~35 % při 50 MHz (cca 350 ms na kompletní analýzu snímku).
- **Telemetrie:** Science Report – matice 20 detekovaných orientačních bodů (cca 240 bytů na snímek).

---

### 🟢 Kategorie 2: Autonomous Decision Logic
*Název konceptu:* **Opportunistic Science Agent: Autonomní detektor výtrysků a multi-spektrální spouštěč**

#### Princip a algoritmus:
1. **Limb Scatter Analysis:** Algoritmus v polárních souřadnicích analyzuje vnější okraj asteroidu (limb) na AFC snímku a měří rozptyl světla na pozadí vesmíru. Hledá lokální anomálie jasu indikující uvolňování prachu nebo impakt mikrometeoritu.
2. **Korelace s Data Poolem:** Z Data Poolu čte sluneční fázový úhel a teploty přístrojů.
3. **Autonomní akce:** Pokud jas na okraji překročí prahovou hodnotu o $3\sigma$, agent **autonomně zavolá `Hera_TIRI_AcquireImage()` nebo `Hera_HS_AcquireImage()`**, aby pořídil termální / hyperspektrální snímek probíhajícího dynamického jevu.

#### Odhad zdrojů:
- **RAM:** 95 kB.
- **CPU zátěž:** ~15 % (běh trvá < 100 ms na snímek).
- **Telemetrie:** PUS Event Report (Service 5) o spuštění akvizice (42 bytů) + Housekeeping souhrn.

---

### 🟢 Kategorie 3: Advanced Guidance, Navigation and Control (GNC)
*Název konceptu:* **Horizon-PALT Sensor Fusion: Palubní fúze laserového výškoměru a optického těžiště**

#### Princip a algoritmus:
1. **Extrakce těžiště:** Rychlý algoritmus momentů plochy vypočte z AFC snímku optické těžiště (Center of Brightness) a zdánlivý průměr Didymosu.
2. **Laserový dálkoměr:** Každé 2 s přečte z Data Poolu přesnou vzdálenost z přístroje PALT (`Hera_Read_Parameter_float64()`).
3. **Rozšířený Kalmanův filtr (EKF):** 9stavový EKF integruje optický směr, laserovou vzdálenost a data ze star trackerů/gyroskopů pro přesný odhad polohy sondy vůči těžišti binárního systému v reálném čase.

#### Odhad zdrojů:
- **RAM:** 60 kB.
- **CPU zátěž:** ~20 % (využívá knihovnu `LibmCS` pro maticové operace).
- **Telemetrie:** Vědecký vektor stavu (poloha, rychlost, kovariance) – 64 bytů každých 30 s.

---

### 🟢 Kategorie 4: Data Compression, Security and Prioritisation
*Název konceptu:* **AI Saliency-Based ROI Compression & Science Value Ranking (Sémantická komprese)**

#### Princip a algoritmus:
1. **Sémantická segmentace:** Snímek 1020×1020 je rozdělen na dlaždice 60×60. Každá dlaždice je ohodnocena indexem významnosti (Saliency Score: kontrast, hustota hran, rozhraní stín/světlo, přítomnost kráteru DART).
2. **Adaptivní komprese:**
   - Černé pozadí vesmíru (score = 0): Komprese nulových řad (úspora > 98 %).
   - Homogenní povrch (score = 1): Integer Wavelet Transform 5/3 (ztrátová komprese 10:1).
   - Vědecké zájmové oblasti (ROI, score = 2): Bezeztrátová prediktivní komprese DPCM + Huffman (bezeztrátový detail).
3. **Prioritní fronta:** Pakety s nejvyšším indexem významnosti jsou odesílány přednostně.

#### Odhad zdrojů:
- **RAM:** 240 kB (line-by-line streaming, žádná velká mezipaměť).
- **CPU zátěž:** ~45 % (cca 800 ms na celý 1MB snímek).
- **Úspora:** **Snížení objemu downlinku o 75–85 %**, science downlink < 2,5 MB na 3hodinové okno.

---

### 🟢 Kategorie 5: Inference for Anomaly Detection or Science Classification
*Název konceptu:* **TinyML Telemetry Isolation Forest & Regolith Texture Classifier**

#### Princip a algoritmus:
1. **Telemetrický Isolation Forest:** Kvantizovaný stromový model běží nad 40 parametry Data Poolu (teploty PCDU, proudy, čítače chyb SpaceWire, tření setrvačníků). Hledá nelineární korelace a odchylky.
2. **Texturový klasifikátor:** Na oříznutých částech povrchu počítá matici GLCM (Gray-Level Co-occurrence Matrix) a klasifikuje povrch na jemný regolit, štěrk a monolitické balvany.

#### Odhad zdrojů:
- **RAM:** 110 kB.
- **CPU zátěž:** ~25 %.
- **Telemetrie:** Event Report při anomálii + statistická mapa distribuce textur.

---

### 🟢 Kategorie 6: New Deep-Space Operational Concepts
*Název konceptu:* **Goal-Oriented Autonomous Mission Executive (Palubní autonomní dispečer)**

#### Princip a algoritmus:
1. **Cílově orientovaný model:** Pozemní středisko pošle pouze obecný cíl (např. *„Zmapuj kráter DART při fázovém úhlu slunce < 25° a zaplnění paměti < 80 %“*).
2. **Autonomní plánovač:** ESW monitoruje orbitální pozici a telemetrii v Data Poolu, samostatně vybere nejvhodnější časové okno a provede sekvenci snímání bez zásahu ze Země.

#### Odhad zdrojů:
- **RAM:** 75 kB.
- **CPU zátěž:** < 10 %.

---

## 🏆 3. Doporučený vítězný koncept (The Sweet Spot)

Pro podání do soutěže je strategicky nejvýhodnější **hybridní koncept spojující Kategorii 4 (Sémantická komprese) a Kategorii 1 (Detekce kráterů / TinyML)**:

- **Pracovní název:** `A-SENSE (Asteroid Saliency-Engine & Neural SEmantic Compression)`
- **Proč právě tento:**
  1. Nabízí **jasný měřitelný přínos pro ESA** (úspora 80 % drahocenného downlinku).
  2. Demonstruje **reálnou palubní AI (TinyML)**, která zaujme vedení mise (Ian Carnelli).
  3. Je **100% realizovatelný na procesoru LEON3** bez překročení paměťových a časových limitů (potěší Jorgeho i ESOC).
