#!/usr/bin/env python3
"""
MDN Format Demo Script
Demonstrates Excel ↔ MDN conversion using sample files.
"""

import os
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mdn_converter import MDNConverter


def main():
    """Run the MDN format demo."""
    print("🎯 MDN Format Demo")
    print("=" * 50)
    
    # Check if sample files exist
    sample_files = ['test_files/financial_sample.xlsx', 'test_files/budget_sample.xlsx']
    available_files = []
    
    for file in sample_files:
        if os.path.exists(file):
            available_files.append(file)
            print(f"✅ Found sample file: {file}")
        else:
            print(f"❌ Missing sample file: {file}")
    
    if not available_files:
        print("\n❌ No sample files found. Please ensure the Excel sample files are in the current directory.")
        return
    
    print(f"\n🚀 Starting demo with {len(available_files)} sample file(s)...")
    
    # Test each sample file
    for sample_file in available_files:
        print(f"\n{'='*60}")
        print(f"📊 Testing: {sample_file}")
        print(f"{'='*60}")
        
        try:
            # Run round-trip test with output directory
            success = MDNConverter.round_trip_test(sample_file, "test_files")
            
            if success:
                print(f"\n🎉 Round-trip test PASSED for {sample_file}")
            else:
                print(f"\n💥 Round-trip test FAILED for {sample_file}")
                
        except Exception as e:
            print(f"\n💥 Error testing {sample_file}: {e}")
    
    print(f"\n{'='*60}")
    print("🏁 Demo completed!")
    print(f"{'='*60}")
    
    # Show generated files
    print("\n📁 Generated files:")
    for file in os.listdir('test_files'):
        if file.endswith('.mdn') or file.endswith('_roundtrip.xlsx'):
            file_path = os.path.join('test_files', file)
            size = os.path.getsize(file_path)
            print(f"   test_files/{file} ({size:,} bytes)")
    
    print(f"\n💡 Try these commands for more control:")
    print(f"   python mdn_converter.py excel2mdn test_files/financial_sample.xlsx")
    print(f"   python mdn_converter.py mdn2excel test_files/financial_sample_intermediate.mdn output.xlsx")
    print(f"   python mdn_converter.py roundtrip test_files/budget_sample.xlsx")


if __name__ == "__main__":
    main()
