# MDN Format Specification  
**Markdown Numbers (.mdn) - AI-Optimized Spreadsheet Format**

Version: 1.0  
Created: January 2025  
Purpose: Token-efficient spreadsheet format preserving business logic  

## Overview

MDN (Markdown Numbers) is a linearly structured format combining YAML metadata, CSV sheet data, and JSON blocks for formulas and formatting. It is optimized for AI context and business document workflows by preserving spreadsheet formulas and relationships while maintaining maximum readability and token efficiency.

## File Structure

The MDN file is composed of clearly delimited sections in a fixed order:

```
--- MDN:HEADER YAML
# YAML header with document info and metadata
---
--- MDN:SHEET CSV name=SheetName
# CSV data for the sheet
---
--- MDN:SHEET CSV name=AnotherSheet
# CSV data for another sheet
---
--- MDN:FORMULAS JSON
{
  "SheetName!CellRef": "=FORMULA",
  "AnotherSheet!CellRef": "=FORMULA"
}
---
--- MDN:FORMAT JSON
{
  "SheetName!Range": {
    "numberFormat": "string",
    "bold": boolean,
    "color": "hex"
  }
}
---
END DOCUMENT
```

### Example

```
--- MDN:HEADER YAML
source: filename.xlsx
version: 1.0
created: 2025-01-15T12:00:00Z
sheets:
  - Revenue
  - Costs
---
# optional context section
purpose: quarterly_forecast
keyMetrics:
  - total_sales
  - profit_margin
businessRules:
  - Sales must be forecasted monthly
  - Costs include fixed and variable components
---
--- MDN:SHEET CSV name=Revenue
Month,Sales,Growth,Forecast
Jan,10000,0.05,10500
Feb,10500,0.05,11025
---
--- MDN:SHEET CSV name=Costs
Category,Fixed,Variable,Total
Dev,5000,2000,7000
Marketing,3000,1500,4500
---
--- MDN:FORMULAS JSON
{
  "Revenue!D2": "=B2*(1+C2)",
  "Costs!D3": "=SUM(B2:B3)"
}
---
--- MDN:FORMAT JSON
{
  "Revenue!D:D": {"numberFormat": "$#,##0"}
}
---
END DOCUMENT
```

## Section Definitions

### 1. Header Section (YAML)
- **Required**: YAML block with document metadata
- **Purpose**: Provides document info, sheet list, and optional AI/business context sections

### 2. Sheet Data Sections (CSV)
- **Required**: One or more CSV blocks, each representing a sheet
- **Purpose**: Contains tabular data in CSV format for AI and tools
- **Format**: Standard CSV with header row

### 3. Formulas Section (JSON)
- **Required**: JSON block mapping cell references to formulas
- **Purpose**: Preserves spreadsheet business logic and calculations

### 4. Formatting Section (JSON)
- **Optional**: JSON block defining number formats, styles, colors by cell or range

### 5. End Marker
- **Required**: Literal `END DOCUMENT` line to indicate end of file

## JSON Metadata Schema

### YAML Header Schema

The YAML header must include the core document metadata fields typically present in standard Excel exports. Only these core fields are required for minimal compliance:

```yaml
source: string            # Original filename
version: string           # MDN format version
created: string           # ISO-8601 timestamp
sheets:                   # List of sheet names
  - string
```

### Context Sections (Optional)

The following fields are optional **context sections** that extend the YAML metadata to provide richer AI, documentation, or business-related information. These fields are **not required** for basic compliance but can guide AI systems or provide additional semantic context:

```yaml
purpose: string           # Optional purpose description
keyMetrics:               # Optional key metrics list
  - string
businessRules:            # Optional business rules list
  - string
```

Additional context fields may include any arbitrary key-value pairs useful for AI interpretation, documentation, or business logic. Consumers of the MDN format may safely ignore these fields if they are not relevant to their use case.

### Formulas JSON Schema

```json
{
  "SheetName!CellRef": "=FORMULA"
}
```

### Formatting JSON Schema

```json
{
  "SheetName!Range": {
    "numberFormat": "string",
    "bold": boolean,
    "color": "hex"
  }
}
```

### Range References
- **Contiguous ranges**: `A1:B10`, `A:A`, `B:B`
- **Non-contiguous ranges**: `A1,A3,A5`, `B2:B5,D2:D5`
- **Single cells**: `A1`, `B2`

### Processing Rules

#### Override Behavior
- More specific cell/range references override broader ones
- **Applies to both formulas and formatting**
- Example: `A1` formatting overrides `A:A` formatting
- Example: `B2:B5` formatting overrides `B:B` formatting
- Example: `C3` formula overrides `C:C` formula
- This allows efficient broad application with selective overrides

## Benefits

### For AI/LLMs
- **Linearly Parseable**: Simple top-to-bottom structure eases parsing
- **Token Efficient**: Minimal JSON and YAML overhead, no nested markdown tables
- **Clear Separation**: Metadata, data, formulas, and formatting are distinct
- **Context Rich**: Formulas and metadata provide business logic understanding

### For Developers
- **Human Readable**: Plain text with familiar formats (YAML, CSV, JSON)
- **Easy Version Control**: Line-based diffs and merges
- **Tool Friendly**: Compatible with standard parsers and editors
- **Extensible**: Additional JSON blocks can be added while preserving structure

### For Business Users
- **Preserves Formulas**: Maintains spreadsheet logic transparently
- **Excel Compatible**: Can be converted back to .xlsx files
- **Audit Trail**: Changes visible in text format for review
- **AI Integration**: Enables AI workflows on spreadsheet data and logic

## Use Cases

### 1. AI Business Analysis
- Store spreadsheet data and formulas in a token-efficient format
- Enable AI to understand business logic and perform analysis

### 2. Version Control
- Track changes to spreadsheet data and formulas in Git or similar systems
- Resolve merge conflicts in a human-readable way

### 3. Documentation
- Self-documenting spreadsheets with embedded metadata and rules
- AI can explain formula logic using preserved business rules

## File Extensions

- **.mdn** - Primary extension (Markdown Numbers)
- **.mdnumbers** - Alternative verbose extension
- **.markdownnumbers** - Full descriptive name

## MIME Type

- **text/x-markdown-numbers**  
- **application/x-mdn**

## Conversion Tools

### Export (Excel → MDN)

```javascript
// L3W implementation
const mdn = await excelService.exportToMDN('file.xlsx');
await fs.writeFile('file.mdn', mdn.content);
```

### Import (MDN → Excel)

```javascript
// L3W implementation
const mdnContent = await fs.readFile('file.mdn', 'utf8');
await excelService.importFromMDN(mdnContent, 'output.xlsx');
```

## Validation

### Required Elements
1. YAML header section (`--- MDN:HEADER YAML`) with valid YAML
2. At least one CSV sheet section (`--- MDN:SHEET CSV name=...`) with valid CSV data
3. Formulas section (`--- MDN:FORMULAS JSON`) with valid JSON formulas
4. End marker line: `END DOCUMENT`

### Optional Elements
- Formatting section (`--- MDN:FORMAT JSON`) with valid JSON formatting
- Multiple sheets and extended metadata fields (context sections)

## Future Extensions

- Schema growth to include additional JSON blocks for charts, pivot tables, macros, and validation rules  
- Maintain lightweight, linearly parseable structure for token efficiency  
- Support enhanced AI context metadata while preserving simplicity  

## Reference Implementation

The MDN format was created by L3W (AI Document Editor) and first implemented in January 2025. Reference implementation available at: https://github.com/l3w/mdn-format

## License

MDN Format Specification is released under Creative Commons Attribution 4.0 International License. Free for commercial and non-commercial use.

---

*"Making spreadsheets AI-friendly while preserving business logic"*