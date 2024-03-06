#!/usr/bin/env python3

import asyncio
import os
import sys
import httpx
import time
from anthropic import AsyncAnthropic, HUMAN_PROMPT, AI_PROMPT

def file_exists(filepath):
    return os.path.exists(filepath) and os.path.isfile(filepath)

class ClaudeClient:
    def __init__(self, api_key, question_file_path=None, additional_file_path=None, output_file_path=None):
        if not api_key:
            raise ValueError("API key not found. Please set the ANTHROPIC_API_KEY environment variable.")
        
        self.question_file_path = question_file_path
        self.additional_file_path = additional_file_path
        self.output_file_path = output_file_path
        
        if question_file_path and not file_exists(question_file_path):
            raise FileNotFoundError(f"Question file not found: {question_file_path}")
        if additional_file_path and not file_exists(additional_file_path):
            raise FileNotFoundError(f"Additional text file not found: {additional_file_path}")
        output_dir = os.path.dirname(output_file_path)
        if output_dir and not os.path.exists(output_dir):
            raise FileNotFoundError(f"Output directory does not exist: {output_dir}")
        
        self.anthropic = AsyncAnthropic(api_key=api_key)

    async def ask_claude(self):
        start_time = time.time()
        with open(self.question_file_path, 'r') as file:
            user_question = file.read().strip()

        with open(self.additional_file_path, 'r') as file:
            additional_text = file.read().strip()

        combined_prompt = f"{user_question}\n\n{additional_text}"
        prompt_tokens = self.count_tokens(combined_prompt)  # Count tokens in the prompt

        try:
            completion = await self.anthropic.completions.create(
                model="claude-2.1",
                max_tokens_to_sample=3000,
                prompt=f"{HUMAN_PROMPT} {combined_prompt}{AI_PROMPT}"
            )
            answer_tokens = self.count_tokens(completion.completion)  # Count tokens in the response
            end_time = time.time()
            time_taken = end_time - start_time
            self.write_output("SUCCESS", completion.completion, time_taken, prompt_tokens, answer_tokens)
        except httpx.HTTPStatusError as e:
            end_time = time.time()
            time_taken = end_time - start_time
            error_message = self.handle_http_error(e)
            self.write_output("ERROR", error_message, time_taken, prompt_tokens=0, answer_tokens=0)
        except Exception as e:
            end_time = time.time()
            time_taken = end_time - start_time
            self.write_output("ERROR", f"An unexpected error occurred: {e}", time_taken, prompt_tokens=0, answer_tokens=0)

    def count_tokens(self, text):
        # Placeholder method for token counting
        # Replace this with an actual call to count tokens using the anthropic API
        return len(text.split())  # Simplified token counting for demonstration

    def write_output(self, status, message, time_taken, prompt_tokens, answer_tokens):
        with open(self.output_file_path, 'w') as file:
            file.write(f"Status: {status}\nMessage: {message}\n")
            file.write("=" * 80 + "\nMETADATA:\n")
            file.write(f"prompt_tokens: {prompt_tokens}\nanswer_tokens: {answer_tokens}\n")
            file.write(f"time_taken: {time_taken:.2f} seconds\n")

    def handle_http_error(self, error):
        status_code_to_message = {
            400: "Error: There was an issue with the format or content of your request.",
            401: "Error: There's an issue with your API key.",
            403: "Error: Your API key does not have permission to use the specified resource.",
            404: "Error: The requested resource was not found.",
            429: "Error: Your account has hit a rate limit.",
            500: "Error: An unexpected error has occurred internal to Anthropic's systems.",
            529: "Error: Anthropic's API is temporarily overloaded."
        }
        return status_code_to_message.get(error.response.status_code, f"An unexpected HTTP error occurred: HTTP {error.response.status_code}")

if __name__ == "__main__":
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if len(sys.argv) != 4:
        print("Usage: script.py <question_file_path> <additional_file_path> <output_file_path>")
        sys.exit(1)

    question_file_path, additional_file_path, output_file_path = sys.argv[1], sys.argv[2], sys.argv[3]
    
    try:
        client = ClaudeClient(api_key=api_key, question_file_path=question_file_path, additional_file_path=additional_file_path, output_file_path=output_file_path)
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)

    async def main():
        await client.ask_claude()

    asyncio.run(main())
