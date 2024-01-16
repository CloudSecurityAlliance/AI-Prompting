#!/usr/bin/env python3

import json
import sys

def process_element(element, indent=0):
    md = ""
    indent_str = "  " * indent  # Two spaces per indentation level

    if isinstance(element, dict):
        for key, value in element.items():
            if isinstance(value, (dict, list)):
                md += f"{indent_str}- **{key}**: \n" + process_element(value, indent + 1)
            else:
                md += f"{indent_str}- **{key}**: {value}\n"
    elif isinstance(element, list):
        for item in element:
            md += f"{indent_str}- " + process_element(item, indent + 1).lstrip('- ')
    else:
        md += f"{indent_str}{element}\n"

    return md

def json_to_markdown(json_file, markdown_file):
    with open(json_file, 'r') as file:
        data = json.load(file)

    markdown_content = process_element(data)
    
    with open(markdown_file, 'w') as file:
        file.write(markdown_content)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py [input_json_file] [output_markdown_file]")
        sys.exit(1)

    json_file = sys.argv[1]  # First argument: JSON file path
    markdown_file = sys.argv[2]  # Second argument: Markdown file path

    json_to_markdown(json_file, markdown_file)

