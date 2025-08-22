"""
Utility functions for MDN format conversion.
"""

import re
from typing import Dict, List, Tuple, Any


def parse_cell_reference(cell_ref: str) -> Tuple[str, int, int]:
    """
    Parse Excel cell reference (e.g., 'A1', 'B2') into column and row.
    
    Args:
        cell_ref: Excel cell reference like 'A1', 'B2', etc.
        
    Returns:
        Tuple of (column_letter, column_index, row_index)
        
    Example:
        >>> parse_cell_reference('A1')
        ('A', 1, 1)
        >>> parse_cell_reference('B2')
        ('B', 2, 2)
    """
    # Extract column letters and row number
    match = re.match(r'([A-Z]+)(\d+)', cell_ref)
    if not match:
        raise ValueError(f"Invalid cell reference: {cell_ref}")
    
    column_letters = match.group(1)
    row_number = int(match.group(2))
    
    # Convert column letters to index (A=1, B=2, AA=27, etc.)
    column_index = 0
    for i, letter in enumerate(column_letters):
        column_index += (ord(letter) - ord('A') + 1) * (26 ** (len(column_letters) - i - 1))
    
    return column_letters, column_index, row_number


def column_letter_to_index(column_letter: str) -> int:
    """
    Convert Excel column letter to column index.
    
    Args:
        column_letter: Column letter(s) like 'A', 'B', 'AA', etc.
        
    Returns:
        Column index (1-based)
        
    Example:
        >>> column_letter_to_index('A')
        1
        >>> column_letter_to_index('AA')
        27
    """
    result = 0
    for i, letter in enumerate(column_letter):
        result += (ord(letter) - ord('A') + 1) * (26 ** (len(column_letter) - i - 1))
    return result


def column_index_to_letter(column_index: int) -> str:
    """
    Convert Excel column index to column letter.
    
    Args:
        column_index: Column index (1-based)
        
    Returns:
        Column letter(s) like 'A', 'B', 'AA', etc.
        
    Example:
        >>> column_index_to_letter(1)
        'A'
        >>> column_index_to_letter(27)
        'AA'
    """
    if column_index < 1:
        raise ValueError("Column index must be 1 or greater")
    
    result = ""
    while column_index > 0:
        column_index -= 1
        result = chr(ord('A') + (column_index % 26)) + result
        column_index //= 26
    
    return result


def parse_range_reference(range_ref: str) -> List[str]:
    """
    Parse Excel range reference into individual cell references.
    
    Args:
        range_ref: Excel range like 'A1:B3', 'A:A', 'A1,A3,A5'
        
    Returns:
        List of individual cell references
        
    Example:
        >>> parse_range_reference('A1:B3')
        ['A1', 'A2', 'A3', 'B1', 'B2', 'B3']
        >>> parse_range_reference('A:A')
        ['A1', 'A2', 'A3', ...]  # All cells in column A
        >>> parse_range_reference('A1,A3,A5')
        ['A1', 'A3', 'A5']
    """
    cells = []
    
    # Split by comma for non-contiguous ranges
    parts = range_ref.split(',')
    
    for part in parts:
        part = part.strip()
        
        if ':' in part:
            # Contiguous range like 'A1:B3' or 'A:A'
            start, end = part.split(':')
            
            if start.isalpha() and end.isalpha():
                # Column range like 'A:A'
                start_col = column_letter_to_index(start)
                end_col = column_letter_to_index(end)
                for col_idx in range(start_col, end_col + 1):
                    col_letter = column_index_to_letter(col_idx)
                    # Note: For column ranges, we'd need to know the max row
                    # For now, we'll use a reasonable default
                    for row in range(1, 1001):  # Assume max 1000 rows
                        cells.append(f"{col_letter}{row}")
            else:
                # Cell range like 'A1:B3'
                start_col, start_row = parse_cell_reference(start)[:2]
                end_col, end_row = parse_cell_reference(end)[:2]
                
                for col_idx in range(start_col, end_col + 1):
                    for row_idx in range(start_row, end_row + 1):
                        col_letter = column_index_to_letter(col_idx)
                        cells.append(f"{col_letter}{row_idx}")
        else:
            # Single cell reference
            cells.append(part)
    
    return cells


def validate_mdn_structure(content: str) -> Dict[str, Any]:
    """
    Validate MDN file structure and return section information.
    
    Args:
        content: MDN file content as string
        
    Returns:
        Dictionary with validation results and section info
        
    Example:
        >>> result = validate_mdn_structure(mdn_content)
        >>> result['valid']
        True
        >>> result['sections']
        ['header', 'sheet', 'formulas', 'format', 'end']
    """
    sections = []
    required_sections = ['header', 'sheet', 'formulas']
    optional_sections = ['format']
    
    # Check for required sections
    if '--- MDN:HEADER YAML' not in content:
        return {'valid': False, 'error': 'Missing required HEADER section'}
    
    if '--- MDN:SHEET CSV' not in content:
        return {'valid': False, 'error': 'Missing required SHEET section'}
    
    if '--- MDN:FORMULAS JSON' not in content:
        return {'valid': False, 'error': 'Missing required FORMULAS section'}
    
    if 'END DOCUMENT' not in content:
        return {'valid': False, 'error': 'Missing required END DOCUMENT marker'}
    
    # Extract section information
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('--- MDN:'):
            section_type = line.split(' ')[1].split(':')[1]
            sections.append(section_type.lower())
    
    return {
        'valid': True,
        'sections': sections,
        'total_lines': len(lines)
    }


def format_timestamp() -> str:
    """
    Generate ISO-8601 timestamp for MDN files.
    
    Returns:
        ISO-8601 formatted timestamp string
        
    Example:
        >>> format_timestamp()
        '2025-01-15T12:00:00Z'
    """
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
