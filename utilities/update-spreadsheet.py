#!/usr/bin/env python3

import csv
import hashlib
import os
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Process and update a CSV file based on markdown files in a specified directory.")
    parser.add_argument("input_csv", help="Path to the input CSV file")
    parser.add_argument("output_csv", help="Path for the output CSV file")
    parser.add_argument("data_directory", help="Directory containing markdown data files")
    return parser.parse_args()

def load_and_process_csv(input_csv, data_directory):
    processed_data = []

    with open(input_csv, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            url = row['Link to primary content']
            file_type = determine_file_type(url)
            sha256_checksum = hashlib.sha256(url.encode()).hexdigest().lower()

            exists, file_path = find_markdown_file(data_directory, sha256_checksum, file_type)
            markdown_content = read_markdown_file(file_path) if exists else ""

            processed_row = {
                **row, 
                'file_type': file_type, 
                'url_checksum': sha256_checksum, 
                'markdown_exists': exists, 
                'Primary_Content_markdown': markdown_content
            }
            processed_data.append(processed_row)

    return processed_data

def determine_file_type(url):
    if url.endswith('.pdf'):
        return 'pdf'
    elif url.endswith('.json'):
        return 'json'
    elif url.endswith('.html') or '.' not in url.split('/')[-1]:
        return 'html'
    else:
        return 'unknown'

def find_markdown_file(data_directory, sha256_checksum, file_extension):
    filename = f"{sha256_checksum}.{file_extension}.md"
    file_path = os.path.join(data_directory, filename)
    return os.path.isfile(file_path), file_path

def read_markdown_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def write_csv(output_csv, data):
    with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys(), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, escapechar='\\', lineterminator='\r\n')
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def main():
    args = parse_arguments()

    processed_data = load_and_process_csv(args.input_csv, args.data_directory)
    write_csv(args.output_csv, processed_data)

if __name__ == "__main__":
    main()
