# MDN Format Demo

A Python-based demonstration of bidirectional conversion between Excel (.xlsx) files and MDN (Markdown Numbers) format.

## Overview

This demo validates the MDN format specification by providing:
- **Excel → MDN conversion**: Convert Excel files to MDN format
- **MDN → Excel conversion**: Convert MDN files back to Excel
- **Round-trip testing**: Validate no data loss in conversions
- **Format validation**: Ensure MDN files meet specification requirements

## Features

- ✅ **Bidirectional Conversion**: Excel ↔ MDN
- ✅ **Formula Preservation**: Maintains spreadsheet business logic
- ✅ **Formatting Support**: Preserves number formats, styles, colors
- ✅ **Multi-sheet Support**: Handles workbooks with multiple sheets
- ✅ **Validation**: Checks MDN file structure compliance
- ✅ **Round-trip Testing**: Ensures data integrity

## Requirements

- Python 3.8+
- Required packages (see `requirements.txt`):
  - `openpyxl` - Excel file handling
  - `PyYAML` - YAML parsing
  - `pandas` - Data processing

## Installation

1. **Clone or download** the demo files
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Quick Start

### Run the Demo
```bash
python demo.py
```

This will automatically test both sample Excel files and perform round-trip conversions.

### Manual Conversion

#### Excel to MDN
```bash
python mdn_converter.py excel2mdn financial_sample.xlsx
```

#### MDN to Excel
```bash
python mdn_converter.py mdn2excel financial_sample_intermediate.mdn output.xlsx
```

#### Round-trip Test
```bash
python mdn_converter.py roundtrip budget_sample.xlsx
```

#### Validate MDN File
```bash
python mdn_converter.py validate sample.mdn
```

## Sample Files

The demo includes two sample Excel files:
- `financial_sample.xlsx` - Financial data with formulas
- `budget_sample.xlsx` - Budget data with formatting

## Output Files

After running the demo, you'll see:
- `*_intermediate.mdn` - MDN format intermediate files
- `*_roundtrip.xlsx` - Excel files after round-trip conversion

## Project Structure

```
├── README.md              # This file
├── requirements.txt       # Python dependencies
├── utils.py              # Utility functions
├── excel_parser.py       # Excel → MDN converter
├── mdn_parser.py         # MDN → Excel converter
├── mdn_converter.py      # Main converter interface
├── .gitignore            # Git ignore rules
├── test_files/           # Sample files and test outputs
│   ├── financial_sample.xlsx
│   └── budget_sample.xlsx
├── examples/             # Example usage scripts
│   └── demo.py          # Demo script
└── mdn_format_spec.md   # MDN format specification
```

## How It Works

### 1. Excel → MDN Conversion
- Reads Excel workbook using OpenPyXL
- Extracts sheet data as CSV
- Captures formulas and cell references
- Preserves formatting rules
- Generates MDN format with proper sections

### 2. MDN → Excel Conversion
- Parses MDN sections (YAML, CSV, JSON)
- Creates Excel workbook with sheets
- Applies data from CSV sections
- Restores formulas to cells
- Applies formatting rules

### 3. Round-trip Validation
- Converts Excel → MDN → Excel
- Validates MDN structure
- Compares file sizes
- Ensures data integrity

## MDN Format Structure

The demo generates MDN files with this structure:
```
--- MDN:HEADER YAML
# Document metadata
---
--- MDN:SHEET CSV name=SheetName
# CSV data
---
--- MDN:FORMULAS JSON
# Cell formulas
---
--- MDN:FORMAT JSON
# Formatting rules
---
END DOCUMENT
```

## Error Handling

The demo includes comprehensive error handling:
- **File validation**: Checks file existence and format
- **Structure validation**: Ensures MDN files meet specification
- **Conversion errors**: Graceful handling of parsing issues
- **Detailed logging**: Clear progress and error messages

## Customization

### Adding New Excel Files
1. Place your `.xlsx` file in the `test_files/` directory
2. Update the `sample_files` list in `examples/demo.py`
3. Run the demo to test conversion

### Modifying Conversion Logic
- **Excel parsing**: Modify `excel_parser.py`
- **MDN parsing**: Modify `mdn_parser.py`
- **Utilities**: Modify `utils.py`

## Troubleshooting

### Common Issues

**Import Errors**
```bash
pip install -r requirements.txt
```

**File Not Found**
- Ensure Excel files are in the `test_files/` directory
- Check file permissions

**Conversion Errors**
- Verify Excel files are valid `.xlsx` format
- Check for unsupported Excel features

### Debug Mode
Add debug prints to see detailed conversion steps:
```python
# In excel_parser.py or mdn_parser.py
print(f"DEBUG: Processing {variable}")
```

## Contributing

This demo is designed to validate the MDN format specification. To contribute:
1. Test with different Excel file types
2. Report any conversion issues
3. Suggest improvements to the format
4. Add support for additional Excel features

## License

This demo is part of the MDN format specification project, released under Creative Commons Attribution 4.0 International License.

## Support

For issues or questions:
1. Check the error messages for specific problems
2. Verify your Excel files are valid
3. Review the MDN format specification
4. Test with the provided sample files

---

*"Making spreadsheets AI-friendly while preserving business logic"*
