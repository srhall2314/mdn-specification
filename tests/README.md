# MDN Tests

This directory contains test files and testing utilities for the MDN format.

## Test Files

### Sample Data
- **`budget_sample.xlsx`** - Budget spreadsheet for testing Excel to MDN conversion
- **`financial_sample.xlsx`** - Financial data for testing complex formulas and relationships

## Testing Strategy

### Validation Testing
- Test the validator with various file formats
- Verify error detection for invalid files
- Check warning generation for optimization suggestions

### Conversion Testing
- Test Excel to MDN conversion
- Verify formula preservation
- Check data integrity

### Format Testing
- Test different section combinations
- Verify optional section handling
- Check section order validation

## Running Tests

### Manual Testing
```bash
cd ../tools/python
python3 mdn_validator.py ../../tests/your_test_file.mdn
```

### Automated Testing
```bash
cd ../tools/python
python3 -m pytest ../../tests/
```

## Test Coverage

- **File Structure** - Section presence and order
- **Content Validation** - YAML, JSON, and CSV syntax
- **Business Logic** - Formula preservation and cell references
- **Error Handling** - Invalid file detection and reporting

## Contributing

To add new tests:

1. Create test files that cover specific scenarios
2. Include both valid and invalid examples
3. Document what each test validates
4. Ensure tests pass with current tools
