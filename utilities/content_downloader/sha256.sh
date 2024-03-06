#!/bin/bash

# Check if a file path is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <path_to_file>"
    exit 1
fi

# Read from the provided file line by line
while IFS= read -r line || [[ -n "$line" ]]; do
    # Compute the SHA-256 hash of the line, excluding the newline
    hash=$(echo -n "$line" | sha256sum | awk '{print $1}')
    # Print the line followed by its hash
    echo "$line,$hash"
done < "$1"
