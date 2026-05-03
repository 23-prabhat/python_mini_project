# Project: Git Conflict Resolver (Groq-Powered)

This project is a CLI tool designed to resolve Git merge conflicts with the assistance of Groq AI.

## Core Mandates
- **AI Provider:** This project MUST ONLY use Groq API. All Google Gemini or other provider integrations should be removed.
- **UI Framework:** Use the `rich` library for all console output, including banners, panels, syntax highlighting, and progress bars.
- **Project Structure:**
    - `main.py`: Entry point and CLI argument parsing.
    - `parser.py`: Logic for detecting and extracting git conflict markers.
    - `resolver.py`: Interactive resolution logic and file reconstruction.
    - `ai_helper.py`: Groq API integration and response handling.
    - `utils.py`: Rich-based UI helper functions and styling.

## Implementation Guidelines
- Ensure `ai_helper.py` only uses `groq`.
- **On-Demand AI:** AI analysis MUST NOT trigger automatically. It should only run when the user explicitly selects the option to ask Groq for help during interactive resolution.
- Securely handle the Groq API key via environment variables (`GROQ_API_KEY`) or fallback to `getpass` only when AI is requested.
- Use syntax highlighting in `rich` panels to display conflict blocks.
- Maintain a consistent color theme (e.g., green for HEAD, red for INCOMING).
- Support both single file path arguments and an `--all` flag for repo-wide resolution.

## UI & CLI Interface Specifications

The interface must provide a high-signal, visual experience using the `rich` library.

### Visual Elements
- **Main Banner:** A centered green banner displayed at startup.
- **Rules & Dividers:** 
    - Use `console.rule` for file transitions (Yellow).
    - Use `console.rule` for individual conflict markers (White).
- **Code Panels:** 
    - Titled panels with syntax highlighting (Monokai theme).
    - `HEAD` blocks: Green border.
    - `INCOMING` blocks: Red border.
    - `PREVIEW` blocks: Success (Green) or Combined (Blue) border.
- **AI Analysis:** 
    - Displayed in a `Panel` with a Magenta border.
    - Content rendered as `Markdown` for proper formatting of code blocks and lists.
    - Use a `console.status` spinner ("Asking Groq AI...") during API calls.
- **Tables:** 
    - Use `Table` for the final resolution summary.
    - Headers should be Bold Magenta.

### Interactive Flow
1. **Selection:** Users choose between Keeping HEAD, Keeping Incoming, Combining, Skipping, or requesting AI help.
2. **Preview:** Always show a preview of the resolved block before confirming.
3. **Confirmation:** Require explicit 'y/n' for writing changes to disk (unless `--auto` is used).
4. **Post-Action:** Display a Cyan "Next Steps" panel suggesting `git add` and `git commit` commands.
