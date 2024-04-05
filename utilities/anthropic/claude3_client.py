#!/usr/bin/env python3

# TODO: add support for detecting and reporting:
#
# model='claude-3-opus-20240229'
# role='assistant'
# stop_reason='end_turn'
# stop_sequence=None
# type='message'
# usage=Usage(input_tokens=10, output_tokens=18))
#

import argparse
import anthropic
import os

class ClaudeClient:
    def __init__(self, api_key, prompt_file, additional_data_file, output_file, model, temperature, max_tokens):
        self.api_key = api_key
        self.prompt_file = prompt_file
        self.additional_data_file = additional_data_file
        self.output_file = output_file
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.client = anthropic.Anthropic(api_key=self.api_key)

    def run(self):
        try:
            with open(self.prompt_file, "r") as file:
                prompt = file.read().strip()

            with open(self.additional_data_file, "r") as file:
                additional_data = file.read().strip()

            response = self.client.messages.create(
                messages=[
                    {"role": "user", "content": f"{prompt}\n\nAdditional Data: {additional_data}"}
                ],
                max_tokens=self.max_tokens,
                model=self.model,
                temperature=self.temperature,
            )

            with open(self.output_file, "w") as file:
                file.write(response.content[0].text)

            print(f"Claude's answer has been written to {self.output_file}")

        except Exception as e:
            if hasattr(e, "status_code"):
                status_code = e.status_code
                if status_code == 400:
                    print("Invalid request error: There was an issue with the format or content of your request.")
                elif status_code == 401:
                    print("Authentication error: There's an issue with your API key.")
                elif status_code == 403:
                    print("Permission error: Your API key does not have permission to use the specified resource.")
                elif status_code == 404:
                    print("Not found error: The requested resource was not found.")
                elif status_code == 429:
                    print("Rate limit error: Your account has hit a rate limit.")
                elif status_code >= 500:
                    print("Server error: An unexpected error occurred on Anthropic's side.")
                else:
                    print(f"An error occurred: {str(e)}")
            else:
                print(f"An error occurred: {str(e)}")

def validate_max_tokens(value):
    value = int(value)
    if value < 1 or value > 4096:
        raise argparse.ArgumentTypeError("Max tokens must be between 1 and 4096")
    return value

def validate_model(value):
    valid_models = ["opus", "sonnet", "haiku"]
    if value not in valid_models:
        raise argparse.ArgumentTypeError(f"Invalid model. Choose from: {', '.join(valid_models)}")
    return value

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Claude API Client")
    parser.add_argument("--prompt", required=True, help="The file containing the prompt to send to Claude")
    parser.add_argument("--data", required=True, help="The file containing additional data to include with the prompt")
    parser.add_argument("--output", required=True, help="The file to write Claude's answer to")
    parser.add_argument("--model", type=validate_model, default="opus", help="The model to use (default: opus, options: opus, sonnet, haiku)")
    parser.add_argument("--temperature", type=float, default=1.0, help="The temperature for sampling (default: 1.0)")
    parser.add_argument("--max-tokens", type=validate_max_tokens, default=1000, help="Max tokens in the generated response (default: 1000, range: 1-4096)")

    args = parser.parse_args()

    model_mapping = {
        "opus": "claude-3-opus-20240229",
        "sonnet": "claude-3-sonnet-20240229",
        "haiku": "claude-3-haiku-20240307"
    }

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Please set the ANTHROPIC_API_KEY environment variable.")
        exit(1)

    client = ClaudeClient(api_key, args.prompt, args.data, args.output, model_mapping[args.model], args.temperature, args.max_tokens)
    client.run()
