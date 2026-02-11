---
name: pdf
version: 1.0.0
author: onetest-ai
description: PDF processing — read, create, merge, split, watermark, fill forms, encrypt, and OCR scanned documents.
tags: [document, pdf, office]
model-invocation: true

dependencies:
  python:
    - pypdf>=4.0
    - pdfplumber>=0.11
    - reportlab>=4.0
  npm: []
  mcp: []
  system:
    - poppler

requires: []

permissions:
  filesystem: write
  network: false
  shell: true
  mcp_servers: []
---

# PDF Processing

You are handling PDF file operations. Choose the right tool for each task.

## Quick Reference

| Task | Tool | Example |
|------|------|---------|
| Read/extract text | `pdfplumber` | `page.extract_text()` |
| Extract tables | `pdfplumber` | `page.extract_tables()` |
| Merge PDFs | `pypdf` | `PdfWriter.append(reader)` |
| Split PDFs | `pypdf` | `writer.add_page(reader.pages[i])` |
| Rotate pages | `pypdf` | `page.rotate(90)` |
| Add watermark | `pypdf` | `page.merge_page(watermark)` |
| Create new PDF | `reportlab` | `Canvas` or `SimpleDocTemplate` |
| Fill forms | `pypdf` | `writer.update_page_form_field_values()` |
| Encrypt/decrypt | `pypdf` | `writer.encrypt()` / `reader.decrypt()` |
| OCR scanned PDF | `pytesseract` + `pdf2image` | Convert to images, then OCR |
| Convert to images | `pdftoppm` (CLI) | `pdftoppm -png input.pdf output` |
| CLI merge/split | `qpdf` | `qpdf --empty --pages a.pdf b.pdf -- out.pdf` |

## Reading PDFs

### Text Extraction (pdfplumber)

```python
import pdfplumber

with pdfplumber.open("input.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)
```

### Table Extraction

```python
with pdfplumber.open("input.pdf") as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            for row in table:
                print(row)
```

For structured analysis, convert tables to pandas DataFrames:

```python
import pandas as pd
df = pd.DataFrame(table[1:], columns=table[0])
```

## Merging PDFs

```python
from pypdf import PdfWriter

writer = PdfWriter()
for pdf_path in ["a.pdf", "b.pdf", "c.pdf"]:
    writer.append(pdf_path)
writer.write("merged.pdf")
writer.close()
```

## Splitting PDFs

```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    writer.write(f"page_{i+1}.pdf")
    writer.close()
```

## Creating New PDFs (reportlab)

### Simple Canvas

```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

c = canvas.Canvas("output.pdf", pagesize=letter)
c.setFont("Helvetica", 12)
c.drawString(72, 720, "Hello, World!")
c.save()
```

### Structured Documents (Platypus)

```python
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("output.pdf", pagesize=letter)
styles = getSampleStyleSheet()

elements = [
    Paragraph("Title", styles["Title"]),
    Spacer(1, 12),
    Paragraph("Body text here.", styles["Normal"]),
]
doc.build(elements)
```

**Important:** For subscripts/superscripts in reportlab, use `<sub>` and `<super>` markup tags. Never use Unicode superscript characters — they render incorrectly.

## Watermarks

```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
watermark = PdfReader("watermark.pdf").pages[0]

writer = PdfWriter()
for page in reader.pages:
    page.merge_page(watermark)
    writer.add_page(page)
writer.write("watermarked.pdf")
writer.close()
```

## Form Filling

```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("form.pdf")
writer = PdfWriter()
writer.append(reader)

# List form fields
for page in reader.pages:
    fields = page.get("/Annots")
    if fields:
        for field in fields:
            obj = field.get_object()
            name = obj.get("/T")
            print(f"Field: {name}")

# Fill fields
writer.update_page_form_field_values(
    writer.pages[0],
    {"field_name": "value"},
    auto_regenerate=False,
)
writer.write("filled.pdf")
```

## Encryption

```python
from pypdf import PdfWriter

writer = PdfWriter()
writer.append("input.pdf")
writer.encrypt(user_password="read_pass", owner_password="admin_pass")
writer.write("encrypted.pdf")
```

## OCR (Scanned PDFs)

```python
from pdf2image import convert_from_path
import pytesseract

images = convert_from_path("scanned.pdf")
for i, img in enumerate(images):
    text = pytesseract.image_to_string(img)
    print(f"--- Page {i+1} ---\n{text}")
```

## CLI Tools

### pdftoppm (convert to images)
```bash
pdftoppm -png -r 300 input.pdf output_prefix
```

### qpdf (merge, split, encrypt)
```bash
# Merge
qpdf --empty --pages a.pdf b.pdf -- merged.pdf

# Extract pages 1-3
qpdf input.pdf --pages . 1-3 -- extracted.pdf

# Decrypt
qpdf --decrypt input.pdf output.pdf
```

## Guidelines

- Always check if a PDF is encrypted before processing — use `reader.is_encrypted`
- For large PDFs, process pages in batches to manage memory
- When extracting tables, verify structure with a sample before processing all pages
- For form filling, inspect field names first — they're often non-obvious
- Prefer pdfplumber over pypdf for text extraction (better layout handling)
- Use CLI tools (qpdf, pdftoppm) for batch operations — they're faster than Python
