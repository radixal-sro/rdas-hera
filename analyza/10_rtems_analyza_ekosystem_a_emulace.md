# 🛰️ 10. RTEMS – Operační systém pro hluboký vesmír (Ekosystém, API a Emulace)

Tento dokument detailně popisuje operační systém **RTEMS** (*Real-Time Executive for Multiprocessor Systems*), který běží na jádře **Core 0** sondy Hera a představuje de-facto standardní operační systém pro evropské a světové meziplanetární mise.

---

## 📌 1. Co to je RTEMS?

**RTEMS** je otevřený (Open-Source), deterministický, tvrdě reálný operační systém (**Hard Real-Time RTOS**) navržený speciálně pro vysoce spolehlivé vestavné (embedded) a kosmické systémy.

- **Původ a historie:** Původně vyvinut v pozdních 80. letech pro americké vojenské a kosmické aplikace (*Real-Time Executive for Missile Systems*), později uvolněn pod svobodnou licencí (modifikovaná BSD/GPL) a přejmenován na *Real-Time Executive for Multiprocessor Systems*.
- **Vesmírný zlatý standard:** Je to hlavní a nejrozšířenější RTOS používaný agenturami **ESA, NASA i JAXA**.
- **Mise, na kterých RTEMS letěl / letí:**
  - 🔭 **James Webb Space Telescope (JWST)** – hlavní řízení přístrojů
  - 🔴 **Mars Reconnaissance Orbiter (MRO) & Curiosity / Perseverance rovery**
  - ☄️ **Rosetta & Philae** (první přistání na kometě 67P)
  - ☀️ **Solar Orbiter & BepiColombo** (mise k Merkuru)
  - 🛰️ **Hera (Core 0)** – řízení letu u asteroidu Didymos
  - Desítky evropských vědeckých družic a CubeSatů.

---

## ⚙️ 2. Klíčové architektonické vlastnosti RTEMS

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                          ARCHITEKTURA SYSTÉMU RTEMS                              │
├──────────────────────────────────────────────────────────────────────────────────┤
│ 🔹 **Single Address Space:** Všechny úlohy (tasky) sdílejí jeden paměťový       │
│    prostor. Žádné virtuální adresování / swapping ➔ nulová režie.                │
│                                                                                  │
│ 🔹 **Tvrdý determinismus (Hard Real-Time):** Přesně garantované, sub-mikrosekundové│
│    časy odezvy na hardwarová přerušení (Interrupt Latency) a přepnutí úloh.      │
│                                                                                  │
│ 🔹 **Plná podpora POSIX API:** Umožňuje používat standardní unixové funkce      │
│    (pthreads, mutexy, semafory, fronty zpráv, časovače).                         │
│                                                                                  │
│ 🔹 **C / C++ Runtime (Newlib):** Kompletní standardní knihovna libc a libm      │
│    optimalizovaná pro embedded procesory.                                        │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ 3. Vývojové prostředí, toolchain a dostupné knihovny

Pro RTEMS existuje špičkově zdokumentovaný, volně dostupný vývojový ekosystém:

### A. Kompilátory a toolchainy
1. **Frontgrade Gaisler RCC (RTEMS Cross Compiler):**
   - Oficiální distribuce od výrobce procesorů LEON3 (Gaisler).
   - Toolchain: `sparc-gaisler-rtems5-gcc` nebo `sparc-gaisler-rtems6-gcc`.
   - Podporuje všechny procesory řady LEON2, LEON3, LEON4 a RISC-V (NOEL-V).
2. **RSB (RTEMS Source Builder):**
   - Oficiální open-source sestavovací skript, který zkompiluje kompletní GCC/G++ toolchain a Newlib pro jakoukoliv architekturu na Linuxu, Windows (WSL / MSYS2) i macOS.

### B. Podporovaná API a knihovny
- **POSIX API (IEEE 1003.1):** Standardní `pthread_create`, `pthread_mutex_lock`, `mq_send`, `timer_create` – kód z Linuxu lze přenést téměř beze změn!
- **Classic RTEMS API:** Původní nativní C rozhraní (`rtems_task_create`, `rtems_semaphore_obtain`, `rtems_message_queue_send`).
- **Komunikační a síťové stacky:** lwIP / FreeBSD TCP/IP stack, CAN bus drivery, SpaceWire protokoly, MIL-STD-1553, I2C, SPI.
- **Souborové systémy:** FAT16/FAT32, IMFS (In-Memory RAM disk), RFS, TFTP.

### C. IDE a editory
- **VS Code** (s pluginy pro C/C++, Cortex-Debug / GDB), **CLion**, **Eclipse CDT**, nebo klasické terminálové nástroje s **Makefile / CMake / Waf**.

---

## 💻 4. Dá se RTEMS emulovat na běžném hardware (PC / Notebook)?

**ANO, NAPROSTO DOKONALE A BĚHEM NĚKOLIKA SEKUND!**

K vývoji a ladění pro sondu Hera nepotřebujeme žádný drahý letový hardware. Celý systém lze v reálném čase simulovat přímo na běžném notebooku pomocí několika nástrojů:

### 1. QEMU SPARC LEON3 (Nejrychlejší a bezplatný):
- Standardní QEMU obsahuje plnohodnotný emulátor desky LEON3 (`qemu-system-sparc -M leon3_generic`).
- Emuluje kompletní instrukční sadu SPARC V8, systémové časovače (GPTIMER), řadič přerušení (IRQMP) i sériovou linku (APBUART).
- Spuštění RTEMS kernelu v QEMU trvá **méně než 1 sekundu**.

### 2. Gaisler TSIM3 (Cyklově přesný simulátor):
- Profesionální simulátor od výrobce procesorů Gaisler.
- Emuluje procesor LEON3 s přesností na jednotlivé hodinové cykly, simuluje paměťové cache, wait-states a sběrnice SpaceWire.
- K dispozici je bezplatná verze pro vývoj a evaluaci.

### 3. GDB Remote Debugging:
- QEMU i TSIM umožňují připojit debugger `sparc-gaisler-rtems-gdb` přes TCP port `1234`.
- Můžeme krokovat C kód řádek po řádku, nastavovat breakpointy a kontrolovat registry i paměť.

---

## 📚 5. Oficiální dokumentace a zdroje

- 🌐 **Hlavní web projektu RTEMS:** [https://www.rtems.org/](https://www.rtems.org/)
- 📖 **Oficiální dokumentace (tisíce stran manuálů):** [https://docs.rtems.org/](https://docs.rtems.org/)
  - *RTEMS POSIX API User's Guide*
  - *RTEMS Classic API Guide*
  - *RTEMS BSP (Board Support Package) & Driver Guide*
- 🚀 **Gaisler RTEMS distribuce pro LEON3:** [https://www.gaisler.com/index.php/products/operating-systems/rtems](https://www.gaisler.com/index.php/products/operating-systems/rtems)
- 🇪🇺 **ESA Space Profile:** RTEMS prošel oficiální kosmickou kvalifikací ESA podle standardů ECSS (ECSS Space Qualification of RTEMS).

---

## 💡 Kontext pro naši soutěž:

Na sondě Hera běží **RTEMS na jádře Core 0** (kde zajišťuje letový provoz a drivery pro hardware), zatímco **naše jádro Core 1 je záměrně čistý Bare-Metal**, aby:
1. Náš kód neměl žádnou režii operačního systému (využil 100 % výkonu 50MHz CPU pro algoritmy).
2. Naše C aplikace byla naprosto izolovaná a nemohla jakkoliv ohrozit RTEMS jádro na Core 0.
