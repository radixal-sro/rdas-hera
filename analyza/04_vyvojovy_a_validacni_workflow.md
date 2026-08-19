# 🛠️ 04. Vývojový a validační workflow (Python ➔ MISRA-C ➔ QEMU)

Tento dokument slouží jako praktický návod, jak vyvíjet, trénovat, optimalizovat a validovat experimentální software pro sondu Hera v lokálním vývojovém prostředí.

---

## 🔄 1. Třífázový vývojový cyklus

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│ FÁZE 1: Algoritmický vývoj & Trénování AI (Python na běžném PC / GPU)             │
│ - Trénování modelů v PyTorch / TensorFlow (TinyML, Decision Trees, Wavelets)     │
│ - Validace na staženém datasetu 2400+ snímků AFC (podklady/AFC_images.tar.gz)    │
│ - Kvantizace do 8-bit INT8 / Fixed-Point, export vah do C hlaviček (bin2c.py)   │
└──────────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│ FÁZE 2: Implementace v ANSI / MISRA-C (Bez dynamické alokace)                    │
│ - Čistý C kód bez malloc (statická paměť, lookup tabulky, celočíselná matematika)│
│ - Integrace s hera_interface.h a simulačním stubem hera_client_stub.c           │
└──────────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│ FÁZE 3: Přesná emulace v QEMU SPARC LEON3 (Lokální simulace sondy)               │
│ - Kompilace přes sparc-gaisler-elf-gcc -mcpu=leon3 -O2                           │
│ - Spuštění v QEMU: qemu-system-sparc -M leon3_generic -kernel hera_test.elf      │
│ - Měření počtu cyklů, spotřeby paměti v RAM a generování PUS paketů             │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🧪 2. Práce s testovacími daty a simulačním balíčkem

Všechny nástroje a data dodaná agenturou ESA jsou připraveny ve složce [`podklady/`](file:///c:/Users/vikto/Disk%20Google/Radixal/Zakázky/2026_026%20Hera%20Space%20Probe%20Code%20Contest/podklady/):

1. **Dataset reálných snímků:**
   - Archiv `AFC_images.tar.gz` obsahuje více než 2 400 snímků kamery AFC (formáty PNG, BIN, TXT metadata s APID 292).
   - Tyto snímky slouží jako trénovací a validační sada pro palubní algoritmy.

2. **Konverze snímků do C kódu (`bin2c.py`):**
   - Pomocí skriptu popsaného v [Annexu D](file:///c:/Users/vikto/Disk%20Google/Radixal/Zakázky/2026_026%20Hera%20Space%20Probe%20Code%20Contest/podklady/ANNEX_D_-_bin2c__binary_to_c_header_converter.pdf) převedeme vybrané binární snímky do pole `images_data.h`:
   ```bash
   python bin2c.py test_image1.bin test_image2.bin
   ```

3. **Simulační vrstva (`hera_client_stub.c`):**
   - Nachází se v [`podklady/simulation_layer/esw_interface/`](file:///c:/Users/vikto/Disk%20Google/Radixal/Zakázky/2026_026%20Hera%20Space%20Probe%20Code%20Contest/podklady/simulation_layer/esw_interface/).
   - Simuluje chování jádra Core 0, prodlevy při snímání (7 s pro AFC, 15 min pro HyperScout, 10 min pro TIRI) a umožňuje ladit UART výstupy na standardním terminálu.

---

## ⚙️ 3. Kompilace a spuštění v QEMU SPARC

### Kompilace binárního souboru ELF:
```bash
sparc-gaisler-elf-gcc -mcpu=leon3 -g -O2 -nostartfiles -Ttext=0x40000000 \
    start.S main.c hera_client_stub.c -o hera_test.elf
```

### Spuštění emulátoru QEMU:
```bash
qemu-system-sparc -M leon3_generic -display none -serial stdio -kernel hera_test.elf
```

### Ladění přes GDB:
```bash
# Spuštění QEMU s čekáním na GDB (port 1234):
qemu-system-sparc -M leon3_generic -display none -serial stdio -kernel hera_test.elf -s -S

# V druhém terminálu:
sparc-gaisler-elf-gdb hera_test.elf
(gdb) target remote localhost:1234
(gdb) break main
(gdb) continue
```

---

## 📋 4. Kontrolní seznam před odevzdáním návrhu (Checklist)

- [ ] **Žádná dynamická paměť:** Ověřeno, že v C kódu není ani jeden `malloc`, `calloc`, `realloc` nebo `free`.
- [ ] **Paměťový limit:** Statická alokace RAM je pod 250 kB, velikost zásobníku (stack) nepřekračuje 64 KB.
- [ ] **Deterministický běh:** Čas výpočtu na snímek je střízlivě spočten na 50MHz CPU (< 1 sekunda na AFC snímek).
- [ ] **PUS Telemetrie:**
  - Housekeeping (Service 3) max. 1× za 5–10 minut (do 256 B).
  - Eventy (Service 5) pouze při významných událostech (do 50 B).
  - Vědecká data celkem do 2,5 MB na 3hodinové okno (hluboko pod limitem 12 MB).
- [ ] **Bezstavovost (Stateless):** Aplikace může být kdykoliv vypnuta bez poškození integrity.
- [ ] **Validace v simulátoru:** Kód úspěšně proběhne v QEMU a projde testy na reálných snímcích.
