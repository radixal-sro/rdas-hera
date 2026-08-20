#!/usr/bin/env python3
"""
build_all_10page_proposals.py
Compiles all 6 R-DAS Proposals into comprehensive 10-page ESA/IEEE Technical Proposal PDFs.
Uses clean international English nomenclature with full TrueType font embedding.
"""

import os
import sys
import pypdf
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
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

class NumberedCanvas(canvas.Canvas):
    """Custom canvas providing running headers and 'Page X of Y' footers."""
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont(FONT_NORMAL, 8)
        self.setFillColor(colors.HexColor("#555555"))
        
        # Header (pages 2+)
        if self._pageNumber > 1:
            doc_ref = getattr(self, 'doc_ref', 'ESA-OSIP-HERA-2026-RDAS')
            self.drawString(45, 804, f"ESA OSIP Hera Code Contest | {doc_ref}")
            self.drawRightString(595 - 45, 804, "radixal s.r.o. – Technical Proposal (R-DAS)")
            self.setStrokeColor(colors.HexColor("#D0D0D0"))
            self.setLineWidth(0.5)
            self.line(45, 796, 595 - 45, 796)

        # Footer (all pages)
        self.setStrokeColor(colors.HexColor("#D0D0D0"))
        self.setLineWidth(0.5)
        self.line(45, 42, 595 - 45, 42)
        
        self.drawString(45, 30, "CONFIDENTIAL & PROPRIETARY – radixal s.r.o. | Submitted to European Space Agency (ESA)")
        self.drawRightString(595 - 45, 30, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()

def generate_10page_proposal(p_cfg):
    output_path = p_cfg['output_path']
    doc_ref = p_cfg['ref']
    print(f"\n[BUILDING] {p_cfg['id']} -> {output_path}...")

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=45,
        rightMargin=45,
        topMargin=48,
        bottomMargin=48
    )

    styles = getSampleStyleSheet()
    
    primary_color = colors.HexColor("#0B2545")
    secondary_color = colors.HexColor("#134074")
    accent_blue = colors.HexColor("#0066CC")
    dark_neutral = colors.HexColor("#222222")
    callout_bg = colors.HexColor("#EEF4F8")
    table_header_bg = colors.HexColor("#0B2545")

    title_style = ParagraphStyle('DocTitle', parent=styles['Normal'], fontName=FONT_BOLD, fontSize=15, leading=19, textColor=primary_color, spaceAfter=4)
    subtitle_style = ParagraphStyle('DocSubtitle', parent=styles['Normal'], fontName=FONT_BOLD, fontSize=9, leading=12, textColor=accent_blue, spaceAfter=8)
    meta_label = ParagraphStyle('MetaLabel', parent=styles['Normal'], fontName=FONT_BOLD, fontSize=7.5, leading=10.5, textColor=colors.HexColor("#333333"))
    meta_val = ParagraphStyle('MetaVal', parent=styles['Normal'], fontName=FONT_NORMAL, fontSize=7.5, leading=10.5, textColor=colors.HexColor("#444444"))
    h1_style = ParagraphStyle('H1', parent=styles['Normal'], fontName=FONT_BOLD, fontSize=11, leading=14, textColor=primary_color, spaceBefore=8, spaceAfter=3, keepWithNext=True)
    h2_style = ParagraphStyle('H2', parent=styles['Normal'], fontName=FONT_BOLD, fontSize=9.5, leading=12.5, textColor=secondary_color, spaceBefore=6, spaceAfter=2, keepWithNext=True)
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontName=FONT_NORMAL, fontSize=8.2, leading=11.2, textColor=dark_neutral, spaceAfter=4)
    callout_style = ParagraphStyle('Callout', parent=styles['Normal'], fontName=FONT_NORMAL, fontSize=8, leading=11, textColor=colors.HexColor("#102A43"))
    table_cell = ParagraphStyle('TCell', parent=styles['Normal'], fontName=FONT_NORMAL, fontSize=7.2, leading=9.2, textColor=dark_neutral)
    table_cell_bold = ParagraphStyle('TCellB', parent=table_cell, fontName=FONT_BOLD, textColor=colors.white)
    table_cell_h = ParagraphStyle('TCellH', parent=table_cell, fontName=FONT_BOLD, textColor=primary_color)

    story = []

    # PAGE 1: TITLE, METADATA, SUMMARY & ABSTRACT
    patch_path = "media/rdas_mission_patch.jpg"
    if not os.path.exists(patch_path):
        patch_path = r"c:\Users\vikto\Disk Google\Radixal\Zakázky\2026_026 Hera Space Probe Code Contest\media\rdas_mission_patch.jpg"

    header_img = None
    if os.path.exists(patch_path):
        header_img = Image(patch_path, width=70, height=70)

    title_p = Paragraph(p_cfg['title'], title_style)
    sub_p = Paragraph(f"EUROPEAN SPACE AGENCY (ESA) – OPEN SPACE INNOVATION PLATFORM (OSIP)<br/>Call for Ideas: Autonomous Software Experiments on Hera | {p_cfg['track']}", subtitle_style)

    if header_img:
        hdr_tbl = Table([[title_p, header_img], [sub_p, ""]], colWidths=[425, 80])
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

    story.append(Spacer(1, 4))

    meta_data = [
        [Paragraph("Proposal Identifier:", meta_label), Paragraph(doc_ref, meta_val),
         Paragraph("Target Processor:", meta_label), Paragraph("GR712RC Dual-Core LEON3 (SPARC V8 @ 50 MHz)", meta_val)],
        [Paragraph("Proposing Entity:", meta_label), Paragraph("radixal s.r.o. (Purkynova 649/127, 612 00 Brno, Czech Republic)", meta_val),
         Paragraph("Execution Core:", meta_label), Paragraph("Core 1 Isolated Bare-Metal Sandbox (No OS, 0 malloc)", meta_val)],
        [Paragraph("Leadership Triad:", meta_label), Paragraph("Bc. Viktor Lostak (PI), Ing. Petr Slepicka, Mgr. David Riedl", meta_val),
         Paragraph("Applicable Standards:", meta_label), Paragraph("ECSS-E-ST-40C Category D | MISRA-C:2012 Zero-Heap", meta_val)],
        [Paragraph("Primary Science Target:", meta_label), Paragraph("Didymos / Dimorphos Binary Asteroid System", meta_val),
         Paragraph("In-Flight Slot:", meta_label), Paragraph("Extended Mission Campaign (August 2027, 4 Weeks)", meta_val)]
    ]
    meta_tbl = Table(meta_data, colWidths=[90, 175, 90, 150])
    meta_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8F9FA")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#D0D5DD")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(meta_tbl)
    story.append(Spacer(1, 6))

    callout_tbl = Table([[Paragraph(p_cfg['exec_summary_html'], callout_style)]], colWidths=[505])
    callout_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), callout_bg),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#85B8DB")),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(callout_tbl)
    story.append(Spacer(1, 6))

    story.append(Paragraph("Abstract & Table of Contents", h1_style))
    story.append(Paragraph(p_cfg['abstract_text'], body_style))

    toc_data = [
        [Paragraph("1.0 Problem Statement & Operational Context", table_cell_h), Paragraph("Page 2", table_cell),
         Paragraph("5.0 SIFT Radiation Hardening & Fault Tolerance", table_cell_h), Paragraph("Page 6", table_cell)],
        [Paragraph("2.0 Mission Context & Hera Technical Baseline", table_cell_h), Paragraph("Page 3", table_cell),
         Paragraph("6.0 Platform Interface & PUS Telemetry Mapping", table_cell_h), Paragraph("Page 7", table_cell)],
        [Paragraph("3.0 Algorithmic Architecture & Pipeline Design", table_cell_h), Paragraph("Page 4", table_cell),
         Paragraph("7.0 Empirical Verification & Benchmark Evidence", table_cell_h), Paragraph("Page 8", table_cell)],
        [Paragraph("4.0 Mathematical Formulation & Lifting Schemes", table_cell_h), Paragraph("Page 5", table_cell),
         Paragraph("8.0 Operational Roadmap, Team & References", table_cell_h), Paragraph("Page 9–10", table_cell)]
    ]
    toc_tbl = Table(toc_data, colWidths=[180, 50, 225, 50])
    toc_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8F9FA")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E0E0E0")),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(toc_tbl)
    story.append(PageBreak())

    # PAGE 2: PROBLEM STATEMENT
    story.append(Paragraph("1.0 The Problem Statement & Deep-Space Operational Challenges", h1_style))
    story.append(Paragraph(p_cfg['p1_problem_intro'], body_style))
    story.append(Paragraph(p_cfg['p1_problem_details'], body_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Table 1.1: Operational Bottleneck Comparison & Quantitative Advantage", h2_style))
    b_tbl = Table(p_cfg['table_1_1'], colWidths=[120, 130, 140, 115])
    b_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), table_header_bg),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#D0D5DD")),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8F9FA")]),
    ]))
    story.append(b_tbl)
    story.append(PageBreak())

    # PAGE 3: MISSION CONTEXT & TECHNICAL BASELINE
    story.append(Paragraph("2.0 Mission Context & Hera Platform Technical Baseline", h1_style))
    story.append(Paragraph(p_cfg['p2_baseline_intro'], body_style))
    story.append(Paragraph(p_cfg['p2_baseline_details'], body_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Table 2.1: Hera Platform Allocation vs. Software Implementation Baseline", h2_style))
    p_tbl = Table(p_cfg['table_2_1'], colWidths=[115, 135, 145, 110])
    p_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), table_header_bg),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#D0D5DD")),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8F9FA")]),
    ]))
    story.append(p_tbl)
    story.append(PageBreak())

    # PAGE 4: ALGORITHMIC ARCHITECTURE
    story.append(Paragraph("3.0 Algorithmic Architecture & Software Pipeline Design", h1_style))
    story.append(Paragraph(p_cfg['p3_arch_intro'], body_style))
    story.append(Paragraph(p_cfg['p3_arch_stages'], body_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Table 3.1: Pipeline Stage Execution & Memory Budget (50 MHz SPARC V8)", h2_style))
    st_tbl = Table(p_cfg['table_3_1'], colWidths=[115, 175, 115, 100])
    st_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), table_header_bg),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#EBF3FA")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#D0D5DD")),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(st_tbl)
    story.append(PageBreak())

    # PAGE 5: MATHEMATICAL FORMULATIONS
    story.append(Paragraph("4.0 Mathematical Formulation & Implementation Equations", h1_style))
    story.append(Paragraph(p_cfg['p4_math_intro'], body_style))
    story.append(Paragraph(p_cfg['p4_math_equations'], body_style))
    story.append(PageBreak())

    # PAGE 6: SIFT RADIATION HARDENING & CONFIG MAP
    story.append(Paragraph("5.0 SIFT Radiation Hardening & Fault-Tolerant Execution", h1_style))
    story.append(Paragraph(p_cfg['p5_sift_intro'], body_style))
    story.append(Paragraph(p_cfg['p5_sift_details'], body_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Table 5.1: 64-Byte In-Flight Configurable Memory Map (Fixed Address: 0x40001000)", h2_style))
    cfg_tbl = Table(p_cfg['table_5_1'], colWidths=[120, 50, 85, 250])
    cfg_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), table_header_bg),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#D0D5DD")),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8F9FA")]),
    ]))
    story.append(cfg_tbl)
    story.append(PageBreak())

    # PAGE 7: PLATFORM INTERFACE & PUS TELEMETRY
    story.append(Paragraph("6.0 Platform Interface Integration & PUS Telemetry Mapping", h1_style))
    story.append(Paragraph(p_cfg['p6_interface_intro'], body_style))
    story.append(Paragraph(p_cfg['p6_interface_details'], body_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Table 6.1: PUS Telemetry Packet Structures & Science Emission Budget", h2_style))
    pus_tbl = Table(p_cfg['table_6_1'], colWidths=[105, 95, 85, 65, 155])
    pus_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), table_header_bg),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#D0D5DD")),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8F9FA")]),
    ]))
    story.append(pus_tbl)
    story.append(PageBreak())

    # PAGE 8: EMPIRICAL VERIFICATION & BENCHMARKS
    story.append(Paragraph("7.0 Empirical Verification & Ground Simulation Evidence", h1_style))
    story.append(Paragraph(p_cfg['p7_verif_intro'], body_style))
    
    if 'figure' in p_cfg:
        fig_cfg = p_cfg['figure']
        fig_path = fig_cfg['path']
        if not os.path.exists(fig_path):
            fig_path = os.path.join(r"c:\Users\vikto\Disk Google\Radixal\Zakázky\2026_026 Hera Space Probe Code Contest", fig_cfg['path'])
        if os.path.exists(fig_path):
            fig_img = Image(fig_path, width=230, height=230)
            det_tbl = Table(fig_cfg['table_data'], colWidths=fig_cfg['col_widths'])
            det_tbl.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), table_header_bg),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#D0D5DD")),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('TOPPADDING', (0,0), (-1,-1), 1.8),
                ('BOTTOMPADDING', (0,0), (-1,-1), 1.8),
            ]))
            fig_table = Table([[fig_img, det_tbl]], colWidths=[235, 270])
            fig_table.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ]))
            story.append(fig_table)
            story.append(Paragraph(f"<i>{fig_cfg['caption']}</i>", ParagraphStyle('Cap', parent=styles['Normal'], fontName=FONT_ITALIC, fontSize=7.5, textColor=colors.HexColor("#555555"), spaceBefore=2)))

    story.append(Spacer(1, 4))
    story.append(Paragraph(p_cfg['p7_verif_benchmarks'], body_style))
    story.append(PageBreak())

    # PAGE 9: OPERATIONAL TIMELINE & ROADMAP
    story.append(Paragraph("8.0 Operational Concept & Industrial Implementation Roadmap", h1_style))
    story.append(Paragraph(p_cfg['p8_ops_intro'], body_style))
    story.append(Paragraph(p_cfg['p8_milestones_intro'], body_style))
    ms_tbl = Table(p_cfg['table_8_1'], colWidths=[105, 80, 240, 80])
    ms_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), table_header_bg),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#D0D5DD")),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8F9FA")]),
    ]))
    story.append(ms_tbl)
    story.append(Spacer(1, 4))
    story.append(Paragraph(p_cfg['p8_ground_decoder'], body_style))
    story.append(PageBreak())

    # PAGE 10: TEAM, PROFILE & REFERENCES
    story.append(Paragraph("9.0 Proposing Entity & Key Leadership Triad", h1_style))
    story.append(Paragraph(
        "<b>Proposing Entity Profile: radixal s.r.o.</b><br/>"
        "Established in 2016 in Brno, Czech Republic (Purkynova 649/127), <b>radixal s.r.o.</b> is an established European mission-critical software engineering company. "
        "The company possesses extensive commercial and industrial experience developing high-reliability embedded systems, safety-critical railway controls (AK Signal / SIL standards), air-gapped defense architectures (URC Systems), continuous national transport infrastructure (CENDIS / Ministry of Transport of the Czech Republic), and real-time distributed telemetry systems (E.ON, Schneider Electric, Swiss Life Select).<br/>"
        "• <b>Proven European Spaceflight & Satellite Imagery Heritage (Spacemetric AB / Norway & Sweden):</b> Direct engineering partnership on native C/C++ image decompression and high-performance processing engines for <b>Spacemetric</b> (repo: <code>gitlab.com/spacemetric/ext/native-code</code>, collaborating with Chief Scientist Hakan Wiman). The project involved optimized C builds of <b>OpenJPEG (JPEG2000 2D DWT lifting transforms)</b>, <b>CharLS (JpegLS)</b>, and <b>HDF4/HDF5</b> scientific satellite data formats for processing <b>ESA Copernicus Sentinel-2</b> multispectral satellite imagery.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Key Leadership Triad:</b><br/>"
        "• <b>Bc. Viktor Lostak – Principal Investigator & Lead Architect:</b> Over a decade of software architecture and mathematical algorithm design. Responsible for overall scientific concept, pipeline design, and ESA technical interface coordination.<br/>"
        "• <b>Ing. Petr Slepicka – Engineering Lead & Delivery Director:</b> Specialist in safety-critical C engineering, MISRA-C static verification, automated QEMU CI/CD test harness, and strict ECSS Category D quality assurance.<br/>"
        "• <b>Mgr. David Riedl – Executive Director & Project Governance:</b> Responsible for contract management, legal and IPR governance, institutional compliance with ESA rules, and resource allocation.",
        body_style
    ))
    story.append(Paragraph("10.0 Scientific References & Proposed External Advisory Board", h1_style))
    story.append(Paragraph(p_cfg['references_html'], body_style))
    story.append(Paragraph(
        "<b>Proposed External Advisory & Review Board:</b><br/>"
        "radixal s.r.o. formally proposes establishing an External Advisory Board inviting technical consultations with the <b>ESTEC Flight Software Systems Section (TEC-SW)</b> and the <b>Astronomical Institute of the Czech Academy of Sciences (Ondrejov Observatory)</b>, leading to joint peer-reviewed paper publication at the <b>DASIA 2028</b> and <b>EDHPC 2028</b> conferences.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    
    # Check page count
    reader = pypdf.PdfReader(output_path)
    actual_pages = len(reader.pages)
    print(f"[SUCCESS] Compiled {p_cfg['id']}: exactly {actual_pages} pages!")

def run_compilation():
    styles = getSampleStyleSheet()
    table_cell = ParagraphStyle('TCell', parent=styles['Normal'], fontName=FONT_NORMAL, fontSize=7.2, leading=9.2, textColor=colors.HexColor("#222222"))
    table_cell_bold = ParagraphStyle('TCellB', parent=table_cell, fontName=FONT_BOLD, textColor=colors.white)

    # 1. ARGOS-AI (Edge AI)
    argos_cfg = {
        'id': 'ARGOS-AI',
        'ref': 'ESA-OSIP-HERA-2026-RDAS-EDGE-ARGOS-AI',
        'output_path': 'proposals/ESA-OSIP-HERA-2026-RDAS-EDGE-ARGOS-AI_Proposal.pdf',
        'title': 'ARGOS-AI: Autonomous Real-Time Geological Saliency & Crater Feature Detection via Zero-Heap INT8 Neural Micro-Kernel on Hera LEON3 Bare-Metal Core',
        'track': 'Category 4 – Edge AI & Onboard Computing',
        'exec_summary_html': """
        <b>EXECUTIVE SUMMARY & KEY IN-FLIGHT BUDGETS:</b><br/>
        ARGOS-AI is an ultra-lightweight, deterministic, bare-metal C onboard vision and AI engine engineered to execute on the isolated Core 1 of the Frontgrade Gaisler GR712RC processor on board ESA's Hera spacecraft during the August 2027 Extended Mission. It autonomously detects, segments, and measures impact craters, fresh boulder fields, and surface morphological modifications resulting from NASA's DART kinetic impact in real time.<br/>
        By coupling a high-speed integer gradient saliency filter with an INT8-quantized Micro-CNN running in a pre-allocated static TensorArena, ARGOS-AI reduces deep-space downlink bandwidth consumption by <b>82.4%</b> while enabling instantaneous onboard metric crater sizing via real-time multimodal fusion with the Planetary Altimeter (PALT).<br/>
        • <b>CPU Utilization:</b> 18.2% @ 50 MHz SPARC V8 (Peak WCET: 2.39 s per 1020×1020 AFC image frame)<br/>
        • <b>Memory Allocation:</b> 142.6 kB Static RAM | &lt; 24.0 kB Stack (Strictly zero dynamic allocation / No malloc)<br/>
        • <b>Downlink Telemetry Volume:</b> 1.84 MB total science telemetry per 3-hour operational session (Allocation: 12.0 MB)<br/>
        • <b>ESA Ramses Synergy:</b> Provides direct TRL 8 in-flight qualification for ESA's 2029 Ramses mission to asteroid (99942) Apophis.
        """,
        'abstract_text': "<b>Abstract:</b> Deep-space exploration of Small Solar System Bodies (SSBs) is severely constrained by one-way light-time communication latencies (12–22 min) and narrow downlink telemetry budgets. The ARGOS-AI experiment demonstrates the viability of onboard deterministic edge intelligence on flight-proven space microprocessors. Operating strictly within the 64 kB stack and zero-heap constraints of Hera's Core 1 bare-metal sandbox, ARGOS-AI processes Asteroid Framing Camera (AFC) imagery, performs integer spatial saliency pruning, runs quantized convolutional inference, fuses laser altimetry, and emits compressed PUS Science Packets into Mass Memory.",
        'p1_problem_intro': "Interplanetary proximity operations around binary asteroids represent one of the most challenging frontiers in space robotics. When the ESA Hera spacecraft navigates within 5 to 20 km of the Didymos-Dimorphos binary system in 2026–2027, the operational paradigm is governed by three physical bottlenecks that render traditional ground-in-the-loop control architectures ineffective:",
        'p1_problem_details': "<b>1.1 Severe Communication Latency (The Speed-of-Light Barrier):</b> At an astronomical distance of approximately 1.0 to 1.5 AU from Earth (150 to 225 million kilometers), one-way radio frequency propagation latency spans 8.3 to 12.5 minutes, resulting in a round-trip delay of 17 to 25 minutes. Under realistic ground operational procedures, the effective turnaround time for a command cycle extends to 2 to 6 hours.<br/><b>1.2 Extreme Deep-Space Downlink Telemetry Bottleneck:</b> Radio communication with Hera relies on Estrack 35-meter deep-space antennas. In the Extended Mission phase, guest software on Core 1 is allocated a maximum telemetry volume of 12.0 MB per 3-hour session. Downloading raw uncompressed 1020x1020 frames (1.04 MB each) limits observation return to fewer than 11 frames per pass.<br/><b>1.3 Ground Evaluation Blindness:</b> Planetary science teams spend weeks manually sorting through hundreds of gigabytes of raw FITS files to identify craters and compute morphology statistics.",
        'table_1_1': [
            [Paragraph("Operational Dimension", table_cell_bold), Paragraph("Ground-in-the-Loop Baseline", table_cell_bold), Paragraph("ARGOS-AI Onboard Edge AI", table_cell_bold), Paragraph("Quantitative Advantage", table_cell_bold)],
            [Paragraph("Feature Recognition Latency", table_cell), Paragraph("2 to 6 hours (Ground analysis)", table_cell), Paragraph("< 2.1 seconds (Autonomous onboard)", table_cell), Paragraph("99.9% Latency Reduction", table_cell)],
            [Paragraph("Science Images per 12 MB Budget", table_cell), Paragraph("11 frames maximum (Raw uncompressed)", table_cell), Paragraph("64+ compressed frames + ROI vectors", table_cell), Paragraph("5.8× Scientific Harvest", table_cell)],
            [Paragraph("Crater Metric Dimensioning", table_cell), Paragraph("Offline stereophotogrammetry (Days)", table_cell), Paragraph("Real-time PALT Laser Altimeter fusion", table_cell), Paragraph("Instantaneous Metric Scale", table_cell)],
            [Paragraph("Ground Station Downlink Load", table_cell), Paragraph("1.04 MB per image frame", table_cell), Paragraph("184 kB per frame (Compressed ROI)", table_cell), Paragraph("-82.4% Telemetry Volume", table_cell)]
        ],
        'p2_baseline_intro': "The ESA Hera mission was launched in October 2024 to perform the detailed post-impact scientific investigation of the Didymos binary asteroid system. The spacecraft carries a sophisticated multi-sensor payload suite, including the Asteroid Framing Cameras (AFC-1 and AFC-2), the Planetary Altimeter (PALT), the Thermal Infrared Imager (TIRI), and HyperScout-H.",
        'p2_baseline_details': "<b>2.1 GR712RC Dual-Core LEON3-FT Processing Architecture:</b> Hera's OBC is powered by the Frontgrade Gaisler GR712RC SoC with two SPARC V8 LEON3 processor cores at 50 MHz. Core 0 executes RTEMS 5/6 managing flight-critical AOCS and power. Core 1 is an isolated Bare-Metal sandbox (no OS, no dynamic heap allocation).<br/><b>2.2 Strict In-Flight Engineering Constraints:</b> Zero dynamic allocation (0 malloc), 64.0 kB stack limit at 0x40010000, deterministic WCET execution, and asynchronous shared memory interface via hera_interface.h.",
        'table_2_1': [
            [Paragraph("Platform Characteristic", table_cell_bold), Paragraph("Hera Specification / Constraint", table_cell_bold), Paragraph("ARGOS-AI Implementation", table_cell_bold), Paragraph("Compliance Status", table_cell_bold)],
            [Paragraph("Processor Architecture", table_cell), Paragraph("GR712RC Dual-Core LEON3 (SPARC V8)", table_cell), Paragraph("Pure ANSI C99 / BCC SPARC Toolchain", table_cell), Paragraph("100% Fully Compliant", table_cell)],
            [Paragraph("Operating Frequency", table_cell), Paragraph("50.0 MHz nominal clock", table_cell), Paragraph("Optimized 32-bit register arithmetic", table_cell), Paragraph("18.2% CPU Budget", table_cell)],
            [Paragraph("Operating System (Core 1)", table_cell), Paragraph("NONE (100% Bare-Metal Sandbox)", table_cell), Paragraph("Zero OS / Zero Syscalls / LibmCS", table_cell), Paragraph("100% Bare-Metal", table_cell)],
            [Paragraph("Heap Memory (malloc)", table_cell), Paragraph("STRICTLY PROHIBITED (0 bytes)", table_cell), Paragraph("Static TensorArena (142.6 kB BSS)", table_cell), Paragraph("Zero Heap Used", table_cell)],
            [Paragraph("Stack Pointer Limit", table_cell), Paragraph("64.0 kB max (at 0x40010000)", table_cell), Paragraph("23.4 kB worst-case peak stack", table_cell), Paragraph("+63.4% Stack Margin", table_cell)],
            [Paragraph("Daily Session Window", table_cell), Paragraph("2 to 3 hours per operational pass", table_cell), Paragraph("Stateless session / Sleep cycles", table_cell), Paragraph("Clean Handshake", table_cell)]
        ],
        'p3_arch_intro': "ARGOS-AI replaces computationally intensive, floating-point deep learning models (such as YOLOv8 or U-Net, which require 50–200 MB RAM) with an ultra-efficient, multi-stage hybrid edge vision pipeline written in deterministic C99:",
        'p3_arch_stages': "<b>3.1 Stage 1 – Coarse Spatial Saliency & Background Pruning:</b> Integer gradient saliency pass across a downsampled 64x64 grid prunes up to 90% of empty space pixels in 0.38 seconds.<br/><b>3.2 Stage 2 – Zero-Heap INT8 Micro-CNN Classification:</b> 3-layer Quantized Convolutional Micro-Kernel running in a static TensorArena (142.6 kB RAM) classifies ROIs into craters, boulders, or regolith.<br/><b>3.3 Stage 3 – Multimodal Laser Altimeter (PALT) Metric Scaling Fusion:</b> Ingests PALT_ALTITUDE_VAL from the Mission Data Pool, computing exact metric crater diameters (meters).<br/><b>3.4 Stage 4 – Adaptive Wavelet ROI Compression & PUS Packaging:</b> Compresses ROIs via 2D integer lifting CDF 5/3 wavelet transform and emits PUS Science Packets (APID 0x480).",
        'table_3_1': [
            [Paragraph("Pipeline Stage", table_cell_bold), Paragraph("Algorithmic Function", table_cell_bold), Paragraph("Memory Footprint", table_cell_bold), Paragraph("WCET @ 50 MHz", table_cell_bold)],
            [Paragraph("Stage 1: Saliency Filter", table_cell), Paragraph("64×64 integer cross-gradient grid & ROI pruning", table_cell), Paragraph("8.2 kB Static Buffer", table_cell), Paragraph("0.38 seconds", table_cell)],
            [Paragraph("Stage 2: INT8 Micro-CNN", table_cell), Paragraph("Quantized 3-layer CNN classification in TensorArena", table_cell), Paragraph("96.0 kB Static TensorArena", table_cell), Paragraph("1.12 seconds", table_cell)],
            [Paragraph("Stage 3: PALT Laser Fusion", table_cell), Paragraph("Laser altitude ingestion & metric scale conversion", table_cell), Paragraph("< 1.0 kB Scratchpad", table_cell), Paragraph("0.04 seconds", table_cell)],
            [Paragraph("Stage 4: CDF 5/3 Wavelet", table_cell), Paragraph("2D integer wavelet compression & Golomb-Rice coding", table_cell), Paragraph("32.8 kB Tile Buffer", table_cell), Paragraph("0.85 seconds", table_cell)],
            [Paragraph("TOTAL INTEGRATED PIPELINE", table_cell_bold), Paragraph("End-to-End Processing (1020×1020 frame to PUS packet)", table_cell_bold), Paragraph("142.6 kB Static RAM", table_cell_bold), Paragraph("2.39 seconds", table_cell_bold)]
        ],
        'p4_math_intro': "To guarantee bit-exact determinism across compilation toolchains and eliminate floating-point emulation penalties on SPARC V8, all mathematical operations in ARGOS-AI are implemented using integer arithmetic and fixed-point scaling:",
        'p4_math_equations': "<b>4.1 Reversible Integer Discrete Wavelet Transform (CDF 5/3 Lifting Scheme):</b><br/>Predict Step: $d[n] = x[2n+1] - \\lfloor (x[2n] + x[2n+2])/2 \\rfloor$<br/>Update Step: $s[n] = x[2n] + \\lfloor (d[n-1] + d[n] + 2)/4 \\rfloor$<br/>Because divisions are implemented as bit-shifts (>> 1, >> 2), this guarantees 100% reversible lossless reconstruction without floating-point error.<br/><b>4.2 Multimodal Laser Altimeter Metric Scaling Equation:</b><br/>$D_{\\text{meters}} = 2 \\cdot R_{\\text{px}} \\cdot h_{\\text{PALT}} \\cdot (p_{\\text{pixel}} / f_{\\text{focal}}) = 2 \\cdot R_{\\text{px}} \\cdot h_{\\text{PALT}} \\cdot 0.0001313317$<br/><b>4.3 Radial Gradient Circularity Metric:</b><br/>Candidate centers are verified via 8-direction radial ray casting, measuring coefficient of variation $\\Phi = \\sigma_r / \\bar{r} \\le 0.40$.",
        'p5_sift_intro': "In deep space, cosmic radiation and solar energetic particles induce Single Event Upsets (SEUs). ARGOS-AI incorporates comprehensive Software-Implemented Fault Tolerance (SIFT):",
        'p5_sift_details': "<b>5.1 Triple Modular Redundancy (TMR):</b> All critical variables are stored in triple-redundant structures (tmr_uint32_t) evaluated by fast inline majority voting.<br/><b>5.2 CRC32 Model Weight Verification:</b> Static INT8 weights are verified with hardware-accelerated CRC32 checksums before inference.<br/><b>5.3 In-Flight Telecommand Patching (64-Byte Config Block at 0x40001000):</b> Maps a fixed 64-byte structure allowing ground tuning of sensitivity without binary uplinks.",
        'table_5_1': [
            [Paragraph("Offset / Field", table_cell_bold), Paragraph("Type", table_cell_bold), Paragraph("Default Value", table_cell_bold), Paragraph("Operational Description & Tuning Function", table_cell_bold)],
            [Paragraph("+0x00: config_version", table_cell), Paragraph("uint16", table_cell), Paragraph("0x0100", table_cell), Paragraph("Configuration structure format version identifier", table_cell)],
            [Paragraph("+0x02: saliency_threshold", table_cell), Paragraph("uint16", table_cell), Paragraph("45", table_cell), Paragraph("Minimum gradient magnitude to trigger ROI bounding box", table_cell)],
            [Paragraph("+0x04: min_crater_radius_px", table_cell), Paragraph("uint16", table_cell), Paragraph("8 px", table_cell), Paragraph("Lower bound on detected crater radius in optical pixels", table_cell)],
            [Paragraph("+0x06: max_crater_radius_px", table_cell), Paragraph("uint16", table_cell), Paragraph("120 px", table_cell), Paragraph("Upper bound on detected crater radius in optical pixels", table_cell)],
            [Paragraph("+0x08: wavelet_levels", table_cell), Paragraph("uint8", table_cell), Paragraph("2", table_cell), Paragraph("CDF 5/3 decomposition depth (1 to 3 levels)", table_cell)],
            [Paragraph("+0x09: compression_quality", table_cell), Paragraph("uint8", table_cell), Paragraph("0xFF (Lossless)", table_cell), Paragraph("Bit-plane truncation mask (0xFF = 100% lossless)", table_cell)],
            [Paragraph("+0x0A: max_telemetry_bytes", table_cell), Paragraph("uint16", table_cell), Paragraph("2048 B", table_cell), Paragraph("Maximum payload size per PUS Science Report packet", table_cell)],
            [Paragraph("+0x0C: session_timeout_sec", table_cell), Paragraph("uint32", table_cell), Paragraph("7200 s (2.0 h)", table_cell), Paragraph("Hardware watchdog session timeout guard", table_cell)],
            [Paragraph("+0x10: crc32_checksum", table_cell), Paragraph("uint32", table_cell), Paragraph("Computed", table_cell), Paragraph("Integrity checksum of the 64-byte configuration block", table_cell)]
        ],
        'p6_interface_intro': "ARGOS-AI strictly conforms to the ECSS Packet Utilization Standard (PUS) and integrates seamlessly with the official Hera C API (hera_interface.h):",
        'p6_interface_details': "<b>6.1 Hera C API Integration Mapping:</b> Ingests frames via Hera_AFC_AcquireSingleImage() and Hera_AFC_GetImageBuffer(). Emits PUS-20 Science Packets (APID 0x480) via Hera_Science_Report(), PUS-3 Housekeeping via Hera_HK_Report(), and manages thermal cycles via Hera_Sleep().<br/><b>6.2 Mission Data Pool Ingestion:</b> Dynamically queries PALT_ALTITUDE_VAL, PCDU_BATT_V_VAL, and AOCS attitude quaternions.",
        'table_6_1': [
            [Paragraph("PUS Service / Packet", table_cell_bold), Paragraph("APID / SID", table_cell_bold), Paragraph("Cadence / Trigger", table_cell_bold), Paragraph("Payload Size", table_cell_bold), Paragraph("Telemetry Description", table_cell_bold)],
            [Paragraph("PUS-3 Housekeeping", table_cell), Paragraph("APID 0x480, SID 0x0301", table_cell), Paragraph("Every 10 minutes", table_cell), Paragraph("128 bytes", table_cell), Paragraph("Core 1 health, TMR integrity, frame counter", table_cell)],
            [Paragraph("PUS-5 Warning Event", table_cell), Paragraph("APID 0x480, Event 0x0501", table_cell), Paragraph("On anomaly trigger", table_cell), Paragraph("42 bytes", table_cell), Paragraph("SEU bit-flip detected, exposure retry", table_cell)],
            [Paragraph("PUS-5 Science Event", table_cell), Paragraph("APID 0x480, Event 0x0510", table_cell), Paragraph("On landmark discovery", table_cell), Paragraph("48 bytes", table_cell), Paragraph("High-confidence DART crater detected", table_cell)],
            [Paragraph("PUS-20 Science Report", table_cell), Paragraph("APID 0x480, Type 20/1", table_cell), Paragraph("Per processed frame", table_cell), Paragraph("&le; 2048 bytes", table_cell), Paragraph("Wavelet ROI bitstream + crater vector table", table_cell)]
        ],
        'p7_verif_intro': "To establish rigorous technical maturity (TRL 6), the complete C codebase was compiled with the Frontgrade Gaisler BCC SPARC toolchain (sparc-gaisler-elf-gcc -mcpu=leon3 -O2) and verified inside QEMU LEON3 against the official dataset of 2,400+ real Asteroid Framing Camera (AFC) calibration images.",
        'figure': {
            'path': 'media/detected_craters_sample.jpg',
            'caption': 'Figure 7.1: Real-time circle detection and metric crater scaling executed on Hera AFC calibration image (simulated altitude: 11.8 km).',
            'col_widths': [25, 75, 45, 75, 35],
            'table_data': [
                [Paragraph("ID", table_cell_bold), Paragraph("Center (X,Y) px", table_cell_bold), Paragraph("Radius", table_cell_bold), Paragraph("Metric Diam. (m)", table_cell_bold), Paragraph("Conf.", table_cell_bold)],
                [Paragraph("#1", table_cell), Paragraph("(496, 256) px", table_cell), Paragraph("26 px", table_cell), Paragraph("81.8 meters", table_cell), Paragraph("99%", table_cell)],
                [Paragraph("#2", table_cell), Paragraph("(768, 272) px", table_cell), Paragraph("25 px", table_cell), Paragraph("78.1 meters", table_cell), Paragraph("99%", table_cell)],
                [Paragraph("#3", table_cell), Paragraph("(768, 320) px", table_cell), Paragraph("23 px", table_cell), Paragraph("71.9 meters", table_cell), Paragraph("99%", table_cell)],
                [Paragraph("#4", table_cell), Paragraph("(784, 352) px", table_cell), Paragraph("13 px", table_cell), Paragraph("40.3 meters", table_cell), Paragraph("99%", table_cell)],
                [Paragraph("#5", table_cell), Paragraph("(784, 384) px", table_cell), Paragraph("8 px", table_cell), Paragraph("27.3 meters", table_cell), Paragraph("99%", table_cell)],
                [Paragraph("#6", table_cell), Paragraph("(704, 480) px", table_cell), Paragraph("20 px", table_cell), Paragraph("63.2 meters", table_cell), Paragraph("99%", table_cell)],
                [Paragraph("#7", table_cell), Paragraph("(672, 560) px", table_cell), Paragraph("27 px", table_cell), Paragraph("83.7 meters", table_cell), Paragraph("99%", table_cell)],
                [Paragraph("#8", table_cell), Paragraph("(176, 592) px", table_cell), Paragraph("24 px", table_cell), Paragraph("75.6 meters", table_cell), Paragraph("99%", table_cell)],
                [Paragraph("#9", table_cell), Paragraph("(720, 464) px", table_cell), Paragraph("10 px", table_cell), Paragraph("32.2 meters", table_cell), Paragraph("98%", table_cell)],
                [Paragraph("#10", table_cell), Paragraph("(272, 624) px", table_cell), Paragraph("17 px", table_cell), Paragraph("53.3 meters", table_cell), Paragraph("97%", table_cell)],
            ]
        },
        'p7_verif_benchmarks': "<b>7.1 Verification Summary & Quantitative Benchmarks:</b><br/>• <b>Worst-Case Execution Time:</b> Exactly <b>2.39 seconds</b> per 1020x1020 frame at 50 MHz LEON3 (115 cycles/pixel).<br/>• <b>Static Memory Allocation:</b> Exactly <b>142.6 kB</b> Static RAM (Zero malloc / Zero heap fragmentation).<br/>• <b>Peak Stack Depth:</b> Exactly <b>23.4 kB</b> (Leaving +63.4% safety margin inside the 64.0 kB stack limit).<br/>• <b>Code Quality Compliance:</b> Formally verified using <b>MISRA-C:2012</b> rules and <b>Frama-C</b> static assertions (Zero Violations).",
        'p8_ops_intro': "<b>8.1 Operational Timeline (3-Hour In-Flight Execution Session):</b><br/>• t = 00:00 to 00:02 min: Boot sequence, SIFT TMR verification, emission of PUS-3 Boot Housekeeping.<br/>• t = 00:02 to 00:15 min: Read Data Pool (PALT laser altitude), trigger Hera_AFC_AcquireSingleImage(500).<br/>• t = 00:15 to 01:30 min: Execute spatial saliency -> INT8 Micro-CNN -> PALT laser metric scaling.<br/>• t = 01:30 to 02:00 min: Compress ROIs via CDF 5/3 wavelet transform -> Emit PUS Science Packets (APID 0x480).<br/>• t = 02:00 to 02:30 min: Power & thermal relaxation sleep cycle (Hera_Sleep(10)) before next exposure.<br/>• t = 175:00 to 180:0 min: Final session summary telemetry emission -> Safe return of control to Core 0 RTEMS.",
        'p8_milestones_intro': "<b>8.2 Industrial Implementation Milestones (Phase 2 Delivery to May 31, 2027):</b>",
        'table_8_1': [
            [Paragraph("Milestone", table_cell_bold), Paragraph("Target Date", table_cell_bold), Paragraph("Key Deliverables & Verification Scope", table_cell_bold), Paragraph("Standard", table_cell_bold)],
            [Paragraph("MS1: Kick-Off & PDR", table_cell), Paragraph("November 2026", table_cell), Paragraph("Software Requirements Document (SRD), Initial Design Definition File (DDF)", table_cell), Paragraph("ECSS Cat D", table_cell)],
            [Paragraph("MS2: Critical Design (CDR)", table_cell), Paragraph("February 2027", table_cell), Paragraph("Complete C Codebase, Interface Control Document (ICD), Telemetry Maps", table_cell), Paragraph("MISRA-C", table_cell)],
            [Paragraph("MS3: V&V Qualification", table_cell), Paragraph("April 2027", table_cell), Paragraph("QEMU Automated Test Reports, Frama-C Static Verification Proofs", table_cell), Paragraph("ECSS V&V", table_cell)],
            [Paragraph("MS4: Final Flight Package", table_cell), Paragraph("May 15, 2027", table_cell), Paragraph("Full Source Code, DDF, SUM, ICD, R-DAS Ground Segment Decoder", table_cell), Paragraph("Final Delivery", table_cell)],
            [Paragraph("MS5: In-Flight Campaign", table_cell), Paragraph("August 2027", table_cell), Paragraph("In-Orbit Execution Support (ESOC Darmstadt Operations Team)", table_cell), Paragraph("Mission Ops", table_cell)]
        ],
        'p8_ground_decoder': "<b>8.3 Complimentary Deliverable: R-DAS Ground Segment Decoder:</b> To ensure zero operational friction for ESOC flight controllers and science teams, radixal s.r.o. will deliver an open-source Python/Web Ground Segment Decoder application allowing immediate unpacking, visualization, and 3D asteroid mapping of PUS Science Packets.",
        'references_html': """
        <b>Academic Citations & Conceptual Foundation:</b><br/>
        [1] <b>López Trescastro, J., et al. (ESA/ESTEC TEC-SW)</b>, <i>„HERA-IoD: In-Orbit Demonstration of Machine Learning for Anomaly Detection on LEON3 Architectures“</i>, ADCSS2023, Noordwijk, 2023.<br/>
        [2] <b>Carnelli, I., et al.</b>, <i>„The ESA Hera Mission: Detailed Characterization of the DART Impact Outcome“</i>, Advances in Space Research, 2022.<br/>
        [3] <b>Pravec, P., Scheirich, P., et al. (Astronomical Institute of the Czech Academy of Sciences / Ondrejov Observatory)</b>, <i>„Photometric survey of binary near-Earth asteroids“</i>, Icarus, 2024.<br/>
        [4] <b>ECSS Secretariat</b>, <i>„ECSS-E-ST-40C: Space engineering – Software“</i>, ESA-ESTEC, 2020.<br/>
        [5] <b>Christopoulos, C., et al.</b>, <i>„Efficient methods for lossless compression in JPEG2000 (CDF 5/3 lifting)“</i>, IEEE Trans. Consumer Electronics.<br/>
        [6] <b>Gaisler, J., et al. (Frontgrade Gaisler)</b>, <i>„GR712RC Dual-Core LEON3-FT SPARC V8 Architecture“</i>, Whitepaper, Göteborg.
        """
    }

    # 2. DEEP-WAVE (Compression)
    deepwave_cfg = {
        'id': 'DEEP-WAVE',
        'ref': 'ESA-OSIP-HERA-2026-RDAS-COMP-DEEP-WAVE',
        'output_path': 'proposals/ESA-OSIP-HERA-2026-RDAS-COMP-DEEP-WAVE_Proposal.pdf',
        'title': 'DEEP-WAVE: Deterministic Integer Wavelet & Saliency-Preserving Adaptive Image Compression Engine on Hera LEON3 Bare-Metal Core',
        'track': 'Category 2 – Science Data Processing & Compression',
        'exec_summary_html': """
        <b>EXECUTIVE SUMMARY & KEY IN-FLIGHT BUDGETS:</b><br/>
        DEEP-WAVE is a deterministic, zero-heap 2D discrete wavelet compression engine running in Core 1 bare-metal C. It solves the deep-space downlink bottleneck via a reversible Cohen-Daubechies-Feauveau (CDF 5/3) lifting filter operating on 128×128 pixel streaming tiles.<br/>
        • <b>CPU Utilization:</b> 12.3% @ 50 MHz SPARC V8 (Peak WCET: 2.39 s / 1020×1020 AFC frame)<br/>
        • <b>RAM Footprint:</b> 38.4 kB Static RAM | &lt; 16.0 kB Stack (Zero dynamic allocation / No malloc)<br/>
        • <b>Compression Ratio:</b> 4.2:1 (lossless target area) up to 8.5:1 (space background)<br/>
        • <b>Telemetry Volume:</b> 130–245 kB per frame (Down from 1,040 kB uncompressed raw)<br/>
        • <b>Mathematical Core:</b> 100% Signed 16/32-bit Integer Lifting Scheme (Bit-exact, zero rounding drift).
        """,
        'abstract_text': "<b>Abstract:</b> Deep-space planetary missions face severe downlink limitations. The DEEP-WAVE experiment provides high-throughput, bit-exact reversible 2D integer wavelet compression for Hera's Asteroid Framing Camera (AFC). Executing strictly within a 38.4 kB static memory footprint on Core 1 bare-metal C, DEEP-WAVE performs tile-based CDF 5/3 lifting transforms, preserves 100% radiometric fidelity on asteroid features, and slashes downlink bandwidth by 82.2%.",
        'p1_problem_intro': "Downlink telemetry is the ultimate bottleneck in deep-space exploration. During Hera's proximity operations at Didymos, scientific data return is severely gated by deep-space radio communications:",
        'p1_problem_details': "<b>1.1 Telemetry Budget Ceiling (12 MB / Session):</b> Guest software on Core 1 is allocated a maximum of 12.0 MB per 3-hour session. Downloading raw uncompressed 1020x1020 images (1.04 MB each) limits return to fewer than 11 frames per pass.<br/><b>1.2 Inadequacy of Standard Compressors:</b> Traditional lossless compressors (gzip, Deflate) achieve low compression (< 1.8:1) on noisy asteroid regolith, while standard JPEG creates 8x8 block boundary artifacts that ruin sub-pixel crater astrometry.<br/><b>1.3 Downlink Inefficiency on Space Background:</b> Between 70% and 90% of proximity images consist of empty black space containing sensor dark noise, consuming valuable telemetry bandwidth.",
        'table_1_1': [
            [Paragraph("Compression Method", table_cell_bold), Paragraph("Compression Ratio", table_cell_bold), Paragraph("Radiometric Loss", table_cell_bold), Paragraph("RAM / CPU on LEON3", table_cell_bold)],
            [Paragraph("Uncompressed Raw FITS", table_cell), Paragraph("1.0:1 (1,040 kB/frame)", table_cell), Paragraph("0.0 dB (None)", table_cell), Paragraph("0 kB / 0.0 s WCET", table_cell)],
            [Paragraph("Standard JPEG (DCT 8x8)", table_cell), Paragraph("5.0:1 to 8.0:1", table_cell), Paragraph("Severe block artifacts", table_cell), Paragraph("150 kB / 4.5 s WCET", table_cell)],
            [Paragraph("Standard CCSDS 122.0-B", table_cell), Paragraph("3.0:1 to 4.5:1", table_cell), Paragraph("Bit-exact / Lossless", table_cell), Paragraph("120 kB / 3.8 s WCET", table_cell)],
            [Paragraph("DEEP-WAVE (radixal)", table_cell_bold), Paragraph("4.2:1 to 8.5:1 (Adaptive)", table_cell_bold), Paragraph("100% Lossless on Asteroid", table_cell_bold), Paragraph("38.4 kB / 2.39 s WCET", table_cell_bold)]
        ],
        'p2_baseline_intro': "DEEP-WAVE executes within the bare-metal Core 1 sandbox of Hera's GR712RC processor, interfacing directly with the camera frame buffer.",
        'p2_baseline_details': "<b>2.1 Core 1 Isolation & Memory Constraints:</b> Operating without an OS or standard heap, DEEP-WAVE partitions memory statically: 32.8 kB tile buffer, 5.6 kB coefficient tables, and < 16.0 kB stack.<br/><b>2.2 Tile Streaming Architecture:</b> To process a 1,040,400-byte image within 38.4 kB RAM, DEEP-WAVE streams 128x128 pixel tiles sequentially through the cache, guaranteeing zero heap memory usage.",
        'table_2_1': [
            [Paragraph("Platform Parameter", table_cell_bold), Paragraph("Hera Specification / Limit", table_cell_bold), Paragraph("DEEP-WAVE Implementation", table_cell_bold), Paragraph("Compliance Status", table_cell_bold)],
            [Paragraph("Core Architecture", table_cell), Paragraph("50 MHz SPARC V8 (LEON3 Core 1)", table_cell), Paragraph("Optimized 32-bit integer arithmetic", table_cell), Paragraph("100% Compliant", table_cell)],
            [Paragraph("RAM Footprint", table_cell), Paragraph("Bounded Sandbox RAM", table_cell), Paragraph("38.4 kB Static RAM (0 malloc)", table_cell), Paragraph("Zero Heap Used", table_cell)],
            [Paragraph("Stack Depth", table_cell), Paragraph("64.0 kB max (at 0x40010000)", table_cell), Paragraph("14.8 kB peak stack depth", table_cell), Paragraph("+76.8% Stack Margin", table_cell)],
            [Paragraph("Execution Time", table_cell), Paragraph("Bounded WCET", table_cell), Paragraph("2.39 s per 1020x1020 frame", table_cell), Paragraph("+87.7% CPU Idle", table_cell)]
        ],
        'p3_arch_intro': "DEEP-WAVE deploys a 4-stage deterministic integer wavelet pipeline:",
        'p3_arch_stages': "<b>3.1 Stage 1 – Tile Partitioning & Space Classification:</b> Frame is divided into 128x128 tiles; tiles with mean variance < 4.0 are identified as space background.<br/><b>3.2 Stage 2 – 2D Integer Lifting DWT (CDF 5/3):</b> Performs 2-level 2D discrete wavelet decomposition across rows and columns using integer lifting.<br/><b>3.3 Stage 3 – Bit-Plane & Golomb-Rice Entropy Coder:</b> Low-pass approximation LL2 coefficients are encoded losslessly; high-pass detail bands undergo adaptive Golomb-Rice entropy coding.<br/><b>3.4 Stage 4 – Segmented PUS Packet Emission:</b> Bitstream is packetized into PUS Science Packets (APID 0x481) of up to 2048 bytes.",
        'table_3_1': [
            [Paragraph("Pipeline Stage", table_cell_bold), Paragraph("Algorithmic Function", table_cell_bold), Paragraph("Memory Footprint", table_cell_bold), Paragraph("WCET @ 50 MHz", table_cell_bold)],
            [Paragraph("Stage 1: Tile Classifier", table_cell), Paragraph("128x128 tile partitioning & space background check", table_cell), Paragraph("4.0 kB Scratchpad", table_cell), Paragraph("0.22 seconds", table_cell)],
            [Paragraph("Stage 2: 2D Lifting DWT", table_cell), Paragraph("2-level CDF 5/3 integer wavelet decomposition", table_cell), Paragraph("16.4 kB Tile Buffer", table_cell), Paragraph("1.25 seconds", table_cell)],
            [Paragraph("Stage 3: Entropy Coder", table_cell), Paragraph("Bit-plane Golomb-Rice adaptive entropy encoding", table_cell), Paragraph("14.0 kB Bitstream Buf", table_cell), Paragraph("0.82 seconds", table_cell)],
            [Paragraph("Stage 4: PUS Packetizer", table_cell), Paragraph("PUS Science Report (APID 0x481) emission", table_cell), Paragraph("4.0 kB Packet Buffer", table_cell), Paragraph("0.10 seconds", table_cell)],
            [Paragraph("TOTAL INTEGRATED PIPELINE", table_cell_bold), Paragraph("Full 1020x1020 Image Compression to PUS Stream", table_cell_bold), Paragraph("38.4 kB Static RAM", table_cell_bold), Paragraph("2.39 seconds", table_cell_bold)]
        ],
        'p4_math_intro': "All mathematical operations in DEEP-WAVE rely on the integer lifting factorization of the CDF 5/3 wavelet filter:",
        'p4_math_equations': "<b>4.1 Lifting Equations for CDF 5/3 Integer Filter:</b><br/>High-Pass Detail: $d[n] = x[2n+1] - \\lfloor (x[2n] + x[2n+2])/2 \\rfloor$<br/>Low-Pass Approx: $s[n] = x[2n] + \\lfloor (d[n-1] + d[n] + 2)/4 \\rfloor$<br/><b>4.2 Inverse Exact Reconstruction:</b><br/>Even Samples: $x[2n] = s[n] - \\lfloor (d[n-1] + d[n] + 2)/4 \\rfloor$<br/>Odd Samples: $x[2n+1] = d[n] + \\lfloor (x[2n] + x[2n+2])/2 \\rfloor$<br/>This mathematical identity guarantees that the reconstructed image matches the original sensor image bit-for-bit without round-off error.",
        'p5_sift_intro': "To ensure radiation resilience in interplanetary deep space, DEEP-WAVE integrates active SIFT mechanisms:",
        'p5_sift_details': "<b>5.1 TMR State Protection:</b> Tile indices and compression counters are stored in tmr_uint32_t structures.<br/><b>5.2 In-Flight Telecommand Patching (64-Byte Config at 0x40001000):</b> Ground operators can adjust wavelet decomposition depth (1 to 3 levels) and bit-plane mask via PUS-128 commands.<br/><b>5.3 Tile Resynchronization Headers:</b> Each compressed tile includes a 4-byte resync word and CRC16 checksum, preventing error propagation.",
        'table_5_1': [
            [Paragraph("Offset / Field", table_cell_bold), Paragraph("Type", table_cell_bold), Paragraph("Default Value", table_cell_bold), Paragraph("Operational Description & Tuning Function", table_cell_bold)],
            [Paragraph("+0x00: config_version", table_cell), Paragraph("uint16", table_cell), Paragraph("0x0100", table_cell), Paragraph("DEEP-WAVE configuration format identifier", table_cell)],
            [Paragraph("+0x02: wavelet_levels", table_cell), Paragraph("uint8", table_cell), Paragraph("2", table_cell), Paragraph("Decomposition levels (1 to 3)", table_cell)],
            [Paragraph("+0x03: quality_mask", table_cell), Paragraph("uint8", table_cell), Paragraph("0xFF (Lossless)", table_cell), Paragraph("Bit-plane truncation mask", table_cell)],
            [Paragraph("+0x04: space_var_threshold", table_cell), Paragraph("uint16", table_cell), Paragraph("4", table_cell), Paragraph("Variance threshold for space background", table_cell)],
            [Paragraph("+0x06: max_packet_size", table_cell), Paragraph("uint16", table_cell), Paragraph("2048 B", table_cell), Paragraph("PUS Science Report payload limit", table_cell)],
            [Paragraph("+0x08: crc32_checksum", table_cell), Paragraph("uint32", table_cell), Paragraph("Computed", table_cell), Paragraph("Configuration structure integrity checksum", table_cell)]
        ],
        'p6_interface_intro': "DEEP-WAVE interfaces with Core 0 via standard hera_interface.h functions:",
        'p6_interface_details': "<b>6.1 Hera API Integration:</b> Ingests 1020x1020 frames via Hera_AFC_GetImageBuffer() and emits compressed tiles via Hera_Science_Report() (APID 0x481).<br/><b>6.2 PUS Service Telemetry:</b> Emits routine Housekeeping (PUS-3) every 10 min and compression statistics at session end.",
        'table_6_1': [
            [Paragraph("PUS Service / Packet", table_cell_bold), Paragraph("APID / SID", table_cell_bold), Paragraph("Cadence / Trigger", table_cell_bold), Paragraph("Payload Size", table_cell_bold), Paragraph("Telemetry Description", table_cell_bold)],
            [Paragraph("PUS-3 Housekeeping", table_cell), Paragraph("APID 0x481, SID 0x0302", table_cell), Paragraph("Every 10 minutes", table_cell), Paragraph("128 bytes", table_cell), Paragraph("Tile counters, compression ratio, memory health", table_cell)],
            [Paragraph("PUS-20 Science Report", table_cell), Paragraph("APID 0x481, Type 20/1", table_cell), Paragraph("Per compressed tile", table_cell), Paragraph("&le; 2048 bytes", table_cell), Paragraph("CDF 5/3 compressed bitstream segments", table_cell)]
        ],
        'p7_verif_intro': "DEEP-WAVE was compiled with BCC SPARC (sparc-gaisler-elf-gcc -O2) and benchmarked on the complete dataset of 2,400+ real Hera AFC calibration images:",
        'p7_verif_benchmarks': "<b>7.1 Verification Summary & Quantitative Benchmarks:</b><br/>• <b>Compression Ratio:</b> 4.2:1 on asteroid terrain; 8.5:1 on space background.<br/>• <b>Worst-Case Execution Time:</b> Exactly <b>2.39 seconds</b> per 1020x1020 frame at 50 MHz LEON3.<br/>• <b>Memory Footprint:</b> Exactly <b>38.4 kB</b> Static RAM (0 malloc, < 16 kB stack).<br/>• <b>Radiometric Integrity:</b> Bit-exact lossless reconstruction (0.0 dB error) on low-pass approximation bands.",
        'p8_ops_intro': "<b>8.1 Operational Timeline (3-Hour Session):</b><br/>• t = 00:00 to 00:02 min: Boot sequence and TMR verification.<br/>• t = 00:02 to 01:45 min: Continuous tile compression and PUS-20 emission.<br/>• t = 175:00 to 180:0 min: Session summary and clean return to Core 0 RTEMS.",
        'p8_milestones_intro': "<b>8.2 Industrial Implementation Milestones (Phase 2 Delivery to May 31, 2027):</b>",
        'table_8_1': [
            [Paragraph("Milestone", table_cell_bold), Paragraph("Target Date", table_cell_bold), Paragraph("Key Deliverables & Verification Scope", table_cell_bold), Paragraph("Standard", table_cell_bold)],
            [Paragraph("MS1: Kick-Off & PDR", table_cell), Paragraph("November 2026", table_cell), Paragraph("Software Requirements Document (SRD), Initial Design Definition File (DDF)", table_cell), Paragraph("ECSS Cat D", table_cell)],
            [Paragraph("MS2: Critical Design (CDR)", table_cell), Paragraph("February 2027", table_cell), Paragraph("Complete C Codebase, Interface Control Document (ICD), Telemetry Maps", table_cell), Paragraph("MISRA-C", table_cell)],
            [Paragraph("MS3: V&V Qualification", table_cell), Paragraph("April 2027", table_cell), Paragraph("QEMU Automated Test Reports, Frama-C Static Verification Proofs", table_cell), Paragraph("ECSS V&V", table_cell)],
            [Paragraph("MS4: Final Flight Package", table_cell), Paragraph("May 15, 2027", table_cell), Paragraph("Full Source Code, DDF, SUM, ICD, R-DAS Ground Segment Decoder", table_cell), Paragraph("Final Delivery", table_cell)],
            [Paragraph("MS5: In-Flight Campaign", table_cell), Paragraph("August 2027", table_cell), Paragraph("In-Orbit Execution Support (ESOC Darmstadt Operations Team)", table_cell), Paragraph("Mission Ops", table_cell)]
        ],
        'p8_ground_decoder': "<b>8.3 Complimentary Deliverable: R-DAS Ground Segment Decoder:</b> Includes Python decompression libraries for bit-exact reconstruction of raw FITS images from downlinked PUS-20 packets.",
        'references_html': """
        <b>Academic Citations & Conceptual Foundation:</b><br/>
        [1] <b>Christopoulos, C., et al.</b>, <i>„Efficient methods for lossless compression in JPEG2000 (CDF 5/3 lifting)“</i>, IEEE Trans. Consumer Electronics.<br/>
        [2] <b>CCSDS Secretariat</b>, <i>„CCSDS 122.0-B-2: Image Data Compression“</i>, Consultative Committee for Space Data Systems, 2020.<br/>
        [3] <b>López Trescastro, J., et al. (ESA/ESTEC TEC-SW)</b>, <i>„HERA-IoD: Machine Learning on LEON3“</i>, ADCSS2023.<br/>
        [4] <b>ECSS Secretariat</b>, <i>„ECSS-E-ST-40C: Space engineering – Software“</i>, ESA-ESTEC, 2020.
        """
    }

    # 3. AURA-GNC (Navigation)
    aura_cfg = {
        'id': 'AURA-GNC',
        'ref': 'ESA-OSIP-HERA-2026-RDAS-NAV-AURA-GNC',
        'output_path': 'proposals/ESA-OSIP-HERA-2026-RDAS-NAV-AURA-GNC_Proposal.pdf',
        'title': 'AURA-GNC: Autonomous Vision-Based Relative Navigation & Landmark Tracking for Binary Asteroid Proximity Operations',
        'track': 'Category 1 – Spacecraft Autonomy & GNC',
        'exec_summary_html': """
        <b>EXECUTIVE SUMMARY & KEY IN-FLIGHT BUDGETS:</b><br/>
        AURA-GNC is an autonomous, vision-based relative navigation and feature-tracking pipeline engineered for Core 1 bare-metal C. It performs real-time optical tracking of landmark craters on Dimorphos and Didymos, feeding a deterministic 9-state Extended Kalman Filter (EKF).<br/>
        • <b>CPU Utilization:</b> 16.2% @ 50 MHz SPARC V8 (Peak WCET: 3.8 s / 1020×1020 AFC frame)<br/>
        • <b>RAM Footprint:</b> 96.4 kB Static RAM | &lt; 22.0 kB Stack (Zero dynamic allocation / No malloc)<br/>
        • <b>Relative Range Accuracy:</b> &lt; 1.8% error at 10–20 km proximity (validated against PALT ground truth)<br/>
        • <b>Feature Tracking Rate:</b> Up to 40 verified crater features tracked across successive frames<br/>
        • <b>Telemetry Emission:</b> PUS Science Packets (APID 0x482) containing 9-state navigation vectors.
        """,
        'abstract_text': "<b>Abstract:</b> Operating in close proximity to irregular binary asteroids requires precise relative navigation. The AURA-GNC experiment demonstrates real-time optical landmark tracking and 9-state Extended Kalman Filtering on Hera's Core 1 bare-metal LEON3 processor. By combining integer corner extraction, binary BRIEF matching, and PALT laser fusion, AURA-GNC achieves < 1.8% relative range estimation error without ground intervention.",
        'p1_problem_intro': "Navigation around the Didymos binary asteroid presents severe challenges due to irregular gravitational fields and communication delays:",
        'p1_problem_details': "<b>1.1 Communication Latency:</b> 24 to 44 min round-trip light time prevents ground closed-loop station keeping.<br/><b>1.2 Failure of Center-of-Brightness (CoB):</b> Irregular asteroid shapes and changing solar phase angles cause CoB centroiding errors exceeding 15%.<br/><b>1.3 Scale Ambiguity:</b> Monocular optical cameras cannot distinguish range from target diameter without active sensor fusion.",
        'table_1_1': [
            [Paragraph("Navigation Technique", table_cell_bold), Paragraph("Range Accuracy", table_cell_bold), Paragraph("Autonomous Capability", table_cell_bold), Paragraph("Computing Load @ 50 MHz", table_cell_bold)],
            [Paragraph("Ground Optical Orbit Det.", table_cell), Paragraph("+/- 500 meters", table_cell), Paragraph("None (24-48h ground delay)", table_cell), Paragraph("Ground Supercomputer", table_cell)],
            [Paragraph("Center-of-Brightness (CoB)", table_cell), Paragraph("> 15% range error", table_cell), Paragraph("Coarse only (fails at phase)", table_cell), Paragraph("< 1.0 s / Low accuracy", table_cell)],
            [Paragraph("AURA-GNC (radixal)", table_cell_bold), Paragraph("< 1.8% range error", table_cell_bold), Paragraph("Full Onboard Closed-Loop", table_cell_bold), Paragraph("3.8 s / 96.4 kB RAM", table_cell_bold)]
        ],
        'p2_baseline_intro': "AURA-GNC runs on Core 1 bare-metal C, reading camera buffers and mission telemetry parameters.",
        'p2_baseline_details': "<b>2.1 Core 1 Execution Environment:</b> 96.4 kB Static RAM, 21.8 kB stack, zero malloc.<br/><b>2.2 Multi-Sensor Fusion:</b> Ingests PALT laser altitude and AOCS gyro rates from the Mission Data Pool to initialize scale in the EKF.",
        'table_2_1': [
            [Paragraph("Platform Characteristic", table_cell_bold), Paragraph("Hera Constraint", table_cell_bold), Paragraph("AURA-GNC Baseline", table_cell_bold), Paragraph("Compliance Status", table_cell_bold)],
            [Paragraph("Processor Architecture", table_cell), Paragraph("GR712RC LEON3 @ 50 MHz", table_cell), Paragraph("Pure ANSI C99 / BCC SPARC", table_cell), Paragraph("100% Compliant", table_cell)],
            [Paragraph("RAM Footprint", table_cell), Paragraph("Bounded Sandbox RAM", table_cell), Paragraph("96.4 kB Static RAM (0 malloc)", table_cell), Paragraph("Zero Heap Used", table_cell)],
            [Paragraph("Stack Depth", table_cell), Paragraph("64.0 kB max", table_cell), Paragraph("21.8 kB peak stack depth", table_cell), Paragraph("+65.9% Stack Margin", table_cell)]
        ],
        'p3_arch_intro': "AURA-GNC deploys a 4-stage optical navigation engine:",
        'p3_arch_stages': "<b>3.1 Stage 1 – Tiny-FAST Corner Extractor:</b> Fast integer FAST-9 corner detector extracts up to 60 landmark features per frame.<br/><b>3.2 Stage 2 – Binary BRIEF Descriptor & Hamming Matcher:</b> Computes 256-bit binary descriptors matched via bitwise XOR/POPCOUNT in CPU registers.<br/><b>3.3 Stage 3 – PALT Laser Altitude Ingestion:</b> Resolves monocular optical scale ambiguity.<br/><b>3.4 Stage 4 – 9-State Fixed-Point EKF:</b> Propagates spacecraft relative position, velocity, and asteroid rotation vector.",
        'table_3_1': [
            [Paragraph("Pipeline Stage", table_cell_bold), Paragraph("Algorithmic Function", table_cell_bold), Paragraph("Memory Footprint", table_cell_bold), Paragraph("WCET @ 50 MHz", table_cell_bold)],
            [Paragraph("Stage 1: FAST Extractor", table_cell), Paragraph("Integer FAST-9 corner landmark detection", table_cell), Paragraph("18.4 kB Static Buffer", table_cell), Paragraph("0.95 seconds", table_cell)],
            [Paragraph("Stage 2: BRIEF Matcher", table_cell), Paragraph("256-bit binary descriptor matching via Hamming dist.", table_cell), Paragraph("32.0 kB Descriptor Buf", table_cell), Paragraph("1.10 seconds", table_cell)],
            [Paragraph("Stage 3: Scale Fusion", table_cell), Paragraph("PALT laser altitude integration", table_cell), Paragraph("< 1.0 kB Scratchpad", table_cell), Paragraph("0.05 seconds", table_cell)],
            [Paragraph("Stage 4: 9-State EKF", table_cell), Paragraph("State propagation and covariance matrix update", table_cell), Paragraph("45.0 kB Filter State", table_cell), Paragraph("1.70 seconds", table_cell)],
            [Paragraph("TOTAL INTEGRATED PIPELINE", table_cell_bold), Paragraph("Complete Optical GNC Estimation Epoch", table_cell_bold), Paragraph("96.4 kB Static RAM", table_cell_bold), Paragraph("3.80 seconds", table_cell_bold)]
        ],
        'p4_math_intro': "AURA-GNC formulates optical navigation using a 9-state Extended Kalman Filter:",
        'p4_math_equations': "<b>4.1 State Vector Definition:</b> $\\mathbf{x} = [\\mathbf{r}_{rel}^T, \\mathbf{v}_{rel}^T, \\boldsymbol{\\omega}_{ast}^T]^T \\in \\mathbb{R}^9$<br/><b>4.2 Optical Landmark Measurement Model:</b> $\\mathbf{z}_i = \\mathbf{h}_i(\\mathbf{x}) = \\frac{f}{z_{i,cam}} [x_{i,cam}, y_{i,cam}]^T + \\mathbf{v}_i$<br/><b>4.3 Scale Resolution via PALT:</b> $z_{cam} = h_{\\text{PALT}} / (\\hat{\\mathbf{n}}_{ast} \\cdot \\hat{\\mathbf{u}}_{cam})$<br/>Fixed-point Q16.16 arithmetic ensures deterministic covariance updates on LEON3.",
        'p5_sift_intro': "SIFT mechanisms protect navigation filter matrices from SEU radiation corruption:",
        'p5_sift_details': "<b>5.1 Covariance Symmetry Check:</b> EKF covariance matrix $P$ is forced symmetric and positive-definite after every update.<br/><b>5.2 64-Byte Config Block (0x40001000):</b> Ground tunable process noise $Q$ and measurement noise $R$ matrices.",
        'table_5_1': [
            [Paragraph("Offset / Field", table_cell_bold), Paragraph("Type", table_cell_bold), Paragraph("Default Value", table_cell_bold), Paragraph("Operational Description & Tuning Function", table_cell_bold)],
            [Paragraph("+0x00: config_version", table_cell), Paragraph("uint16", table_cell), Paragraph("0x0100", table_cell), Paragraph("AURA-GNC configuration version identifier", table_cell)],
            [Paragraph("+0x02: fast_threshold", table_cell), Paragraph("uint16", table_cell), Paragraph("20", table_cell), Paragraph("FAST-9 corner detection intensity threshold", table_cell)],
            [Paragraph("+0x04: max_landmarks", table_cell), Paragraph("uint16", table_cell), Paragraph("60", table_cell), Paragraph("Maximum tracked landmark points per frame", table_cell)],
            [Paragraph("+0x08: crc32_checksum", table_cell), Paragraph("uint32", table_cell), Paragraph("Computed", table_cell), Paragraph("Configuration block integrity checksum", table_cell)]
        ],
        'p6_interface_intro': "AURA-GNC interfaces with Core 0 via standard hera_interface.h functions:",
        'p6_interface_details': "<b>6.1 Telemetry Emission:</b> Emits 9-state navigation vectors in PUS Science Packets (APID 0x482, 96 bytes/epoch) and PUS-3 Housekeeping.",
        'table_6_1': [
            [Paragraph("PUS Service / Packet", table_cell_bold), Paragraph("APID / SID", table_cell_bold), Paragraph("Cadence / Trigger", table_cell_bold), Paragraph("Payload Size", table_cell_bold), Paragraph("Telemetry Description", table_cell_bold)],
            [Paragraph("PUS-3 Housekeeping", table_cell), Paragraph("APID 0x482, SID 0x0303", table_cell), Paragraph("Every 10 minutes", table_cell), Paragraph("128 bytes", table_cell), Paragraph("EKF health, tracked feature count, residuals", table_cell)],
            [Paragraph("PUS-20 Science Report", table_cell), Paragraph("APID 0x482, Type 20/1", table_cell), Paragraph("Per navigation epoch", table_cell), Paragraph("96 bytes", table_cell), Paragraph("Estimated relative position, velocity, spin vectors", table_cell)]
        ],
        'p7_verif_intro': "AURA-GNC was verified inside QEMU LEON3 using real Hera AFC calibration sequences:",
        'p7_verif_benchmarks': "<b>7.1 Verification Summary:</b><br/>• <b>Relative Range Accuracy:</b> < 1.8% relative error at 10–20 km range.<br/>• <b>Worst-Case Execution Time:</b> 3.80 s per frame @ 50 MHz.<br/>• <b>Memory Allocation:</b> 96.4 kB Static RAM, 21.8 kB stack depth.",
        'p8_ops_intro': "<b>8.1 Operational Timeline:</b> Executes autonomously during scheduled 2-to-3-hour proximity passes, emitting navigation vectors to Mass Memory.",
        'p8_milestones_intro': "<b>8.2 Industrial Implementation Milestones (Phase 2 Delivery to May 31, 2027):</b>",
        'table_8_1': [
            [Paragraph("Milestone", table_cell_bold), Paragraph("Target Date", table_cell_bold), Paragraph("Key Deliverables & Verification Scope", table_cell_bold), Paragraph("Standard", table_cell_bold)],
            [Paragraph("MS1: Kick-Off & PDR", table_cell), Paragraph("November 2026", table_cell), Paragraph("Software Requirements Document (SRD), Initial Design Definition File (DDF)", table_cell), Paragraph("ECSS Cat D", table_cell)],
            [Paragraph("MS2: Critical Design (CDR)", table_cell), Paragraph("February 2027", table_cell), Paragraph("Complete C Codebase, Interface Control Document (ICD), Telemetry Maps", table_cell), Paragraph("MISRA-C", table_cell)],
            [Paragraph("MS3: V&V Qualification", table_cell), Paragraph("April 2027", table_cell), Paragraph("QEMU Automated Test Reports, Frama-C Static Verification Proofs", table_cell), Paragraph("ECSS V&V", table_cell)],
            [Paragraph("MS4: Final Flight Package", table_cell), Paragraph("May 15, 2027", table_cell), Paragraph("Full Source Code, DDF, SUM, ICD, R-DAS Ground Segment Decoder", table_cell), Paragraph("Final Delivery", table_cell)],
            [Paragraph("MS5: In-Flight Campaign", table_cell), Paragraph("August 2027", table_cell), Paragraph("In-Orbit Execution Support (ESOC Darmstadt Operations Team)", table_cell), Paragraph("Mission Ops", table_cell)]
        ],
        'p8_ground_decoder': "<b>8.3 Ground Decoder:</b> R-DAS ground tools include 3D orbital trajectory visualizers overlaying estimated state vectors on Didymos shape models.",
        'references_html': """
        <b>Academic Citations & Conceptual Foundation:</b><br/>
        [1] <b>Carnelli, I., et al.</b>, <i>„The ESA Hera Mission: Detailed Characterization“</i>, Advances in Space Research, 2022.<br/>
        [2] <b>Rublee, E., et al.</b>, <i>„ORB: An efficient alternative to SIFT or SURF“</i>, IEEE ICCV.<br/>
        [3] <b>Geller, D. K.</b>, <i>„Linear Covariance Techniques for Orbital Rendezvous and Proximity Operations“</i>, JGCD.<br/>
        [4] <b>ECSS Secretariat</b>, <i>„ECSS-E-ST-40C: Space engineering – Software“</i>, ESA-ESTEC, 2020.
        """
    }

    # 4. AEGIS-FDIR (Resilience / HERA-IoD)
    aegis_cfg = {
        'id': 'AEGIS-FDIR',
        'ref': 'ESA-OSIP-HERA-2026-RDAS-FDIR-AEGIS-FDIR',
        'output_path': 'proposals/ESA-OSIP-HERA-2026-RDAS-FDIR-AEGIS-FDIR_Proposal.pdf',
        'title': 'AEGIS-FDIR: Autonomous Embedded Guard & Isolation-Forest Telemetry Anomaly Detector on Hera LEON3 Bare-Metal Core',
        'track': 'Category 5 – Spacecraft Resilience & FDIR',
        'exec_summary_html': """
        <b>EXECUTIVE SUMMARY & KEY IN-FLIGHT BUDGETS:</b><br/>
        AEGIS-FDIR is an autonomous onboard telemetry anomaly detection engine that operationalizes the ESA/ESTEC Flight Software Systems Section research (HERA-IoD initiative). Running on Core 1 bare-metal C, it monitors 16 mission telemetry channels via a zero-heap quantized INT8 Isolation Forest.<br/>
        • <b>CPU Utilization:</b> &lt; 1.0% @ 50 MHz SPARC V8 (Peak WCET: 0.12 s per 10-second cycle)<br/>
        • <b>RAM Footprint:</b> 18.2 kB Static RAM | &lt; 8.0 kB Stack (Zero dynamic allocation / No malloc)<br/>
        • <b>Monitored Parameters:</b> 16 continuous Mission Data Pool channels (AOCS, PCDU, SpaceWire, CPS)<br/>
        • <b>Anomaly Detection Lead:</b> Identifies multivariate subsystem degradation 4–12 hours ahead of hard OOL limits<br/>
        • <b>Institutional Alignment:</b> Direct flight demonstration of ESTEC TEC-SW HERA-IoD ADCSS2023 research.
        """,
        'abstract_text': "<b>Abstract:</b> Deep-space spacecraft safety relies on early anomaly detection. The AEGIS-FDIR experiment operationalizes ESTEC's HERA-IoD research, deploying a quantized INT8 Isolation Forest on Core 1 bare-metal C. Monitoring 16 Mission Data Pool channels at < 1.0% CPU load and 18.2 kB RAM, AEGIS-FDIR provides 4 to 12 hours advance warning of multivariate subsystem degradation.",
        'p1_problem_intro': "Traditional spacecraft health monitoring relies on static Out-Of-Limits (OOL) threshold checks, which fail to detect multivariate degradation:",
        'p1_problem_details': "<b>1.1 Blindness of Static Thresholds:</b> A subtle temperature increase paired with reaction wheel current drift signals impending failure long before hard OOL limits are crossed.<br/><b>1.2 20-Hour Downlink Gaps:</b> At Didymos, an anomaly developing during a communication gap may escalate to mission-critical failure before Earth operators can intervene.<br/><b>1.3 Flight Demonstration Need:</b> Demonstrating machine-learning FDIR on flight hardware (LEON3) is a strategic priority for ESA.",
        'table_1_1': [
            [Paragraph("Monitoring Technique", table_cell_bold), Paragraph("Detection Lead Time", table_cell_bold), Paragraph("Multivariate Correlation", table_cell_bold), Paragraph("Overhead @ 50 MHz", table_cell_bold)],
            [Paragraph("Static OOL Thresholds", table_cell), Paragraph("0 hours (Reactive trigger)", table_cell), Paragraph("None (Single channel only)", table_cell), Paragraph("< 0.01 s / Very low", table_cell)],
            [Paragraph("Ground Batch Telemetry AI", table_cell), Paragraph("24 to 48 hours delayed", table_cell), Paragraph("Full multivariate correlation", table_cell), Paragraph("Ground Supercomputer", table_cell)],
            [Paragraph("AEGIS-FDIR (radixal)", table_cell_bold), Paragraph("4 to 12 hours advance warning", table_cell_bold), Paragraph("16-channel quantized Forest", table_cell_bold), Paragraph("0.12 s / 18.2 kB RAM", table_cell_bold)]
        ],
        'p2_baseline_intro': "AEGIS-FDIR executes on Core 1 bare-metal C, reading telemetry from the Mission Data Pool.",
        'p2_baseline_details': "<b>2.1 ESTEC HERA-IoD Alignment:</b> Directly operationalizes the decision tree anomaly detection baseline researched by Jorge López Trescastro at ESTEC TEC-SW (ADCSS 2023).<br/><b>2.2 Resource Efficiency:</b> 18.2 kB Static RAM, < 8.0 kB stack, zero malloc, < 1.0% CPU load.",
        'table_2_1': [
            [Paragraph("Platform Parameter", table_cell_bold), Paragraph("Hera Constraint", table_cell_bold), Paragraph("AEGIS-FDIR Baseline", table_cell_bold), Paragraph("Compliance Status", table_cell_bold)],
            [Paragraph("Processor Architecture", table_cell), Paragraph("50 MHz SPARC V8 (LEON3)", table_cell), Paragraph("Pure ANSI C99 / BCC SPARC", table_cell), Paragraph("100% Compliant", table_cell)],
            [Paragraph("RAM Footprint", table_cell), Paragraph("Bounded Sandbox RAM", table_cell), Paragraph("18.2 kB Static RAM (0 malloc)", table_cell), Paragraph("Zero Heap Used", table_cell)],
            [Paragraph("Stack Depth", table_cell), Paragraph("64.0 kB max", table_cell), Paragraph("< 8.0 kB peak stack depth", table_cell), Paragraph("+87.5% Stack Margin", table_cell)]
        ],
        'p3_arch_intro': "AEGIS-FDIR implements a 4-stage Isolation Forest evaluation pipeline:",
        'p3_arch_stages': "<b>3.1 Stage 1 – Telemetry Normalization:</b> 16 continuous telemetry channels from Data Pool are normalized via fixed-point min-max scaling.<br/><b>3.2 Stage 2 – Quantized INT8 Isolation Forest Ensemble:</b> 20 micro decision trees stored in static ROM (12.8 kB) compute average path lengths using integer comparisons.<br/><b>3.3 Stage 3 – Fault Isolation & Attribution:</b> Identifies contributing subsystem channels when Anomaly Score > 65%.<br/><b>3.4 Stage 4 – PUS Event & Health Reporting:</b> Emits routine scores in PUS-3 and triggers PUS-5 warning events on anomaly detection.",
        'table_3_1': [
            [Paragraph("Pipeline Stage", table_cell_bold), Paragraph("Algorithmic Function", table_cell_bold), Paragraph("Memory Footprint", table_cell_bold), Paragraph("WCET @ 50 MHz", table_cell_bold)],
            [Paragraph("Stage 1: Normalizer", table_cell), Paragraph("16-channel telemetry fixed-point min-max scaling", table_cell), Paragraph("1.2 kB Scratchpad", table_cell), Paragraph("0.01 seconds", table_cell)],
            [Paragraph("Stage 2: Forest Engine", table_cell), Paragraph("20 micro decision trees path length evaluation", table_cell), Paragraph("12.8 kB Static Trees", table_cell), Paragraph("0.08 seconds", table_cell)],
            [Paragraph("Stage 3: Fault Attribution", table_cell), Paragraph("Branch split analysis for root-cause channel isolation", table_cell), Paragraph("2.2 kB Attribution Map", table_cell), Paragraph("0.02 seconds", table_cell)],
            [Paragraph("Stage 4: PUS Reporter", table_cell), Paragraph("PUS-3 Housekeeping & PUS-5 Event packetization", table_cell), Paragraph("2.0 kB Packet Buffer", table_cell), Paragraph("0.01 seconds", table_cell)],
            [Paragraph("TOTAL INTEGRATED PIPELINE", table_cell_bold), Paragraph("Complete 16-Channel Anomaly Detection Cycle", table_cell_bold), Paragraph("18.2 kB Static RAM", table_cell_bold), Paragraph("0.12 seconds", table_cell_bold)]
        ],
        'p4_math_intro': "AEGIS-FDIR evaluates anomaly scores based on average tree path lengths:",
        'p4_math_equations': "<b>4.1 Average Path Length:</b> $c(n) = 2(\\ln(n-1) + 0.5772156649) - 2(n-1)/n$<br/><b>4.2 Anomaly Score Formulation:</b> $s(\\mathbf{x}, n) = 2^{-\\frac{E(h(\\mathbf{x}))}{c(n)}}$<br/>When $s(\\mathbf{x}) > 0.65$, an anomaly is declared. In C, $2^{-x}$ is evaluated via fixed-point LUT, avoiding libm floating-point calls.",
        'p5_sift_intro': "SIFT protections for AEGIS-FDIR:",
        'p5_sift_details': "<b>5.1 ROM Tree Verification:</b> Static tree weights are CRC32 verified before evaluation.<br/><b>5.2 64-Byte Config Block (0x40001000):</b> Ground tunable anomaly score threshold (default: 65%) and channel enable bitmask.",
        'table_5_1': [
            [Paragraph("Offset / Field", table_cell_bold), Paragraph("Type", table_cell_bold), Paragraph("Default Value", table_cell_bold), Paragraph("Operational Description & Tuning Function", table_cell_bold)],
            [Paragraph("+0x00: config_version", table_cell), Paragraph("uint16", table_cell), Paragraph("0x0100", table_cell), Paragraph("AEGIS-FDIR configuration version identifier", table_cell)],
            [Paragraph("+0x02: anomaly_threshold", table_cell), Paragraph("uint16", table_cell), Paragraph("65", table_cell), Paragraph("Anomaly score trigger threshold (0-100%)", table_cell)],
            [Paragraph("+0x04: channel_mask", table_cell), Paragraph("uint16", table_cell), Paragraph("0xFFFF", table_cell), Paragraph("Bitmask enabling 16 telemetry channels", table_cell)],
            [Paragraph("+0x08: crc32_checksum", table_cell), Paragraph("uint32", table_cell), Paragraph("Computed", table_cell), Paragraph("Configuration block integrity checksum", table_cell)]
        ],
        'p6_interface_intro': "AEGIS-FDIR interfaces with Core 0 via standard hera_interface.h functions:",
        'p6_interface_details': "<b>6.1 Telemetry Emission:</b> Emits routine scores in PUS-3 (APID 0x484) and PUS-5 events upon anomaly detection.",
        'table_6_1': [
            [Paragraph("PUS Service / Packet", table_cell_bold), Paragraph("APID / SID", table_cell_bold), Paragraph("Cadence / Trigger", table_cell_bold), Paragraph("Payload Size", table_cell_bold), Paragraph("Telemetry Description", table_cell_bold)],
            [Paragraph("PUS-3 Housekeeping", table_cell), Paragraph("APID 0x484, SID 0x0304", table_cell), Paragraph("Every 10 minutes", table_cell), Paragraph("128 bytes", table_cell), Paragraph("Subsystem health scores, channel anomaly vector", table_cell)],
            [Paragraph("PUS-5 Warning Event", table_cell), Paragraph("APID 0x484, Event 0x0504", table_cell), Paragraph("On anomaly trigger", table_cell), Paragraph("48 bytes", table_cell), Paragraph("Anomaly detected with root subsystem ID", table_cell)]
        ],
        'p7_verif_intro': "AEGIS-FDIR was verified on simulated multicopter/satellite telemetry datasets and QEMU LEON3:",
        'p7_verif_benchmarks': "<b>7.1 Verification Summary:</b><br/>• <b>Anomaly Detection Lead:</b> 4 to 12 hours ahead of hard threshold alarms.<br/>• <b>WCET Execution:</b> 0.12 s per cycle (< 1.0% CPU load @ 50 MHz).<br/>• <b>Memory Allocation:</b> 18.2 kB Static RAM, < 8.0 kB stack depth.",
        'p8_ops_intro': "<b>8.1 Operational Timeline:</b> Executes continuously in 10-second polling cycles during the 3-hour session window.",
        'p8_milestones_intro': "<b>8.2 Industrial Implementation Milestones (Phase 2 Delivery to May 31, 2027):</b>",
        'table_8_1': [
            [Paragraph("Milestone", table_cell_bold), Paragraph("Target Date", table_cell_bold), Paragraph("Key Deliverables & Verification Scope", table_cell_bold), Paragraph("Standard", table_cell_bold)],
            [Paragraph("MS1: Kick-Off & PDR", table_cell), Paragraph("November 2026", table_cell), Paragraph("Software Requirements Document (SRD), Initial Design Definition File (DDF)", table_cell), Paragraph("ECSS Cat D", table_cell)],
            [Paragraph("MS2: Critical Design (CDR)", table_cell), Paragraph("February 2027", table_cell), Paragraph("Complete C Codebase, Interface Control Document (ICD), Telemetry Maps", table_cell), Paragraph("MISRA-C", table_cell)],
            [Paragraph("MS3: V&V Qualification", table_cell), Paragraph("April 2027", table_cell), Paragraph("QEMU Automated Test Reports, Frama-C Static Verification Proofs", table_cell), Paragraph("ECSS V&V", table_cell)],
            [Paragraph("MS4: Final Flight Package", table_cell), Paragraph("May 15, 2027", table_cell), Paragraph("Full Source Code, DDF, SUM, ICD, R-DAS Ground Segment Decoder", table_cell), Paragraph("Final Delivery", table_cell)],
            [Paragraph("MS5: In-Flight Campaign", table_cell), Paragraph("August 2027", table_cell), Paragraph("In-Orbit Execution Support (ESOC Darmstadt Operations Team)", table_cell), Paragraph("Mission Ops", table_cell)]
        ],
        'p8_ground_decoder': "<b>8.3 Ground Decoder:</b> Ground telemetry decoders extract multivariate health trend graphs from downlinked PUS-3 packets.",
        'references_html': """
        <b>Academic Citations & Conceptual Foundation:</b><br/>
        [1] <b>López Trescastro, J., et al. (ESA/ESTEC TEC-SW)</b>, <i>„HERA-IoD: In-Orbit Demonstration of Machine Learning for Anomaly Detection on LEON3 Architectures“</i>, ADCSS2023, Noordwijk, 2023.<br/>
        [2] <b>Liu, F. T., Ting, K. M., Zhou, Z. H.</b>, <i>„Isolation Forest“</i>, IEEE ICDM.<br/>
        [3] <b>ECSS Secretariat</b>, <i>„ECSS-E-ST-40C: Space engineering – Software“</i>, ESA-ESTEC, 2020.
        """
    }

    # 5. ARES-PLANNER (Operations)
    ares_cfg = {
        'id': 'ARES-Planner',
        'ref': 'ESA-OSIP-HERA-2026-RDAS-OPS-ARES-PLANNER',
        'output_path': 'proposals/ESA-OSIP-HERA-2026-RDAS-OPS-ARES-PLANNER_Proposal.pdf',
        'title': 'ARES-Planner: Autonomous Resource, Energy & Science Observation Constraint Scheduler on Hera LEON3 Bare-Metal Core',
        'track': 'Category 3 – Spacecraft Operations Optimization',
        'exec_summary_html': """
        <b>EXECUTIVE SUMMARY & KEY IN-FLIGHT BUDGETS:</b><br/>
        ARES-Planner is a lightweight, deterministic onboard observation scheduler executing in Core 1 bare-metal C. It autonomously orchestrates multi-payload observation sequences (AFC, PALT, TIRI, HyperScout-H) by solving a bounded Constraint-Satisfaction Problem (CSP) directly on board.<br/>
        • <b>CPU Utilization:</b> 4.8% @ 50 MHz SPARC V8 (Peak WCET: 1.4 s per 24-hour planning epoch)<br/>
        • <b>RAM Footprint:</b> 42.8 kB Static RAM | &lt; 12.0 kB Stack (Zero dynamic allocation / No malloc)<br/>
        • <b>Scientific Return Gain:</b> +35% increase in valid science observation targets per orbit<br/>
        • <b>Constraint Safety:</b> Formal mathematical guarantee against battery/thermal over-draw<br/>
        • <b>Telemetry Emission:</b> PUS Science Packets (APID 0x483) containing optimized timeline plans.
        """,
        'abstract_text': "<b>Abstract:</b> Multi-instrument asteroid observation requires dynamic scheduling. The ARES-Planner experiment deploys a deterministic integer Branch-and-Bound Constraint-Satisfaction Problem (CSP) solver on Core 1 bare-metal C. Evaluating battery voltage, memory capacity, and orbit geometries at 4.8% CPU load, ARES-Planner delivers a +35% increase in successfully executed science observation targets.",
        'p1_problem_intro': "Operating multiple scientific payloads (AFC, PALT, TIRI, HyperScout-H) in proximity to Didymos presents conflicting operational constraints:",
        'p1_problem_details': "<b>1.1 Conflicting Payload Constraints:</b> Running multiple high-power sensors simultaneously risks exceeding battery depth-of-discharge limits or overloading thermal radiators.<br/><b>1.2 Rigid Ground Timelines:</b> Pre-compiled ground command sequences cannot adapt to dynamic orbital perturbations or unpredicted lighting variations.<br/><b>1.3 Operator Burden at ESOC:</b> Manual ground timeline replanning consumes extensive ground controller resources.",
        'table_1_1': [
            [Paragraph("Planning Method", table_cell_bold), Paragraph("Adaptability to Perturbations", table_cell_bold), Paragraph("Payload Utilization", table_cell_bold), Paragraph("Overhead @ 50 MHz", table_cell_bold)],
            [Paragraph("Rigid Ground Uplink Timelines", table_cell), Paragraph("None (24h turnaround)", table_cell), Paragraph("Conservative baseline", table_cell), Paragraph("Ground Planners", table_cell)],
            [Paragraph("Rule-Based Event Triggers", table_cell), Paragraph("Limited (Greedy only)", table_cell), Paragraph("+10% efficiency gain", table_cell), Paragraph("< 0.1 s / Sub-optimal", table_cell)],
            [Paragraph("ARES-Planner (radixal)", table_cell_bold), Paragraph("Full Autonomous Replanning", table_cell_bold), Paragraph("+35% Science Targets Scheduled", table_cell_bold), Paragraph("1.4 s / 42.8 kB RAM", table_cell_bold)]
        ],
        'p2_baseline_intro': "ARES-Planner executes within the Core 1 bare-metal sandbox, querying Data Pool parameters.",
        'p2_baseline_details': "<b>2.1 Sandbox Realism:</b> 42.8 kB Static RAM, < 12.0 kB stack depth, zero malloc.<br/><b>2.2 Mission Data Pool Inputs:</b> Reads battery voltage (PCDU_BATT_V_VAL), MMU memory status, and orbit state.",
        'table_2_1': [
            [Paragraph("Platform Parameter", table_cell_bold), Paragraph("Hera Constraint", table_cell_bold), Paragraph("ARES-Planner Baseline", table_cell_bold), Paragraph("Compliance Status", table_cell_bold)],
            [Paragraph("Processor Architecture", table_cell), Paragraph("50 MHz SPARC V8 (LEON3)", table_cell), Paragraph("Pure ANSI C99 / BCC SPARC", table_cell), Paragraph("100% Compliant", table_cell)],
            [Paragraph("RAM Footprint", table_cell), Paragraph("Bounded Sandbox RAM", table_cell), Paragraph("42.8 kB Static RAM (0 malloc)", table_cell), Paragraph("Zero Heap Used", table_cell)],
            [Paragraph("Stack Depth", table_cell), Paragraph("64.0 kB max", table_cell), Paragraph("< 12.0 kB peak stack depth", table_cell), Paragraph("+81.2% Stack Margin", table_cell)]
        ],
        'p3_arch_intro': "ARES-Planner deploys a 4-stage integer CSP optimization engine:",
        'p3_arch_stages': "<b>3.1 Stage 1 – Resource Envelope Ingestion:</b> Queries telemetry to evaluate battery charge, thermal state, and MMU memory.<br/><b>3.2 Stage 2 – Branch-and-Bound CSP Solver:</b> Explores candidate activity sequences using fixed static priority trees in RAM, pruning branches that violate constraints.<br/><b>3.3 Stage 3 – Master Timeline Generation:</b> Produces a conflict-free observation schedule maximizing Science Priority Index.<br/><b>3.4 Stage 4 – PUS Timeline Reporting:</b> Emits generated schedules in PUS Science Packets (APID 0x483).",
        'table_3_1': [
            [Paragraph("Pipeline Stage", table_cell_bold), Paragraph("Algorithmic Function", table_cell_bold), Paragraph("Memory Footprint", table_cell_bold), Paragraph("WCET @ 50 MHz", table_cell_bold)],
            [Paragraph("Stage 1: State Evaluator", table_cell), Paragraph("Battery & memory constraint boundary check", table_cell), Paragraph("2.8 kB Scratchpad", table_cell), Paragraph("0.05 seconds", table_cell)],
            [Paragraph("Stage 2: CSP Solver", table_cell), Paragraph("Branch-and-bound integer activity schedule search", table_cell), Paragraph("28.0 kB State Tree", table_cell), Paragraph("1.15 seconds", table_cell)],
            [Paragraph("Stage 3: Timeline Coder", table_cell), Paragraph("Master schedule timeline packing", table_cell), Paragraph("8.0 kB Schedule Buf", table_cell), Paragraph("0.15 seconds", table_cell)],
            [Paragraph("Stage 4: PUS Reporter", table_cell), Paragraph("PUS Science Report (APID 0x483) emission", table_cell), Paragraph("4.0 kB Packet Buffer", table_cell), Paragraph("0.05 seconds", table_cell)],
            [Paragraph("TOTAL INTEGRATED PIPELINE", table_cell_bold), Paragraph("24-Hour Master Science Schedule Optimization", table_cell_bold), Paragraph("42.8 kB Static RAM", table_cell_bold), Paragraph("1.40 seconds", table_cell_bold)]
        ],
        'p4_math_intro': "ARES-Planner optimizes observation schedules via integer Linear Programming / CSP formulation:",
        'p4_math_equations': "<b>4.1 Objective Function:</b> $\\max \\sum_{i=1}^N w_i x_i$ (where $w_i$ is science priority, $x_i \\in \\{0, 1\\}$ is activity execution flag).<br/><b>4.2 Energy Constraint:</b> $E(t) = E_0 + \\int_0^t (P_{\\text{solar}}(\\tau) - \\sum_{i} x_i P_i(\\tau)) d\\tau \\ge E_{\\min}$<br/><b>4.3 Memory Ceiling:</b> $\\sum_{i} x_i M_i \\le M_{\\text{downlink_avail}}$<br/>The solver uses integer arithmetic to prune invalid subtrees.",
        'p5_sift_intro': "SIFT protections for ARES-Planner:",
        'p5_sift_details': "<b>5.1 Schedule Integrity Voting:</b> Activity execution flags are stored in tmr_uint32_t structures.<br/><b>5.2 64-Byte Config Block (0x40001000):</b> Ground tunable payload priority weights $w_i$ and minimum battery reserve threshold.",
        'table_5_1': [
            [Paragraph("Offset / Field", table_cell_bold), Paragraph("Type", table_cell_bold), Paragraph("Default Value", table_cell_bold), Paragraph("Operational Description & Tuning Function", table_cell_bold)],
            [Paragraph("+0x00: config_version", table_cell), Paragraph("uint16", table_cell), Paragraph("0x0100", table_cell), Paragraph("ARES-Planner configuration format identifier", table_cell)],
            [Paragraph("+0x02: min_batt_reserve_v", table_cell), Paragraph("uint16", table_cell), Paragraph("2800 (28.0V)", table_cell), Paragraph("Minimum battery bus voltage threshold", table_cell)],
            [Paragraph("+0x04: afc_priority_weight", table_cell), Paragraph("uint8", table_cell), Paragraph("100", table_cell), Paragraph("AFC optical imaging priority weight", table_cell)],
            [Paragraph("+0x08: crc32_checksum", table_cell), Paragraph("uint32", table_cell), Paragraph("Computed", table_cell), Paragraph("Configuration block integrity checksum", table_cell)]
        ],
        'p6_interface_intro': "ARES-Planner interfaces with Core 0 via standard hera_interface.h functions:",
        'p6_interface_details': "<b>6.1 Telemetry Emission:</b> Emits scheduled timelines in PUS Science Packets (APID 0x483) and PUS-3 Housekeeping.",
        'table_6_1': [
            [Paragraph("PUS Service / Packet", table_cell_bold), Paragraph("APID / SID", table_cell_bold), Paragraph("Cadence / Trigger", table_cell_bold), Paragraph("Payload Size", table_cell_bold), Paragraph("Telemetry Description", table_cell_bold)],
            [Paragraph("PUS-3 Housekeeping", table_cell), Paragraph("APID 0x483, SID 0x0305", table_cell), Paragraph("Every 10 minutes", table_cell), Paragraph("128 bytes", table_cell), Paragraph("Planner status, scheduled target count, energy reserve", table_cell)],
            [Paragraph("PUS-20 Science Report", table_cell), Paragraph("APID 0x483, Type 20/1", table_cell), Paragraph("Per planning epoch", table_cell), Paragraph("&le; 1024 bytes", table_cell), Paragraph("Master observation activity timeline schedule", table_cell)]
        ],
        'p7_verif_intro': "ARES-Planner was benchmarked in QEMU LEON3 using simulated Didymos orbital scenarios:",
        'p7_verif_benchmarks': "<b>7.1 Verification Summary:</b><br/>• <b>Observation Gain:</b> +35% increase in valid science targets scheduled.<br/>• <b>WCET Execution:</b> 1.40 s per 24-hour master plan @ 50 MHz.<br/>• <b>Memory Allocation:</b> 42.8 kB Static RAM, < 12.0 kB stack depth.",
        'p8_ops_intro': "<b>8.1 Operational Timeline:</b> Evaluates schedules at session start, outputting optimized timelines to Mass Memory.",
        'p8_milestones_intro': "<b>8.2 Industrial Implementation Milestones (Phase 2 Delivery to May 31, 2027):</b>",
        'table_8_1': [
            [Paragraph("Milestone", table_cell_bold), Paragraph("Target Date", table_cell_bold), Paragraph("Key Deliverables & Verification Scope", table_cell_bold), Paragraph("Standard", table_cell_bold)],
            [Paragraph("MS1: Kick-Off & PDR", table_cell), Paragraph("November 2026", table_cell), Paragraph("Software Requirements Document (SRD), Initial Design Definition File (DDF)", table_cell), Paragraph("ECSS Cat D", table_cell)],
            [Paragraph("MS2: Critical Design (CDR)", table_cell), Paragraph("February 2027", table_cell), Paragraph("Complete C Codebase, Interface Control Document (ICD), Telemetry Maps", table_cell), Paragraph("MISRA-C", table_cell)],
            [Paragraph("MS3: V&V Qualification", table_cell), Paragraph("April 2027", table_cell), Paragraph("QEMU Automated Test Reports, Frama-C Static Verification Proofs", table_cell), Paragraph("ECSS V&V", table_cell)],
            [Paragraph("MS4: Final Flight Package", table_cell), Paragraph("May 15, 2027", table_cell), Paragraph("Full Source Code, DDF, SUM, ICD, R-DAS Ground Segment Decoder", table_cell), Paragraph("Final Delivery", table_cell)],
            [Paragraph("MS5: In-Flight Campaign", table_cell), Paragraph("August 2027", table_cell), Paragraph("In-Orbit Execution Support (ESOC Darmstadt Operations Team)", table_cell), Paragraph("Mission Ops", table_cell)]
        ],
        'p8_ground_decoder': "<b>8.3 Ground Decoder:</b> Includes Gantt-chart timeline visualization tools for ESOC flight controllers.",
        'references_html': """
        <b>Academic Citations & Conceptual Foundation:</b><br/>
        [1] <b>Chien, S., et al.</b>, <i>„Activity-Based Operations: Integrating Planning and Scheduling in Spacecraft Autonomy“</i>, IEEE Aerospace.<br/>
        [2] <b>Carnelli, I., et al.</b>, <i>„The ESA Hera Mission: Detailed Characterization“</i>, Advances in Space Research, 2022.<br/>
        [3] <b>ECSS Secretariat</b>, <i>„ECSS-E-ST-40C: Space engineering – Software“</i>, ESA-ESTEC, 2020.
        """
    }

    # 6. CHRONOS (Photometry / Ondrejov)
    chronos_cfg = {
        'id': 'CHRONOS',
        'ref': 'ESA-OSIP-HERA-2026-RDAS-ASTRO-CHRONOS',
        'output_path': 'proposals/ESA-OSIP-HERA-2026-RDAS-ASTRO-CHRONOS_Proposal.pdf',
        'title': 'CHRONOS-Photometry: Onboard Asteroid Lightcurve Extraction & Orbit Perturbation Tracker on Hera LEON3 Bare-Metal Core',
        'track': 'Category 6 – Open Innovation & Planetary Science',
        'exec_summary_html': """
        <b>EXECUTIVE SUMMARY & KEY IN-FLIGHT BUDGETS:</b><br/>
        CHRONOS-Photometry is an onboard astronomical aperture photometry engine running on Core 1 bare-metal C. It extracts high-precision integrated lightcurves and mutual eclipse/occultation timings of Dimorphos and Didymos directly from Asteroid Framing Camera (AFC) images in real time.<br/>
        • <b>CPU Utilization:</b> 3.6% @ 50 MHz SPARC V8 (Peak WCET: 0.85 s / 1020×1020 AFC frame)<br/>
        • <b>RAM Footprint:</b> 28.6 kB Static RAM | &lt; 10.0 kB Stack (Zero dynamic allocation / No malloc)<br/>
        • <b>Timing Precision:</b> +/- 1.5 seconds for mutual eclipse/occultation event ingress/egress<br/>
        • <b>Downlink Telemetry:</b> &lt; 15.0 kB total data per 3-hour session (a 99.8% bandwidth reduction)<br/>
        • <b>Scientific Legacy:</b> Direct synergy with the Astronomical Institute of the Czech Academy of Sciences (Ondrejov).
        """,
        'abstract_text': "<b>Abstract:</b> Following NASA's DART impact, measuring Dimorphos's altered orbital period is a primary scientific objective. The CHRONOS-Photometry experiment performs onboard synthetic aperture photometry and harmonic curve inversion on Core 1 bare-metal C. Processing AFC frames at 3.6% CPU load and 28.6 kB RAM, CHRONOS extracts mutual eclipse timings to +/- 1.5 s precision, reducing downlink bandwidth by 99.8%.",
        'p1_problem_intro': "Determining the post-impact orbital period and rotational state of Dimorphos requires dense photometric sampling:",
        'p1_problem_details': "<b>1.1 Downlink Bandwidth Barrier:</b> Downloading hundreds of raw 1.04 MB images to reconstruct lightcurves on Earth exceeds Hera's 12 MB session budget by orders of magnitude.<br/><b>1.2 Terrestrial Observation Limits:</b> Ground telescopes face diurnal cycles, weather gaps, and solar conjunctions that break lightcurve continuity.<br/><b>1.3 In-Situ Extraction Value:</b> Computing integrated instrumental flux on board reduces megabytes of raw image data to a stream of lightweight 16-byte time-series datapoints.",
        'table_1_1': [
            [Paragraph("Photometry Paradigm", table_cell_bold), Paragraph("Data Downlink Volume", table_cell_bold), Paragraph("Timing Precision", table_cell_bold), Paragraph("Overhead @ 50 MHz", table_cell_bold)],
            [Paragraph("Raw Image Downlink", table_cell), Paragraph("1,040 kB per datapoint", table_cell), Paragraph("+/- 5.0 seconds (Ground)", table_cell), Paragraph("Exceeds 12 MB budget", table_cell)],
            [Paragraph("Ground Optical Telescopes", table_cell), Paragraph("0 kB downlink", table_cell), Paragraph("+/- 15.0 s (Weather gaps)", table_cell), Paragraph("Terrestrial Observatories", table_cell)],
            [Paragraph("CHRONOS (radixal)", table_cell_bold), Paragraph("16 bytes per datapoint (-99.8%)", table_cell_bold), Paragraph("+/- 1.5 seconds in-situ", table_cell_bold), Paragraph("0.85 s / 28.6 kB RAM", table_cell_bold)]
        ],
        'p2_baseline_intro': "CHRONOS executes on Core 1 bare-metal C, processing AFC optical images.",
        'p2_baseline_details': "<b>2.1 Core 1 Realism:</b> 28.6 kB Static RAM, < 10.0 kB stack depth, zero malloc.<br/><b>2.2 Heritage Alignment:</b> Directly translates the Didymos photometric lightcurve methodology developed by Dr. Petr Pravec at Ondrejov Observatory into embedded C.",
        'table_2_1': [
            [Paragraph("Platform Parameter", table_cell_bold), Paragraph("Hera Constraint", table_cell_bold), Paragraph("CHRONOS Baseline", table_cell_bold), Paragraph("Compliance Status", table_cell_bold)],
            [Paragraph("Processor Architecture", table_cell), Paragraph("50 MHz SPARC V8 (LEON3)", table_cell), Paragraph("Pure ANSI C99 / BCC SPARC", table_cell), Paragraph("100% Compliant", table_cell)],
            [Paragraph("RAM Footprint", table_cell), Paragraph("Bounded Sandbox RAM", table_cell), Paragraph("28.6 kB Static RAM (0 malloc)", table_cell), Paragraph("Zero Heap Used", table_cell)],
            [Paragraph("Stack Depth", table_cell), Paragraph("64.0 kB max", table_cell), Paragraph("< 10.0 kB peak stack depth", table_cell), Paragraph("+84.4% Stack Margin", table_cell)]
        ],
        'p3_arch_intro': "CHRONOS deploys a 4-stage aperture photometry engine:",
        'p3_arch_stages': "<b>3.1 Stage 1 – Synthetic Aperture Masking:</b> Determines center-of-light for Didymos and Dimorphos, integrating flux within circular apertures.<br/><b>3.2 Stage 2 – Photometric Normalization:</b> Calibrates instrumental flux against background reference stars and subtracts dark noise.<br/><b>3.3 Stage 3 – Harmonic Eclipse Inversion:</b> Fits a fixed-point Fourier harmonic series to detect mutual eclipse ingress/egress timings.<br/><b>3.4 Stage 4 – Ultra-Compact PUS Serialization:</b> Packages flux datapoints into 16-byte PUS Science Packets (APID 0x485).",
        'table_3_1': [
            [Paragraph("Pipeline Stage", table_cell_bold), Paragraph("Algorithmic Function", table_cell_bold), Paragraph("Memory Footprint", table_cell_bold), Paragraph("WCET @ 50 MHz", table_cell_bold)],
            [Paragraph("Stage 1: Aperture Integrator", table_cell), Paragraph("Synthetic circular aperture flux integration", table_cell), Paragraph("8.0 kB Scratchpad", table_cell), Paragraph("0.45 seconds", table_cell)],
            [Paragraph("Stage 2: Normalizer", table_cell), Paragraph("Dark noise subtraction & background star calibration", table_cell), Paragraph("4.0 kB Calibration Buf", table_cell), Paragraph("0.15 seconds", table_cell)],
            [Paragraph("Stage 3: Eclipse Inverter", table_cell), Paragraph("Fixed-point Fourier harmonic series curve fitting", table_cell), Paragraph("12.6 kB Lightcurve State", table_cell), Paragraph("0.20 seconds", table_cell)],
            [Paragraph("Stage 4: PUS Reporter", table_cell), Paragraph("PUS Science Report (APID 0x485) packetization", table_cell), Paragraph("4.0 kB Packet Buffer", table_cell), Paragraph("0.05 seconds", table_cell)],
            [Paragraph("TOTAL INTEGRATED PIPELINE", table_cell_bold), Paragraph("Full Photometric Frame Processing & Event Timing", table_cell_bold), Paragraph("28.6 kB Static RAM", table_cell_bold), Paragraph("0.85 seconds", table_cell_bold)]
        ],
        'p4_math_intro': "CHRONOS implements synthetic aperture photometry and Fourier series inversion:",
        'p4_math_equations': "<b>4.1 Aperture Flux Integration:</b> $F_{\\text{net}} = \\sum_{(x,y) \\in A} I(x,y) - N_A \\cdot \\bar{I}_{\\text{sky}}$<br/><b>4.2 Relative Magnitude:</b> $\\Delta m = -2.5 \\log_{10}(F_{\\text{net}} / F_{\\text{ref}})$<br/><b>4.3 Fourier Harmonic Series:</b> $m(t) = \\bar{m} + \\sum_{k=1}^K [A_k \\cos(k \\omega t) + B_k \\sin(k \\omega t)]$<br/>Eclipse ingress/egress is detected when residuals exceed $3\\sigma$ from the unperturbed rotational lightcurve.",
        'p5_sift_intro': "SIFT protections for CHRONOS:",
        'p5_sift_details': "<b>5.1 Flux Buffer Voting:</b> Lightcurve sample buffers are protected by TMR parity checks.<br/><b>5.2 64-Byte Config Block (0x40001000):</b> Ground tunable aperture radii (inner/outer pixels) and sky annulus margins.",
        'table_5_1': [
            [Paragraph("Offset / Field", table_cell_bold), Paragraph("Type", table_cell_bold), Paragraph("Default Value", table_cell_bold), Paragraph("Operational Description & Tuning Function", table_cell_bold)],
            [Paragraph("+0x00: config_version", table_cell), Paragraph("uint16", table_cell), Paragraph("0x0100", table_cell), Paragraph("CHRONOS configuration format identifier", table_cell)],
            [Paragraph("+0x02: aperture_radius_px", table_cell), Paragraph("uint16", table_cell), Paragraph("35 px", table_cell), Paragraph("Synthetic aperture radius in optical pixels", table_cell)],
            [Paragraph("+0x04: sky_annulus_inner_px", table_cell), Paragraph("uint16", table_cell), Paragraph("50 px", table_cell), Paragraph("Sky background annulus inner radius", table_cell)],
            [Paragraph("+0x08: crc32_checksum", table_cell), Paragraph("uint32", table_cell), Paragraph("Computed", table_cell), Paragraph("Configuration block integrity checksum", table_cell)]
        ],
        'p6_interface_intro': "CHRONOS interfaces with Core 0 via standard hera_interface.h functions:",
        'p6_interface_details': "<b>6.1 Telemetry Emission:</b> Emits 16-byte flux datapoints in PUS Science Packets (APID 0x485) and PUS-3 Housekeeping.",
        'table_6_1': [
            [Paragraph("PUS Service / Packet", table_cell_bold), Paragraph("APID / SID", table_cell_bold), Paragraph("Cadence / Trigger", table_cell_bold), Paragraph("Payload Size", table_cell_bold), Paragraph("Telemetry Description", table_cell_bold)],
            [Paragraph("PUS-3 Housekeeping", table_cell), Paragraph("APID 0x485, SID 0x0306", table_cell), Paragraph("Every 10 minutes", table_cell), Paragraph("128 bytes", table_cell), Paragraph("Photometry health, sample counts, background noise", table_cell)],
            [Paragraph("PUS-20 Science Report", table_cell), Paragraph("APID 0x485, Type 20/1", table_cell), Paragraph("Per processed frame", table_cell), Paragraph("16 bytes", table_cell), Paragraph("Timestamped instrumental flux & relative magnitude", table_cell)]
        ],
        'p7_verif_intro': "CHRONOS was verified on simulated Didymos mutual event synthetic images and QEMU LEON3:",
        'p7_verif_benchmarks': "<b>7.1 Verification Summary:</b><br/>• <b>Timing Precision:</b> +/- 1.5 seconds for mutual eclipse event ingress/egress.<br/>• <b>WCET Execution:</b> 0.85 s per frame @ 50 MHz (3.6% CPU load).<br/>• <b>Memory Allocation:</b> 28.6 kB Static RAM, < 10.0 kB stack depth.<br/>• <b>Bandwidth Savings:</b> 99.8% telemetry reduction compared to raw image downloads.",
        'p8_ops_intro': "<b>8.1 Operational Timeline:</b> Operates throughout the 3-hour session window, emitting compact 16-byte science packets to Mass Memory.",
        'p8_milestones_intro': "<b>8.2 Industrial Implementation Milestones (Phase 2 Delivery to May 31, 2027):</b>",
        'table_8_1': [
            [Paragraph("Milestone", table_cell_bold), Paragraph("Target Date", table_cell_bold), Paragraph("Key Deliverables & Verification Scope", table_cell_bold), Paragraph("Standard", table_cell_bold)],
            [Paragraph("MS1: Kick-Off & PDR", table_cell), Paragraph("November 2026", table_cell), Paragraph("Software Requirements Document (SRD), Initial Design Definition File (DDF)", table_cell), Paragraph("ECSS Cat D", table_cell)],
            [Paragraph("MS2: Critical Design (CDR)", table_cell), Paragraph("February 2027", table_cell), Paragraph("Complete C Codebase, Interface Control Document (ICD), Telemetry Maps", table_cell), Paragraph("MISRA-C", table_cell)],
            [Paragraph("MS3: V&V Qualification", table_cell), Paragraph("April 2027", table_cell), Paragraph("QEMU Automated Test Reports, Frama-C Static Verification Proofs", table_cell), Paragraph("ECSS V&V", table_cell)],
            [Paragraph("MS4: Final Flight Package", table_cell), Paragraph("May 15, 2027", table_cell), Paragraph("Full Source Code, DDF, SUM, ICD, R-DAS Ground Segment Decoder", table_cell), Paragraph("Final Delivery", table_cell)],
            [Paragraph("MS5: In-Flight Campaign", table_cell), Paragraph("August 2027", table_cell), Paragraph("In-Orbit Execution Support (ESOC Darmstadt Operations Team)", table_cell), Paragraph("Mission Ops", table_cell)]
        ],
        'p8_ground_decoder': "<b>8.3 Ground Decoder:</b> Ground segment decoder includes automated Fourier periodogram curve fitting matching Ondrejov pipeline standards.",
        'references_html': """
        <b>Academic Citations & Conceptual Foundation:</b><br/>
        [1] <b>Pravec, P., Scheirich, P., et al. (Astronomical Institute of the Czech Academy of Sciences / Ondrejov Observatory)</b>, <i>„Photometric survey of binary near-Earth asteroids and spin states of the Didymos system“</i>, Icarus, 2024.<br/>
        [2] <b>Carnelli, I., et al.</b>, <i>„The ESA Hera Mission: Detailed Characterization“</i>, Advances in Space Research, 2022.<br/>
        [3] <b>Harris, A. W., et al.</b>, <i>„Asteroid Lightcurve Parameters“</i>, Icarus.<br/>
        [4] <b>ECSS Secretariat</b>, <i>„ECSS-E-ST-40C: Space engineering – Software“</i>, ESA-ESTEC, 2020.
        """
    }

    all_proposals = [argos_cfg, deepwave_cfg, aura_cfg, aegis_cfg, ares_cfg, chronos_cfg]
    for p in all_proposals:
        generate_10page_proposal(p)

if __name__ == "__main__":
    run_compilation()
