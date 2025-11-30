"""
PDF Parser Testing & Debugging Script
This script helps test the PDF parser without uploading to the web interface
"""

import os
import sys
import django
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kcet_project.settings')
django.setup()

from cutoff.utils.pdf_parser import PDFParser, save_cutoff_data
from cutoff.models import Year, Round


def test_parse_pdf(pdf_path):
    """Test parsing a PDF file"""
    print(f"\n{'='*70}")
    print(f"Testing PDF Parser: {pdf_path}")
    print(f"{'='*70}\n")

    if not os.path.exists(pdf_path):
        print(f"❌ File not found: {pdf_path}")
        return False

    # Parse PDF
    print("📄 Parsing PDF...")
    with open(pdf_path, 'rb') as f:
        parser = PDFParser(f)
        success, result = parser.parse()

    # Show results
    if success:
        print(f"✅ PDF parsed successfully!")
        print(f"\n📊 Extraction Results:")
        print(f"   - College Name: {result.get('college_name', 'Not found')}")
        print(f"   - Total Rows: {result.get('total_rows', 0)}")
        print(f"   - Errors: {len(result.get('errors', []))}")

        if result.get('errors'):
            print(f"\n⚠️  Errors encountered:")
            for error in result.get('errors', []):
                print(f"   - {error}")

        # Show sample data
        data = result.get('extracted_data', [])
        if data:
            print(f"\n📋 Sample Data (first 5 rows):")
            for i, row in enumerate(data[:5]):
                print(f"\n   Row {i+1}:")
                print(f"      Branch: {row['branch_name']}")
                print(f"      Category: {row['category_code']}")
                print(f"      Rank: {row['cutoff_rank']}")

            print(f"\n   ... and {len(data) - 5} more rows" if len(data) > 5 else "")

        # Try saving to database
        print(f"\n💾 Saving to database...")
        try:
            # Get or create year and round
            year, _ = Year.objects.get_or_create(year=2024)
            round_obj, _ = Round.objects.get_or_create(
                name='Round 1',
                defaults={'round_number': 1}
            )

            college_name = result.get('college_name', 'Test College')
            extracted_data = result.get('extracted_data', [])

            inserted, updated, errors = save_cutoff_data(
                extracted_data,
                college_name,
                year,
                round_obj
            )

            print(f"✅ Data saved successfully!")
            print(f"   - Inserted: {inserted}")
            print(f"   - Updated: {updated}")
            
            if errors:
                print(f"   - Warnings: {len(errors)}")
                for error in errors[:3]:
                    print(f"      - {error}")

        except Exception as e:
            print(f"❌ Error saving data: {str(e)}")

        return True
    else:
        print(f"❌ PDF parsing failed!")
        print(f"\n❌ Errors:")
        for error in result.get('errors', []):
            print(f"   - {error}")
        return False


def list_pdf_files():
    """List all PDF files in media directory"""
    media_dir = Path('media/uploads')
    if media_dir.exists():
        pdfs = list(media_dir.glob('*.pdf'))
        if pdfs:
            print("\n📁 Available PDF files:")
            for i, pdf in enumerate(pdfs, 1):
                print(f"   {i}. {pdf.name}")
            return pdfs
    return []


def main():
    """Main function"""
    print("""
    ╔════════════════════════════════════════╗
    ║  KCET PDF Parser Testing Tool           ║
    ╚════════════════════════════════════════╝
    """)

    # List available PDFs
    pdfs = list_pdf_files()

    if not pdfs:
        print("\n❌ No PDF files found in media/uploads/")
        print("\nTo test:")
        print("1. Copy your PDF to: media/uploads/")
        print("2. Run this script again")
        print("3. Or provide PDF path as argument:")
        print("   python test_pdf_parser.py path/to/your/file.pdf")
        return

    # Get PDF to test
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        print("\n📝 Select PDF to test:")
        for i, pdf in enumerate(pdfs, 1):
            print(f"   {i}. {pdf.name}")
        
        choice = input("\nEnter number (or press Enter for first): ").strip()
        pdf_index = int(choice) - 1 if choice else 0
        
        if pdf_index < 0 or pdf_index >= len(pdfs):
            print("❌ Invalid choice")
            return
        
        pdf_path = str(pdfs[pdf_index])

    # Test parsing
    test_parse_pdf(pdf_path)


if __name__ == '__main__':
    main()
