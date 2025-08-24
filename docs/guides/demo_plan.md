# MDN Format Demo Code Plan

## Overview
Create a Python-based demo that demonstrates bidirectional conversion between MDN (Markdown Numbers) format and Excel (.xlsx) files. The focus is on **readability and understanding** rather than performance optimization.

## Goals
- **Educational**: Show how the MDN format works step-by-step
- **Validation**: Prove the format specification is complete and accurate
- **Round-trip Testing**: Ensure no data loss when converting back and forth
- **Real-world Usability**: Demonstrate practical workflow applications

## Toolset
- **Python 3.8+** - For readability and cross-platform compatibility
- **OpenPyXL** - Excel file creation and manipulation
- **PyYAML** - YAML header parsing
- **Built-in modules**: `csv`, `json`, `re` for data processing

## Project Structure
```
mdn_demo/
├── README.md
├── requirements.txt
├── mdn_converter.py      # Main conversion logic
├── excel_parser.py       # Excel → MDN conversion
├── mdn_parser.py         # MDN → Excel conversion
├── utils.py              # Shared utility functions
├── test_files/           # Sample files for testing
│   ├── sample.xlsx
│   └── sample.mdn
└── examples/             # Example usage scripts
    ├── export_demo.py    # Excel → MDN demo
    ├── import_demo.py    # MDN → Excel demo
    └── round_trip_demo.py # Complete workflow demo
```

## Core Functions

### 1. Excel → MDN (Export)
```python
def excel_to_mdn(excel_file_path):
    """Convert Excel file to MDN format"""
    # Read Excel workbook
    # Extract sheets, data, formulas, formatting
    # Generate MDN content with proper sections
    # Return MDN string content
```

**Key Steps:**
- Parse Excel workbook structure
- Extract CSV data from each sheet
- Capture formulas and cell references
- Extract formatting rules (number formats, styles, colors)
- Generate YAML header with metadata
- Assemble complete MDN document

### 2. MDN → Excel (Import)
```python
def mdn_to_excel(mdn_content, output_file_path):
    """Convert MDN content to Excel file"""
    # Parse MDN sections
    # Create Excel workbook
    # Apply data, formulas, and formatting
    # Save to file
```

**Key Steps:**
- Parse YAML header for document info
- Extract CSV data for each sheet
- Apply formulas to appropriate cells
- Apply formatting rules with override handling
- Create and save Excel file

### 3. Round-trip Testing
```python
def test_round_trip(excel_file_path):
    """Test Excel → MDN → Excel conversion"""
    # Convert Excel to MDN
    # Convert MDN back to Excel
    # Compare original and final Excel files
    # Report any differences
```

## Implementation Details

### Parsing Strategy
- **Linear parsing**: Process MDN file top-to-bottom as specified
- **Section delimiters**: Use `--- MDN:SECTION_TYPE` markers
- **Error handling**: Clear messages for malformed MDN files
- **Validation**: Check required sections and data integrity

### Range Reference Handling
- **Contiguous ranges**: `A1:B10`, `A:A`, `B:B`
- **Non-contiguous ranges**: `A1,A3,A5`, `B2:B5,D2:D5`
- **Override behavior**: More specific references override broader ones
- **Apply to both**: Formulas and formatting use same range logic

### Data Type Preservation
- **Number formats**: Preserve currency, date, percentage formats
- **Cell styles**: Bold, italic, colors, borders
- **Formulas**: Maintain calculation logic and cell references

## Demo Scenarios

### 1. Basic Conversion
- Simple spreadsheet with data and basic formulas
- Show clear input/output comparison

### 2. Complex Formatting
- Multiple sheets with various number formats
- Demonstrate override behavior
- Show style preservation

### 3. Formula Complexity
- Cross-sheet references (if supported)
- Complex mathematical formulas
- Error handling for invalid formulas

### 4. Edge Cases
- Empty sheets
- Very large datasets
- Special characters in data
- Malformed MDN files

## Output Examples

### Console Output
```
Converting sample.xlsx to MDN...
✓ Parsed 3 sheets
✓ Extracted 15 formulas
✓ Applied 8 formatting rules
✓ Generated MDN file: sample.mdn

Converting sample.mdn to Excel...
✓ Parsed YAML header
✓ Created 3 sheets
✓ Applied 15 formulas
✓ Applied 8 formatting rules
✓ Saved Excel file: sample_output.xlsx

Round-trip test completed successfully!
✓ No data loss detected
✓ All formulas preserved
✓ All formatting maintained
```

### File Comparison
- **Before/after screenshots** of Excel files
- **MDN content** showing the intermediate format
- **Diff reports** for any discrepancies

## Testing Strategy

### Unit Tests
- Individual parsing functions
- Range reference handling
- Override behavior
- Error conditions

### Integration Tests
- Complete conversion workflows
- Round-trip validation
- Performance benchmarks (optional)

### Sample Files
- **Simple**: Basic data and formulas
- **Complex**: Multiple sheets, advanced formatting
- **Edge Cases**: Empty data, special characters
- **Invalid**: Malformed MDN for error testing

## Future Enhancements
- **Web interface** for online conversion
- **Batch processing** for multiple files
- **Format validation** tools
- **Performance optimization** (if needed)
- **Additional Excel features** (charts, pivot tables, etc.)

## Success Criteria
- [ ] Successfully convert Excel → MDN
- [ ] Successfully convert MDN → Excel
- [ ] Round-trip conversion preserves all data
- [ ] Code is readable and well-documented
- [ ] Demo handles edge cases gracefully
- [ ] Clear examples and usage instructions

## Timeline
- **Week 1**: Basic Excel → MDN conversion
- **Week 2**: MDN → Excel conversion
- **Week 3**: Round-trip testing and validation
- **Week 4**: Documentation, examples, and polish

This demo will serve as both a proof-of-concept for the MDN format and an educational tool for understanding how the specification works in practice.
