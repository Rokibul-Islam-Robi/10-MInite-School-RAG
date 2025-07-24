import pdfplumber
import re
import os
from langdetect import detect

PDF_PATH = os.path.join(os.path.dirname(__file__), 'hsc26_bangla_1st_paper.pdf')

# Basic cleaning for Bangla and English
BANGLA_UNICODE_RANGE = r"\u0980-\u09FF"
ENGLISH_UNICODE_RANGE = r"A-Za-z"


def clean_text(text):
    # Remove extra whitespace, newlines, and non-textual artifacts
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\u0980-\u09FFA-Za-z0-9.,?!;:()\-\'\" ]', '', text)
    return text.strip()


def extract_text_from_pdf(pdf_path=PDF_PATH):
    all_text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            raw = page.extract_text() or ''
            cleaned = clean_text(raw)
            if cleaned:
                all_text.append(cleaned)
    return '\n'.join(all_text)

if __name__ == "__main__":
    text = extract_text_from_pdf()
    with open(os.path.join(os.path.dirname(__file__), 'cleaned_text.txt'), 'w', encoding='utf-8') as f:
        f.write(text)
    print("Text extracted and cleaned. Saved to cleaned_text.txt.") 