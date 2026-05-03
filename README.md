# Git Conflict Resolver CLI

A powerful, interactive Python CLI tool to help developers understand and resolve Git merge conflicts directly from the terminal with beautiful output and smart UX.

## Features

- **Visual Conflict Markers**: Highlights HEAD and Incoming changes in colored panels.
- **Interactive Resolution**: Choose between keeping HEAD, Incoming, or combining both.
- **Syntax Highlighting**: Automatically detects language from file extension for better readability.
- **Summary Reports**: Shows a table of all resolved conflicts before saving.
- **Dry Run Support**: Use `--output <path>` to save resolved files without overwriting the original.
- **Auto Mode**: Quickly resolve all conflicts by keeping current changes with `--auto`.

## Installation

1. Ensure you have Python 3.8+ installed.
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage
Resolve conflicts in a specific file:
```bash
python main.py path/to/conflicted_file.py
```

### Auto Resolve
Automatically keep all current (HEAD) changes:
```bash
python main.py path/to/conflicted_file.py --auto
```

### Save to Different File
Save the resolved content to a new path instead of overwriting:
```bash
python main.py path/to/conflicted_file.py --output resolved_file.py
```

### AI Analysis
Use Gemini or Groq AI to get smart resolution suggestions:
1. Set your API key (optional):
   - Gemini: `$env:GEMINI_API_KEY="your-key-here"`
   - Groq: `$env:GROQ_API_KEY="your-key-here"`
2. Run with the AI flag:
   ```bash
   python main.py path/to/conflicted_file.py --ai
   ```
   If no key is set, the tool will prompt you to choose a provider and enter the key.

## Testing

You can test the tool immediately using the provided `test_conflict.py` file, which contains 3 realistic Python merge conflicts:

```bash
python main.py test_conflict.py
```

## Project Structure

- `main.py`: CLI entry point, argument parsing, and process orchestration.
- `parser.py`: Logic for detecting and extracting Git conflict markers.
- `resolver.py`: Interactive resolution prompts and file reconstruction logic.
- `utils.py`: UI helpers, syntax highlighting, and rich formatting.
- `test_conflict.py`: A sample file with 3 real Git conflicts for testing.
- `requirements.txt`: List of external dependencies (`rich`, `colorama`).

## Error Handling

The tool gracefully handles:
- Missing files
- Files without conflict markers
- Malformed conflict markers (skips them with a warning)
- User interruptions (Ctrl+C) without saving partial changes
