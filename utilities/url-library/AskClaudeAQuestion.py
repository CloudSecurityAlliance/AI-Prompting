#!/usr/bin/env python3

import asyncio
import os
import sys
import httpx
from anthropic import AsyncAnthropic, HUMAN_PROMPT, AI_PROMPT

# Get the API key from the environment variable
api_key = os.getenv('ANTHROPIC_API_KEY')
if not api_key:
    raise ValueError("No API key found. Please set the ANTHROPIC_API_KEY environment variable.")

# Initialize the AsyncAnthropic client
anthropic = AsyncAnthropic(api_key=api_key)

async def ask_claude():
    # Check if the file paths are given as command line arguments
    if len(sys.argv) != 3:
        raise ValueError("Please provide two file paths as command line arguments.")

    question_file_path = sys.argv[1]
    additional_file_path = sys.argv[2]

    # Read the user question from the first file
    try:
        with open(question_file_path, 'r') as file:
            user_question = file.read().strip()
    except FileNotFoundError:
        raise FileNotFoundError(f"Question file not found: {question_file_path}")

    # Read additional text from the second file
    try:
        with open(additional_file_path, 'r') as file:
            additional_text = file.read().strip()
    except FileNotFoundError:
        raise FileNotFoundError(f"Additional text file not found: {additional_file_path}")

    # Combine user question with additional text
    combined_prompt = f"{user_question}\n\n{additional_text}"

    # Try to send the combined prompt to Claude
    try:
        completion = await anthropic.completions.create(
            model="claude-2.1",
            max_tokens_to_sample=3000,
            prompt=f"{HUMAN_PROMPT} {combined_prompt}{AI_PROMPT}"
        )

        # Print the response from Claude
        print("Claude's response:", completion.completion)
    except httpx.RemoteProtocolError:
        print("Error: Server disconnected without sending a response.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Run the async function
asyncio.run(ask_claude())
