# File-Type Validator

A security-focused Python application designed to verify file integrity by validating magic bytes (file signatures) against file extensions.

## Overview

In secure environments, malicious files often masquerade as harmless documents (e.g., a `.exe` renamed to `.pdf`). This tool prevents such "Extension Spoofing" by inspecting the binary header of a file and comparing it with a trusted JSON database of magic bytes.

### Key Features
- **Zero Dependencies:** Optimized for environments without internet access.
- **Drag & Drop Interface:** Modern UI for efficient file processing.
- **External Configuration:** Signatures are managed via an external `signatures.json` for easy maintainability.
- **Defensive Programming:** Includes startup diagnostics to ensure database integrity.

##️ Tech Stack & Concepts

- **Language:** Python 3.13
- **GUI Framework:** Tkinter & TkinterDnD2
- **Data Handling:** Binary I/O, JSON Parsing
- **Security Concepts:** Magic Bytes Analysis, Defensive Programming, Secure Workflows

## Installation & Usage

### Prerequisites
- Python 3.10 or higher
- `tkinterdnd2` library

### Setup
1. Clone the repository:
   ```bash
   git clone [https://github.com/devTobias876/File-Type-Validator.git](https://github.com/devTobias876/File-Type-Validator.git)
   cd File-Type-Validator