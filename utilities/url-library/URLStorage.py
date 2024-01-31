#!/usr/bin/env python3

# To fdind the SHA512 of a URL at the command line:
#
# echo -n "https://github.com/cloudsecurityalliance/gsd-database" | sha512sum
#
# Make sure you remove the line return at the end of the URL

# We do NOT ignore any part of the URL, e.g. #anchors or query strings, we rely on the data 
# to be cleaned up and processed prior to being used here, that is a decision for another level of the system

# Cleaning of typical URL file: 
# get rid of anchors and duplicates:
#
# cat urls.txt | sed 's/#.*$//' | sort | uniq > urls-cleaned.txt

import sys
import os
import os.path
import subprocess
from urllib.parse import urlparse
import hashlib
import requests
from requests.exceptions import ConnectionError, Timeout, RequestException

def extract_info(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    path = parsed_url.path

    # Check if the URL ends with / or \ and treat it as HTML
    if path.endswith(('/', '\\')) or '.' not in path.split('/')[-1]:
        extension = 'html'
    else:
        extension = path.split('.')[-1]

    print(f"URL: {url}, Domain: {domain}, Extension: {extension}")
    return domain, extension

def download_url(url, domain, extension):
    hash_name = hashlib.sha512(url.encode()).hexdigest()
    file_name = f"{hash_name}.{extension.lower()}"
    dir_name = os.path.join("downloads", domain)

    os.makedirs(dir_name, exist_ok=True)
    file_path = os.path.join(dir_name, file_name)

    try:
        if extension == 'html':
            command = ["google-chrome", "--no-sandbox", "--crash-dumps-dir=/tmp/www",
                       "--disable-crash-reporter", "--headless", "--disable-gpu",
                       "--enable-javascript", "--dump-dom", url]
            with open(file_path, "w") as file:
                subprocess.run(command, stdout=file)
        else:
            response = requests.get(url, timeout=10)  # Setting a timeout of 10 seconds
            response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
            with open(file_path, "wb") as file:
                file.write(response.content)
    except ConnectionError:
        print(f"Failed to connect to {url}. Please check your connection or the URL and try again.")
    except Timeout:
        print(f"Request to {url} timed out. Please try again later.")
    except RequestException as e:
        print(f"An error occurred while handling your request to {url}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while downloading from {url}: {e}")

def main(input_arg):
    if os.path.isfile(input_arg):
        with open(input_arg, 'r') as file:
            for line in file:
                url = line.strip()
                if url:
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

