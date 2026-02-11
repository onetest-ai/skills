# pdf

Full PDF processing: read, create, merge, split, rotate, watermark, fill forms, encrypt, and OCR.

## Usage

```
/pdf merge these three reports into one
/pdf extract the tables from quarterly_report.pdf
/pdf fill the tax form with my details
```

## Dependencies

- `pypdf` — merge, split, rotate, encrypt, forms
- `pdfplumber` — text/table extraction
- `reportlab` — create new PDFs
- `poppler` (system) — pdftoppm, pdftotext CLI tools

Install: `octo skills install pdf --deps`
