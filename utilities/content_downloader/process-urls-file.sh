#!/bin/bash

# Check for the correct number of arguments
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <input_file> <output_directory>"
    exit 1
fi

# Assign command line arguments to variables
input_file=$1
output_dir=$2

# Create the output directory if it does not exist
if [ ! -d "$output_dir" ]; then
    mkdir -p "$output_dir"
fi

# Change into the output directory
cd "$output_dir"

# Process each URL in the input file
while IFS= read -r url; do
    # Run the content downloader script for each URL
    ~/GitHub/AI-Prompting/utilities/content_downloader/content_downloader.py --url="$url"
done < "$input_file"

