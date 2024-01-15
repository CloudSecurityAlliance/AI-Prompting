#!/usr/bin/env python3

# HTML uses about 2-3x times as many tokens as simple markdown text
# So converting web pages to markdown decreases costs, increases speed and is all around a good idea.

import html2text
import sys

def convert_html_to_markdown(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
            markdown = html2text.html2text(html_content)
            return markdown
    except Exception as e:
        return f"An error occurred: {e}"

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <file.html>")
        sys.exit(1)

    file_path = sys.argv[1]
    markdown_content = convert_html_to_markdown(file_path)
    print(markdown_content)

if __name__ == "__main__":
    main()
