#!/usr/bin/env python3

import argparse
import csv
import string
import os
import requests
from fuzzywuzzy import process

# Function to remove punctuation and lowercase a string
def clean_string(s):
    return s.translate(str.maketrans('', '', string.punctuation)).lower()

# Parse the command line argument for the CSV file path
parser = argparse.ArgumentParser(description='Prompt Optimization Checker')
parser.add_argument('csv_file', type=str, help='Path to the CSV file containing prompts')
args = parser.parse_args()

# Read CSV file and store data
prompts_data = []
with open(args.csv_file, mode='r', newline='', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        prompts_data.append(row)

# Load API key from environment variable
PROMPTPERFECT_API_KEY = os.environ.get("PROMPTPERFECT_API_KEY")

# Function to call PromptPerfect API
def get_optimized_prompt(user_prompt, target_model):
    url = "https://api.promptperfect.jina.ai/optimize"
    headers = {
        "x-api-key": f"token {PROMPTPERFECT_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "data": {
            "prompt": user_prompt,
            "targetModel": target_model
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    response_data = response.json()
    return response_data["result"]["results"][0]["promptOptimized"]

# Get user input for prompt and target model
user_prompt = input("Please enter your AI prompt: ").strip()
target_model_input = input("Please enter the target model (press Enter for default 'claude-2'): ").strip()

# Use 'claude-2' as default if user presses Enter
target_model = target_model_input if target_model_input else 'claude-2'

# Clean the user prompt for comparison
cleaned_user_prompt = clean_string(user_prompt)

# Check for exact matching prompts
exact_matching_prompts = []
for prompt in prompts_data:
    if clean_string(prompt['prompt']) == cleaned_user_prompt and prompt['target_model'].lower() == target_model.lower():
        exact_matching_prompts.append(prompt)

# Fuzzy matching - find the top 3 matches that are not in the exact matches
fuzzy_matches = process.extractBests(cleaned_user_prompt, [clean_string(p['prompt']) for p in prompts_data], limit=3)
fuzzy_matching_prompts = []

for p, score in fuzzy_matches:
    if score < 50:  # Exclude matches with a score below 50
        continue
    for prompt in prompts_data:
        if clean_string(prompt['prompt']) == p and prompt not in exact_matching_prompts:
            fuzzy_matching_prompts.append((prompt, score))

# Display matching prompts and ask for user choice
if exact_matching_prompts or fuzzy_matching_prompts:
    print("\nMatching prompts found:")
    for i, match in enumerate(exact_matching_prompts, 1):
        print(f"{i}) original prompt: {match['prompt']}\n   optimized_prompt: {match['prompt_optimized']}\n   target_model: {match['target_model']}")
    
    for i, (match, score) in enumerate(fuzzy_matching_prompts, len(exact_matching_prompts) + 1):
        print(f"{i}) original prompt: {match['prompt']}\n   optimized_prompt: {match['prompt_optimized']}\n   target_model: {match['target_model']}\n   Text matching score: {score}")

    choice = input("\nDo you want to use one of these previously optimized prompts? Please enter 'no', a number to pick a prompt, or 'reject' to get a new optimized prompt: ").strip().lower()
    if choice.isdigit() and 1 <= int(choice) <= (len(exact_matching_prompts) + len(fuzzy_matching_prompts)):
        selected_match = exact_matching_prompts + [match for match, score in fuzzy_matching_prompts]
        print("Selected optimized prompt:", selected_match[int(choice) - 1]['prompt_optimized'])
    elif choice == 'reject':
        print("Fetching an optimized prompt from the PromptPerfect API...")
        optimized_prompt = get_optimized_prompt(user_prompt, target_model)
        print("Optimized Prompt:", optimized_prompt)
        use_optimized = input("Do you want to use this optimized prompt? (Y/N): ").strip().lower()
        if use_optimized == 'y':
            print(optimized_prompt)
            # Log to CSV file
            with open(args.csv_file, mode='a', newline='', encoding='utf-8') as file:
                csv_writer = csv.DictWriter(file, fieldnames=['prompt', 'prompt_optimized', 'target_model'], quoting=csv.QUOTE_ALL)
                csv_writer.writerow({'prompt': user_prompt, 'prompt_optimized': optimized_prompt, 'target_model': target_model})

    
        else:
            print("Optimized prompt not used.")
else:
    print("No matching prompts found. Fetching an optimized prompt from the PromptPerfect API...")
    optimized_prompt = get_optimized_prompt(user_prompt, target_model)
    print("Optimized Prompt:", optimized_prompt)
    use_optimized = input("Do you want to use this optimized prompt? (Y/N): ").strip().lower()
    if use_optimized == 'y':
        print(optimized_prompt)
        # Log to CSV file
        with open(args.csv_file, mode='a', newline='', encoding='utf-8') as file:
            csv_writer = csv.DictWriter(file, fieldnames=['prompt', 'prompt_optimized', 'target_model'])
            csv_writer.writerow({'prompt': user_prompt, 'prompt_optimized': optimized_prompt, 'target_model': target_model})
    else:
        print("Optimized prompt not used.")
