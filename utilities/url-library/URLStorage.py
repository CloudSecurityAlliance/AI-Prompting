#!/usr/bin/env python3

# To fdind the SHA512 of a URL at the command line:
#
# echo -n "https://github.com/cloudsecurityalliance/gsd-database" | sha512sum
#
# Make sure you remove the line return at the end of the URL

import sys
import os
import os.path
import subprocess
from urllib.parse import urlparse
import hashlib
import requests

def extract_info(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    path = parsed_url.path
    extension = path.split('.')[-1] if '.' in path else 'html'
    print(f"URL: {url}, Domain: {domain}, Extension: {extension}")
    return domain, extension

def download_url(url, domain, extension):
    hash_name = hashlib.sha512(url.encode()).hexdigest()
    file_name = f"{hash_name}.{extension.lower()}"
    dir_name = os.path.join("downloads", domain)

    os.makedirs(dir_name, exist_ok=True)
    file_path = os.path.join(dir_name, file_name)

    if extension == 'html':
        command = ["google-chrome", "--no-sandbox", "--crash-dumps-dir=/tmp/www",
                   "--disable-crash-reporter", "--headless", "--disable-gpu",
                   "--enable-javascript", "--dump-dom", url]
        with open(file_path, "w") as file:
            subprocess.run(command, stdout=file)
    else:
        response = requests.get(url)
        with open(file_path, "wb") as file:
            file.write(response.content)

def main(input_arg):
    if os.path.isfile(input_arg):
        with open(input_arg, 'r') as file:
            for line in file:
                url = line.strip()
                if url:  # Check to ensure the line is not empty
                    domain, extension = extract_info(url)
                    download_url(url, domain, extension)
    else:
        domain, extension = extract_info(input_arg)
        download_url(input_arg, domain, extension)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: script.py <URL or file>")
        sys.exit(1)
    
    main(sys.argv[1])

