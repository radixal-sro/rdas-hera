#!/usr/bin/env python3
"""
send_diplomatic_emails.py
Sends the 3 emails via SMTP (SSL 465) and appends them to IMAP "Sent" (SSL 993).
"""

import os
import json
import smtplib
import imaplib
import time
from email.message import EmailMessage
from email.utils import formataddr, make_msgid, formatdate
from email.header import Header

# Load credentials
creds_path = r"C:/Users/vikto/Disk Google/Osobní/radixal/Prodej/SUDOP e Redbaenk/email-credentials.json"
with open(creds_path, 'r', encoding='utf-8') as f:
    creds = json.load(f)

USER = creds['auth']['user']
PASS = creds['auth']['pass']
SMTP_HOST = "wes1-smtp.wedos.net"
SMTP_PORT = 465
IMAP_HOST = "wes1-imap.wedos.net"
IMAP_PORT = 993

CC_LIST = [
    "petr.slepicka@radixal.net",
    "david.riedl@radixal.net",
    "monika.berkyova@radixal.net"
]

def send_and_save_email(to_addrs, cc_addrs, subject, html_body, plain_body, attachment_path=None):
    msg = EmailMessage()
    msg['From'] = formataddr(('Bc. Viktor Lošťák', USER))
    
    if isinstance(to_addrs, list):
        msg['To'] = ", ".join(to_addrs)
    else:
        msg['To'] = to_addrs
        
    if cc_addrs:
        if isinstance(cc_addrs, list):
            msg['Cc'] = ", ".join(cc_addrs)
        else:
            msg['Cc'] = cc_addrs

    msg['Subject'] = subject
    msg['Date'] = formatdate(localtime=True)
    msg['Message-ID'] = make_msgid(domain='radixal.net')

    msg.set_content(plain_body)
    msg.add_alternative(html_body, subtype='html')

    if attachment_path and os.path.exists(attachment_path):
        filename = os.path.basename(attachment_path)
        with open(attachment_path, 'rb') as f:
            file_data = f.read()
        msg.add_attachment(file_data, maintype='application', subtype='pdf', filename=filename)
        print(f"Attached: {filename} ({len(file_data)} bytes)")

    # All recipients for SMTP envelope
    all_recipients = []
    if isinstance(to_addrs, list):
        all_recipients.extend(to_addrs)
    else:
        all_recipients.append(to_addrs)
    if cc_addrs:
        if isinstance(cc_addrs, list):
            all_recipients.extend(cc_addrs)
        else:
            all_recipients.append(cc_addrs)

    # 1. Send via SMTP
    print(f"Connecting to SMTP {SMTP_HOST}:{SMTP_PORT}...")
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(USER, PASS)
        server.send_message(msg, from_addr=USER, to_addrs=all_recipients)
    print(f"[SUCCESS] Email sent via SMTP to: {all_recipients}")

    # 2. Append to IMAP Sent
    try:
        print(f"Connecting to IMAP {IMAP_HOST}:{IMAP_PORT}...")
        imap = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
        imap.login(USER, PASS)
        
        # Check folder names
        typ, folders = imap.list()
        sent_folder = "Sent"
        for f in folders:
            f_str = f.decode('utf-8', errors='ignore')
            if 'sent' in f_str.lower():
                # Extract exact folder name
                parts = f_str.split(' "/" ')
                if len(parts) == 2:
                    sent_folder = parts[1].strip('"')
                    break

        print(f"Appending to IMAP folder: {sent_folder}...")
        raw_msg = msg.as_bytes()
        res = imap.append(sent_folder, '\\Seen', imaplib.Time2Internaldate(time.time()), raw_msg)
        imap.logout()
        print(f"[SUCCESS] Appended to IMAP Sent: {res}")
    except Exception as e:
        print(f"[WARNING] Could not append to IMAP Sent: {e}")

if __name__ == "__main__":
    base_dir = r"c:\Users\vikto\Disk Google\Radixal\Zakázky\2026_026 Hera Space Probe Code Contest\navrhy"
    
    # -------------------------------------------------------------
    # 1. Email: JUDr. Václav Kobera (MD ČR)
    # -------------------------------------------------------------
    kobera_to = "vaclav.kobera@mdcr.cz"
    kobera_subj = "Iniciativa pro misi ESA Hera (R-DAS) – technologický briefing a synergie pro Českou cestu do vesmíru"
    kobera_pdf = os.path.join(base_dir, "R-DAS_Hera_Executive_Brief_CZ_Draft.pdf")
    
    kobera_html = """<!DOCTYPE html>
<html>
<body style="font-family: Georgia, serif; font-size: 11pt; line-height: 1.6; color: #333333;">
<p>Vážený pane řediteli,</p>

<p>dovoluji si vás v návaznosti na národní iniciativu Česká cesta do vesmíru a účast České republiky v programech Evropské vesmírné agentury (ESA) v krátkosti informovat o technologické iniciativě naší brněnské společnosti radixal s.r.o.</p>

<p>V rámci aktuální otevřené výzvy ESA OSIP (<i>Call for Ideas: Autonomous Software Experiments on Hera</i>) podáváme ucelenou sadu 6 inženýrských návrhů R-DAS (<i>Radixal Deep-Space Autonomy Suite</i>). Náš experimentální software v jazyce C je navržen pro běh v hlubokém vesmíru na palubním počítači GR712RC (LEON3 @ 50 MHz) sondy ESA Hera během její rozšířené mise u binárního asteroidu Didymos v srpnu 2027.</p>

<p>Rád bych vyzdvihl klíčové strategické a národní aspekty našeho řešení:</p>
<ol style="padding-left: 20px;">
  <li><strong>Přímá vědecká synergie s Astronomickým ústavem AV ČR v Ondřejově (Dr. Petr Pravec)</strong> v oblasti palubní fotometrie a sledování periody Dimorphosu.</li>
  <li><strong>In-flight demonstrátor a technologická příprava (TRL 8)</strong> autonomní navigace a 3D modelování pro chystanou misi ESA Ramses k asteroidu Apophis v roce 2029.</li>
  <li><strong>Kontinuita ověřeného průmyslového vývoje</strong> – navazujeme na naše zkušenosti z vývoje safety-critical systémů (AK Signal / SIL) a zpracování vlnkových dat z programu ESA Copernicus Sentinel-2 pro společnost Spacemetric.</li>
</ol>

<p>V této fázi nežádáme o žádné národní dofinancování – veškerý vývoj a validaci v QEMU simulátoru realizujeme z vlastních kapacit radixal s.r.o. Velmi bychom však ocenili diplomatické povědomí a institucionální podporu české delegace v programových výborech ESA a případné zařazení této iniciativy pod hlavičku národního programu Česká cesta do vesmíru.</p>

<p>V příloze vám pro informaci postupuji stručný 1stránkový pracovní koncept (<i>Executive Brief</i>) shrnující všech 6 navrhovaných modulů a inženýrské rozpočty.</p>

<p>Rádi vám projekt v krátkosti (15–20 minut) představíme osobně v Praze či online. Kdy by se vám v nadcházejících dnech hodil krátký hovor?</p>

<p>S úctou a přáním mnoha úspěchů v rozvoji českých kosmických aktivit,</p>

<p><strong>Bc. Viktor Lošťák</strong><br/>
Principal Investigator & Lead Architect<br/>
radixal s.r.o. | Purkyňova 649/127, 612 00 Brno<br/>
Tel: +420 604 761 154 | E-mail: viktor.lostak@radixal.net | Web: <a href="https://radixal.net" style="color: #0066CC;">https://radixal.net</a><br/>
Otevřený repozitář: <a href="https://github.com/radixal-sro/rdas-hera" style="color: #0066CC;">https://github.com/radixal-sro/rdas-hera</a></p>
</body>
</html>"""

    kobera_plain = """Vážený pane řediteli,

dovoluji si vás v návaznosti na národní iniciativu Česká cesta do vesmíru a účast České republiky v programech Evropské vesmírné agentury (ESA) v krátkosti informovat o technologické iniciativě naší brněnské společnosti radixal s.r.o.

V rámci aktuální otevřené výzvy ESA OSIP (Call for Ideas: Autonomous Software Experiments on Hera) podáváme ucelenou sadu 6 inženýrských návrhů R-DAS (Radixal Deep-Space Autonomy Suite). Náš experimentální software v jazyce C je navržen pro běh v hlubokém vesmíru na palubním počítači GR712RC (LEON3 @ 50 MHz) sondy ESA Hera během její rozšířené mise u binárního asteroidu Didymos v srpnu 2027.

Rád bych vyzdvihl klíčové strategické a národní aspekty našeho řešení:
1. Přímá vědecká synergie s Astronomickým ústavem AV ČR v Ondřejově (Dr. Petr Pravec) v oblasti palubní fotometrie a sledování periody Dimorphosu.
2. In-flight demonstrátor a technologická příprava (TRL 8) autonomní navigace a 3D modelování pro chystanou misi ESA Ramses k asteroidu Apophis v roce 2029.
3. Kontinuita ověřeného průmyslového vývoje – navazujeme na naše zkušenosti z vývoje safety-critical systémů (AK Signal / SIL) a zpracování vlnkových dat z programu ESA Copernicus Sentinel-2 pro společnost Spacemetric.

V této fázi nežádáme o žádné národní dofinancování – veškerý vývoj a validaci v QEMU simulátoru realizujeme z vlastních kapacit radixal s.r.o. Velmi bychom však ocenili diplomatické povědomí a institucionální podporu české delegace v programových výborech ESA a případné zařazení této iniciativy pod hlavičku národního programu Česká cesta do vesmíru.

V příloze vám pro informaci postupuji stručný 1stránkový pracovní koncept (Executive Brief) shrnující všech 6 navrhovaných modulů a inženýrské rozpočty.

Rádi vám projekt v krátkosti (15–20 minut) představíme osobně v Praze či online. Kdy by se vám v nadcházejících dnech hodil krátký hovor?

S úctou a přáním mnoha úspěchů v rozvoji českých kosmických aktivit,

Bc. Viktor Lošťák
Principal Investigator & Lead Architect
radixal s.r.o. | Purkyňova 649/127, 612 00 Brno
Tel: +420 604 761 154 | E-mail: viktor.lostak@radixal.net | Web: https://radixal.net
Otevřený repozitář: https://github.com/radixal-sro/rdas-hera"""

    print("\n=======================================================")
    print("SENDING EMAIL 1: JUDr. Václav Kobera (MD ČR)")
    print("=======================================================")
    send_and_save_email(kobera_to, CC_LIST, kobera_subj, kobera_html, kobera_plain, kobera_pdf)

    # -------------------------------------------------------------
    # 2. Email: Jorge López Trescastro (ESA / ESTEC)
    # -------------------------------------------------------------
    jorge_to = "jorge.lopez.trescastro@esa.int"
    jorge_subj = "ESA OSIP Hera Call for Ideas – R-DAS Suite: Technical Interface Alignment & Working Brief"
    jorge_pdf = os.path.join(base_dir, "R-DAS_Hera_Executive_Brief_EN_Draft.pdf")
    
    jorge_html = """<!DOCTYPE html>
<html>
<body style="font-family: Georgia, serif; font-size: 11pt; line-height: 1.6; color: #333333;">
<p>Dear Mr. López Trescastro,</p>

<p>I am reaching out regarding the open ESA OSIP Call for Ideas for Autonomous Software Experiments on the Hera mission.</p>

<p>At radixal s.r.o. (Brno, Czech Republic), we have finalized the architectural definition and QEMU SPARC V8 benchmarking of a comprehensive software suite (R-DAS) tailored specifically for the Core 1 bare-metal execution environment on the GR712RC processor.</p>

<p>Having closely followed your published research and presentations at ADCSS regarding the HERA-IoD initiative and on-board telemetry anomaly detection, we have engineered an integer-quantized Isolation Forest micro-kernel (AEGIS-FDIR) that operationalizes these exact principles within an ultra-low WCET (&lt; 0.15 s @ 50 MHz) and strict zero-malloc constraints.</p>

<p>In addition, our suite covers in-situ 3D landmark triangulation, reversible integer CDF 5/3 wavelet compression (drawing on our engineering heritage with Spacemetric on Sentinel-2 pipelines), and a passive Shadow-Mode GNC benchmarking experiment designed to downlink maneuver recommendations via PUS-20 (APID 0x482) for ground-truth validation against ESOC flight dynamics.</p>

<p>Our objective is to ensure that R-DAS seamlessly executes in-flight with zero friction for the operations team. We would appreciate your confirmation on whether the <strong>64-byte configuration block (at offset 0x40001000)</strong> and telemetry packet structures match your planned Phase 2 Core 1 RTEMS-BareMetal ingestion harness.</p>

<p>Please find attached our 1-page Working Consultation Brief summarizing the engineering budgets (RAM, stack depth, CPU load, and telemetry mapping) across all 6 categories.</p>

<p>We are ready to share our QEMU SPARC V8 test harness and static analysis proofs at your convenience. Would you be available for a brief 15-minute technical alignment call next week?</p>

<p>Best regards,</p>

<p><strong>Bc. Viktor Lostak</strong><br/>
Principal Investigator & Lead Architect<br/>
radixal s.r.o. | Brno, Czech Republic<br/>
Phone: +420 604 761 154 | Email: viktor.lostak@radixal.net | Web: <a href="https://radixal.net" style="color: #0066CC;">https://radixal.net</a><br/>
Open Flight Code Repository: <a href="https://github.com/radixal-sro/rdas-hera" style="color: #0066CC;">https://github.com/radixal-sro/rdas-hera</a></p>
</body>
</html>"""

    jorge_plain = """Dear Mr. López Trescastro,

I am reaching out regarding the open ESA OSIP Call for Ideas for Autonomous Software Experiments on the Hera mission.

At radixal s.r.o. (Brno, Czech Republic), we have finalized the architectural definition and QEMU SPARC V8 benchmarking of a comprehensive software suite (R-DAS) tailored specifically for the Core 1 bare-metal execution environment on the GR712RC processor.

Having closely followed your published research and presentations at ADCSS regarding the HERA-IoD initiative and on-board telemetry anomaly detection, we have engineered an integer-quantized Isolation Forest micro-kernel (AEGIS-FDIR) that operationalizes these exact principles within an ultra-low WCET (< 0.15 s @ 50 MHz) and strict zero-malloc constraints.

In addition, our suite covers in-situ 3D landmark triangulation, reversible integer CDF 5/3 wavelet compression (drawing on our engineering heritage with Spacemetric on Sentinel-2 pipelines), and a passive Shadow-Mode GNC benchmarking experiment designed to downlink maneuver recommendations via PUS-20 (APID 0x482) for ground-truth validation against ESOC flight dynamics.

Our objective is to ensure that R-DAS seamlessly executes in-flight with zero friction for the operations team. We would appreciate your confirmation on whether the 64-byte configuration block (at offset 0x40001000) and telemetry packet structures match your planned Phase 2 Core 1 RTEMS-BareMetal ingestion harness.

Please find attached our 1-page Working Consultation Brief summarizing the engineering budgets (RAM, stack depth, CPU load, and telemetry mapping) across all 6 categories.

We are ready to share our QEMU SPARC V8 test harness and static analysis proofs at your convenience. Would you be available for a brief 15-minute technical alignment call next week?

Best regards,

Bc. Viktor Lostak
Principal Investigator & Lead Architect
radixal s.r.o. | Brno, Czech Republic
Phone: +420 604 761 154 | Email: viktor.lostak@radixal.net | Web: https://radixal.net
Open Flight Code Repository: https://github.com/radixal-sro/rdas-hera"""

    print("\n=======================================================")
    print("SENDING EMAIL 2: Jorge López Trescastro (ESA / ESTEC)")
    print("=======================================================")
    send_and_save_email(jorge_to, CC_LIST, jorge_subj, jorge_html, jorge_plain, jorge_pdf)

    # -------------------------------------------------------------
    # 3. Email: Společníci (Petr Slepička, David Riedl; kopie Monika Berkyová)
    # -------------------------------------------------------------
    partners_to = ["petr.slepicka@radixal.net", "david.riedl@radixal.net"]
    partners_cc = ["monika.berkyova@radixal.net"]
    partners_subj = "Informace pro společníky: Soutěž ESA Hera (R-DAS) – ekonomika, stav a reference"
    
    partners_html = """<!DOCTYPE html>
<html>
<body style="font-family: Georgia, serif; font-size: 11pt; line-height: 1.6; color: #333333;">
<p>Ahoj Davide a Petře (v kopii paní Berkyová),</p>

<p>posílám stručné a věcné shrnutí k výzvě Evropské vesmírné agentury (ESA) pro sondu Hera, do které jsme právě odeslali úvodní podklady:</p>

<p><strong>1. O co věcně a ekonomicky jde:</strong><br/>
I když to mediálně působí jako exotika, z obchodního a procesního hlediska jde o standardní veřejnou soutěž / zakázku ESA (program OSIP). Úspěšné projekty, které postoupí do realizační fáze (Fáze 2 od podzimu 2026 do května 2027), získávají standardní implementační kontrakt s pevnou cenou (Firm Fixed Price) v rozmezí <strong>200 000 až 500 000 EUR</strong>. Financování těchto kontraktů probíhá z české národní obálky v ESA (princip Geo-Return, který má na starosti Ministerstvo dopravy ČR – proto jsme dnes informovali ředitele odboru JUDr. Koberu).</p>

<p><strong>2. Naše aktuální náklady a pracnost:</strong><br/>
Z naší strany je to prakticky hotové bez dalších nákladů. Máme vyvinutý prototyp v C, otestovaný v simulátoru na reálných datech kamery AFC a sepsanou kompletní sadu 6 nabídek pokrývajících všech 6 soutěžních kategorií. Příprava je uzavřená a nevyžaduje v tuto chvíli žádné další interní hodiny ani zatížení vývojového týmu.</p>

<p><strong>3. Komerční přínos a reference (i v případě nevybrání):</strong><br/>
I v případě, že ESA nakonec vybere jiné týmy, je už samotná účast a hotová dokumentace obrovským přínosem:</p>
<ul style="padding-left: 20px;">
  <li>Získáváme ucelené mezinárodní portfolio a špičkovou referenci v oblasti safety-critical systémů a vestavného C kódu, kterou můžeme přímo využívat u dalších veřejných zakázek (např. CENDIS, drážní systémy, obranné technologie i civilní tendry).</li>
  <li>100 % duševního vlastnictví (IPR) i vyvinutých algoritmů zůstává společnosti radixal s.r.o.</li>
</ul>

<p>Pokud byste k tomu chtěli cokoliv probrat nebo doplnit, rád vám detaily ukážu.</p>

<p>Hezký den,</p>

<p><strong>Bc. Viktor Lošťák</strong><br/>
radixal s.r.o.</p>
</body>
</html>"""

    partners_plain = """Ahoj Davide a Petře (v kopii paní Berkyová),

posílám stručné a věcné shrnutí k výzvě Evropské vesmírné agentury (ESA) pro sondu Hera, do které jsme právě odeslali úvodní podklady:

1. O co věcně a ekonomicky jde:
I když to mediálně působí jako exotika, z obchodního a procesního hlediska jde o standardní veřejnou soutěž / zakázku ESA (program OSIP). Úspěšné projekty, které postoupí do realizační fáze (Fáze 2 od podzimu 2026 do května 2027), získávají standardní implementační kontrakt s pevnou cenou (Firm Fixed Price) v rozmezí 200 000 až 500 000 EUR. Financování těchto kontraktů probíhá z české národní obálky v ESA (princip Geo-Return, který má na starosti Ministerstvo dopravy ČR – proto jsme dnes informovali ředitele odboru JUDr. Koberu).

2. Naše aktuální náklady a pracnost:
Z naší strany je to prakticky hotové bez dalších nákladů. Máme vyvinutý prototyp v C, otestovaný v simulátoru na reálných datech kamery AFC a sepsanou kompletní sadu 6 nabídek pokrývajících všech 6 soutěžních kategorií. Příprava je uzavřená a nevyžaduje v tuto chvíli žádné další interní hodiny ani zatížení vývojového týmu.

3. Komerční přínos a reference (i v případě nevybrání):
I v případě, že ESA nakonec vybere jiné týmy, je už samotná účast a hotová dokumentace obrovským přínosem:
• Získáváme ucelené mezinárodní portfolio a špičkovou referenci v oblasti safety-critical systémů a vestavného C kódu, kterou můžeme přímo využívat u dalších veřejných zakázek (např. CENDIS, drážní systémy, obranné technologie i civilní tendry).
• 100 % duševního vlastnictví (IPR) i vyvinutých algoritmů zůstává společnosti radixal s.r.o.

Pokud byste k tomu chtěli cokoliv probrat nebo doplnit, rád vám detaily ukážu.

Hezký den,

Bc. Viktor Lošťák
radixal s.r.o."""

    print("\n=======================================================")
    print("SENDING EMAIL 3: Partners (Petr Slepička, David Riedl, Monika Berkyová)")
    print("=======================================================")
    send_and_save_email(partners_to, partners_cc, partners_subj, partners_html, partners_plain)
    print("\n[ALL 3 EMAILS SUCCESSFULLY SENT AND RECORDED!]")
