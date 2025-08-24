"""
Main MDN format converter module.
Provides unified interface for Excel ↔ MDN conversions.
"""

from typing import Dict, Any
from excel_parser import excel_to_mdn
from mdn_parser import mdn_to_excel
from utils import validate_mdn_structure


class MDNConverter:
    """Main converter class for MDN format operations."""
    
    @staticmethod
    def excel_to_mdn(excel_file_path: str, output_file_path: str = None) -> str:
        """
        Convert Excel file to MDN format.
        
        Args:
            excel_file_path: Path to the Excel file
            output_file_path: Optional path to save MDN file (if None, returns content only)
            
        Returns:
            MDN format content as string
        """
        print(f"🔄 Converting Excel to MDN: {excel_file_path}")
        
        # Convert Excel to MDN
        mdn_content = excel_to_mdn(excel_file_path)
        
        # Save to file if output path provided
        if output_file_path:
            with open(output_file_path, 'w', encoding='utf-8') as f:
                f.write(mdn_content)
            print(f"💾 MDN file saved as: {output_file_path}")
        
        return mdn_content
    
    @staticmethod
    def mdn_to_excel(mdn_file_path: str, output_file_path: str) -> None:
        """
        Convert MDN file to Excel format.
        
        Args:
            mdn_file_path: Path to the MDN file
            output_file_path: Path for the output Excel file
        """
        print(f"🔄 Converting MDN to Excel: {mdn_file_path}")
        
        # Read MDN file
        with open(mdn_file_path, 'r', encoding='utf-8') as f:
            mdn_content = f.read()
        
        # Convert MDN to Excel
        mdn_to_excel(mdn_content, output_file_path)
        
        print(f"💾 Excel file saved as: {output_file_path}")
    
    @staticmethod
    def validate_mdn(mdn_file_path: str) -> Dict[str, Any]:
        """
        Validate MDN file structure.
        
        Args:
            mdn_file_path: Path to the MDN file
            
        Returns:
            Dictionary with validation results
        """
        print(f"🔍 Validating MDN file: {mdn_file_path}")
        
        with open(mdn_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        validation_result = validate_mdn_structure(content)
        
        if validation_result['valid']:
            print(f"✅ MDN file is valid")
            print(f"   Sections found: {', '.join(validation_result['sections'])}")
            print(f"   Total lines: {validation_result['total_lines']}")
        else:
            print(f"❌ MDN file is invalid: {validation_result['error']}")
        
        return validation_result
    
    @staticmethod
    def round_trip_test(excel_file_path: str, output_dir: str = ".") -> bool:
        """
        Test round-trip conversion: Excel → MDN → Excel.
        
        Args:
            excel_file_path: Path to the original Excel file
            output_dir: Directory to save intermediate and output files
            
        Returns:
            True if round-trip was successful, False otherwise
        """
        import os
        
        print(f"🔄🔄🔄 Starting round-trip test: {excel_file_path}")
        
        # Step 1: Excel → MDN
        print("\n📤 Step 1: Converting Excel to MDN...")
        mdn_content = excel_to_mdn(excel_file_path)
        
        # Save intermediate MDN file
        base_name = os.path.splitext(os.path.basename(excel_file_path))[0]
        mdn_file_path = os.path.join(output_dir, f"{base_name}_intermediate.mdn")
        
        with open(mdn_file_path, 'w', encoding='utf-8') as f:
            f.write(mdn_content)
        
        print(f"   💾 Intermediate MDN saved as: {mdn_file_path}")
        
        # Step 2: MDN → Excel
        print("\n📥 Step 2: Converting MDN back to Excel...")
        output_excel_path = os.path.join(output_dir, f"{base_name}_roundtrip.xlsx")
        mdn_to_excel(mdn_content, output_excel_path)
        
        print(f"   💾 Round-trip Excel saved as: {output_excel_path}")
        
        # Step 3: Validate MDN structure
        print("\n🔍 Step 3: Validating MDN structure...")
        validation_result = validate_mdn_structure(mdn_content)
        
        if not validation_result['valid']:
            print(f"   ❌ MDN validation failed: {validation_result['error']}")
            return False
        
        print(f"   ✅ MDN structure is valid")
        
        # Step 4: Compare file sizes (basic check)
        print("\n📊 Step 4: Basic file comparison...")
        original_size = os.path.getsize(excel_file_path)
        roundtrip_size = os.path.getsize(output_excel_path)
        
        print(f"   Original Excel: {original_size:,} bytes")
        print(f"   Round-trip Excel: {roundtrip_size:,} bytes")
        print(f"   MDN intermediate: {len(mdn_content):,} characters")
        
        # Success criteria
        success = True
        if roundtrip_size == 0:
            print("   ❌ Round-trip Excel file is empty")
            success = False
        elif validation_result['valid']:
            print("   ✅ Round-trip test completed successfully!")
        else:
            print("   ❌ Round-trip test failed validation")
            success = False
        
        return success


def main():
    """Main function for command-line usage."""
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='MDN Format Converter')
    parser.add_argument('command', choices=['excel2mdn', 'mdn2excel', 'validate', 'roundtrip'],
                       help='Conversion command to perform')
    parser.add_argument('input_file', help='Input file path')
    parser.add_argument('output_file', nargs='?', help='Output file path (optional for some commands)')
    parser.add_argument('--output-dir', default='.', help='Output directory for round-trip tests')
    
    args = parser.parse_args()
    
    try:
        if args.command == 'excel2mdn':
            if args.output_file:
                MDNConverter.excel_to_mdn(args.input_file, args.output_file)
            else:
                mdn_content = MDNConverter.excel_to_mdn(args.input_file)
                print("\n" + "="*50)
                print("MDN CONTENT:")
                print("="*50)
                print(mdn_content)
        
        elif args.command == 'mdn2excel':
            if not args.output_file:
                print("Error: output_file is required for mdn2excel command")
                sys.exit(1)
            MDNConverter.mdn_to_excel(args.input_file, args.output_file)
        
        elif args.command == 'validate':
            MDNConverter.validate_mdn(args.input_file)
        
        elif args.command == 'roundtrip':
            success = MDNConverter.round_trip_test(args.input_file, args.output_dir)
            sys.exit(0 if success else 1)
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
