#!/usr/bin/env python3

import sys
from anthropic import Anthropic

def read_input():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        with open(filename, 'r') as file:
            return file.read()
    else:
        return input("Please paste your text here:\n")

def sync_tokens(text: str) -> None:
    client = Anthropic()
    tokens = client.count_tokens(text)
    print(f"The text is {tokens} tokens")

text = read_input()
sync_tokens(text)
