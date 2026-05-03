# Git Conflict Resolver CLI

A powerful, interactive Python CLI tool to help developers understand and resolve Git merge conflicts directly from the terminal with beautiful output and smart UX.

## Features

- **Visual Conflict Markers**: Highlights HEAD and Incoming changes in colored panels.
- **Interactive Resolution**: Choose between keeping HEAD, Incoming, or combining both.
- **Syntax Highlighting**: Automatically detects language from file extension for better readability.
- **Summary Reports**: Shows a table of all resolved conflicts before saving.
- **Batch Processing**: Automatically detect and resolve all conflicts in a repo with `--all`.
- **AI Integration**: Get smart resolution suggestions using Gemini or Groq.

---

## Installation — Use gcr from Anywhere

To use the tool globally from any folder or project without copying files, use one of the following installation methods. Once installed, the command `gcr` will be available in your terminal.

### Method 1: Windows (Automated)
1. Open a terminal in the `git-conflict-resolver/` folder.
2. Run the setup script:
   ```powershell
   .\setup.bat
   ```
3. **Restart your terminal** to apply the PATH changes.
4. You can now run `gcr` from any project folder.

### Method 2: Mac / Linux (Automated)
1. Open a terminal in the `git-conflict-resolver/` folder.
2. Run the setup script:
   ```bash
   bash setup.sh
   ```
3. The script will create a symlink in `/usr/local/bin/gcr`.
4. You can now run `gcr` from any project folder.

### Method 3: Pip (Cross-platform)
This method is recommended for developers who want to manage the tool as a Python package.
1. Navigate to the `git-conflict-resolver/` folder.
2. Install in editable mode:
   ```bash
   pip install -e .
   ```
3. You can now run `gcr` from any project folder.

---

## Usage

### Resolve All Conflicts in a Repo
Detect and resolve every conflicted file in your current Git repository automatically:
```bash
gcr --all
```

### Resolve a Specific File
```bash
gcr path/to/conflicted_file.py
```

### Auto Resolve
Automatically keep all current (HEAD) changes for a file:
```bash
gcr path/to/conflicted_file.py --auto
```

### AI Analysis
Use Gemini or Groq AI to get smart resolution suggestions:
1. Set your API key (optional):
   - Gemini: `$env:GEMINI_API_KEY="your-key-here"`
   - Groq: `$env:GROQ_API_KEY="your-key-here"`
2. Run with the AI flag:
   ```bash
   gcr --ai path/to/conflicted_file.py
   ```
   If no key is set, the tool will prompt you to choose a provider and enter the key.

---

## Testing

You can test the tool immediately using the provided `test_conflict.py` file, which contains 3 realistic Python merge conflicts:

```bash
gcr test_conflict.py
```

## Project Structure

- `main.py`: CLI entry point, argument parsing, and process orchestration.
- `parser.py`: Logic for detecting and extracting Git conflict markers.
- `resolver.py`: Interactive resolution prompts and file reconstruction logic.
- `ai_helper.py`: LLM integration for Gemini and Groq.
- `utils.py`: UI helpers, syntax highlighting, and rich formatting.
- `setup.bat / setup.sh / setup.py`: Installation scripts for global access.
- `test_conflict.py`: A sample file with 3 real Git conflicts for testing.
- `requirements.txt`: List of external dependencies.

## Error Handling

The tool gracefully handles:
- Missing files
- Files without conflict markers
- Malformed conflict markers (skips them with a warning)
- User interruptions (Ctrl+C) without saving partial changes
