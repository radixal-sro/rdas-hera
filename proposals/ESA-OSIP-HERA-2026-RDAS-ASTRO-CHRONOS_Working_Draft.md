# EUROPEAN SPACE AGENCY – OPEN SPACE INNOVATION PLATFORM (OSIP)
## Call for Ideas: Autonomous Software Experiments on Hera
### IDEA PROPOSAL & TECHNICAL WORKING DRAFT

---

```
====================================================================================================
PROPOSAL IDENTIFIER:  ESA-OSIP-HERA-2026-RDAS-ASTRO-CHRONOS
PROPOSAL TITLE:       CHRONOS-Photometry: Onboard Real-Time Asteroid Lightcurve Extraction & 
                      Mutual Orbit Perturbation Tracker on Hera LEON3 Bare-Metal Core
PRIMARY TRACK:        Category 6 – Open Innovation & Planetary Science
COMPLEMENTARY TRACKS: Category 2 (Science Data Processing) & Category 4 (Edge AI & Computing)
PROPOSING ENTITY:     radixal s.r.o. (Purkyňova 649/127, 612 00 Brno, Czech Republic / Pan-European)

KEY LEADERSHIP TRIAD:
• Principal Investigator (PI) & Lead Architect:  Bc. Viktor Lošťák (radixal s.r.o.)
• Engineering Lead & Software Delivery Director: Ing. Petr Slepička (radixal s.r.o.)
• Executive Director & Project Governance:       Mgr. David Riedl (radixal s.r.o.)

TARGET ARCHITECTURE:  GR712RC Dual-Core LEON3 (SPARC V8 @ 50 MHz), Core 1 Bare-Metal Sandbox
MISSION STAGE:        Hera Extended Mission In-Flight Experiment (Didymos / Dimorphos, August 2027)
SOFTWARE STANDARD:    ECSS-E-ST-40C Category D | MISRA-C:2012 Zero-Heap Deterministic Runtime
====================================================================================================
```

---

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                EXECUTIVE SUMMARY & KEY METRICS                                   │
├──────────────────────────────────────────────────────────────────────────────────────────────────┤
│ CHRONOS-Photometry is an onboard astronomical science and aperture photometry engine designed to │
│ run on the bare-metal Core 1 of the GR712RC processor on board Hera. It extracts high-precision │
│ integrated photometric lightcurves and mutual eclipse/occultation timings of Dimorphos and       │
│ Didymos directly from Asteroid Framing Camera (AFC) images in real time.                        │
│                                                                                                  │
│ Building upon foundational research by the Astronomical Institute of the Czech Academy of       │
│ Sciences (Ondřejov Observatory), CHRONOS measures Dimorphos's post-impact orbital period and    │
│ tumbling spin state to +/- 1.5 seconds accuracy while transmitting under 15 kB of telemetry      │
│ (a 99.8% bandwidth reduction compared to raw imagery).                                          │
│                                                                                                  │
│ 📊 KEY IN-FLIGHT BUDGETS & METRICS:                                                              │
│ • CPU Utilization:          3.6% @ 50 MHz SPARC V8 (Peak WCET: 0.85 s per 1020×1020 AFC frame)  │
│ • RAM Footprint:            28.6 kB static memory (Zero malloc / Zero heap fragmentation)        │
│ • Stack Memory:             < 10.0 kB (Within the hard 64.0 kB stack limit at 0x40010000)        │
│ • Period Timing Accuracy:   +/- 1.5 seconds for mutual eclipse / occultation events              │
│ • Downlink Volume:          < 15.0 kB total telemetry per 3-hour session (Down from 12.0 MB)     │
│ • Telemetry Reduction:      99.8% reduction compared to raw uncompressed optical frames          │
│ • Mathematical Core:        100% Fixed-Point Aperture Photometry & Discrete Fourier Inversion   │
│ • Scientific Legacy:        Direct synergy with Czech Ondřejov Didymos Photometric Survey        │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 1. The Problem Statement & Planetary Science Objectives

Following NASA's DART kinetic impact on September 26, 2022, Dimorphos's orbital period around Didymos was shortened by approximately 33 minutes (from 11 hours 55 minutes to ~11 hours 22 minutes). Key scientific questions remain:

1. **Non-Principal Axis Rotation (Tumbling):** Models suggest the kinetic impact induced complex non-principal axis rotation (chaotic tumbling and libration) in Dimorphos. Confirming this requires dense, continuous photometric sampling across complete orbital revolutions.
2. **Limitations of Terrestrial Observations:** Earth-based optical telescopes are restricted by diurnal day-night cycles, atmospheric seeing, weather disruptions, and poor viewing phase angles ($g$-phase geometry).
3. **Downlink Bandwidth Impossibility:** Downloading continuous sequences of 1020×1020 raw images to reconstruct high-cadence lightcurves on Earth would require gigabytes of downlink bandwidth—far exceeding Hera's 12 MB session limit.

---

## 2. The CHRONOS-Photometry Algorithmic Architecture

CHRONOS-Photometry solves this by performing **aperture photometry and harmonic curve inversion directly on board**:

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               CHRONOS-PHOTOMETRY PIPELINE ARCHITECTURE                           │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘

 [ AFC Camera Buffer ] 1020×1020 Grayscale Image (hera_interface.h)
       │
       ▼
 ┌────────────────────────────────────────────────────────────────────────────────────────────────┐
 │ STAGE 1: Dynamic Centroiding & Adaptive Synthetic Aperture Ring Masking                        │
 │ • Computes center-of-light for Didymos primary and Dimorphos secondary                        │
 │ • Integrates flux within adaptive circular apertures (inner target, outer sky background ring) │
 │ • Calibrates instrumental flux against fixed background star catalog entries                   │
 └────────────────────────────────────────────────────────────────────────────────────────────────┘
       │
       ▼
 ┌────────────────────────────────────────────────────────────────────────────────────────────────┐
 │ STAGE 2: Fixed-Point Photometric Normalization & Outlier Rejection                             │
 │ • Subtracts dark current and local zodiacal/space background noise using integer math           │
 │ • Normalizes relative magnitude to standard phase-angle curve ($H-G$ magnitude model)           │
 └────────────────────────────────────────────────────────────────────────────────────────────────┘
       │
       ▼
 ┌────────────────────────────────────────────────────────────────────────────────────────────────┐
 │ STAGE 3: Mutual Eclipse & Occultation Event Detection (Harmonic Inversion)                     │
 │ • Tracks lightcurve minimums corresponding to mutual occultation and shadow ingress/egress     │
 │ • Fits fixed-point Fourier harmonic series to extract instantaneous orbital period $P_{orb}$   │
 └────────────────────────────────────────────────────────────────────────────────────────────────┘
       │
       ▼
 ┌────────────────────────────────────────────────────────────────────────────────────────────────┐
 │ STAGE 4: Ultra-Compact PUS Science Telemetry Serialization                                     │
 │ • Packages extracted time-stamped flux datapoints into compact PUS Science Packets (APID 0x485)│
 │ • Total packet size per frame: exactly 16 bytes (Timestamp, Normalized Flux, Error, Event Flag)│
 └────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Technical Feasibility & Embedded Realism on GR712RC (LEON3)

```
┌──────────────────────────────────────┬─────────────────────────────┬─────────────────────────────┐
│ Parameter                            │ Hera Platform Constraint    │ CHRONOS Implementation      │
├──────────────────────────────────────┼─────────────────────────────┼─────────────────────────────┤
│ Target Processor                     │ GR712RC LEON3 @ 50 MHz      │ SPARC V8, Bare-Metal Core 1 │
│ Dynamic Memory (Heap)                │ STRICTLY FORBIDDEN          │ Zero malloc() / Static Pools│
│ Total RAM Footprint                  │ Pre-allocated sandbox RAM   │ 28.6 kB Static RAM          │
│ Stack Depth                          │ 64.0 kB max (at 0x40010000) │ < 10.0 kB Stack Depth       │
│ Execution Time per Frame (WCET)      │ Sub-second processing       │ 0.85 seconds per frame      │
│ CPU Load                             │ Extremely low               │ 3.6% of 50 MHz core         │
│ Code Quality Standard                │ ECSS-E-ST-40C Category D    │ MISRA-C:2012 Zero-Warning   │
└──────────────────────────────────────┴─────────────────────────────┴─────────────────────────────┘
```

---

## 4. Compliance with Hera Interfaces & PUS Architecture

- Ingestion of Datapool parameters from ANNEX B:
  - `AOCS_EST_ATT_Q1_VAL` through `Q4` (Phase angle correction)
  - `PALT_ALTITUDE_VAL` (Distance-compensated flux normalization)
- Emits compact PUS Science Packets (APID 0x485) and PUS Service 3 Housekeeping packets via `Hera_Science_Report` and `Hera_HK_Report`.

---

## 5. Direct Scientific Synergy with Czech Planetary Science Heritage

CHRONOS-Photometry directly bridges the Hera mission with the world-leading asteroid photometry legacy of the **Astronomical Institute of the Czech Academy of Sciences (Ondřejov Observatory)**:
- **Dr. Petr Pravec and Dr. Petr Scheirich** at Ondřejov discovered the binary nature of Didymos in 2003 via ground-based photometric lightcurves.
- CHRONOS-Photometry provides the first in-situ spaceborne operationalization of their photometric lightcurve inversion methodology, comparing onboard real-time measurements with 20+ years of Ondřejov ground archival data.

---

## 6. Industrial Implementation Roadmap & Leadership

- Delivered by **radixal s.r.o.** under the leadership of **Bc. Viktor Lošťák** (PI), **Ing. Petr Slepička** (Engineering Lead), and **Mgr. David Riedl** (Governance).
- Final flight package delivered before **May 31, 2027** including full source code, DDF, SUM, ICD, and V&V Test Reports.

---
*Document prepared by radixal s.r.o. for submission to the European Space Agency (ESA OSIP Campaign: Autonomous Software Experiments on Hera).*
