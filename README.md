# AI Test Generator Action

A GitHub Action that automatically generates and runs parameterized unit tests using an LLM based on code changes in a Pull Request.

---

## Overview

This action analyzes Python source files changed in a PR, extracts function definitions, and prompts an LLM to produce executable pytest tests.  
It then formats the generated tests, runs them, and provides coverage output for CI integration.

The goal is to reduce manual test authoring and integrate AI-driven test generation directly into existing CI/CD pipelines.

---

## Features

- Generates parameterized pytest tests for modified code.
- Runs automatically on every Pull Request.
- Formats generated tests with `black` and lints with `ruff`.
- Produces `coverage.xml` for downstream reporting.
- Falls back to a deterministic stub plan if no API key or model call fails.
- Requires no manual setup beyond one secret and a workflow file.

---

## Requirements

- GitHub repository with a Python project.
- OpenAI API key (added as a GitHub Actions secret).
- Python 3.11 or higher in the workflow environment.

---

## Setup

### 1. Add your API key

In your repository:

1. Go to **Settings → Secrets and variables → Actions → New repository secret**
2. Add a secret named `LLM_API_KEY`
3. Paste your OpenAI API key as the value

### 2. Create a workflow file

Create `.github/workflows/ai-testgen.yml` in your repository:

```yaml
name: AI Test Generator
on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  ai-tests:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: AI test generation
        uses: your-username/ai-testgen-action@v1
        env:
          LLM_API_KEY: ${{ secrets.LLM_API_KEY }}
        with:
          llm-model: gpt-4o-mini
          test-framework: pytest
