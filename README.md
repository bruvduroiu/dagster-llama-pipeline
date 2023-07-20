# Dagster ❤️ Llama 🦙

Toy example using Dagster orchestration in conjunction with [llama.cpp](https://github.com/ggerganov/llama.cpp) to achieve a performant and observable data pipeline.

This repo is the supporting material for the blog post: **TBD**

## Installation

```bash
pyenv local 3.9.x

poetry config virtualenvs.in-project true --local

poetry install
```

## To run

```bash
# Start up Llama server
poetry run python -m llama_cpp.server --model ggml-model-q4_0.bin

# Start dagit
poetry run dagit -f src/__init__.py -d .
```
