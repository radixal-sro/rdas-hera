# EUROPEAN SPACE AGENCY – OPEN SPACE INNOVATION PLATFORM (OSIP)
## Call for Ideas: Autonomous Software Experiments on Hera
### IDEA PROPOSAL & TECHNICAL WORKING DRAFT

---

```
====================================================================================================
PROPOSAL IDENTIFIER:  ESA-OSIP-HERA-2026-RDAS-FDIR-AEGIS-FDIR
PROPOSAL TITLE:       AEGIS-FDIR: Autonomous Embedded Guard & Isolation-Forest Telemetry Anomaly 
                      Detector on Hera LEON3 Bare-Metal Core (HERA-IoD Framework Operationalization)
PRIMARY TRACK:        Category 5 – Spacecraft Resilience & FDIR
COMPLEMENTARY TRACKS: Category 4 (Edge AI & Computing) & Category 3 (Operations Optimization)
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
│ AEGIS-FDIR is an autonomous, onboard telemetry anomaly detection engine that operationalizes the │
│ pioneering research of the ESA/ESTEC Flight Software Systems Section (HERA-IoD initiative).      │
│ Running on the bare-metal Core 1 of the GR712RC processor, it monitors 16 mission telemetry      │
│ channels in real time using a zero-heap, quantized INT8 Isolation Forest ensemble.               │
│                                                                                                  │
│ By detecting subtle multi-dimensional anomalies (thermal drift, micro-vibrations, SpaceWire bus │
│ retries) hours before traditional threshold alarms trigger, AEGIS-FDIR demonstrates next-gen    │
│ autonomous resilience for European deep-space exploration and future long-duration missions.     │
│                                                                                                  │
│ 📊 KEY IN-FLIGHT BUDGETS & METRICS:                                                              │
│ • CPU Utilization:          < 1.0% @ 50 MHz SPARC V8 (Peak WCET: 0.12 s per 10-second cycle)      │
│ • RAM Footprint:            18.2 kB static memory (Zero malloc / Zero heap fragmentation)        │
│ • Stack Memory:             < 8.0 kB (Within the hard 64.0 kB stack limit at 0x40010000)         │
│ • Monitored Channels:       16 continuous Mission Data Pool parameters (AOCS, PCDU, SpaceWire)   │
│ • Anomaly Detection Lead:   Detects multivariate degradation 4–12 hours ahead of hard OOL limits │
│ • Telemetry Emission:       PUS Service 3 HK (128 B / 10 min) & PUS Service 5 Anomaly Events     │
│ • Mathematical Core:        100% Fixed-Point integer trees (Bit-exact, zero float non-determ.)   │
│ • Institutional Synergy:    Direct in-flight validation of ESTEC TEC-SW HERA-IoD ADCSS2023 work  │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 1. The Problem Statement & Spacecraft FDIR Bottlenecks

Current deep-space spacecraft health monitoring relies primarily on **static Out-Of-Limits (OOL) threshold checks**:

1. **Blindness to Multivariate Correlations:** Static thresholds only trigger when a physical parameter (e.g. temperature, voltage, gyro drift) crosses an absolute safety envelope. They cannot detect subtle multivariate anomalies—such as a temperature rise correlating with an unexpected rise in reaction wheel current—which indicate incipient bearing degradation long before hard limits are exceeded.
2. **Ground Analysis Delay:** Ground operations teams at ESOC in Darmstadt analyze telemetry offline after scheduled Estrack downlink passes. At Didymos, an anomaly developing during an unmonitored 20-hour gap may progress to component failure before ground operators receive the data.
3. **The Need for Lightweight Onboard AI FDIR:** To achieve true autonomy, spacecraft must evaluate their own multivariate telemetry streams continuously on board using low-power, radiation-tolerant computing cores.

---

## 2. The AEGIS-FDIR Algorithmic Architecture

AEGIS-FDIR operationalizes the **HERA-IoD** research developed by the ESA/ESTEC Flight Software Systems Section (López Trescastro et al., ADCSS 2023) by implementing a **deterministic, quantized INT8 Isolation Forest**:

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 AEGIS-FDIR PROCESSING PIPELINE                                   │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘

 [ Mission Data Pool ] Ingestion of 16 Telemetry Parameters (ANNEX B)
       │
       ▼
 ┌────────────────────────────────────────────────────────────────────────────────────────────────┐
 │ STAGE 1: Real-Time Telemetry Normalization & Feature Vector Assembly                           │
 │ • Reads 16 parameters (AOCS Gyros, Wheel Speeds, Bus Voltages, SpaceWire Error Counters)       │
 │ • Fixed-point min-max scaling to 8-bit integer domain: x_norm = ((x - min) * 255) / (max - min)│
 └────────────────────────────────────────────────────────────────────────────────────────────────┘
       │
       ▼
 ┌────────────────────────────────────────────────────────────────────────────────────────────────┐
 │ STAGE 2: Quantized INT8 Isolation Forest Ensemble (20 Micro-Trees)                             │
 │ • Ensemble of 20 decision trees (depth = 6) stored in compact static ROM table (12.8 kB)       │
 │ • Computes average path length h(x) across all trees using integer pointer arithmetic           │
 │ • Anomaly Score calculation: S(x, n) = 2^(-E(h(x)) / c(n)) mapped to 0–100 integer score       │
 └────────────────────────────────────────────────────────────────────────────────────────────────┘
       │
       ▼
 ┌────────────────────────────────────────────────────────────────────────────────────────────────┐
 │ STAGE 3: Fault Isolation & Attribution Engine                                                  │
 │ • If Anomaly Score > 65%, analyzes tree branch splits to identify top contributing parameters   │
 │ • Generates structured fault isolation code (e.g., "AOCS_RW_CURRENT_DEGRADATION")              │
 └────────────────────────────────────────────────────────────────────────────────────────────────┘
       │
       ▼
 ┌────────────────────────────────────────────────────────────────────────────────────────────────┐
 │ STAGE 4: PUS Telemetry & Warning Event Emission                                                │
 │ • Emits routine health score in PUS Service 3 (SID 0x484, 128 bytes every 10 min)              │
 │ • Emits PUS Service 5 Event (ID 0x510) only when severe novel anomaly is identified            │
 └────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Technical Feasibility & Embedded Realism on GR712RC (LEON3)

```
┌──────────────────────────────────────┬─────────────────────────────┬─────────────────────────────┐
│ Parameter                            │ Hera Platform Constraint    │ AEGIS-FDIR Implementation   │
├──────────────────────────────────────┼─────────────────────────────┼─────────────────────────────┤
│ Processor Target                     │ GR712RC LEON3 @ 50 MHz      │ SPARC V8, Bare-Metal Core 1 │
│ Dynamic Memory Allocation            │ STRICTLY FORBIDDEN (0 heap) │ Zero malloc() / Static Data │
│ Total RAM Footprint                  │ Pre-allocated sandbox RAM   │ 18.2 kB Static RAM          │
│ Stack Depth                          │ 64.0 kB max (at 0x40010000) │ < 8.0 kB Stack Depth        │
│ Cycle Execution Time (WCET)          │ Sub-second evaluation       │ 0.12 seconds per cycle      │
│ CPU Load                             │ Negligible overhead         │ < 1.0% of 50 MHz core       │
│ Code Quality Standard                │ ECSS-E-ST-40C Category D    │ MISRA-C:2012 Zero-Warning   │
└──────────────────────────────────────┴─────────────────────────────┴─────────────────────────────┘
```

---

## 4. Compliance with Hera Interfaces & PUS Architecture

- Ingestion of Datapool parameters from ANNEX B:
  - `AOCS_GYRO_RATE_X_VAL`, `Y_VAL`, `Z_VAL`
  - `PCDU_BATT_V_VAL`, `PCDU_BATT_I_VAL`
  - `MMU_ACTIVE_PARTITION`
  - `CPS_PRESS_VAL` (Propulsion pressure)
  - `PALT_STATUS`, `PALT_ALTITUDE_VAL`
- Emits standard PUS Service 3 Housekeeping and PUS Service 5 Event packets via `Hera_HK_Report` and `Hera_Event_Report`.

---

## 5. Direct Institutional Synergy with ESA/ESTEC HERA-IoD Initiative

AEGIS-FDIR directly honors and extends the research conducted by **Jorge López Trescastro and the ESTEC Flight Software Systems Section** presented at the **17th ESA Workshop on Avionics, Data, Control and Software Systems (ADCSS2023)**:
- *Laboratory Concept:* The ESTEC team demonstrated the viability of ML anomaly detection on LEON3 using simulated XMM/MEX data.
- *In-Flight Realization:* radixal s.r.o. provides the flight-ready, MISRA-C qualified execution engine to transition this ESTEC concept into **the first in-flight operational demonstration of AI-driven FDIR on a deep-space mission**.

---

## 6. Industrial Implementation Roadmap & Leadership

- Delivered by **radixal s.r.o.** under the leadership of **Bc. Viktor Lošťák** (PI), **Ing. Petr Slepička** (Engineering Lead), and **Mgr. David Riedl** (Governance).
- Final flight package delivered before **May 31, 2027** including full source code, DDF, SUM, ICD, and V&V Test Reports.

---
*Document prepared by radixal s.r.o. for submission to the European Space Agency (ESA OSIP Campaign: Autonomous Software Experiments on Hera).*
