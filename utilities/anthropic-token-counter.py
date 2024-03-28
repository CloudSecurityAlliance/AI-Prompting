#!/usr/bin/env python3

# This is a token counter

import sys
from anthropic import Anthropic

def read_input():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        with open(filename, 'r') as file:
            return filename, file.read()
    else:
        return None, input("Please paste your text here:\n")

def sync_tokens(filename: str, text: str) -> None:
    client = Anthropic()
    tokens = client.count_tokens(text)
    if filename:
        print(f"{filename}:{tokens}")
    else:
        print(f"{tokens}")

filename, text = read_input()
sync_tokens(filename, text)
