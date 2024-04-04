#!/usr/bin/env python3

import pycurl
from io import BytesIO
import magic
import hashlib
import os
import argparse
import subprocess  # To call Google Chrome headless mode
import sys  # To terminate the program if needed
import urllib.parse  # For parsing the URL and extracting the filename

class ContentDownloader:
    def __init__(self, url, output_format):
        self.url = url
        self.output_format = output_format
        self.sha256_hash = self._generate_sha256_hash(url)
        self.filename = self.sha256_hash  # Initial filename is just the hash
        self.ca_bundle_path = self.find_ca_bundle([
            '/etc/ssl/certs/ca-certificates.crt',
            '/etc/pki/tls/certs/ca-bundle.crt',
            '/etc/ssl/ca-bundle.pem',
            '/etc/pki/tls/cacert.pem',
            '/etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem',
            '/etc/ssl/cert.pem',
        ])
        if not self.ca_bundle_path:
            sys.exit("No CA bundle found. SSL certificate verification might fail. Exiting.")
        self.content = None  # To store the downloaded content

    def _generate_sha256_hash(self, text):
        """Generates a SHA256 hash for the given text."""
        sha256 = hashlib.sha256()
        sha256.update(text.encode('utf-8'))
        return sha256.hexdigest()

    def find_ca_bundle(self, paths):
        """Finds the CA bundle from a list of paths."""
        for path in paths:
            if os.path.exists(path):
                return path
        return None

    def fetch_url(self):
        """Fetches content from the URL and handles 0-sized objects."""
        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, self.url)
        c.setopt(c.WRITEDATA, buffer)
        c.setopt(c.CAINFO, self.ca_bundle_path)
        c.perform()

        if buffer.tell() == 0:
            print("Error: Downloaded content is 0 bytes. No content fetched.")
            c.close()
            return

        self.content = buffer.getvalue()
        c.close()

        # Check for "error code: 1010" in the content if it's text/plain
        if b"error code: 1010" in self.content:
            print("Blocked by Cloudflare")
            sys.exit()

        # Save the content temporarily to determine its MIME type
        temp_filename = f"{self.filename}.tmp"
        with open(temp_filename, "wb") as f:
            f.write(self.content)

        self.filename = temp_filename  # Update filename to temporary file
        self.identify_and_rename_file()  # Rename file based on MIME type

        # If HTML, re-fetch based on the output format
        if self.mime_type == 'text/html':
            if self.output_format == 'pdf':
                print(f"HTML content detected, converting to {self.output_format.upper()} using headless Chrome...")
                self.fetch_html_url_to_pdf()
            elif self.output_format == 'dom':
                print(f"HTML content detected, extracting {self.output_format.upper()} using headless Chrome...")
                self.fetch_html_url_to_dom()

    def fetch_html_url_to_pdf(self):
        """Uses headless Google Chrome to fetch the HTML URL and save it as a PDF."""
        output_filename = f"{self.sha256_hash}.pdf"
        command = [
            "google-chrome",
            "--no-sandbox",
            "--crash-dumps-dir=/tmp",
            "--disable-crash-reporter",
            "--headless",
            "--disable-gpu",
            "--print-to-pdf=" + output_filename,
            self.url
        ]

        try:
            subprocess.run(command, check=True)
            print(f"HTML page saved as PDF: {output_filename}")
            if os.path.exists(self.filename):  # Remove temporary HTML file if exists
                os.remove(self.filename)
            self.filename = output_filename  # Update the filename to the output file
        except subprocess.CalledProcessError as e:
            print(f"Error converting HTML to PDF:", e)

    def fetch_html_url_to_dom(self):
        """Uses headless Google Chrome to fetch the HTML URL and save its DOM."""
        output_filename = f"{self.sha256_hash}.htmldom"
        command = [
            "google-chrome",
            "--no-sandbox",
            "--crash-dumps-dir=/tmp",
            "--disable-crash-reporter",
            "--headless",
            "--disable-gpu",
            "--dump-dom",
            self.url
        ]

        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            with open(output_filename, "w") as file:
                file.write(result.stdout)
            print(f"HTML DOM saved as: {output_filename}")
            if os.path.exists(self.filename):  # Remove temporary HTML file if exists
                os.remove(self.filename)
            self.filename = output_filename  # Update the filename to the output file
        except subprocess.CalledProcessError as e:
            print(f"Error extracting HTML DOM:", e)

    def identify_and_rename_file(self):
        """Identifies the file type and renames the file to include the appropriate extension."""
        # Use python-magic to identify the file MIME type
        mime = magic.Magic(mime=True)
        self.mime_type = mime.from_file(self.filename)

        # Map MIME types to file extensions
        extension_map = {
            'application/pdf': '.pdf',
            'text/plain': '.txt',
            'text/html': '.html',
            'image/jpeg': '.jpg',
            'image/png': '.png',
            # Add more MIME types and extensions as needed
        }
        extension = extension_map.get(self.mime_type, '.unknown')  # Default to '.unknown' for unidentified MIME types

        # Special handling for text/plain to check URL for specific extensions
        if self.mime_type == 'text/plain':
            parsed_url = urllib.parse.urlparse(self.url)
            path_extension = os.path.splitext(parsed_url.path)[1].lower()  # Extract and lowercase the extension
            special_extensions = ['.md', '.json']  # Extend this list as needed

            # If the path's extension is one of the special cases, use it instead
            if path_extension in special_extensions:
                extension = path_extension

        # Rename the file with the determined or default extension
        new_filename = self.sha256_hash + extension
        os.rename(self.filename, new_filename)
        self.filename = new_filename  # Update the filename attribute
        print(f"File saved as: {new_filename}")

def process_url(url, output_format):
    downloader = ContentDownloader(url, output_format)
    downloader.fetch_url()

def process_file(file_path, output_format):
    with open(file_path, 'r') as file:
        urls = file.readlines()
        for url in urls:
            url = url.strip()  # Remove leading/trailing whitespace
            if url:  # Skip empty lines
                process_url(url, output_format)

def main():
    parser = argparse.ArgumentParser(description='Download content, identify its type, and handle HTML by converting it to the specified output format.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--url', help='URL of the content to download')
    group.add_argument('--file', help='File containing a list of URLs to download')
    parser.add_argument('--output', default='pdf', choices=['pdf', 'dom'], help='Output format for HTML content (default: pdf)')
    args = parser.parse_args()

    if args.url:
        process_url(args.url, args.output)
    elif args.file:
        process_file(args.file, args.output)

if __name__ == "__main__":
    main()
