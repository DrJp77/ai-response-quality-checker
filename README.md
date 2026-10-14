# AI Response Quality Checker

A lightweight, rule-based tool for auditing the structural quality of AI response datasets — built with pure Python and no paid APIs.

> **Note:** This tool evaluates **data completeness and structure**, not factual correctness. It cannot determine whether an AI's answer is true or false.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Example Report](#example-report)
- [Running Tests](#running-tests)
- [Limitations](#limitations)

---

## Overview

When working with AI response datasets — such as output from LLMs collected for evaluation, fine-tuning, or benchmarking — raw data often contains quality issues:

- **Empty or whitespace-only responses** (the model failed to answer)
- **Missing required fields** (corrupted records or schema changes)
- **Wrong data types** (e.g., a prompt stored as a number instead of text)
- **Duplicate prompts or responses** (wasted computation or biased datasets)

This tool automatically detects all of the above and generates a structured JSON report — making it easy to audit data quality before using it in ML pipelines or evaluations.

---

## Features

| Feature | Description |
|---|---|
| **Empty response detection** | Flags responses that are empty, whitespace-only, or `null` |
| **Schema validation** | Ensures every record has both `"prompt"` and `"response"` as strings |
| **Type checking** | Reports records where fields have the wrong data type (e.g., integer instead of text) |
| **Duplicate prompt detection** | Finds prompts that appear more than once (case-insensitive) |
| **Duplicate response detection** | Finds identical responses across different prompts |
| **JSON report output** | Saves a full quality report to `reports/quality_report.json` |
| **Unit tests** | 16 automated tests covering normal, edge case, and invalid inputs |
| **Zero cost** | No API keys, no internet connection, no paid services required |

---

## Project Structure

```
ai-response-quality-checker/
├── data/
│   └── sample_responses.json     # Sample dataset with realistic edge cases
├── src/
│   ├── __init__.py               # Marks src as a Python package
│   ├── metrics.py                # Individual rule-based check functions
│   └── report.py                 # Orchestrates checks and generates report
├── tests/
│   ├── __init__.py
│   ├── test_metrics.py           # Unit tests for metrics.py (8 tests)
│   └── test_report.py            # Unit tests for report.py (8 tests)
├── reports/
│   └── quality_report.json       # Auto-generated report (created on run)
├── .env.example                  # Template for environment configuration
├── .gitignore                    # Excludes .venv, cache, and .env from Git
├── pytest.ini                    # pytest configuration
├── requirements.txt              # Project dependencies
└── README.md                     # This file
```

---

## Installation

### Prerequisites

- Python 3.10 or higher
- pip

### Steps

**1. Clone the repository:**
```bash
git clone https://github.com/your-username/ai-response-quality-checker.git
cd ai-response-quality-checker
```

**2. Create and activate a virtual environment:**
```bash
# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

> If you see an execution policy error on Windows, run this once:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

---

## Usage

### Run the quality checker

```bash
python src/report.py
```

This will:
1. Load `data/sample_responses.json`
2. Run all quality checks
3. Print a summary to the terminal
4. Save the full report to `reports/quality_report.json`

### Sample terminal output

```
=== LAPORAN KUALITAS DATA AI ===
Total data: 12
Respons kosong: [2, 3]
Data tidak valid: 4
  ID 8: Field wajib 'response' tidak ditemukan.
  ID 9: Field wajib 'prompt' tidak ditemukan.
  ID 10: Tipe data 'prompt' harus teks (str), tetapi ditemukan int.
  ID 11: Tipe data 'response' harus teks (str), tetapi ditemukan NoneType.
Grup prompt duplikat: 2
Grup respons duplikat: 1
Laporan berhasil disimpan ke: D:\ai-response-quality-checker\reports\quality_report.json
```

### Use as a Python module

You can import and use the functions directly in your own scripts:

```python
import json
from src.report import generate_report, save_report

with open("data/sample_responses.json", encoding="utf-8") as f:
    data = json.load(f)

report = generate_report(data)
print(f"Total: {report['total_items']}")
print(f"Empty responses: {report['empty_responses']}")
save_report(report, "reports/my_custom_report.json")
```

---

## Example Report

The generated `reports/quality_report.json` follows this structure:

```json
{
  "total_items": 12,
  "empty_responses": [2, 3],
  "invalid_items": [
    {
      "id": 8,
      "errors": ["Field wajib 'response' tidak ditemukan."]
    },
    {
      "id": 10,
      "errors": ["Tipe data 'prompt' harus teks (str), tetapi ditemukan int."]
    }
  ],
  "duplicate_prompts": {
    "apa ibu kota negara indonesia?": [4, 5]
  },
  "duplicate_responses": {
    "ibu kota indonesia adalah nusantara (ikn)...": [4, 5]
  }
}
```

---

## Running Tests

```bash
.\.venv\Scripts\python.exe -m pytest -v
```

Expected output:

```
============================= test session starts =============================
collected 16 items

tests/test_metrics.py::test_empty_response PASSED
tests/test_metrics.py::test_required_fields PASSED
tests/test_metrics.py::test_missing_response PASSED
tests/test_metrics.py::test_missing_prompt PASSED
tests/test_metrics.py::test_invalid_types_in_fields PASSED
tests/test_metrics.py::test_non_dictionary_item PASSED
tests/test_metrics.py::test_duplicate_prompts PASSED
tests/test_metrics.py::test_duplicate_responses PASSED
tests/test_report.py::test_generate_report_invalid_input_type PASSED
tests/test_report.py::test_generate_report_empty_dataset PASSED
tests/test_report.py::test_generate_report_valid_and_invalid_data PASSED
tests/test_report.py::test_generate_report_with_non_dict_items PASSED
tests/test_report.py::test_save_report_creates_valid_json PASSED
tests/test_report.py::test_generate_report_auto_saves PASSED
tests/test_report.py::test_report_contains_all_required_keys PASSED
tests/test_report.py::test_all_invalid_items_have_id_and_errors PASSED

16 passed in 0.65s
```

---

## Limitations

> **Important:** Please read these limitations before drawing conclusions from the output.

| Limitation | Details |
|---|---|
| **No factual verification** | This tool cannot determine if an AI response is factually correct. A response like *"The sun orbits the Earth"* will pass all checks because it is a non-empty, properly typed string. |
| **No semantic evaluation** | The tool does not measure relevance, coherence, or fluency. It only checks data structure and format. |
| **No LLM scoring** | No AI model or external service is used. All checks are deterministic, rule-based functions. |
| **English/Indonesian only tested** | The duplicate detection uses basic `.lower()` normalization and does not account for Unicode-specific case rules in other languages. |
| **No scoring system yet** | The current version reports issues but does not produce a numeric quality score per item. |

---

## Tech Stack

- **Language:** Python 3.10+
- **Testing:** [pytest](https://pytest.org)
- **Dependencies:** Standard library only (no third-party packages besides pytest)

---

## Author

Built as a portfolio project to demonstrate skills in:
- AI/LLM dataset quality evaluation
- Rule-based data validation
- Python project structure and testing
- Reproducible, cost-free ML tooling
