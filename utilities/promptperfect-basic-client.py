#!/usr/bin/env python3

import requests
import os
import json

# Load API key from environment variable
PROMPTPERFECT_API_KEY = os.environ.get("PROMPTPERFECT_API_KEY")

url = "https://api.promptperfect.jina.ai/optimize"

headers = {
    "x-api-key": f"token {PROMPTPERFECT_API_KEY}",
    "Content-Type": "application/json"
}

# Prompt the user for input
user_prompt = input("Please enter your AI prompt: ")

payload = {
    "data": {
        "prompt": user_prompt,
        "targetModel": "claude-2"  # Updated to use Claude-2
    }
}

response = requests.post(url, headers=headers, json=payload)

# Parse the JSON response and extract the 'promptOptimized' field
response_data = response.json()
#prompt_optimized = response_data.get('results', {}).get('promptOptimized', 'No optimized prompt found.')
prompt_optimized = response_data["result"]["results"][0]["promptOptimized"]

print(prompt_optimized)
