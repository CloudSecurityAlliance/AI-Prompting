#!/usr/bin/env python3
import sys
import os  # Import os module to work with file paths
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

    # Derive Markdown filename from the original PDF path
    md_filename = os.path.splitext(pdf_path)[0] + '.md'

    # Save the markdown text to the new file name
    with open(md_filename, 'w') as md_file:
        md_file.write(markdown_text)

        
