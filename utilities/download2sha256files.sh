#!/bin/bash

# Check if the correct number of command-line arguments is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <url_list_file>"
    exit 1
fi

# Create the 'data' directory if it doesn't exist
mkdir -p data

# Loop through each URL in the provided text file
while IFS= read -r url; do
    # Calculate the SHA256 hash of the URL
    sha256=$(echo -n "$url" | sha256sum | awk '{print $1}')

    echo "Getting $sha256"
    
    # Determine the file extension of the URL
    extension="${url##*.}"

    # Define the output file name based on the extension
    if [ "$extension" == "pdf" ] || [ "$extension" == "json" ]; then
        output_file="data/$sha256.$extension"
    else
        output_file="data/$sha256.html"
    fi

    # Check if the output file already exists, if yes, skip this URL
    if [ -e "$output_file" ]; then
        echo "Skipping $url as $output_file already exists."
        continue
    fi

    # Use curl to download the URL and save it to the appropriate file
    if [ "$extension" == "pdf" ] || [ "$extension" == "json" ]; then
        curl -o "$output_file" "$url"
    else
        google-chrome --no-sandbox \
                      --crash-dumps-dir=/tmp/www \
                      --disable-crash-reporter \
                      --headless --disable-gpu \
                      --enable-javascript \
                      --dump-dom "$url" \
                      2>/dev/null > "$output_file"

	# --headless --disable-gpu --print-to-pdf="$output_file" "$url"
    fi

    # Print a message indicating the download status
    if [ $? -eq 0 ]; then
        echo "Downloaded $url and saved as $output_file"
    else
        echo "Failed to download $url"
    fi

    sleep 1

done < "$1"

echo "Download and processing completed."
