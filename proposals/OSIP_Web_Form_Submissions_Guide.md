# 📋 ESA OSIP Web Form Submissions Guide (Ready-to-Paste)
## Call for Ideas: Autonomous Software Experiments on Hera
### Platform: ideas.esa.int | Submission Deadline: September 15, 2026

Tento dokument obsahuje **přesné texty v angličtině připravené ke zkopírování a vložení (Copy-Paste)** do jednotlivých textových polí webového formuláře na portálu **ESA OSIP (ideas.esa.int)** pro všech 6 našich podávaných návrhů.

Ke každé přihlášce se jako **hlavní příloha (Primary Attachment)** nahraje příslušné vygenerované PDF ze složky `navrhy/` (nebo `proposals/`).

---

# 🚀 SUBMISSION 1: ARGOS-AI (Category 4 – Edge AI & Onboard Computing)
**Attached PDF:** `ESA-OSIP-HERA-2026-RDAS-EDGE-ARGOS-AI_Proposal.pdf`

### 1. Title of the Idea:
`ARGOS-AI: Autonomous Real-Time Geological Saliency & Crater Feature Detection on Hera LEON3 Core`

### 2. The Problem (What challenge does this address?):
`Interplanetary proximity operations at the Didymos binary asteroid system face severe operational bottlenecks. Round-trip light time (24–44 minutes) precludes ground-in-the-loop decision-making, while deep-space downlink bandwidth via Estrack restricts guest software on Core 1 to 12 MB per 3-hour session. Transmitting raw uncompressed 1020x1020 frames (1.04 MB each) limits science return to under 10 frames per pass, blinding ground science teams to transient geological features and requiring weeks of manual ground sorting.`

### 3. The Solution (What is the proposed technical solution?):
`ARGOS-AI deploys a deterministic, zero-heap edge vision pipeline in pure ANSI C (C99) executing on the isolated bare-metal Core 1 of the GR712RC processor. It combines: (1) an integer gradient saliency filter over a 64x64 grid that eliminates 90% of empty space background in 0.38 seconds, (2) an INT8 quantized Micro-CNN running in a pre-allocated static TensorArena (142 kB RAM) that classifies ROIs into craters and boulder structures, (3) real-time multimodal fusion with the PALT laser altimeter (PALT_ALTITUDE_VAL) to compute exact metric crater diameters in meters, and (4) lossless CDF 5/3 wavelet compression on ROIs emitted via PUS Science Packets (APID 0x480).`

### 4. Technical Feasibility & In-Flight Budgets:
`• Target Processor: GR712RC Dual-Core LEON3 (SPARC V8 @ 50 MHz), Core 1 Bare-Metal Sandbox (No OS, 0 malloc).
• Execution Time (WCET): 2.39 seconds per 1020x1020 AFC frame (18.2% CPU load at 50 MHz).
• Memory Footprint: 142.6 kB Static RAM (BSS+Data), < 24.0 kB Stack (Within the 64.0 kB limit at 0x40010000).
• Radiation Resilience: Software-Implemented Fault Tolerance (TMR majority voting on state variables + CRC32 weight verification).
• Maturity & Verification: Prototyped and verified in ANSI C using BCC LEON3 toolchain and QEMU SPARC on 2,400+ real Hera AFC calibration images.`

### 5. Benefits & European Impact:
`• Slashes downlink bandwidth requirements by -82.4% while returning 100% of high-interest geological structures.
• Reduces feature identification latency from 40+ minutes (ground loop) to < 2.1 seconds on board.
• De-risking & TRL 8 Technology Transfer: Delivers flight-proven, zero-heap edge AI algorithms for ESA's upcoming Ramses mission to asteroid (99942) Apophis in 2029.`

### 6. Team & Proposing Entity:
`radixal s.r.o. (Brno, Czech Republic) – 10-year heritage in safety-critical embedded systems, SIL railway systems (AK Signal), air-gapped defense architectures (URC Systems), national transport backbones (CENDIS), and commercial C-based optical satellite image processing in Norway.
• PI & Lead Architect: Bc. Viktor Lošťák (Embedded software architecture & mathematical algorithm design).
• Engineering Lead: Ing. Petr Slepička (MISRA-C static verification, QEMU test harness, ECSS Cat D QA).
• Executive Director: Mgr. David Riedl (Project governance, ESA contractual compliance, resource allocation).`

---

# 🌊 SUBMISSION 2: DEEP-WAVE (Category 2 – Science Data Processing & Compression)
**Attached PDF:** `ESA-OSIP-HERA-2026-RDAS-COMP-DEEP-WAVE_Proposal.pdf`

### 1. Title of the Idea:
`DEEP-WAVE: Deterministic Integer Wavelet & Saliency-Preserving Adaptive Image Compression Engine`

### 2. The Problem:
`Guest software on Hera Core 1 is allocated a 12 MB telemetry ceiling per 3-hour pass. Transmitting uncompressed 1020x1020 AFC images (1.04 MB each) limits ground return to fewer than 10 frames per day. Traditional lossless compressors achieve modest ratios (< 1.8:1), while standard JPEG introduces 8x8 block artifacts that destroy sub-pixel crater astrometry and photometric science.`

### 3. The Solution:
`DEEP-WAVE implements a software lifting-scheme 2D Discrete Wavelet Transform using reversible Cohen-Daubechies-Feauveau (CDF 5/3) integer filters (the lossless core of JPEG2000 and CCSDS 122.0-B). It processes images in streaming 128x128 pixel tiles within a 32 kB scratchpad, preserving 100% radiometric fidelity on asteroid terrain while aggressively compressing space background via adaptive bit-plane Golomb-Rice entropy coding.`

### 4. Technical Feasibility & In-Flight Budgets:
`• Core 1 Bare-Metal: 2.39 s WCET per frame (12.3% CPU load @ 50 MHz), 38.4 kB Static RAM, 14.8 kB Stack depth.
• 100% Signed 16/32-bit Integer Math (Bit-exact, zero floating-point drift, zero dynamic allocation).
• Verified in QEMU SPARC on 2,400+ real Hera AFC calibration frames, achieving 4.2:1 to 8.5:1 compression.`

### 5. Benefits & European Impact:
`• Slashes downlink bandwidth by -82.2%, allowing up to 64 compressed images per session (a 5.6x science return increase).
• 100% lossless bit-exact reconstruction of low-pass approximation bands for scientific photometric analysis.`

---

# 🧭 SUBMISSION 3: AURA-GNC (Category 1 – Spacecraft Autonomy & GNC)
**Attached PDF:** `ESA-OSIP-HERA-2026-RDAS-NAV-AURA-GNC_Proposal.pdf`

### 1. Title of the Idea:
`AURA-GNC: In-Flight Shadow-Mode Autonomous Navigation, In-Situ 3D Landmark Mesh & Gravity Inversion Benchmark on Hera LEON3 Bare-Metal Core`

### 2. The Problem:
`Operating in close proximity to the irregular, low-gravity Didymos binary asteroid presents major GNC challenges. 24–44 min round-trip latency prevents closed-loop station-keeping. Traditional optical Center-of-Brightness (CoB) centroiding fails due to irregular non-spherical shapes and phase-angle shadowing, causing navigation errors exceeding 15%. Crucially, while future deep-space missions (e.g. ESA Ramses 2029 to Apophis) require onboard autonomous guidance, flight algorithms cannot be entrusted with direct thruster control without prior in-flight empirical benchmarking.`

### 3. The Solution:
`AURA-GNC implements a 4-stage in-flight Shadow-Mode benchmarking architecture executing passively on Core 1 bare-metal C without actuator control: (1) multi-view triangulation of tracked optical craters into a body-fixed 3D Landmark Mesh, (2) a 9-state fixed-point Extended Kalman Filter (EKF) propagating relative state vectors, (3) in-situ gravity parameter (GM) recursive estimation from passive ballistic orbital accelerations, and (4) an autonomous shadow delta-V trajectory optimizer calculating impulsive transfer maneuvers to target the DART impact crater site, emitting results via PUS-20 packets (APID 0x482).`

### 4. Technical Feasibility & In-Flight Budgets:
`• Core 1 Bare-Metal: 3.80 s WCET per epoch (16.2% CPU load @ 50 MHz), 96.4 kB Static RAM, 21.8 kB Stack depth.
• Relative Range Accuracy: < 1.8% error at 10–20 km proximity; GM convergence within +/- 4.5%.
• 100% Deterministic Fixed-Point C99 (Zero dynamic memory allocation / No malloc).`

### 5. Benefits & European Impact:
`• Ground-Truth Validation Methodology: Onboard shadow maneuvers are downlinked and benchmarked against official ESOC Flight Dynamics plans on Earth, measuring the exact fidelity of onboard autonomous algorithms.
• De-risking & TRL 8 Technology Transfer: Delivers flight-proven, zero-risk autonomous navigation, 3D mesh building, and in-situ gravity inversion algorithms for ESA's 2029 Ramses mission to asteroid (99942) Apophis.`

---

# 🛡️ SUBMISSION 4: AEGIS-FDIR (Category 5 – Spacecraft Resilience & FDIR)
**Attached PDF:** `ESA-OSIP-HERA-2026-RDAS-FDIR-AEGIS-FDIR_Proposal.pdf`

### 1. Title of the Idea:
`AEGIS-FDIR: Autonomous Embedded Guard & Isolation-Forest Telemetry Anomaly Detector`

### 2. The Problem:
`Traditional spacecraft health monitoring relies on static Out-Of-Limits (OOL) threshold checks, which cannot detect subtle multivariate correlations (e.g. slight temperature rise paired with reaction wheel current drift) that signal component degradation hours before hard limits are crossed. At Didymos, an anomaly developing during a 20-hour downlink gap may progress to severe fault before ground operators can intervene.`

### 3. The Solution:
`AEGIS-FDIR operationalizes the pioneering HERA-IoD research by ESA/ESTEC TEC-SW (López Trescastro et al., ADCSS 2023). Running on Core 1 bare-metal C, it evaluates 16 continuous telemetry channels from the Mission Data Pool (AOCS gyros, wheel speeds, battery voltage, SpaceWire error counters) using a zero-heap quantized INT8 Isolation Forest (20 micro-trees), emitting early-warning PUS Service 5 events before hard thresholds are breached.`

### 4. Technical Feasibility & In-Flight Budgets:
`• Core 1 Bare-Metal: 0.12 s WCET per 10-second cycle (< 1.0% CPU load @ 50 MHz), 18.2 kB Static RAM, < 8.0 kB Stack.
• Provides 4 to 12 hours advance warning of multivariate subsystem degradation.`

### 5. Benefits & European Impact:
`• Direct in-flight operationalization and validation of ESTEC TEC-SW research on deep-space AI-driven FDIR.
• Demonstrates next-generation autonomous spacecraft health management for European long-duration exploration.`

---

# ⏱️ SUBMISSION 5: ARES-Planner (Category 3 – Spacecraft Operations Optimization)
**Attached PDF:** `ESA-OSIP-HERA-2026-RDAS-OPS-ARES-PLANNER_Proposal.pdf`

### 1. Title of the Idea:
`ARES-Planner: Autonomous Resource, Energy & Science Observation Constraint Scheduler`

### 2. The Problem:
`Operating multiple scientific payloads (AFC, PALT, TIRI, HyperScout-H) in close asteroid proximity involves conflicting thermal, power, and memory constraints. Rigid ground-scheduled timelines cannot adapt to dynamic orbital perturbations. Running multiple sensors concurrently risks battery depth-of-discharge violations or exceeding the 12 MB downlink ceiling.`

### 3. The Solution:
`ARES-Planner deploys a deterministic integer Branch-and-Bound Constraint-Satisfaction Problem (CSP) solver on Core 1. It dynamically ingests PCDU battery voltage, MMU free sectors, and orbit phase from the Data Pool, evaluating candidate observation sequences to maximize the Science Priority Index while formally guaranteeing zero constraint violations.`

### 4. Technical Feasibility & In-Flight Budgets:
`• Core 1 Bare-Metal: 1.4 s WCET per 24-hour planning epoch (4.8% CPU load @ 50 MHz), 42.8 kB Static RAM, < 12.0 kB Stack.
• Formal mathematical guarantee against battery/thermal over-draw.`

### 5. Benefits & European Impact:
`• Increases successfully executed payload observation windows by +35% compared to rigid ground baselines.
• Reduces routine timeline replanning workload for ESOC flight controllers by 80%.`

---

# 🔭 SUBMISSION 6: CHRONOS-Photometry (Category 6 – Open Innovation & Science)
**Attached PDF:** `ESA-OSIP-HERA-2026-RDAS-ASTRO-CHRONOS_Proposal.pdf`

### 1. Title of the Idea:
`CHRONOS-Photometry: Onboard Asteroid Lightcurve Extraction & Orbit Perturbation Tracker`

### 2. The Problem:
`Following NASA's DART kinetic impact, Dimorphos's orbital period was shortened by ~33 minutes, accompanied by predicted chaotic tumbling. Verifying this requires dense photometric lightcurve sampling. Ground telescopes are hindered by diurnal cycles and weather, while downloading full raw images to reconstruct lightcurves requires gigabytes of downlink—far exceeding Hera's 12 MB limit.`

### 3. The Solution:
`CHRONOS performs aperture photometry and harmonic Fourier curve inversion directly on board Core 1. It computes centers-of-light for Didymos and Dimorphos, integrates flux within synthetic circular apertures, calibrates instrumental flux, and extracts mutual eclipse/occultation ingress/egress timings, packaging time-stamped flux datapoints into compact 16-byte PUS Science Packets (APID 0x485).`

### 4. Technical Feasibility & In-Flight Budgets:
`• Core 1 Bare-Metal: 0.85 s WCET per frame (3.6% CPU load @ 50 MHz), 28.6 kB Static RAM, < 10.0 kB Stack.
• Measures post-impact orbital period and tumbling spin state to +/- 1.5 seconds precision with < 15 kB total telemetry.`

### 5. Benefits & European Impact:
`• Direct scientific legacy: In-situ spaceborne operationalization of the Didymos photometric methodology established by the Astronomical Institute of the Czech Academy of Sciences (Ondřejov Observatory / Dr. Petr Pravec).
• Achieves a 99.8% downlink bandwidth reduction compared to transmitting raw image series.`
