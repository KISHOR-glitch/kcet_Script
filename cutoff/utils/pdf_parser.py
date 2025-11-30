import pdfplumber
import re
from typing import Dict, List, Tuple
from io import BytesIO


class PDFParser:
    """Parse KCET cutoff PDFs using fast text extraction"""

    def __init__(self, pdf_file):
        self.pdf_file = pdf_file
        self.parsed_data = []

    def parse(self) -> Tuple[bool, Dict]:
        """Fast text-based parsing"""
        try:
            result = {'success': False, 'total_rows': 0, 'extracted_data': [], 'errors': [], 'colleges_found': []}
            
            if hasattr(self.pdf_file, 'read'):
                pdf_content = self.pdf_file.read()
            else:
                with open(self.pdf_file, 'rb') as f:
                    pdf_content = f.read()

            pdf_bytes = BytesIO(pdf_content)

            with pdfplumber.open(pdf_bytes) as pdf:
                if len(pdf.pages) == 0:
                    result['errors'].append('PDF has no pages')
                    return False, result

                full_text = ""
                for page_num in range(len(pdf.pages)):  # Read ALL pages
                    try:
                        text = pdf.pages[page_num].extract_text() or ""
                        full_text += text + "\n"
                    except:
                        pass

            parsed_rows = self._parse_text(full_text)
            if not parsed_rows:
                result['errors'].append('No cutoff data found')
                return False, result

            college_codes = re.findall(r'E\d{3}', full_text)
            result['colleges_found'] = list(set(college_codes))
            result['extracted_data'] = parsed_rows
            result['total_rows'] = len(parsed_rows)
            result['success'] = True
            return True, result

        except Exception as e:
            return False, {'success': False, 'errors': [f'PDF error: {str(e)}'], 'total_rows': 0, 'extracted_data': [], 'colleges_found': []}

    def _parse_text(self, text: str) -> List[Dict]:
        """Parse cutoff lines from text"""
        parsed_rows = []
        lines = text.split('\n')
        
        current_college_code = None
        current_college_name = None
        pending_branch_line = None  # For incomplete branch lines
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line or len(line) < 3:
                continue
            
            # Check if this is a college header line (contains "E" followed by 3 digits)
            college_match = re.search(r'E\d{3}\s+(.+?)(?:\s+\(|$)', line)
            if college_match and re.search(r'E\d{3}', line):
                current_college_code = re.search(r'E\d{3}', line).group()
                college_name = college_match.group(1).strip()
                # Clean up college name
                college_name = re.sub(r'\s*\(.*?\)\s*', ' ', college_name).strip()
                current_college_name = college_name
                pending_branch_line = None
                continue
            
            # Skip header lines with category codes
            if re.search(r'\b[0-9]G\s+[0-9]K\s+[0-9]R\b', line):
                continue
            
            # Check if this is a branch data line (starts with 2 letter codes followed by numbers)
            # Pattern: "XX BranchName Numbers..."
            branch_match = re.match(r'^([A-Z]{2})\s+([A-Za-z\s\.\-]+?)\s+(\d.*)$', line)
            if branch_match and current_college_code:
                branch_code = branch_match.group(1)
                branch_name = branch_match.group(2).strip()
                ranks_part = branch_match.group(3)
                
                # Check next line for continuation (multi-line branch name)
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    # If next line is pure text (no numbers), it's continuation of branch name
                    if next_line and not re.search(r'\d', next_line) and len(next_line) < 50:
                        branch_name += " " + next_line
                        # Skip the next line in next iteration
                        lines[i + 1] = ''
                
                # Parse ranks
                # Split by spaces but keep '-' and '--'
                rank_parts = re.findall(r'--|-|\d+', ranks_part)
                
                # Create records for each category
                categories = ['1G', '1K', '1R', '2AG', '2AK', '2AR', '2BG', '2BK', '2BR', '3AG', '3AK', '3AR', '3BG', '3BK', '3BR', '4G', '4K', '4R', 'STG', 'STK', 'STR']
                
                for idx, cat_code in enumerate(categories):
                    rank_value = None
                    if idx < len(rank_parts):
                        part = rank_parts[idx]
                        if part and part not in ['-', '--']:
                            rank_value = part
                    
                    parsed_rows.append({
                        'college_code': current_college_code,
                        'college_name': current_college_name,
                        'branch_name': branch_name,
                        'category_code': cat_code,
                        'category_description': self._get_category_description(cat_code),
                        'cutoff_rank': rank_value,
                        'page_num': 0
                    })
        
        return parsed_rows

    def _get_category_description(self, code: str) -> str:
        """Get category description"""
        desc = {
            '1G': 'General - 1st', '1K': 'Kannada - 1st', '1R': 'Reserved - 1st',
            '2AG': 'OBC - 2nd', '2AK': 'OBC Kannada - 2nd', '2AR': 'OBC Reserved - 2nd',
            '2BG': 'General - 2nd', '2BK': 'Kannada - 2nd', '2BR': 'Reserved - 2nd',
            '3AG': 'SC - 3rd', '3AK': 'SC Kannada - 3rd', '3AR': 'SC Reserved - 3rd',
            '3BG': 'SC - 3rd', '3BK': 'SC Kannada - 3rd', '3BR': 'SC Reserved - 3rd',
            '4G': 'ST - 4th', '4K': 'ST Kannada - 4th', '4R': 'ST Reserved - 4th',
            'STG': 'Special - General', 'STK': 'Special - Kannada', 'STR': 'Special - Reserved',
        }
        return desc.get(code, code)


def save_cutoff_data(parsed_data: List[Dict], year_obj, round_obj) -> Tuple[int, int, List[str]]:
    """Save parsed data to database"""
    from ..models import College, Branch, Category, Cutoff

    inserted = 0
    updated = 0
    errors = []
    
    colleges = {}
    for row in parsed_data:
        col_code = row.get('college_code', 'Unknown')
        if col_code not in colleges:
            colleges[col_code] = []
        colleges[col_code].append(row)

    for col_code, rows in colleges.items():
        try:
            # Use college_name from parsed data, fallback to code
            col_name = rows[0].get('college_name', col_code) if rows else col_code
            college, _ = College.objects.get_or_create(name=col_name, defaults={'city': 'Not Specified'})
        except Exception as e:
            errors.append(str(e))
            continue

        for row in rows:
            try:
                branch, _ = Branch.objects.get_or_create(
                    college=college,
                    name=row['branch_name']
                )
                category, _ = Category.objects.get_or_create(code=row['category_code'], defaults={'description': row['category_description']})
                cutoff, created = Cutoff.objects.update_or_create(
                    college=college, branch=branch, category=category, year=year_obj, round=round_obj,
                    defaults={'cutoff_rank': row['cutoff_rank']}
                )
                if created:
                    inserted += 1
                else:
                    updated += 1
            except Exception as e:
                errors.append(str(e))

    return inserted, updated, errors
