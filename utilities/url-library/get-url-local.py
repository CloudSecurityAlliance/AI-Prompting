#!/usr/bin/env python3

import sys
import os
import re
from urllib.parse import urlparse


class TransformURL:
    # Transform URLs into their download URLs
    def transform_github_url(self, url):
        pattern = r'https://github\.com/([^/]+)/([^/]+)'
        replacement = r'https://raw.githubusercontent.com/\1/\2/main/README.md'
        return re.sub(pattern, replacement, url)
    

def modify_url_if_domain_matches(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    # Check the domain
    if domain == "github.com":
        transform_url = TransformURL()
        return transform_url.transform_github_url(url)
    else:
        return url
    

def process_url(url):
    # Parse the URL to extract components
    #parsed_url = urlparse(url)
    downloaded_url = modify_url_if_domain_matches(url)
    parsed_downloaded_url = urlparse(downloaded_url)

    print(f"URL: {url}")
    print(f"Download URL: {downloaded_url}")

    # Extract the file extension, if present, else default to 'html'
    path = parsed_downloaded_url.path
    file_extension = os.path.splitext(path)[1][1:]  # Remove the dot from the extension
    if file_extension == '':
        file_extension = 'html'
    print(f"File Extension: {file_extension}")

def main():
    # Check if an argument is provided
    if len(sys.argv) != 2:
        print("Usage: python script.py <URL or file path>")
        sys.exit(1)

    argument = sys.argv[1]

    # Check if the argument is a file
    if os.path.isfile(argument):
        with open(argument, 'r') as file:
            for line in file:
                url = line.strip()
                if url:
                    print(f"\nProcessing URL: {url}")
                    process_url(url)
    else:
        print(f"\nProcessing URL: {argument}")
        process_url(argument)

if __name__ == "__main__":
    main()

    
