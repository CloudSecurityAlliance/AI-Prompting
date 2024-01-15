#!/usr/bin/env python3
import sys
from PyPDF2 import PdfReader
from markdownify import markdownify as md

def convert_pdf_to_markdown(pdf_path):
    # Open the PDF file
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)

        # Initialize a variable to store all text
        full_text = ""

        # Iterate over each page and extract text
        for page in reader.pages:
            text = page.extract_text()
            if text:
                full_text += text

        # Convert extracted text to Markdown
        markdown_text = md(full_text)

    return markdown_text

if __name__ == "__main__":
    # Check if the PDF path is provided as a command line argument
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_pdf>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    markdown_text = convert_pdf_to_markdown(pdf_path)

    # Print or save the markdown text as needed
    print(markdown_text)
    # Optionally, save to a file
    with open('output.md', 'w') as md_file:
        md_file.write(markdown_text)

        
