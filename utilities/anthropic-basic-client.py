#!/usr/bin/env python3
import asyncio
import os
from anthropic import AsyncAnthropic, HUMAN_PROMPT, AI_PROMPT

# Get the API key from the environment variable
api_key = os.getenv('ANTHROPIC_API_KEY')
if not api_key:
    raise ValueError("No API key found. Please set the ANTHROPIC_API_KEY environment variable.")

# Initialize the AsyncAnthropic client
anthropic = AsyncAnthropic(api_key=api_key)

async def ask_claude():
    # Get user input
    user_question = input("Please enter your question: ")

    # Send the question to Claude
    completion = await anthropic.completions.create(
        model="claude-2.1",
        max_tokens_to_sample=3000,
        prompt=f"{HUMAN_PROMPT} {user_question}{AI_PROMPT}"
    )

    # Print the response from Claude
    print("Claude's response:", completion.completion)

# Run the async function
asyncio.run(ask_claude())

