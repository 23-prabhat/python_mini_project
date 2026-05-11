# GCR - Git Conflict Resolver

GCR is a command-line tool that helps developers inspect and resolve Git merge conflicts from the terminal. It detects Git conflict markers, shows both conflicting versions with readable formatting, lets the user choose a resolution, and writes the cleaned file back after confirmation.

The project is designed as a Python mini project for simplifying one of the most common Git workflow problems: manually editing files that contain `<<<<<<<`, `=======`, and `>>>>>>>` conflict markers.

## Team

1. Arihant Gadge : BT24F05F022
2. Prabhat Jha : BT24F05F026
3. Om Kayande : BT24F05F033
4. Tanmay Kolhe : Bt24F05F035

## Features

- Detects Git merge conflicts in a specific file.
- Supports resolving all conflicted files in the current Git repository using `--all`.
- Provides an interactive terminal menu for each conflict.
- Allows keeping the current version, keeping the incoming version, combining both versions, or skipping a conflict.
- Shows syntax-highlighted previews using Rich.
- Displays resolution summaries and suggested Git commands after saving.
- Supports optional Groq AI analysis for conflict explanation and merge suggestions.
- Supports an automatic mode that selects the current `HEAD` version for every conflict.

## Tech Stack

- **Python 3.8+** - Core programming language.
- **Git** - Used to detect conflicted files in repository-wide mode.
- **Rich** - Terminal UI, tables, panels, syntax highlighting, and prompts.
- **Colorama** - Cross-platform terminal color support.
- **Groq SDK** - Optional AI-powered conflict analysis.
- **Setuptools** - Packaging and `gcr` console command setup.
- **Batch/Shell scripts** - Platform-specific setup helpers for Windows, macOS, and Linux.

## Folder Structure

```text
Python_mini_project/
|-- ai_helper.py                      # Groq AI integration and AI analysis display
|-- gcr.bat                           # Windows command shim for running GCR
|-- GEMINI.md                         # Additional project documentation/notes
|-- main.py                           # CLI entry point and command handling
|-- parser.py                         # Git conflict marker parser
|-- README.md                         # Project documentation
|-- requirements.txt                  # Python dependencies
|-- resolver.py                       # Interactive conflict resolution logic
|-- setup.bat                         # Windows setup script
|-- setup.md                          # Setup guide
|-- setup.py                          # Python package configuration
|-- setup.sh                          # macOS/Linux setup script
|-- test_conflict.py                  # Sample/test conflict file
|-- utils.py                          # Rich-based terminal display utilities
|-- git_conflict_resolver.egg-info/   # Generated package metadata
`-- __pycache__/                      # Generated Python bytecode cache
```

## Installation

### 1. Clone or Open the Project

Open a terminal in the project folder:

```bash
cd Python_mini_project
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Optional: Install as a CLI Command

Install the project locally so the `gcr` command is available:

```bash
pip install -e .
```

You can also use the included setup scripts:

```bash
# Windows
setup.bat

# macOS/Linux
chmod +x setup.sh
./setup.sh
```

## How to Use

### Resolve One File

Run GCR with the path of a conflicted file:

```bash
gcr path/to/conflicted_file.py
```

If you do not install the CLI command, run it directly with Python:

```bash
python main.py path/to/conflicted_file.py
```

### Resolve All Conflicted Files

From inside a Git repository with merge conflicts:

```bash
gcr --all
```

Or:

```bash
python main.py --all
```

### Use AI Analysis

Set a Groq API key before using AI mode:

```powershell
$env:GROQ_API_KEY="your_api_key_here"
```

Then run:

```bash
gcr path/to/conflicted_file.py --ai
```

During conflict resolution, choose the AI analysis option from the interactive menu.

### Auto Mode

Automatically keep the current `HEAD` version for every conflict:

```bash
gcr path/to/conflicted_file.py --auto
```

For all conflicted files:

```bash
gcr --all --auto
```

### Save to a Different Output File

For single-file mode, save the resolved result to another file:

```bash
gcr path/to/conflicted_file.py --output resolved_file.py
```

## Typical Workflow

1. Start a merge, rebase, or pull that creates conflicts.
2. Run `gcr --all` or `gcr <file-path>`.
3. Review each conflict in the terminal.
4. Choose the correct resolution.
5. Confirm the final preview and save.
6. Stage and commit the resolved files:

```bash
git add .
git commit -m "Resolve merge conflicts"
```

## Requirements

- Python 3.8 or later
- Git installed and available in PATH
- Internet connection and Groq API key only if using AI analysis

## Notes

- GCR modifies files only after user confirmation in interactive mode.
- The `--all` option works only inside a Git repository.
- AI analysis is optional; normal conflict resolution works without an API key.
