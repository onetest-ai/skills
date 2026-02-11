---
name: pptx
version: 1.0.0
author: onetest-ai
description: Create and edit PowerPoint presentations (.pptx) with design guidelines and visual QA.
tags: [document, powerpoint, presentation, office]
model-invocation: true

dependencies:
  python:
    - python-pptx>=0.6
    - Pillow>=10.0
  npm: []
  mcp: []
  system:
    - libreoffice
    - poppler

requires: []

permissions:
  filesystem: write
  network: false
  shell: true
  mcp_servers: []
---

# PowerPoint Processing

You are creating or editing .pptx files. Focus on content AND design — boring slides with default formatting are unacceptable.

## Quick Reference

| Task | Tool | Notes |
|------|------|-------|
| Read/extract text | `python-pptx` | Iterate shapes |
| Create presentation | `python-pptx` | Full Python API |
| Edit existing | `python-pptx` | Load, modify, save |
| Convert to PDF | LibreOffice | `soffice --headless --convert-to pdf` |
| Convert to images | LibreOffice + pdftoppm | PDF → PNG for visual QA |

## Reading Presentations

```python
from pptx import Presentation

prs = Presentation("input.pptx")
for i, slide in enumerate(prs.slides, 1):
    print(f"\n--- Slide {i} ---")
    for shape in slide.shapes:
        if shape.has_text_frame:
            for para in shape.text_frame.paragraphs:
                print(para.text)
        if shape.has_table:
            table = shape.table
            for row in table.rows:
                print([cell.text for cell in row.cells])
```

## Creating Presentations

```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

prs = Presentation()
prs.slide_width = Inches(13.333)   # 16:9 widescreen
prs.slide_height = Inches(7.5)

# --- Title Slide ---
slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank layout

# Background color
background = slide.background
fill = background.fill
fill.solid()
fill.fore_color.rgb = RGBColor(0x0D, 0x1B, 0x2A)  # dark blue

# Title text
from pptx.util import Inches, Pt
txBox = slide.shapes.add_textbox(Inches(1), Inches(2.5), Inches(11), Inches(2))
tf = txBox.text_frame
p = tf.paragraphs[0]
p.text = "Quarterly Report"
p.font.size = Pt(44)
p.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
p.font.bold = True
p.alignment = PP_ALIGN.LEFT

# Subtitle
p2 = tf.add_paragraph()
p2.text = "Q4 2025 Results"
p2.font.size = Pt(24)
p2.font.color.rgb = RGBColor(0x8E, 0xA8, 0xC8)

# --- Content Slide ---
slide2 = prs.slides.add_slide(prs.slide_layouts[6])

# Add table
rows, cols = 4, 3
table_shape = slide2.shapes.add_table(rows, cols, Inches(1.5), Inches(2), Inches(10), Inches(3.5))
table = table_shape.table

# Style table
headers = ["Metric", "Target", "Actual"]
for i, header in enumerate(headers):
    cell = table.cell(0, i)
    cell.text = header
    for paragraph in cell.text_frame.paragraphs:
        paragraph.font.bold = True
        paragraph.font.size = Pt(14)
        paragraph.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    cell.fill.solid()
    cell.fill.fore_color.rgb = RGBColor(0x0D, 0x1B, 0x2A)

# Add image
slide3 = prs.slides.add_slide(prs.slide_layouts[6])
slide3.shapes.add_picture("chart.png", Inches(1), Inches(1.5), width=Inches(11))

prs.save("presentation.pptx")
```

## Design Guidelines

### Before Starting

1. **Pick a bold color palette** — Commit to 3-4 colors. See palettes below.
2. **Choose a visual motif** — Consistent element that ties slides together (geometric shapes, gradients, icons)
3. **60-70% dominant color** — One color should dominate, not equal distribution

### Color Palettes

| Name | Primary | Secondary | Accent | Text |
|------|---------|-----------|--------|------|
| Midnight Executive | `#0D1B2A` | `#1B2838` | `#D4A84B` | `#FFFFFF` |
| Forest & Moss | `#1A2E1A` | `#2D4A2D` | `#A8C090` | `#F5F0E8` |
| Coral Energy | `#FF6B6B` | `#2C3E50` | `#F39C12` | `#FFFFFF` |
| Warm Terracotta | `#C4704A` | `#2C1810` | `#E8C9A0` | `#FFF8F0` |
| Ocean Gradient | `#0A1628` | `#1A3A5C` | `#4ECDC4` | `#FFFFFF` |
| Charcoal Minimal | `#2D2D2D` | `#F5F5F5` | `#E74C3C` | context |
| Teal Trust | `#006D77` | `#83C5BE` | `#FFDDD2` | `#001524` |

### Typography

| Element | Size | Weight |
|---------|------|--------|
| Slide title | 36-44pt | Bold |
| Section header | 20-24pt | Bold |
| Body text | 14-16pt | Regular |
| Captions | 10-12pt | Regular/Italic |

### Layout Rules

- **0.5" minimum margins** on all sides
- **0.3-0.5" spacing** between content blocks
- **Never center body text** — left-align for readability
- **Vary layouts** — never repeat the same layout on consecutive slides
- **Every slide needs a visual element** — icon, chart, image, or shape

### Anti-Patterns (Never Do These)

- Don't default to blue gradients on white — pick distinctive colors
- Don't use generic clip art or stock photos
- Don't put 200 words on a single slide
- Don't use bullet points on every slide — vary with icons, tables, visuals
- NEVER use accent lines under titles — hallmark of generic AI output
- Don't use identical font sizes for title and body

## QA Process (Required)

After creating a presentation, ALWAYS verify:

### 1. Content QA
- Check for placeholder text left in
- Verify data accuracy in tables/charts
- Ensure consistent terminology

### 2. Visual QA
Convert to images and inspect:

```bash
soffice --headless --convert-to pdf presentation.pptx
pdftoppm -png -r 200 presentation.pdf slide_preview
```

Then use Read tool to inspect each slide image. Check for:
- Text overflow or clipping
- Color contrast issues
- Alignment problems
- Missing images

### 3. Fix-and-Verify Loop

Assume there are problems. Your job is to find them. Do not declare success until you've completed at least one fix-and-verify cycle:
1. Generate → 2. Convert to images → 3. Inspect → 4. List issues → 5. Fix → 6. Re-verify

## Guidelines

- **Design matters** — A well-designed presentation communicates 10x better than bullet points
- **Less is more** — Fewer words per slide, larger text, more whitespace
- **Consistency** — Same colors, fonts, spacing throughout
- **python-pptx blank layout** — Use `slide_layouts[6]` (blank) for full control
- **Images** — Always specify width to control sizing
- **Tables** — Set column widths explicitly; auto-width is unreliable in pptx
