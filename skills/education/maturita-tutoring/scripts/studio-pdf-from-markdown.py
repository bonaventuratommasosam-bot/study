#!/usr/bin/env python3
"""
Generate a well-formatted study PDF from a markdown file.
Parses headers (# ## ###), tables (|...|), blockquotes (> ),
bullet lists (-), and numbered lists into a structured PDF.

Usage:
  python3 studio-pdf-from-markdown.py <input.md> [output.pdf]

Requires: python3-reportlab (install via apt -- not pip)
  $ apt-get install -y -qq python3-reportlab

Input markdown format (see fisica_completa_aggiornata.md for examples):
  - # Title -> H1 (14pt, bold, colored)
  - ## Subtitle -> H2 (12pt, bold, colored)
  - ### Sub-subtitle -> H3 (10.5pt, bold, colored)
  - | col1 | col2 | ... -> tables with header style
  - > text -> blockquote (indented, oblique)
  - - text -> bullet point
  - 1. text -> numbered list item
  - --- -> small spacer
  - **bold** -> <b>bold</b>
  - *italic* -> <i>italic</i>
"""
import sys, os, re

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
    from reportlab.lib.colors import HexColor, colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
except ImportError:
    import subprocess
    subprocess.run(['apt-get', 'install', '-y', '-qq', 'python3-reportlab'], check=True)
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
    from reportlab.lib.colors import HexColor, colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle


def make_table(data_rows, col_widths=None):
    """Create a styled table from a list of lists (first row = header)."""
    if not data_rows:
        return Spacer(1, 0.1*cm)
    t = Table(data_rows, colWidths=col_widths, repeatRows=1)
    style = [
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('LEADING', (0,0), (-1,-1), 11),
        ('BACKGROUND', (0,0), (-1,0), HexColor('#16213e')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.3, HexColor('#cccccc')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, HexColor('#f5f5ff')]),
    ]
    t.setStyle(TableStyle(style))
    return t


def parse_markdown_to_pdf(md_text):
    """Convert markdown text into a list of PDF flowables."""
    story = []
    lines = md_text.split('\n')
    in_table = False
    table_buffer = []

    def flush_table():
        nonlocal table_buffer
        if not table_buffer:
            return
        rows = [r.split('|')[1:-1] for r in table_buffer if r.strip().startswith('|')]
        rows = [[c.strip() for c in r] for r in rows]
        rows = [r for r in rows if not all('-' in c.strip() for c in r)]
        if rows:
            story.append(make_table(rows))
        table_buffer = []
        nonlocal in_table
        in_table = False

    # Styles
    s_h1 = ParagraphStyle('H1', fontSize=14, leading=17, spaceBefore=12, spaceAfter=6,
                          fontName='Helvetica-Bold', textColor=HexColor('#16213e'))
    s_h2 = ParagraphStyle('H2', fontSize=12, leading=15, spaceBefore=9, spaceAfter=4,
                          fontName='Helvetica-Bold', textColor=HexColor('#0f3460'))
    s_h3 = ParagraphStyle('H3', fontSize=10.5, leading=13, spaceBefore=7, spaceAfter=3,
                          fontName='Helvetica-Bold', textColor=HexColor('#533483'))
    s_body = ParagraphStyle('Body', fontSize=9.5, leading=12.5, spaceAfter=4,
                            alignment=TA_JUSTIFY, fontName='Helvetica')
    s_quote = ParagraphStyle('Quote', parent=s_body, leftIndent=1*cm, rightIndent=0.5*cm,
                             fontSize=9, leading=12, fontName='Helvetica-Oblique',
                             textColor=HexColor('#444444'))

    for line in lines:
        stripped = line.strip()

        if not stripped:
            if in_table:
                flush_table()
            continue

        # Table row
        if stripped.startswith('|') and stripped.endswith('|'):
            in_table = True
            table_buffer.append(stripped)
            continue

        # Non-table content — flush table first
        if in_table:
            flush_table()

        # Headers
        if stripped.startswith('# ') and '️⃣' in stripped:
            title = stripped.lstrip('# ').strip()
            # Add page break before each numbered chapter (skip first)
            if story:
                story.append(PageBreak())
            story.append(Paragraph(title, s_h1))
        elif stripped.startswith('## '):
            txt = stripped.lstrip('# ').strip()
            if txt:
                story.append(Paragraph(txt, s_h2))
        elif stripped.startswith('### '):
            txt = stripped.lstrip('# ').strip()
            if txt:
                story.append(Paragraph(txt, s_h3))
        # Blockquotes
        elif stripped.startswith('> '):
            txt = stripped[2:].strip()
            txt = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', txt)
            story.append(Paragraph(txt, s_quote))
        # Horizontal rule
        elif stripped.startswith('---'):
            story.append(Spacer(1, 0.15*cm))
        # Bullet
        elif stripped.startswith('- '):
            txt = stripped[2:].strip()
            if '|' in txt:
                continue
            txt = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', txt)
            txt = re.sub(r'\*(.+?)\*', r'<i>\1</i>', txt)
            story.append(Paragraph(f'• {txt}', s_body))
        # Numbered list
        elif re.match(r'^\d+\.', stripped):
            txt = stripped.split('. ', 1)[-1] if '. ' in stripped else stripped
            txt = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', txt)
            txt = re.sub(r'\*(.+?)\*', r'<i>\1</i>', txt)
            story.append(Paragraph(f'  {txt}', s_body))
        elif stripped.startswith('```'):
            continue
        else:
            txt = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', stripped)
            txt = re.sub(r'\*(.+?)\*', r'<i>\1</i>', txt)
            if '|' not in txt:
                story.append(Paragraph(txt, s_body))

    flush_table()
    return story


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 studio-pdf-from-markdown.py <input.md> [output.pdf]")
        sys.exit(1)

    input_path = sys.argv[1]
    if not os.path.exists(input_path):
        print(f"File not found: {input_path}")
        sys.exit(1)

    output_path = sys.argv[2] if len(sys.argv) > 2 else input_path.rsplit('.', 1)[0] + '.pdf'

    with open(input_path, 'r') as f:
        md = f.read()

    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        topMargin=1.8*cm, bottomMargin=1.8*cm,
        leftMargin=2*cm, rightMargin=2*cm
    )

    story = parse_markdown_to_pdf(md)
    doc.build(story)
    print(f"PDF generato: {output_path}")
