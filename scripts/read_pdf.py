#!/usr/bin/env python3
"""
MAS Hub PDF Reader Utility
Usage: python3 read_pdf.py <pdf_path> [max_pages]
Returns: Full text content of PDF
"""

import sys
import fitz  # PyMuPDF

def read_pdf(pdf_path, max_pages=None):
    """Read PDF and return text content."""
    if not pdf_path.lower().endswith('.pdf'):
        print(f"Error: Not a PDF file: {pdf_path}", file=sys.stderr)
        return None
    
    try:
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        
        if max_pages:
            total_pages = min(total_pages, max_pages)
        
        full_text = ""
        for page_num in range(total_pages):
            text = doc[page_num].get_text("text")
            if text.strip():
                full_text += f"\n\n--- Page {page_num + 1} ---\n\n{text}"
        
        doc.close()
        return full_text.strip()
    
    except Exception as e:
        print(f"Error reading PDF: {e}", file=sys.stderr)
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 read_pdf.py <pdf_path> [max_pages]", file=sys.stderr)
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    max_pages = int(sys.argv[2]) if len(sys.argv) > 2 else None
    
    text = read_pdf(pdf_path, max_pages)
    if text:
        print(text)
    else:
        sys.exit(1)
