#!/usr/bin/env python3

import os
import PyPDF2
import html2text
import chardet  # For detecting encoding

def convert_pdf_to_text(pdf_path, txt_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text() or ''  # Using 'or' to handle None return
    with open(txt_path, 'w', encoding='utf-8') as file:
        file.write(text)

def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        return chardet.detect(file.read())['encoding']

def convert_html_to_text(html_path, txt_path):
    # Detect encoding
    encoding = detect_encoding(html_path)

    try:
        # Try to read with detected encoding
        with open(html_path, 'r', encoding=encoding) as file:
            html_content = file.read()
    except UnicodeDecodeError:
        # If failed, try with 'latin-1' encoding
        with open(html_path, 'r', encoding='latin-1') as file:
            html_content = file.read()

    text_content = html2text.html2text(html_content)
    with open(txt_path, 'w', encoding='utf-8') as file:
        file.write(text_content)


def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            filename, file_extension = os.path.splitext(file_path)
            txt_path = f"{filename}.txt"

            if file_extension.lower() == '.pdf':
                convert_pdf_to_text(file_path, txt_path)
            else:
                convert_html_to_text(file_path, txt_path)

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python script.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    process_directory(directory)
