# Agent's Guide to git-conflict-resolver

This document provides a technical map of the `git-conflict-resolver` project for future AI agents or developers.

## 1. Project Objective
A Python-based CLI tool designed to parse, visualize, and interactively resolve standard Git merge conflicts (`<<<<<<<`, `=======`, `>>>>>>>`). It features beautiful terminal rendering via `rich` and AI-assisted resolution via Gemini or Groq.

## 2. File Architecture

| File | Responsibility | Key Symbols / Logic |
| :--- | :--- | :--- |
| `main.py` | Entry point & Orchestration | `argparse` setup, scanning loop, final file write. |
| `parser.py` | Extraction Logic | `Conflict` dataclass, `parse_conflicts()` (regex-free line scanning). |
| `resolver.py` | User Interaction | `resolve_conflict_interactive()`, `apply_resolutions()` (file reconstruction). |
| `ai_helper.py` | LLM Integration | `analyze_conflict_with_ai()`, support for Gemini (Google) and Groq. |
| `utils.py` | UI/UX Rendering | `rich` console panels, syntax highlighting, summary tables. |
| `test_conflict.py` | Verification | Mock file containing 3 intentional merge conflicts. |
| `requirements.txt` | Dependencies | `rich`, `colorama`, `google-generativeai`, `groq`. |

## 3. Core Workflows

### Conflict Parsing (`parser.py`)
The tool does **not** use complex regex. Instead, it iterates through file lines looking for `<<<<<<< HEAD`. Once found, it captures the "Head" block until `=======`, and the "Incoming" block until `>>>>>>>`. It extracts the branch name from the end marker.

### Interactive Resolution (`resolver.py`)
For each conflict, the user is presented with 5 options:
1. **HEAD**: Discards incoming changes.
2. **Incoming**: Discards local changes.
3. **Combine**: Concatenates both (HEAD first).
4. **Skip**: Leaves markers untouched in the file.
5. **AI Help**: Invokes `ai_helper.py` to get a suggested merge.

### AI Multi-Provider Logic (`ai_helper.py`)
The tool supports a dual-provider system:
- **Groq**: Uses `llama-3.3-70b-versatile`. Triggered by `GROQ_API_KEY`.
- **Gemini**: Uses `gemini-1.5-flash`. Triggered by `GEMINI_API_KEY`.
- **Session Keys**: If keys are missing from the environment, the tool prompts the user at runtime and stores them in `_SESSION_KEYS` (memory-only) for the duration of the process.

### File Reconstruction
Instead of editing the file in-place line-by-line (which is risky), `resolver.py` reconstructs the *entire* file content in memory by joining non-conflicted blocks with the user's chosen resolutions, then performs a single atomic write at the end.

## 4. Technical Constraints
- **Python Version**: 3.8+
- **Encoding**: UTF-8 enforced for file I/O.
- **Marker Format**: Strictly adheres to Git's default conflict marker style.

## 5. Maintenance Notes
- When adding new AI providers, update `_SESSION_KEYS` and the `analyze_conflict_with_ai` switch.
- Syntax highlighting in `utils.py` is dynamic; it guesses the lexer based on the file extension of the target file.
