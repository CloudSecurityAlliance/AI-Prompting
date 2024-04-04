import argparse
import anthropic
import os
from anthropic.api.errors import InvalidRequestError, AuthenticationError, PermissionError, NotFoundError, RateLimitError, APIError, OverloadedError

class ClaudeClient:
    def __init__(self, api_key, prompt_file, additional_data_file, output_file, model, temperature, max_tokens_to_sample):
        self.api_key = api_key
        self.prompt_file = prompt_file
        self.additional_data_file = additional_data_file
        self.output_file = output_file
        self.model = model
        self.temperature = temperature
        self.max_tokens_to_sample = max_tokens_to_sample
        self.client = anthropic.Client(api_key=self.api_key)

    def run(self):
        try:
            with open(self.prompt_file, "r") as file:
                prompt = file.read().strip()

            with open(self.additional_data_file, "r") as file:
                additional_data = file.read().strip()

            response = self.client.completions.create(
                model=self.model,
                prompt=f"{anthropic.HUMAN_PROMPT} {prompt}\n\nAdditional Data: {additional_data} {anthropic.AI_PROMPT}",
                max_tokens_to_sample=self.max_tokens_to_sample,
                temperature=self.temperature,
            )

            answer = response.completion.strip()

            with open(self.output_file, "w") as file:
                file.write(answer)

            print(f"Claude's answer has been written to {self.output_file}")

        except InvalidRequestError as e:
            print(f"Invalid request error: {str(e)}")
        except AuthenticationError as e:
            print(f"Authentication error: {str(e)}")
        except PermissionError as e:
            print(f"Permission error: {str(e)}")
        except NotFoundError as e:
            print(f"Not found error: {str(e)}")
        except RateLimitError as e:
            print(f"Rate limit error: {str(e)}")
        except APIError as e:
            print(f"API error: {str(e)}")
        except OverloadedError as e:
            print(f"Overloaded error: {str(e)}")
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")

def validate_max_tokens(value):
    value = int(value)
    if value < 1 or value > 4096:
        raise argparse.ArgumentTypeError("Max tokens to sample must be between 1 and 4096")
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
    parser.add_argument("--max-tokens", type=validate_max_tokens, default=1000, help="Max tokens to sample (default: 1000, range: 1-4096)")

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
    
