---
name: xlsx
version: 1.0.0
author: onetest-ai
description: Create, read, edit, and analyze Excel spreadsheets (.xlsx/.csv) with formulas and formatting.
tags: [document, excel, spreadsheet, office, data]
model-invocation: true

dependencies:
  python:
    - openpyxl>=3.1
    - pandas>=2.0
  npm: []
  mcp: []
  system:
    - libreoffice

requires: []

permissions:
  filesystem: write
  network: false
  shell: true
  mcp_servers: []
---

# Excel Spreadsheet Processing

You are handling Excel files (.xlsx). Use openpyxl for creating/editing with formatting and formulas, pandas for data analysis, and LibreOffice for formula recalculation.

## Critical Rule

**Always use Excel formulas, never hardcode calculated values.** Write `=SUM(B2:B10)` in a cell, not the Python-computed result. This ensures the spreadsheet remains interactive and recalculates when users change inputs.

## Quick Reference

| Task | Tool | Notes |
|------|------|-------|
| Read/analyze data | `pandas` | `pd.read_excel()` |
| Create with formulas | `openpyxl` | Full formatting + formula support |
| Edit existing | `openpyxl` | `load_workbook()` |
| Recalculate formulas | LibreOffice | `soffice --headless --calc` |
| CSV/TSV conversion | `pandas` | `pd.read_csv()` → `to_excel()` |

## Reading and Analyzing

### With pandas

```python
import pandas as pd

# Read Excel
df = pd.read_excel("data.xlsx", sheet_name="Sheet1")
df = pd.read_excel("data.xlsx", sheet_name=None)  # all sheets → dict

# Read CSV
df = pd.read_csv("data.csv")

# Quick analysis
print(df.describe())
print(df.info())
print(df.head(10))

# Filter, group, aggregate
result = df.groupby("category")["amount"].sum()
result = df[df["status"] == "active"].sort_values("date")
```

### With openpyxl (preserves formatting)

```python
from openpyxl import load_workbook

wb = load_workbook("data.xlsx")
ws = wb.active

for row in ws.iter_rows(min_row=1, max_row=10, values_only=True):
    print(row)

# Access specific cells
value = ws["B2"].value
formula = ws["B2"].value  # returns formula string if cell has one
```

## Creating Spreadsheets

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, numbers

wb = Workbook()
ws = wb.active
ws.title = "Report"

# Headers
headers = ["Item", "Quantity", "Price", "Total"]
for col, header in enumerate(headers, 1):
    cell = ws.cell(row=1, column=col, value=header)
    cell.font = Font(bold=True, size=12)
    cell.fill = PatternFill(start_color="003366", end_color="003366", fill_type="solid")
    cell.font = Font(bold=True, color="FFFFFF", size=12)
    cell.alignment = Alignment(horizontal="center")

# Data with FORMULAS (not computed values)
data = [
    ["Widget A", 100, 9.99],
    ["Widget B", 250, 14.50],
    ["Widget C", 75, 22.00],
]

for row_idx, row_data in enumerate(data, 2):
    for col_idx, value in enumerate(row_data, 1):
        ws.cell(row=row_idx, column=col_idx, value=value)
    # Formula for total: =B*C
    ws.cell(row=row_idx, column=4, value=f"=B{row_idx}*C{row_idx}")

# Summary row with formulas
last_row = len(data) + 2
ws.cell(row=last_row, column=1, value="TOTAL")
ws.cell(row=last_row, column=1).font = Font(bold=True)
ws.cell(row=last_row, column=4, value=f"=SUM(D2:D{last_row-1})")

# Number formatting
for row in ws.iter_rows(min_row=2, min_col=3, max_col=4):
    for cell in row:
        cell.number_format = '$#,##0.00'

# Column widths
ws.column_dimensions["A"].width = 20
ws.column_dimensions["B"].width = 12
ws.column_dimensions["C"].width = 12
ws.column_dimensions["D"].width = 15

wb.save("report.xlsx")
```

## Editing Existing Files

```python
from openpyxl import load_workbook

wb = load_workbook("existing.xlsx")
ws = wb.active

# Modify cells
ws["A1"] = "Updated Value"

# Insert row
ws.insert_rows(3)
ws.cell(row=3, column=1, value="New Row")

# Delete row
ws.delete_rows(5)

# Add new sheet
ws2 = wb.create_sheet("Summary")
ws2["A1"] = "Summary Data"

wb.save("modified.xlsx")
```

## Formatting Standards

### Professional Color Coding (Financial Models)

| Color | Meaning | Hex |
|-------|---------|-----|
| Blue text | Input/assumption (user-editable) | `0000FF` |
| Black text | Formula (calculated) | `000000` |
| Green text | Cross-sheet reference | `008000` |
| Red text | External data link | `FF0000` |
| Yellow background | Key assumptions | `FFFF00` |

### Number Formats

| Type | Format | Example |
|------|--------|---------|
| Currency | `$#,##0.00` | $1,234.56 |
| Percentage | `0.0%` | 12.5% |
| Year | `@` (text) | 2026 |
| Zero values | `#,##0;(#,##0);"-"` | - |
| Multiples | `0.0"x"` | 2.5x |

## Recalculating Formulas

After creating or modifying spreadsheets with formulas, recalculate using LibreOffice:

```bash
soffice --headless --calc --convert-to xlsx output.xlsx
```

This ensures all formula results are computed and cached in the file. Without this step, some viewers may show stale or empty formula results.

## Common Workflow

1. **Choose tool** — pandas for analysis, openpyxl for creation/editing
2. **Create/load** the workbook
3. **Modify** — add data, formulas, formatting
4. **Save** the file
5. **Recalculate** formulas via LibreOffice (if formulas were added/changed)
6. **Verify** — open and check results, fix any formula errors

## Guidelines

- **Formulas over values** — Always write Excel formulas, never Python-computed results
- **openpyxl uses 1-based indexing** — Row 1, Column 1 is the top-left cell
- **data_only=True warning** — `load_workbook(data_only=True)` returns cached values, not formulas. Use only for reading computed results.
- **Font choice** — Use Arial or Calibri for professional output
- **Column widths** — Always set explicit widths; auto-width is unreliable
- **Large datasets** — For 100K+ rows, use pandas for processing and openpyxl only for final formatted output
- **Multiple sheets** — Use meaningful sheet names, not "Sheet1", "Sheet2"
