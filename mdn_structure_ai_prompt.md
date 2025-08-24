# AI Prompt: Understanding MDN File Structure

## What is MDN?

MDN (Markdown Numbers) is an AI-optimized spreadsheet format that converts Excel files into a AI-readable, linearly parseable structure. It preserves all spreadsheet functionality while making data accessible to text based AI systems.

## MDN File Structure - Quick Reference

An MDN file follows a strict linear structure with clearly delimited sections:

```
--- MDN:HEADER YAML
# Document metadata (source file, version, creation date, sheet names)
# Optional: purpose, keyMetrics, businessRules for AI context
---
--- MDN:SHEET CSV name=SheetName
# CSV data for the sheet (headers + data rows)
---
--- MDN:SHEET CSV name=AnotherSheet
# Additional sheet data
---
--- MDN:FORMULAS JSON
# Cell formulas mapped by "SheetName!CellRef": "=FORMULA"
---
--- MDN:FORMAT JSON
# Optional: formatting rules for cells/ranges
---
END DOCUMENT
```

## Key Points for AI Parsing:

1. **Fixed Order**: Sections always appear in the same sequence
2. **Clear Delimiters**: Each section starts with `--- MDN:SECTION_TYPE` and ends with `---`
3. **YAML Header**: Contains metadata and optional AI context fields
4. **CSV Sheets**: One or more data tables in standard CSV format
5. **Formulas**: JSON mapping of cell references to Excel formulas
6. **Formatting**: Optional JSON with styling information
7. **End Marker**: Literal `END DOCUMENT` line

## Cell Reference Format:
- **Single cells**: `A1`, `B2`
- **Ranges**: `A1:B10`, `A:A`, `B:B`
- **Sheet references**: `SheetName!A1`, `SheetName!B2:B5`

## Why This Format Works for AI:
- **Linearly parseable**: Simple top-to-bottom reading
- **Token efficient**: Minimal overhead, no complex nesting
- **Business logic preserved**: All formulas and calculations maintained
- **Context rich**: Optional metadata provides business understanding
- **Human readable**: Plain text with familiar formats (YAML, CSV, JSON)

## Example Use Cases:
- Parse spreadsheet data for analysis
- Extract and understand business formulas
- Convert between Excel and MDN formats
- Version control spreadsheet changes
- AI-powered business analysis workflows
