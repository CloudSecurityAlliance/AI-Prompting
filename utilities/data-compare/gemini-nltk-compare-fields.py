#!/usr/bin/env python3

import pandas as pd
from nltk.tokenize import word_tokenize
import argparse

# Create a parser for command-line arguments
parser = argparse.ArgumentParser(description="Group similar items in a CSV file")
parser.add_argument("input_file", help="Path to the input CSV file")
parser.add_argument("output_file", help="Path to the output file for grouped items")

args = parser.parse_args()

# Load the CSV file
data = pd.read_csv(args.input_file)

# Define functions for tokenization and stop word removal
def tokenize(text):
    """
    Tokenizes text, handling different data types:
    - Converts floats to strings before tokenization.
    - Skips other non-string data types and returns an empty list.
    """
    if isinstance(text, str):
        tokens = word_tokenize(text.lower())
        stopwords = ["the", "a", "is", "of", "in"]
        return [token for token in tokens if token not in stopwords]
    elif isinstance(text, float):
        return word_tokenize(str(text).lower())  # Convert float to string
    else:
        return []  # Skip other data types

# Extract keywords from each field, handling missing values
data["name_keywords"] = data["NAME_OF_ITEM"].apply(tokenize)
data["alias_keywords"] = data["ALSO_KNOWN_AS"].fillna("").apply(tokenize)  # Fill missing values with empty string
data["description_keywords"] = data["DESCRIPTION"].fillna("").apply(tokenize)

# Calculate Jaccard similarity between pairs of items
def jaccard_similarity(a, b):
    intersection = len(set(a) & set(b))
    union = len(set(a) | set(b))
    return intersection / union

# Create an empty dictionary to store groups
groups = {}

# Iterate through each row and find similar items
for i in range(len(data)):
    item_id = data.loc[i, "CSA_ID"]
    item_keywords = data.loc[i, "name_keywords"] + data.loc[i, "alias_keywords"] + data.loc[i, "description_keywords"]
    
    matches = []
    for j in range(i+1, len(data)):
        other_id = data.loc[j, "CSA_ID"]
        other_keywords = data.loc[j, "name_keywords"] + data.loc[j, "alias_keywords"] + data.loc[j, "description_keywords"]
        similarity = jaccard_similarity(item_keywords, other_keywords)
        if similarity > 0.5:  # Adjust threshold as needed
            matches.append([other_id, similarity])
    
    # Add item to a group or create a new one
    if not matches:
        groups[item_id] = [item_id]
    else:
        best_match = max(matches, key=lambda x: x[1])
        group_id = best_match[0]
        if group_id not in groups:
            groups[group_id] = [group_id]
        groups[group_id].append(item_id)

# Write grouped items to the output file
with open(args.output_file, "w") as f:
    for group_id, items in groups.items():
        f.write(f"Group {group_id}: {', '.join(items)}\n")
