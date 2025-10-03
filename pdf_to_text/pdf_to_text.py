#!pip install pdfplumber
import pdfplumber

def pdf_to_text_pdfplumber(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Usage with additional options
def pdf_to_text_advanced(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            # Extract text with layout preservation
            text += page.extract_text(x_tolerance=1, y_tolerance=1)
            
            # Extract tables (if any)
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    text += " | ".join([str(cell) for cell in row if cell]) + "\n"
    return text

# Usage
pdf_file = "/content/sample_data/CV_brief_2025-09-22_1010hr.pdf"

text = pdf_to_text_pdfplumber(pdf_file)

print(text)

# Write to text file
output_file = "/content/sample_data/cv_text.txt"

with open(output_file, 'w', encoding='utf-8') as file:
    file.write(text)

print(f"Text successfully written to {output_file}")

