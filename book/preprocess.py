import pdfplumber
import re
import os
# from langdetect import detect # Not used, can be commented out

PDF_PATH = os.path.join(os.path.dirname(__file__), 'hsc26_bangla_1st_paper.pdf')

# Basic cleaning for Bangla and English
BANGLA_UNICODE_RANGE = r"\u0980-\u09FF"
ENGLISH_UNICODE_RANGE = r"A-Za-z"


def clean_text(text):
    # Remove extra whitespace, newlines, and non-textual artifacts
    text = re.sub(r'\s+', ' ', text)
    # TEMPORARILY RELAXED REGEX: Only remove control characters and multiple spaces
    # This allows us to see if the PDF extraction itself is working before aggressive cleaning.
    text = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', text) # Remove common control characters
    text = re.sub(r'\s+', ' ', text).strip() # Consolidate spaces and strip
    return text


def extract_text_from_pdf(pdf_path=PDF_PATH):
    all_text = []
    print(f"DEBUG: Attempting to open PDF: {pdf_path}")
    if not os.path.exists(pdf_path):
        print(f"ERROR: PDF file not found at: {pdf_path}")
        return ""

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                raw = page.extract_text() or ''
                print(f"DEBUG: Page {i+1} Raw Text (first 100 chars): '{raw[:100]}...' (Length: {len(raw)})")
                cleaned = clean_text(raw)
                print(f"DEBUG: Page {i+1} Cleaned Text (first 100 chars): '{cleaned[:100]}...' (Length: {len(cleaned)})")
                if cleaned:
                    all_text.append(cleaned)
                else:
                    print(f"DEBUG: Page {i+1} yielded no cleaned text.")
        final_text = '\n'.join(all_text)
        print(f"DEBUG: Total extracted text length: {len(final_text)}")
        return final_text
    except Exception as e:
        print(f"ERROR: An error occurred during PDF extraction: {e}")
        return ""

if __name__ == "__main__":
    text = extract_text_from_pdf()
    cleaned_text_path = os.path.join(os.path.dirname(__file__), 'cleaned_text.txt')
    with open(cleaned_text_path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"Text extracted and cleaned. Saved to {cleaned_text_path}. Total length: {len(text)}")