"""PDF parsing utilities for extracting prayer times."""

import re
import pdfplumber
from typing import Tuple, List, Dict

from src.utils.text_utils import extract_zone_from_text, extract_month_from_text, clean_time
from src.utils.date_utils import parse_date


class PDFParser:
    """Parse prayer times from PDF files."""
    
    def extract_text_and_metadata(self, pdf_path: str) -> Tuple[str, str, str]:
        """
        Extract all text and identify zone and month.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Tuple of (all_text, zone, month)
        """
        with pdfplumber.open(pdf_path) as pdf:
            all_text = ""
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                all_text += page_text + "\n"
            
            zone = extract_zone_from_text(all_text)
            month = extract_month_from_text(all_text)
            
            return all_text, zone, month
    
    def extract_tables(self, pdf_path: str) -> List[List[List]]:
        """
        Extract all tables from PDF.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            List of tables from all pages
        """
        all_tables = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                if tables:
                    all_tables.extend(tables)
        return all_tables
    
    def parse_table_rows(self, table: List[List], month: str) -> List[Dict]:
        """
        Parse prayer times from a table.
        
        Args:
            table: 2D list representing table
            month: Month number (01-12)
            
        Returns:
            List of prayer time dictionaries
        """
        if not table or len(table) < 2:
            return []
        
        # Find header row
        header_row_idx = self._find_header_row(table)
        if header_row_idx is None:
            return []
        
        # Parse data rows
        prayer_times = []
        data_rows = table[header_row_idx + 1:]
        
        for row in data_rows:
            prayer_data = self._parse_single_row(row, month)
            if prayer_data:
                prayer_times.append(prayer_data)
        
        return prayer_times
    
    def _find_header_row(self, table: List[List]) -> int:
        """Find the header row in a table."""
        for i, row in enumerate(table):
            if row and len(row) >= 6:
                row_text = ' '.join([str(cell).upper() if cell else '' for cell in row])
                if ('FAJR' in row_text or 'DATE' in row_text) and 'MAGHRIB' in row_text:
                    return i
        return None
    
    def _parse_single_row(self, row: List, month: str) -> Dict:
        """Parse a single table row into prayer times."""
        if not row or len(row) < 6:
            return None
        
        try:
            date_str = str(row[0]).strip() if row[0] else ""
            if not date_str or date_str.lower() in ['none', 'null', '']:
                return None
            if not re.search(r'\d', date_str):
                return None
            
            parsed_date = parse_date(date_str, month)
            if not parsed_date:
                return None
            
            prayer_data = {
                "date": parsed_date,
                "fajr": clean_time(str(row[1] or "")),
                "sunrise": clean_time(str(row[2] or "")),
                "dhuhr": clean_time(str(row[3] or "")),
                "asr": clean_time(str(row[4] or "")),
                "maghrib": clean_time(str(row[5] or "")),
                "isha": clean_time(str(row[6] or "")) if len(row) > 6 else ""
            }
            
            # Validate essential fields
            if all(prayer_data[field] for field in ["fajr", "maghrib", "isha"]):
                return prayer_data
            
        except Exception:
            pass
        
        return None
    
    def extract_from_text_pattern(self, text: str, month: str) -> List[Dict]:
        """
        Fallback text-based extraction using regex.
        
        Args:
            text: PDF text content
            month: Month number (01-12)
            
        Returns:
            List of prayer time dictionaries
        """
        pattern = (
            r'(?:'
            r'(\d{1,2})-(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)'
            r'|'
            r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-(\d{1,2})'
            r')\s+'
            r'(\d{1,2}:\d{2}\s*[APap][Mm]?)\s+'  # Fajr
            r'(\d{1,2}:\d{2}\s*[APap][Mm]?)\s+'  # Sunrise
            r'(\d{1,2}:\d{2}\s*[APap][Mm]?)\s+'  # Luhr
            r'(\d{1,2}:\d{2}\s*[APap][Mm]?)'     # Asr
            r'(?:\s+(\d{1,2}:\d{2}\s*[APap][Mm]?))?'  # Maghrib
            r'(?:\s+(\d{1,2}:\d{2}\s*[APap][Mm]?))?'  # Isha
        )
        
        matches = re.findall(pattern, text, re.IGNORECASE)
        prayer_times = []
        
        for match in matches:
            day1, _, _, day2, fajr, sunrise, dhuhr, asr, maghrib, isha = match
            day = day1 or day2
            
            parsed_date = f"{month}-{int(day):02d}"
            prayer_data = {
                "date": parsed_date,
                "fajr": fajr.strip(),
                "sunrise": sunrise.strip(),
                "dhuhr": dhuhr.strip(),
                "asr": asr.strip(),
                "maghrib": maghrib.strip() if maghrib else "",
                "isha": isha.strip() if isha else ""
            }
            prayer_times.append(prayer_data)
        
        return prayer_times