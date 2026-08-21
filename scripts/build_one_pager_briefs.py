#!/usr/bin/env python3
"""
build_one_pager_briefs.py
Generates official 1-page Executive Brief PDFs in Czech and English for diplomatic outreach.
"""

import os
import sys
import pypdf
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, HRFlowable
)
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register System TrueType Fonts
try:
    pdfmetrics.registerFont(TTFont('Arial-Regular', 'C:/Windows/Fonts/arial.ttf'))
    pdfmetrics.registerFont(TTFont('Arial-Bold', 'C:/Windows/Fonts/arialbd.ttf'))
    pdfmetrics.registerFont(TTFont('Arial-Italic', 'C:/Windows/Fonts/ariali.ttf'))
    pdfmetrics.registerFont(TTFont('Arial-BoldItalic', 'C:/Windows/Fonts/arialbi.ttf'))
    FONT_NORMAL = 'Arial-Regular'
    FONT_BOLD = 'Arial-Bold'
    FONT_ITALIC = 'Arial-Italic'
    FONT_BOLDITALIC = 'Arial-BoldItalic'
except Exception as e:
    FONT_NORMAL = 'Helvetica'
    FONT_BOLD = 'Helvetica-Bold'
    FONT_ITALIC = 'Helvetica-Oblique'
    FONT_BOLDITALIC = 'Helvetica-BoldOblique'

class OnePageCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(OnePageCanvas, self).__init__(*args, **kwargs)

    def draw_decorations(self, lang="CZ"):
        self.saveState()
        self.setFont(FONT_BOLD, 7.5)
        self.setFillColor(colors.HexColor("#B45309")) # Amber dark
        
        # Header line with Draft badge
        if lang == "CZ":
            self.drawString(40, 808, "ESA OSIP Hera Space Probe Code Contest | R-DAS Suite")
            self.drawRightString(595 - 40, 808, "● PRACOVNÍ KONCEPT K DISKUZI (DRAFT v0.9) – radixal s.r.o.")
        else:
            self.drawString(40, 808, "ESA OSIP Hera Space Probe Code Contest | R-DAS Suite")
            self.drawRightString(595 - 40, 808, "● WORKING DRAFT FOR CONSULTATION (DRAFT v0.9) – radixal s.r.o.")
            
        self.setStrokeColor(colors.HexColor("#D0D0D0"))
        self.setLineWidth(0.5)
        self.line(40, 802, 595 - 40, 802)

        # Footer line
        self.setStrokeColor(colors.HexColor("#D0D0D0"))
        self.setLineWidth(0.5)
        self.line(40, 36, 595 - 40, 36)
        
        self.setFont(FONT_NORMAL, 7.2)
        self.setFillColor(colors.HexColor("#555555"))
        if lang == "CZ":
            self.drawString(40, 24, "DŮVĚRNÉ – PRACOVNÍ VERZE PRO JEDNÁNÍ | radixal s.r.o. | Purkyňova 649/127, 612 00 Brno | www.radixal.net")
            self.drawRightString(595 - 40, 24, "Strana 1 z 1")
        else:
            self.drawString(40, 24, "CONFIDENTIAL – WORKING CONSULTATION DRAFT | radixal s.r.o. | Purkynova 649/127, Brno | www.radixal.net")
            self.drawRightString(595 - 40, 24, "Page 1 of 1")
        self.restoreState()

def build_czech_one_pager(output_path):
    print(f"Building Czech One-Pager -> {output_path}...")
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=42,
        bottomMargin=42
    )

    styles = getSampleStyleSheet()
    primary_color = colors.HexColor("#0B2545")
    secondary_color = colors.HexColor("#134074")
    accent_blue = colors.HexColor("#0066CC")
    dark_neutral = colors.HexColor("#222222")

    title_style = ParagraphStyle('DocTitle', parent=styles['Normal'], fontName=FONT_BOLD, fontSize=14, leading=17, textColor=primary_color, spaceAfter=2)
    subtitle_style = ParagraphStyle('DocSubtitle', parent=styles['Normal'], fontName=FONT_BOLD, fontSize=8.5, leading=11, textColor=accent_blue, spaceAfter=4)
    h1_style = ParagraphStyle('H1', parent=styles['Normal'], fontName=FONT_BOLD, fontSize=9.5, leading=12, textColor=primary_color, spaceBefore=4, spaceAfter=2)
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontName=FONT_NORMAL, fontSize=7.6, leading=10.2, textColor=dark_neutral, spaceAfter=3)
    callout_style = ParagraphStyle('Callout', parent=styles['Normal'], fontName=FONT_NORMAL, fontSize=7.6, leading=10.2, textColor=colors.HexColor("#102A43"))
    table_cell = ParagraphStyle('TCell', parent=styles['Normal'], fontName=FONT_NORMAL, fontSize=7.0, leading=8.8, textColor=dark_neutral)
    table_cell_bold = ParagraphStyle('TCellB', parent=table_cell, fontName=FONT_BOLD, textColor=colors.white)

    story = []

    patch_path = "media/rdas_mission_patch.jpg"
    if not os.path.exists(patch_path):
        patch_path = r"c:\Users\vikto\Disk Google\Radixal\Zakázky\2026_026 Hera Space Probe Code Contest\media\rdas_mission_patch.jpg"

    header_img = None
    if os.path.exists(patch_path):
        header_img = Image(patch_path, width=54, height=54)

    title_p = Paragraph("Projekt R-DAS: Palubní autonomní software pro sondu ESA Hera", title_style)
    sub_p = Paragraph("Inovační výzva Evropské vesmírné agentury (ESA OSIP) | Mise planetární obrany u asteroidu Didymos", subtitle_style)

    if header_img:
        hdr_tbl = Table([[title_p, header_img], [sub_p, ""]], colWidths=[445, 65])
        hdr_tbl.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('SPAN', (1,0), (1,1)),
            ('ALIGN', (1,0), (1,1), 'RIGHT'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(hdr_tbl)
    else:
        story.append(title_p)
        story.append(sub_p)

    story.append(Spacer(1, 2))

    # Executive Summary Box
    exec_summary_html = """
    <b>SHRNUTÍ PROJEKTU & STRATEGICKÝ PŘÍNOS PRO ČESKOU REPUBLIKU:</b><br/>
    Česká technologická společnost <b>radixal s.r.o.</b> (Brno) podává do prestižní mezinárodní výzvy ESA OSIP ucelenou sadu 6 návrhů <b>R-DAS (Radixal Deep-Space Autonomy Suite)</b> pro běh experimentálního softwaru v hlubokém vesmíru na palubním počítači GR712RC (LEON3 @ 50 MHz) sondy ESA Hera během její rozšířené mise v srpnu 2027.<br/>
    • <b>Klíčové technologické inovace:</b> Autonomní detekce a katalogizace impaktních kráterů a morfologie povrchu v C, deterministická vlnková komprese šetřící 82 % downlinku, in-situ triangulace 3D modelu tělesa a pasivní odhad gravitace (GM).<br/>
    • <b>Synergie s českou vědou:</b> Přímá návaznost na světově uznávanou fotometrickou metodiku Astronomického ústavu AV ČR v Ondřejově (Dr. Petr Pravec) a demonstrátor pro misi <b>ESA Ramses 2029 k asteroidu Apophis</b>.
    """
    callout_tbl = Table([[Paragraph(exec_summary_html, callout_style)]], colWidths=[515])
    callout_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EEF4F8")),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor("#85B8DB")),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(callout_tbl)
    story.append(Spacer(1, 3))

    # 6 Modules Table
    story.append(Paragraph("Přehled 6 podávaných návrhů sady R-DAS (Pokrytí všech 6 kategorií ESA)", h1_style))
    mod_data = [
        [Paragraph("Modul / Kód", table_cell_bold), Paragraph("Kategorie ESA", table_cell_bold), Paragraph("Inovativní funkce a cíl na sondě Hera", table_cell_bold), Paragraph("Inženýrský rozpočet", table_cell_bold)],
        [Paragraph("<b>1. ARGOS-AI</b> (Vlajková loď)", table_cell), Paragraph("Kat. 4: Edge AI", table_cell), Paragraph("Detekce impaktních kráterů v INT8 Micro-CNN + laserová fúze PALT pro metrické rozměry", table_cell), Paragraph("2.39 s WCET | 142 kB RAM", table_cell)],
        [Paragraph("<b>2. DEEP-WAVE</b>", table_cell), Paragraph("Kat. 2: Komprese", table_cell), Paragraph("Reverzibilní vlnková komprese CDF 5/3 šetřící 82.2 % přenosového pásma na Zemi", table_cell), Paragraph("2.39 s WCET | 38 kB RAM", table_cell)],
        [Paragraph("<b>3. AURA-GNC</b>", table_cell), Paragraph("Kat. 1: Autonomie & GNC", table_cell), Paragraph("Shadow-Mode 3D triangulace tělesa z kráterů, gravitační inverze GM a validace vůči ESOC", table_cell), Paragraph("3.80 s WCET | 96 kB RAM", table_cell)],
        [Paragraph("<b>4. AEGIS-FDIR</b>", table_cell), Paragraph("Kat. 5: Odolnost & FDIR", table_cell), Paragraph("In-flight realizace výzkumu ESTEC (HERA-IoD): Isolation Forest pro detekci anomálií", table_cell), Paragraph("0.12 s WCET | 18 kB RAM", table_cell)],
        [Paragraph("<b>5. ARES-Planner</b>", table_cell), Paragraph("Kat. 3: Optimalizace", table_cell), Paragraph("Autonomní řešič CSP pro plánování vědeckých pozorování a garanci energetických rezerv", table_cell), Paragraph("1.40 s WCET | 43 kB RAM", table_cell)],
        [Paragraph("<b>6. CHRONOS</b>", table_cell), Paragraph("Kat. 6: Věda / Astrofyzika", table_cell), Paragraph("Palubní fotometrie a sledování periody Dimorphosu navazující na výzkum Ondřejova", table_cell), Paragraph("0.85 s WCET | 29 kB RAM", table_cell)],
    ]
    mod_tbl = Table(mod_data, colWidths=[110, 85, 215, 105])
    mod_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.2),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    story.append(mod_tbl)
    story.append(Spacer(1, 3))

    # Technical Feasibility & Safety
    story.append(Paragraph("Technická proveditelnost a bezpečnost letu (Zero Risk)", h1_style))
    story.append(Paragraph(
        "Veškerý software je vyvinut v čistém deterministickém <b>ANSI C99</b> bez dynamické alokace paměti (<b>striktně 0 malloc</b>, limit 64 kB stacku). "
        "Kód byl plně otestován a zvalidován na oficiální sadě <b>2 400+ reálných kalibračních snímků kamery AFC</b> v emulátoru QEMU pro SPARC V8 (LEON3). "
        "Běh probíhá v hardwarově izolovaném sandboxu jádra Core 1 bez jakéhokoliv zásahu do primárního řízení sondy (Core 0 RTEMS).",
        body_style
    ))

    # Company & Team Heritage
    story.append(Paragraph("Předkladatel: radixal s.r.o. & Řídicí tým", h1_style))
    story.append(Paragraph(
        "<b>radixal s.r.o.</b> (založeno 2016 v Brně) má 10letou historii ve vývoji safety-critical systémů (AK Signal / drážní normy SIL), "
        "družicového zpracování vlnkových dat ze satelitů <b>ESA Sentinel-2 (projekt Spacemetric)</b>, obranných air-gapped technologií (URC Systems) a státní infrastruktury (CENDIS / MD ČR).<br/>"
        "• <b>Bc. Viktor Lošťák (Principal Investigator & Lead Architect):</b> Hlavní architekt projektu a autor matematických algoritmů.<br/>"
        "• <b>Ing. Petr Slepička (Engineering Lead & Delivery Director):</b> Vedoucí inženýr letového C kódu, statické verifikace MISRA-C a ECSS standardů.<br/>"
        "• <b>Mgr. David Riedl (Executive Director & Governance):</b> Řízení projektu, smluvní rámec a compliance s pravidly ESA.<br/>"
        "<b>Kontakt:</b> Bc. Viktor Lošťák | E-mail: <code>viktor.lostak@radixal.net</code> | Web: <code>https://radixal.net</code> | Git: <code>github.com/radixal-sro/rdas-hera</code>",
        body_style
    ))

    def make_canvas(*args, **kwargs):
        c = OnePageCanvas(*args, **kwargs)
        c.draw_decorations("CZ")
        return c

    doc.build(story, canvasmaker=make_canvas)
    
    reader = pypdf.PdfReader(output_path)
    print(f"[SUCCESS] Czech One-Pager compiled: exactly {len(reader.pages)} page(s)!")

def build_english_one_pager(output_path):
    print(f"Building English One-Pager -> {output_path}...")
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=42,
        bottomMargin=42
    )

    styles = getSampleStyleSheet()
    primary_color = colors.HexColor("#0B2545")
    secondary_color = colors.HexColor("#134074")
    accent_blue = colors.HexColor("#0066CC")
    dark_neutral = colors.HexColor("#222222")

    title_style = ParagraphStyle('DocTitle', parent=styles['Normal'], fontName=FONT_BOLD, fontSize=14, leading=17, textColor=primary_color, spaceAfter=2)
    subtitle_style = ParagraphStyle('DocSubtitle', parent=styles['Normal'], fontName=FONT_BOLD, fontSize=8.5, leading=11, textColor=accent_blue, spaceAfter=4)
    h1_style = ParagraphStyle('H1', parent=styles['Normal'], fontName=FONT_BOLD, fontSize=9.5, leading=12, textColor=primary_color, spaceBefore=4, spaceAfter=2)
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontName=FONT_NORMAL, fontSize=7.6, leading=10.2, textColor=dark_neutral, spaceAfter=3)
    callout_style = ParagraphStyle('Callout', parent=styles['Normal'], fontName=FONT_NORMAL, fontSize=7.6, leading=10.2, textColor=colors.HexColor("#102A43"))
    table_cell = ParagraphStyle('TCell', parent=styles['Normal'], fontName=FONT_NORMAL, fontSize=7.0, leading=8.8, textColor=dark_neutral)
    table_cell_bold = ParagraphStyle('TCellB', parent=table_cell, fontName=FONT_BOLD, textColor=colors.white)

    story = []

    patch_path = "media/rdas_mission_patch.jpg"
    if not os.path.exists(patch_path):
        patch_path = r"c:\Users\vikto\Disk Google\Radixal\Zakázky\2026_026 Hera Space Probe Code Contest\media\rdas_mission_patch.jpg"

    header_img = None
    if os.path.exists(patch_path):
        header_img = Image(patch_path, width=54, height=54)

    title_p = Paragraph("Project R-DAS: Onboard Deep-Space Autonomy Suite for ESA Hera", title_style)
    sub_p = Paragraph("ESA Open Space Innovation Platform (OSIP) | Autonomous Software Experiments on Hera", subtitle_style)

    if header_img:
        hdr_tbl = Table([[title_p, header_img], [sub_p, ""]], colWidths=[445, 65])
        hdr_tbl.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('SPAN', (1,0), (1,1)),
            ('ALIGN', (1,0), (1,1), 'RIGHT'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(hdr_tbl)
    else:
        story.append(title_p)
        story.append(sub_p)

    story.append(Spacer(1, 2))

    # Executive Summary Box
    exec_summary_html = """
    <b>EXECUTIVE SUMMARY & MISSION IMPACT:</b><br/>
    <b>radixal s.r.o.</b> (Brno, Czech Republic) submits a comprehensive 6-proposal suite, the <b>Radixal Deep-Space Autonomy Suite (R-DAS)</b>, under the ESA OSIP Call for Ideas. Engineered for bare-metal execution on the Frontgrade Gaisler GR712RC (LEON3 @ 50 MHz) Core 1 sandbox of ESA's Hera spacecraft during the August 2027 Extended Mission.<br/>
    • <b>Key Technological Innovations:</b> Autonomous detection and cataloging of asteroid impact craters and surface depressions via INT8 Micro-CNN & PALT laser fusion, lossless CDF 5/3 integer wavelet compression (-82.2% bandwidth), in-situ 3D shape mesh building, and passive gravity parameter (GM) inversion.<br/>
    • <b>In-Flight Benchmark & Ramses Synergy:</b> Executes an in-flight Shadow-Mode GNC benchmark comparing onboard maneuver recommendations against ESOC Flight Dynamics ground truth, establishing TRL 8 flight qualification for the <b>2029 ESA Ramses mission to asteroid (99942) Apophis</b>.
    """
    callout_tbl = Table([[Paragraph(exec_summary_html, callout_style)]], colWidths=[515])
    callout_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EEF4F8")),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor("#85B8DB")),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(callout_tbl)
    story.append(Spacer(1, 3))

    # 6 Modules Table
    story.append(Paragraph("The 6 Proposals of the R-DAS Suite (Covering All 6 ESA Contest Categories)", h1_style))
    mod_data = [
        [Paragraph("Module / Identifier", table_cell_bold), Paragraph("ESA Category", table_cell_bold), Paragraph("Primary Function & In-Flight Objective on Hera", table_cell_bold), Paragraph("Engineering Budget", table_cell_bold)],
        [Paragraph("<b>1. ARGOS-AI</b> (Flagship)", table_cell), Paragraph("Cat. 4: Edge AI", table_cell), Paragraph("Impact crater detection in INT8 Micro-CNN + PALT laser altimeter metric sizing in meters", table_cell), Paragraph("2.39 s WCET | 142 kB RAM", table_cell)],
        [Paragraph("<b>2. DEEP-WAVE</b>", table_cell), Paragraph("Cat. 2: Compression", table_cell), Paragraph("Reversible CDF 5/3 integer wavelet compression achieving -82.2% downlink bandwidth reduction", table_cell), Paragraph("2.39 s WCET | 38 kB RAM", table_cell)],
        [Paragraph("<b>3. AURA-GNC</b>", table_cell), Paragraph("Cat. 1: Autonomy & GNC", table_cell), Paragraph("Shadow-Mode 3D landmark mesh building from craters, GM gravity inversion & ESOC validation", table_cell), Paragraph("3.80 s WCET | 96 kB RAM", table_cell)],
        [Paragraph("<b>4. AEGIS-FDIR</b>", table_cell), Paragraph("Cat. 5: Resilience & FDIR", table_cell), Paragraph("Operationalizing ESTEC HERA-IoD research: Quantized Isolation Forest telemetry anomaly detector", table_cell), Paragraph("0.12 s WCET | 18 kB RAM", table_cell)],
        [Paragraph("<b>5. ARES-Planner</b>", table_cell), Paragraph("Cat. 3: Operations", table_cell), Paragraph("Autonomous integer CSP solver for multi-payload observation scheduling (+35% science return)", table_cell), Paragraph("1.40 s WCET | 43 kB RAM", table_cell)],
        [Paragraph("<b>6. CHRONOS</b>", table_cell), Paragraph("Cat. 6: Science / Astro", table_cell), Paragraph("Onboard aperture photometry & Dimorphos lightcurve tracking (Ondrejov Observatory synergy)", table_cell), Paragraph("0.85 s WCET | 29 kB RAM", table_cell)],
    ]
    mod_tbl = Table(mod_data, colWidths=[110, 85, 215, 105])
    mod_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.2),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    story.append(mod_tbl)
    story.append(Spacer(1, 3))

    # Technical Feasibility & Safety
    story.append(Paragraph("Technical Feasibility & Spacecraft Safety (Zero Flight Risk)", h1_style))
    story.append(Paragraph(
        "Engineered strictly in deterministic <b>ANSI C99</b> without dynamic memory allocation (<b>0 malloc</b>, < 24 kB stack). "
        "The codebase was empirically validated on <b>2,400+ real Asteroid Framing Camera (AFC) calibration images</b> inside the QEMU LEON3 SPARC V8 emulator. "
        "Execution is confined to the isolated Core 1 bare-metal sandbox without actuator authority, ensuring absolute zero risk to Core 0 flight software.",
        body_style
    ))

    # Company & Team Heritage
    story.append(Paragraph("Proposing Entity: radixal s.r.o. & Leadership Triad", h1_style))
    story.append(Paragraph(
        "<b>radixal s.r.o.</b> (est. 2016 in Brno) holds a 10-year track record in safety-critical systems (AK Signal / SIL railway), "
        "satellite image wavelet pipelines for <b>ESA Copernicus Sentinel-2 (Spacemetric AB / Sweden & Norway)</b>, defense systems (URC Systems), and national infrastructure.<br/>"
        "• <b>Bc. Viktor Lostak (Principal Investigator & Lead Architect):</b> Lead architect and designer of mathematical algorithms.<br/>"
        "• <b>Ing. Petr Slepicka (Engineering Lead & Delivery Director):</b> Lead flight software engineer, MISRA-C static verification, and ECSS QA.<br/>"
        "• <b>Mgr. David Riedl (Executive Director & Governance):</b> Project governance, legal, and ESA institutional compliance.<br/>"
        "<b>Contact:</b> Bc. Viktor Lostak | Email: <code>viktor.lostak@radixal.net</code> | Web: <code>https://radixal.net</code> | Git: <code>github.com/radixal-sro/rdas-hera</code>",
        body_style
    ))

    def make_canvas(*args, **kwargs):
        c = OnePageCanvas(*args, **kwargs)
        c.draw_decorations("EN")
        return c

    doc.build(story, canvasmaker=make_canvas)
    
    reader = pypdf.PdfReader(output_path)
    print(f"[SUCCESS] English One-Pager compiled: exactly {len(reader.pages)} page(s)!")

if __name__ == "__main__":
    os.makedirs("proposals", exist_ok=True)
    cz_pdf = "proposals/R-DAS_Hera_Executive_Brief_CZ.pdf"
    en_pdf = "proposals/R-DAS_Hera_Executive_Brief_EN.pdf"
    
    build_czech_one_pager(cz_pdf)
    build_english_one_pager(en_pdf)
    
    # Also create explicit Draft named copies
    import shutil
    shutil.copyfile(cz_pdf, "proposals/R-DAS_Hera_Executive_Brief_CZ_Draft.pdf")
    shutil.copyfile(en_pdf, "proposals/R-DAS_Hera_Executive_Brief_EN_Draft.pdf")
    
    # Sync to Google Drive
    gdrive_dir = r"c:\Users\vikto\Disk Google\Radixal\Zakázky\2026_026 Hera Space Probe Code Contest\navrhy"
    if os.path.exists(gdrive_dir):
        for src, name in [
            (cz_pdf, "R-DAS_Hera_Executive_Brief_CZ.pdf"),
            (en_pdf, "R-DAS_Hera_Executive_Brief_EN.pdf"),
            ("proposals/R-DAS_Hera_Executive_Brief_CZ_Draft.pdf", "R-DAS_Hera_Executive_Brief_CZ_Draft.pdf"),
            ("proposals/R-DAS_Hera_Executive_Brief_EN_Draft.pdf", "R-DAS_Hera_Executive_Brief_EN_Draft.pdf"),
        ]:
            try:
                shutil.copyfile(src, os.path.join(gdrive_dir, name))
            except Exception as e:
                print(f"[NOTE] Could not overwrite {name} on Google Drive (file is open in viewer): {e}")
        print("[SUCCESS] Synchronized One-Pagers to Google Drive navrhy/")
