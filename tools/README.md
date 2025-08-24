# MDN Tools

This directory contains tools for working with the MDN format.

## Python Tools

The Python tools are located in the [`python/`](python/) subdirectory.

### Core Tools

- **[`mdn_validator.py`](python/mdn_validator.py)** - Validates MDN files against the specification
- **[`mdn_parser.py`](python/mdn_parser.py)** - Parses MDN files into structured data
- **[`mdn_converter.py`](python/mdn_converter.py)** - Converts between Excel and MDN formats
- **[`excel_parser.py`](python/excel_parser.py)** - Excel file parsing utilities
- **[`utils.py`](python/utils.py)** - Common utility functions

### Installation

```bash
cd tools/python
pip install -r requirements.txt
```

### Usage

#### Validation
```bash
python3 mdn_validator.py <mdn_file>
```

#### Conversion
```python
from mdn_converter import MDNConverter

converter = MDNConverter()
mdn_content = converter.excel_to_mdn('file.xlsx')
```

#### Parsing
```python
from mdn_parser import MDNParser

parser = MDNParser()
data = parser.parse_file('file.mdn')
```

## Dependencies

See [`python/requirements.txt`](python/requirements.txt) for Python package dependencies.

## Contributing

To add new tools:

1. Place Python tools in the `python/` directory
2. Update this README with usage instructions
3. Add any new dependencies to requirements.txt
4. Include proper documentation and examples
