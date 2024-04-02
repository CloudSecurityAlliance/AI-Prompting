# AI-Prompting

This is broken into directories for various projects using AI prompting. Some of the directories may include scripts, please ensuire any API tokens are set using environmental variables so you don't leak them here.

Most files will be append logs so you can easily view the previous prompts and strategies used.

## Utilities

The utilities assume a system with Python3 and Bash present, so Linux or Mac OS (if you're on WIndows use WSL2/Ubuntu from the Microsoft Store like Kurt does).

## Tools

Please see https://github.com/cloudsecurityalliance/CSA-IT-Operations/tree/main/projects/CSA-AI-Project-Assistant

## Problems we want to solve

* Managing the context window, the attention span of the AI (e.g. here's a prompt, content, now give me results, especially when the results are strongly governed by some document or standard)
* Can we do "lossless" data compression, e.g. summarize text without losing key ideas, words, phrases, tags, etc?
* Can we reuse old techniques like shingling, sharding, etc to get better results (e.g. translate a documeent in overlapping chunks so the text flows better, especially if ideas flow through several pages and are interweaved)
* Can we determine the level of knowledge/exerptise an AI model has in some topic? Can it self report?
