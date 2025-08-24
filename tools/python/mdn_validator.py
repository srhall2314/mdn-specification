#!/usr/bin/env python3
"""
MDN Format Validator

Validates MDN (Markdown Numbers) files against the format specification.
Checks required sections, syntax, and structural integrity.
"""

import re
import yaml
import json
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class ValidationResult:
    """Result of MDN validation"""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    sections_found: List[str]
    sheet_names: List[str]


class MDNValidator:
    """Validates MDN format files"""
    
    REQUIRED_SECTIONS = [
        'MDN:HEADER YAML',
        'MDN:SHEET CSV',
        'MDN:FORMULAS JSON'
    ]
    
    OPTIONAL_SECTIONS = [
        'MDN:FORMAT JSON',
        'MDN:AI_PROMPT'
    ]
    
    ALL_SECTIONS = REQUIRED_SECTIONS + OPTIONAL_SECTIONS
    
    def __init__(self):
        self.content = ""
        self.lines = []
        self.section_positions = {}
        
    def validate_file(self, file_path: str) -> ValidationResult:
        """Validate an MDN file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.content = f.read()
                self.lines = self.content.split('\n')
        except FileNotFoundError:
            return ValidationResult(False, [f"File not found: {file_path}"], [], [], [])
        except Exception as e:
            return ValidationResult(False, [f"Error reading file: {str(e)}"], [], [], [])
        
        return self._validate_content()
    
    def validate_string(self, content: str) -> ValidationResult:
        """Validate MDN content from string"""
        self.content = content
        self.lines = content.split('\n')
        return self._validate_content()
    
    def _validate_content(self) -> ValidationResult:
        """Main validation logic"""
        errors = []
        warnings = []
        sections_found = []
        sheet_names = []
        
        # Check for END DOCUMENT marker
        if 'END DOCUMENT' not in self.content:
            errors.append("Missing 'END DOCUMENT' marker")
        
        # Find all sections
        self._find_sections()
        
        # Validate required sections
        for section in self.REQUIRED_SECTIONS:
            if section not in self.section_positions:
                errors.append(f"Missing required section: {section}")
            else:
                sections_found.append(section)
        
        # Check optional sections
        for section in self.OPTIONAL_SECTIONS:
            if section in self.section_positions:
                sections_found.append(section)
        
        # Validate YAML header
        yaml_errors, yaml_warnings, sheet_names = self._validate_yaml_header()
        errors.extend(yaml_errors)
        warnings.extend(yaml_warnings)
        
        # Validate CSV sections
        csv_errors, csv_warnings = self._validate_csv_sections()
        errors.extend(csv_errors)
        warnings.extend(csv_warnings)
        
        # Validate formulas section
        formula_errors, formula_warnings = self._validate_formulas_section()
        errors.extend(formula_errors)
        warnings.extend(formula_warnings)
        
        # Validate format section (if present)
        if 'MDN:FORMAT JSON' in self.section_positions:
            format_errors, format_warnings = self._validate_format_section()
            errors.extend(format_errors)
            warnings.extend(format_warnings)
        
        # Validate AI prompt section (if present)
        if 'MDN:AI_PROMPT' in self.section_positions:
            prompt_errors, prompt_warnings = self._validate_ai_prompt_section()
            errors.extend(prompt_errors)
            warnings.extend(prompt_warnings)
        
        # Check section order
        order_errors = self._validate_section_order()
        errors.extend(order_errors)
        
        is_valid = len(errors) == 0
        
        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings,
            sections_found=sections_found,
            sheet_names=sheet_names
        )
    
    def _find_sections(self):
        """Find positions of all sections in the file"""
        self.section_positions = {}
        
        for i, line in enumerate(self.lines):
            line = line.strip()
            for section in self.ALL_SECTIONS:
                if line.startswith('--- ') and section in line:
                    # For CSV sections, we need to handle the name parameter
                    if section == 'MDN:SHEET CSV':
                        # Find all CSV sections
                        if 'MDN:SHEET CSV' not in self.section_positions:
                            self.section_positions['MDN:SHEET CSV'] = []
                        if isinstance(self.section_positions['MDN:SHEET CSV'], list):
                            self.section_positions['MDN:SHEET CSV'].append(i)
                        else:
                            self.section_positions['MDN:SHEET CSV'] = [i]
                    else:
                        self.section_positions[section] = i
                    break
    
    def _validate_yaml_header(self) -> Tuple[List[str], List[str], List[str]]:
        """Validate YAML header section"""
        errors = []
        warnings = []
        sheet_names = []
        
        if 'MDN:HEADER YAML' not in self.section_positions:
            return errors, warnings, sheet_names
        
        start_pos = self.section_positions['MDN:HEADER YAML']
        
        # Find end of YAML section
        yaml_content = []
        for i in range(start_pos + 1, len(self.lines)):
            line = self.lines[i].strip()
            if line == '---':
                break
            yaml_content.append(line)
        
        if not yaml_content:
            errors.append("YAML header section is empty")
            return errors, warnings, sheet_names
        
        try:
            yaml_data = yaml.safe_load('\n'.join(yaml_content))
            
            # Check required fields
            required_fields = ['source', 'version', 'created', 'sheets']
            for field in required_fields:
                if field not in yaml_data:
                    errors.append(f"Missing required YAML field: {field}")
            
            # Validate sheets field
            if 'sheets' in yaml_data:
                if not isinstance(yaml_data['sheets'], list):
                    errors.append("'sheets' field must be a list")
                elif len(yaml_data['sheets']) == 0:
                    errors.append("'sheets' list cannot be empty")
                else:
                    sheet_names = yaml_data['sheets']
                    
                    # Check for duplicate sheet names
                    if len(sheet_names) != len(set(sheet_names)):
                        warnings.append("Duplicate sheet names found in YAML header")
            
            # Validate version format
            if 'version' in yaml_data:
                version = str(yaml_data['version'])
                if not re.match(r'^\d+\.\d+(\.\d+)?$', version):
                    warnings.append("Version format should be semantic (e.g., 1.0.0)")
            
        except yaml.YAMLError as e:
            errors.append(f"Invalid YAML syntax: {str(e)}")
        
        return errors, warnings, sheet_names
    
    def _validate_csv_sections(self) -> Tuple[List[str], List[str]]:
        """Validate CSV sheet sections"""
        errors = []
        warnings = []
        
        if 'MDN:SHEET CSV' not in self.section_positions:
            return errors, warnings
        
        csv_positions = self.section_positions['MDN:SHEET CSV']
        if not isinstance(csv_positions, list):
            csv_positions = [csv_positions]
        
        for start_pos in csv_positions:
            # Get the full line to extract sheet name
            section_line = self.lines[start_pos].strip()
            
            # Extract sheet name
            sheet_name_match = re.search(r'name=([^,\s]+)', section_line)
            if not sheet_name_match:
                errors.append(f"Missing sheet name in CSV section at line {start_pos + 1}")
                continue
            
            sheet_name = sheet_name_match.group(1)
            
            # Find end of CSV section
            csv_content = []
            for i in range(start_pos + 1, len(self.lines)):
                line = self.lines[i].strip()
                if line == '---':
                    break
                csv_content.append(line)
            
            if not csv_content:
                errors.append(f"CSV section for sheet '{sheet_name}' is empty")
                continue
            
            # Basic CSV validation
            if len(csv_content) < 2:
                warnings.append(f"Sheet '{sheet_name}' has very few rows")
            
            # Check for consistent column count
            column_counts = []
            for line in csv_content:
                if line.strip():
                    column_counts.append(len(line.split(',')))
            
            if len(set(column_counts)) > 1:
                warnings.append(f"Sheet '{sheet_name}' has inconsistent column counts")
        
        return errors, warnings
    
    def _validate_formulas_section(self) -> Tuple[List[str], List[str]]:
        """Validate formulas JSON section"""
        errors = []
        warnings = []
        
        if 'MDN:FORMULAS JSON' not in self.section_positions:
            return errors, warnings
        
        start_pos = self.section_positions['MDN:FORMULAS JSON']
        
        # Find end of JSON section
        json_content = []
        for i in range(start_pos + 1, len(self.lines)):
            line = self.lines[i].strip()
            if line == '---':
                break
            json_content.append(line)
        
        if not json_content:
            errors.append("Formulas section is empty")
            return errors, warnings
        
        try:
            formulas_data = json.loads('\n'.join(json_content))
            
            if not isinstance(formulas_data, dict):
                errors.append("Formulas section must contain a JSON object")
                return errors, warnings
            
            # Validate cell references
            for cell_ref, formula in formulas_data.items():
                if not isinstance(cell_ref, str):
                    errors.append(f"Invalid cell reference type: {type(cell_ref)}")
                    continue
                
                if not isinstance(formula, str):
                    errors.append(f"Invalid formula type for {cell_ref}: {type(formula)}")
                    continue
                
                # Check cell reference format
                if not re.match(r'^[^!]+![A-Z]+\d+$', cell_ref):
                    warnings.append(f"Cell reference format may be invalid: {cell_ref}")
                
                # Check formula format
                if not formula.startswith('='):
                    warnings.append(f"Formula should start with '=': {formula}")
        
        except json.JSONDecodeError as e:
            errors.append(f"Invalid JSON syntax in formulas section: {str(e)}")
        
        return errors, warnings
    
    def _validate_format_section(self) -> Tuple[List[str], List[str]]:
        """Validate format JSON section"""
        errors = []
        warnings = []
        
        start_pos = self.section_positions['MDN:FORMAT JSON']
        
        # Find end of JSON section
        json_content = []
        for i in range(start_pos + 1, len(self.lines)):
            line = self.lines[i].strip()
            if line == '---':
                break
            json_content.append(line)
        
        if not json_content:
            errors.append("Format section is empty")
            return errors, warnings
        
        try:
            format_data = json.loads('\n'.join(json_content))
            
            if not isinstance(format_data, dict):
                errors.append("Format section must contain a JSON object")
                return errors, warnings
            
            # Basic validation of format structure
            for range_ref, format_info in format_data.items():
                if not isinstance(range_ref, str):
                    errors.append(f"Invalid range reference type: {type(range_ref)}")
                    continue
                
                if not isinstance(format_info, dict):
                    errors.append(f"Format info for {range_ref} must be an object")
                    continue
        
        except json.JSONDecodeError as e:
            errors.append(f"Invalid JSON syntax in format section: {str(e)}")
        
        return errors, warnings
    
    def _validate_ai_prompt_section(self) -> Tuple[List[str], List[str]]:
        """Validate AI prompt section"""
        errors = []
        warnings = []
        
        start_pos = self.section_positions['MDN:AI_PROMPT']
        
        # Find end of section
        prompt_content = []
        for i in range(start_pos + 1, len(self.lines)):
            line = self.lines[i].strip()
            if line == '---':
                break
            prompt_content.append(line)
        
        if not prompt_content:
            warnings.append("AI prompt section is empty")
        
        # Check if content is too long (token efficiency)
        total_chars = sum(len(line) for line in prompt_content)
        if total_chars > 500:  # Rough estimate for token efficiency
            warnings.append("AI prompt section may be too long for optimal token efficiency")
        
        return errors, warnings
    
    def _validate_section_order(self) -> List[str]:
        """Validate that sections appear in correct order"""
        errors = []
        
        # Define expected order
        expected_order = [
            'MDN:HEADER YAML',
            'MDN:SHEET CSV',
            'MDN:FORMULAS JSON',
            'MDN:FORMAT JSON',
            'MDN:AI_PROMPT'
        ]
        
        # Filter to only include sections that are present
        present_sections = [s for s in expected_order if s in self.section_positions]
        
        # Check if order is maintained
        for i in range(len(present_sections) - 1):
            current_pos = self.section_positions[present_sections[i]]
            next_pos = self.section_positions[present_sections[i + 1]]
            
            # Handle CSV section being a list of positions
            if present_sections[i] == 'MDN:SHEET CSV' and isinstance(current_pos, list):
                current_pos = min(current_pos)  # Use the first CSV section position
            if present_sections[i + 1] == 'MDN:SHEET CSV' and isinstance(next_pos, list):
                next_pos = min(next_pos)  # Use the first CSV section position
            
            if current_pos > next_pos:
                errors.append(f"Section order violation: {present_sections[i]} appears after {present_sections[i + 1]}")
        
        return errors


def main():
    """Command line interface for the validator"""
    if len(sys.argv) != 2:
        print("Usage: python mdn_validator.py <mdn_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    validator = MDNValidator()
    result = validator.validate_file(file_path)
    
    print(f"MDN Validation Results for: {file_path}")
    print("=" * 50)
    
    if result.is_valid:
        print("✅ File is VALID")
    else:
        print("❌ File is INVALID")
    
    if result.errors:
        print("\nErrors:")
        for error in result.errors:
            print(f"  ❌ {error}")
    
    if result.warnings:
        print("\nWarnings:")
        for warning in result.warnings:
            print(f"  ⚠️  {warning}")
    
    print(f"\nSections found: {', '.join(result.sections_found)}")
    print(f"Sheet names: {', '.join(result.sheet_names)}")
    
    sys.exit(0 if result.is_valid else 1)


if __name__ == "__main__":
    main()
