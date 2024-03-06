#!/bin/bash

# Check for correct usage
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <path_to_csv_file> <path_to_directory_with_files> <output_csv_file>"
    exit 1
fi

# Assign arguments to variables
csv_file="$1"
dir_with_files="$2"
output_csv_file="$3"

# Create or clear the output file
> "$output_csv_file"

# Read the CSV file line by line
while IFS=, read -r url hash; do
    # Initialize filename as 'Not Found' to handle the case where the file doesn't exist
    filename="Not Found"

    # Check if a file with the hash name exists in the given directory, considering both .json and .pdf extensions
    if [[ -f "$dir_with_files/${hash}.json" ]]; then
        filename="${hash}.json"
    elif [[ -f "$dir_with_files/${hash}.pdf" ]]; then
        filename="${hash}.pdf"
    elif [[ -f "$dir_with_files/${hash}.txt" ]]; then
        filename="${hash}.txt"
    fi

    # Write the original CSV line with the filename (or 'Not Found') appended to the output CSV file
    echo "$url,$hash,$filename" >> "$output_csv_file"
done < "$csv_file"

echo "Processing complete. Output saved to $output_csv_file"
