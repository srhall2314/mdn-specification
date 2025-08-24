# MDN Format Specification v0.8.0

**Markdown Numbers (.mdn) - AI-Optimized Spreadsheet Format**

A linearly structured format combining YAML metadata, CSV sheet data, and JSON blocks for formulas and formatting. Optimized for AI context and business document workflows by preserving spreadsheet formulas and relationships while maintaining maximum readability and token efficiency.

## Overview

The MDN format is designed to solve the challenge of making spreadsheets AI-friendly while preserving business logic. Traditional spreadsheets are difficult for AI systems to parse and understand due to their complex binary structure and nested relationships. MDN provides a human-readable, linearly parseable format that maintains all the essential spreadsheet functionality.

### Key Benefits

- AI-Optimized: Linearly structured for efficient token processing.
- Business Logic Preserved: Keeps all formulas and calculations.
- Human Readable: Uses plain text with YAML, CSV, and JSON.
- Version Control Friendly: Text-based, works with Git and similar tools.
- Token Efficient: Minimal overhead for AI context windows.
- Bidirectional: Converts between Excel and MDN in both directions.

## Format Structure

The MDN file always follows the same linear structure, making it easy to parse sequentially. Each section is clearly delimited and appears in a fixed order.

```
--- MDN:HEADER YAML          # Required: YAML header section with document info
# YAML header with document info and metadata
---                         # This second '---' closes the YAML block
--- MDN:SHEET CSV name=SheetName   # Required: CSV data for the sheet
# CSV data for the sheet
---                         # Section delimiter
--- MDN:SHEET CSV name=AnotherSheet  # Optional additional sheet(s)
# CSV data for another sheet
---
--- MDN:FORMULAS JSON        # Optional: JSON block with cell formulas
{
  "SheetName!CellRef": "=FORMULA",
  "AnotherSheet!CellRef": "=FORMULA"
}
---
--- MDN:FORMAT JSON          # Optional: JSON block with formatting info
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

Note: The YAML header section can include optional context fields such as `purpose`, `keyMetrics`, `businessRules`, and others, which parsers may choose to ignore.

## AI Prompt Integration

The MDN format supports an optional AI prompt section to help AI systems understand the format when they encounter it for the first time. This feature is documented in two complementary files:

### `mdn_structure_ai_prompt.md`
Contains the AI prompt section that can be included at the bottom of MDN files to explain the format to AI systems. This section is optional and can be removed once the MDN format becomes widely known.

### `mdn_ai_prompt_implementation.md`
Provides implementation options and token efficiency strategies for the AI prompt section, including different levels of detail from comprehensive to ultra-minimal approaches.

## Repository Structure

```
mdn/
├── docs/                    # Documentation
│   ├── specification/       # Format specification
│   ├── guides/             # Implementation guides
│   └── examples/           # Example files
├── tools/                  # Implementation tools
│   └── python/            # Python tools and utilities
├── tests/                  # Test files and data
└── README.md              # This file
```

## Documentation

- **[Specification](docs/specification/)** - Complete format specification and AI prompt structure
- **[Implementation Guides](docs/guides/)** - Practical guides for using MDN
- **[Examples](docs/examples/)** - Sample files and usage patterns
- **[Tools](tools/)** - Validation, parsing, and conversion utilities
- **[Tests](tests/)** - Test files and validation data

## Validation

The MDN format includes a comprehensive validation tool ([`tools/python/mdn_validator.py`](tools/python/mdn_validator.py)) that ensures files comply with the specification:

### What It Validates
- **Required Sections**: YAML header, CSV sheets, JSON formulas
- **Optional Sections**: Format JSON, AI prompt
- **Section Order**: Ensures proper sequence
- **Syntax**: Validates YAML, JSON, and CSV syntax
- **Content**: Checks for required fields and data integrity

### Usage
```bash
cd tools/python
python3 mdn_validator.py <mdn_file>
```

### Example Output
```
MDN Validation Results for: example.mdn
==================================================
✅ File is VALID

Sections found: MDN:HEADER YAML, MDN:SHEET CSV, MDN:FORMULAS JSON
Sheet names: Budget, Forecast
```

The validator provides detailed error messages and warnings to help identify and fix format issues.
