# 🛰️ Radixal Deep-Space Autonomy Suite (R-DAS)
### Autonomous Zero-Heap Edge AI & Vision Pipeline for the ESA Hera Asteroid Mission

[![Language: C99](https://img.shields.io/badge/Language-C99-blue.svg)](https://en.wikipedia.org/wiki/C99)
[![Target: LEON3 SPARC V8](https://img.shields.io/badge/Target-LEON3%20GR712RC-orange.svg)](https://www.gaisler.com/)
[![Standard: ECSS Cat D](https://img.shields.io/badge/Standard-ECSS--E--ST--40C%20Cat%20D-green.svg)](https://ecss.nl/)
[![MISRA: C:2012](https://img.shields.io/badge/MISRA-C%3A2012%20Compliant-brightgreen.svg)](https://www.misra.org.uk/)
[![Agency: ESA OSIP](https://img.shields.io/badge/ESA-OSIP%20Campaign-blueviolet.svg)](https://ideas.esa.int)

---

## 📌 Mission & Project Overview

The **Radixal Deep-Space Autonomy Suite (R-DAS)** is an embedded, deterministic, zero-heap edge computing suite designed to execute on the isolated **Core 1 bare-metal sandbox of the Frontgrade Gaisler GR712RC dual-core processor (LEON3 SPARC V8 @ 50 MHz)** on board the European Space Agency's **Hera** planetary defence spacecraft.

During the Hera Extended Mission at the Didymos-Dimorphos binary asteroid system (scheduled for in-flight execution in **August 2027**), R-DAS enables real-time autonomous geological feature detection, 2D integer wavelet image compression, vision-based relative optical navigation, and telemetry anomaly detection without ground intervention.

Developed by **radixal s.r.o.** (Purkyňova 649/127, 612 00 Brno, Czech Republic).

---

## 🏛️ Project Leadership Triad

- **Principal Investigator (PI) & Lead Architect:**  
  **Bc. Viktor Lošťák** (`viktor.lostak@radixal.net`)
- **Engineering Lead & Software Delivery Director:**  
  **Ing. Petr Slepička**
- **Executive Director & Project Governance:**  
  **Mgr. David Riedl**

---

## 🗂️ R-DAS Software Portfolio (6 OSIP Submission Proposals)

The complete suite encompasses 6 self-contained, modular proposals submitted under the ESA Open Space Innovation Platform (**OSIP**) campaign:

| Identifier | Module Name | Track / Category | Key Technical Highlight |
| :--- | :--- | :--- | :--- |
| **`RDAS-EDGE-ARGOS`** | **ARGOS-AI** *(Flagship)* | **Cat. 4 – Edge AI & Onboard Computing** | INT8 Micro-CNN in static TensorArena + PALT laser crater metric scaling. |
| **`RDAS-COMP-WAVE`** | **DEEP-WAVE** | **Cat. 2 – Science Data Processing** | Reversible CDF 5/3 integer wavelet DWT slashing downlink bandwidth by -82.4%. |
| **`RDAS-NAV-AURA`** | **AURA-GNC** | **Cat. 1 – Spacecraft Autonomy & GNC** | Tiny-ORB crater tracking & 9-state Extended Kalman Filter (EKF). |
| **`RDAS-FDIR-AEGIS`** | **AEGIS-FDIR** | **Cat. 5 – Spacecraft Resilience & FDIR** | Quantized INT8 Isolation Forest operationalizing ESTEC's HERA-IoD research. |
| **`RDAS-OPS-ARES`** | **ARES-Planner** | **Cat. 3 – Operations Optimization** | Deterministic CSP branch-and-bound solver maximizing science window returns (+35%). |
| **`RDAS-ASTRO-CHRON`**| **CHRONOS** | **Cat. 6 – Planetary Science / Open Innovation**| Autonomous aperture photometry tracking Dimorphos post-impact orbital period. |

---

## ⚙️ Target Hardware & Execution Constraints

```
┌──────────────────────────────────────┬───────────────────────────────────────────────────────────┐
│ System Parameter                     │ Specification / Hera Flight Constraint                    │
├──────────────────────────────────────┼───────────────────────────────────────────────────────────┤
│ Microprocessor                       │ Frontgrade Gaisler GR712RC Dual-Core LEON3 (SPARC V8)    │
│ Target Execution Core                │ Core 1 (Isolated Guest Software Sandbox)                  │
│ Nominal Core Clock Frequency         │ 50 MHz                                                    │
│ Operating System (Core 1)            │ 100% Bare-Metal (No OS, No Syscalls, No RTOS)             │
│ Dynamic Memory Allocation            │ STRICTLY PROHIBITED (Zero malloc / Static Memory Pools)   │
│ Stack Pointer Constraint             │ 64.0 kB max (Pre-allocated starting at 0x40010000)        │
│ Daily In-Flight Execution Slot       │ 2 to 3 hours per operational pass (Stateless session)     │
│ Telemetry Ceiling                    │ 12.0 MB maximum science volume per 3-hour session         │
│ Software Safety Standard             │ ECSS-E-ST-40C Category D / MISRA-C:2012 Compliant        │
└──────────────────────────────────────┴───────────────────────────────────────────────────────────┘
```

---

## 📁 Repository Directory Layout

```
rdas-hera/
├── README.md                          # Master technical repository documentation (English)
├── .gitignore                         # Build and dataset exclusion rules
├── media/
│   └── rdas_mission_patch.jpg         # Official international R-DAS mission insignia
├── src/                               # Deterministic ANSI/MISRA-C99 flight codebase
│   ├── rdas_types.h                   # Common data types, TMR voting, and fixed-point macros
│   ├── rdas_wavelet.h / .c            # Reversible 2D CDF 5/3 lifting wavelet transform engine
│   ├── rdas_saliency.h / .c           # Integer gradient saliency & crater feature extractor
│   ├── rdas_main.c                    # Main in-flight execution loop (hera_interface.h entry)
│   └── Makefile                       # Toolchain build script (sparc-gaisler-elf-gcc)
├── scripts/
│   └── benchmark_simulation.py        # Python benchmark harness verifying real AFC dataset
├── proposals/                         # Complete 10-page English OSIP Submission Proposals
│   ├── ESA-OSIP-HERA-2026-RDAS-EDGE-ARGOS-AI_Working_Draft.md
│   ├── ESA-OSIP-HERA-2026-RDAS-COMP-DEEP-WAVE_Working_Draft.md
│   ├── ESA-OSIP-HERA-2026-RDAS-NAV-AURA-GNC_Working_Draft.md
│   ├── ESA-OSIP-HERA-2026-RDAS-FDIR-AEGIS-FDIR_Working_Draft.md
│   ├── ESA-OSIP-HERA-2026-RDAS-OPS-ARES-PLANNER_Working_Draft.md
│   └── ESA-OSIP-HERA-2026-RDAS-ASTRO-CHRONOS_Working_Draft.md
└── specs/                             # Official ESA Interface Control & Technical Requirements
    ├── Technical_and_operational_requirements.pdf
    ├── ANNEX_A_-_Hera_interface_API_documentation.pdf
    ├── ANNEX_B_-_Datapool.pdf
    ├── ANNEX_C_-_Hera_client_stub__user_and_integration_guide.pdf
    └── simulation_layer/              # Official ESA client simulation stub in C
```

---

## 🛠️ Building & Verification

### Compiling with the Frontgrade Gaisler BCC SPARC Toolchain:

```bash
cd src/
make CC=sparc-gaisler-elf-gcc
```

### Running the Dataset Benchmark:

```bash
python scripts/benchmark_simulation.py
```

---

## 📜 Intellectual Property & Licensing

All software architectures, algorithms, and documentation contained herein are the proprietary intellectual property of **radixal s.r.o.** (Brno, Czech Republic) in accordance with the **ESA Open Space Innovation Platform (OSIP) General Conditions of Participation**. 100% of Intellectual Property Rights (IPR) remain with radixal s.r.o.

For technical inquiries or academic collaboration, please contact:  
**Bc. Viktor Lošťák** – *Lead Architect & Principal Investigator*, `viktor.lostak@radixal.net`.
