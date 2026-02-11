---
name: docx
version: 1.0.0
author: onetest-ai
description: Create, read, and edit Word documents (.docx). Use for reports, memos, letters, or any .docx task.
tags: [document, word, office]
model-invocation: true

dependencies:
  python:
    - python-docx>=1.0
  npm: []
  mcp: []
  system:
    - pandoc
    - libreoffice

requires: []

permissions:
  filesystem: write
  network: false
  shell: true
  mcp_servers: []
---

# Word Document Processing

You are handling .docx files. A .docx is a ZIP archive containing XML files — understanding this is key for advanced editing.

## Quick Reference

| Task | Tool | Notes |
|------|------|-------|
| Read content | `pandoc` | `pandoc input.docx -t markdown` |
| Create new | `python-docx` | Full Python API for document creation |
| Edit existing | `python-docx` | Load, modify, save |
| Convert to PDF | LibreOffice | `soffice --headless --convert-to pdf` |
| Convert .doc → .docx | LibreOffice | `soffice --headless --convert-to docx` |
| Advanced XML edit | Unzip + edit + rezip | For tracked changes, comments, complex formatting |

## Reading Documents

### With pandoc (preferred for content extraction)

```bash
pandoc input.docx -t markdown
pandoc input.docx -t markdown --track-changes=all  # show tracked changes
```

### With python-docx

```python
from docx import Document

doc = Document("input.docx")
for para in doc.paragraphs:
    print(f"[{para.style.name}] {para.text}")

for table in doc.tables:
    for row in table.rows:
        print([cell.text for cell in row.cells])
```

## Creating New Documents

```python
from docx import Document
from docx.shared import Inches, Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()

# Title
title = doc.add_heading("Document Title", level=0)

# Body text
doc.add_paragraph("Introduction paragraph here.")

# Heading
doc.add_heading("Section 1", level=1)

# Formatted paragraph
p = doc.add_paragraph()
run = p.add_run("Bold text")
run.bold = True
p.add_run(" and normal text.")

# Bullet list
doc.add_paragraph("First item", style="List Bullet")
doc.add_paragraph("Second item", style="List Bullet")

# Table
table = doc.add_table(rows=3, cols=3, style="Table Grid")
table.cell(0, 0).text = "Header 1"
table.cell(0, 1).text = "Header 2"
table.cell(0, 2).text = "Header 3"

# Image
doc.add_picture("image.png", width=Inches(4))

# Page break
doc.add_page_break()

doc.save("output.docx")
```

### Styles and Formatting

```python
from docx.shared import Pt, RGBColor
from docx.enum.style import WD_STYLE_TYPE

# Custom style
style = doc.styles.add_style("CustomHeading", WD_STYLE_TYPE.PARAGRAPH)
font = style.font
font.name = "Arial"
font.size = Pt(16)
font.color.rgb = RGBColor(0x00, 0x33, 0x66)
font.bold = True

# Apply style
doc.add_paragraph("Custom Heading", style="CustomHeading")
```

### Headers and Footers

```python
section = doc.sections[0]
header = section.header
header.paragraphs[0].text = "Company Name"

footer = section.footer
footer.paragraphs[0].text = "Page "
# Page numbers require XML manipulation for dynamic numbering
```

### Page Setup

```python
from docx.shared import Inches, Cm

section = doc.sections[0]
section.page_width = Inches(8.5)    # US Letter
section.page_height = Inches(11)
section.left_margin = Inches(1)
section.right_margin = Inches(1)
section.top_margin = Inches(1)
section.bottom_margin = Inches(1)

# Landscape
section.orientation = 1  # WD_ORIENT.LANDSCAPE
section.page_width, section.page_height = section.page_height, section.page_width
```

## Editing Existing Documents

```python
from docx import Document

doc = Document("existing.docx")

# Replace text
for para in doc.paragraphs:
    if "OLD_TEXT" in para.text:
        for run in para.runs:
            run.text = run.text.replace("OLD_TEXT", "NEW_TEXT")

# Add content at the end
doc.add_paragraph("New paragraph added.")

doc.save("modified.docx")
```

**Important:** When replacing text, iterate over `runs` (not just `para.text`) to preserve formatting. A paragraph may be split across multiple runs with different formatting.

## Converting

### To PDF
```bash
soffice --headless --convert-to pdf input.docx
```

### To images (for visual inspection)
```bash
soffice --headless --convert-to pdf input.docx
pdftoppm -png -r 200 input.pdf preview
```

### .doc to .docx
```bash
soffice --headless --convert-to docx old_file.doc
```

## Guidelines

- **Read before editing** — Always examine the document structure before modifying
- **Preserve formatting** — When replacing text, work at the run level to keep bold/italic/etc.
- **Test with conversion** — Convert to PDF to verify the output looks correct
- **Handle encoding** — Use UTF-8 throughout; smart quotes in XML need proper entities
- **Large documents** — For very large docs, process sections/paragraphs incrementally
- **Templates** — When creating professional docs, start from a template document rather than from scratch
