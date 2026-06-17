#!/usr/bin/env python3
"""
Generate a well-formatted academic PDF for a maturita tesina.
Usage: python3 tesina_accademica.py
Output: Tesina_Accademica.pdf in current directory

Requires: python3-reportlab (install via apt, not pip -- PEP 668)
  $ apt-get install -y python3-reportlab

Template structure:
  - A4, 2.5cm margins
  - 10.5pt Helvetica body, justified
  - 15pt Helvetica-Bold H1, 12pt H2
  - Block quotes: oblique, indented 1.5cm
  - Title page with 3cm top spacer
  - Numbered chapters with PageBreak between
  - Bibliography section at end

Modify the 'story' list between the markers to customize content.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.colors import black

OUTPUT = "Tesina_Accademica.pdf"

doc = SimpleDocTemplate(OUTPUT, pagesize=A4,
    topMargin=2.5*cm, bottomMargin=2.5*cm,
    leftMargin=2.5*cm, rightMargin=2.5*cm)

# ── STYLES ──
title_style = ParagraphStyle('CustomTitle', fontSize=18, leading=22,
    spaceAfter=6, alignment=TA_CENTER, fontName='Helvetica-Bold')
subtitle_style = ParagraphStyle('Sub', fontSize=12, leading=15,
    alignment=TA_CENTER, fontName='Helvetica-Oblique', textColor=black)
author_style = ParagraphStyle('Auth', fontSize=11, leading=14,
    spaceAfter=20, alignment=TA_CENTER)
h1 = ParagraphStyle('H1', fontSize=15, leading=18,
    spaceBefore=18, spaceAfter=10, fontName='Helvetica-Bold')
h2 = ParagraphStyle('H2', fontSize=12, leading=15,
    spaceBefore=12, spaceAfter=6, fontName='Helvetica-Bold')
body = ParagraphStyle('Body', fontSize=10.5, leading=14,
    spaceAfter=8, alignment=TA_JUSTIFY, fontName='Helvetica')
quote = ParagraphStyle('Quote', parent=body, leftIndent=1.5*cm,
    rightIndent=1.5*cm, fontSize=10, leading=13,
    spaceBefore=8, spaceAfter=8, fontName='Helvetica-Oblique')
toc = ParagraphStyle('TOC', parent=body, fontSize=11, leading=16, leftIndent=0.5*cm)
formula = ParagraphStyle('Formula', parent=body, alignment=TA_CENTER,
    fontSize=11, spaceBefore=6, spaceAfter=6)

# ── CONTENT — BUILD THE story LIST ──
story = []

# Cover page
story.append(Spacer(1, 3*cm))
story.append(Paragraph("TITLE", title_style))
story.append(Spacer(1, 0.4*cm))
story.append(Paragraph("Subtitle line 1<br/>Subtitle line 2", subtitle_style))
story.append(Spacer(1, 0.6*cm))
story.append(Paragraph("Tesina di Maturita<br/>Anno scolastico 2025/2026", author_style))
story.append(PageBreak())

# Table of contents
story.append(Paragraph("Indice", h1))
story.append(Paragraph("1. Capitolo 1", toc))
story.append(Paragraph("2. Capitolo 2", toc))
story.append(PageBreak())

# Chapter example
story.append(Paragraph("1. Titolo Capitolo", h1))
story.append(Paragraph("Sottotitolo", h2))
story.append(Paragraph(
    "Testo del paragrafo. Scrivere in terza persona, con periodi complessi "
    "e subordinazione. Evitare espressioni colloquiali.",
    body))
story.append(Paragraph(
    "Citazione rientrata in corsivo.<br/>"
    "- Autore, Opera",
    quote))
story.append(Paragraph(
    "Formula: <b>Δx · Δp ≥ h / (4π)</b>",
    formula))

# Build PDF
doc.build(story)
print(f"PDF generato: {OUTPUT}")
