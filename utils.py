from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
from rich.theme import Theme
import sys

# Define a custom theme for the application
custom_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "bold red",
    "success": "bold green",
    "head": "green",
    "incoming": "red",
    "combined": "blue",
})

console = Console(theme=custom_theme)

def print_banner():
    """Prints a styled banner for the tool."""
    banner_text = Text("\n╔══════════════════════════════════════╗\n"
                       "║   Git Conflict Resolver v1.0.0      ║\n"
                       "╚══════════════════════════════════════╝", style="success")
    console.print(banner_text, justify="center")

def print_error(message: str):
    """Prints an error message in bold red."""
    console.print(f"[error]Error: {message}[/error]")

def print_warning(message: str):
    """Prints a warning message in yellow."""
    console.print(f"[warning]Warning: {message}[/warning]")

def print_info(message: str):
    """Prints an info message in cyan."""
    console.print(f"[info]{message}[/info]")

def display_conflict_header(current: int, total: int, start_line: int, end_line: int):
    """Displays a header for a specific conflict."""
    console.rule(f"[bold white] Conflict #{current} of {total} (Lines {start_line}–{end_line}) [/bold white]", style="white")
    print()

def display_code_panel(code: str, title: str, style: str, filename: str):
    """Displays code in a syntax-highlighted panel."""
    lexer = Syntax.guess_lexer(filename)
    syntax = Syntax(code, lexer, theme="monokai", line_numbers=False)
    panel = Panel(syntax, title=title, border_style=style, padding=(0, 1))
    console.print(panel)

def display_summary_table(resolutions: list):
    """Displays a summary table of all resolutions."""
    console.print("\n[bold]Resolution Summary[/bold]")
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("#", style="dim", width=4)
    table.add_column("Choice", min_width=20)
    table.add_column("Lines", justify="right")

    for i, res in enumerate(resolutions, 1):
        table.add_row(
            str(i),
            res['choice_label'],
            f"{res['start']}–{res['end']}"
        )
    console.print(table)

def display_git_suggestions(file_path: str = None):
    """Displays suggested Git commands after resolution."""
    if file_path:
        suggestion_text = Text.assemble(
            ("\nSuggested Git Commands:\n", "bold cyan"),
            (f"  git add {file_path}\n", "white"),
            (f"  git commit -m \"Resolved merge conflicts in {file_path}\"\n", "white"),
            ("\nAlternative (pick one side entirely):\n", "bold cyan"),
            (f"  git checkout --ours {file_path}\n", "white"),
            (f"  git checkout --theirs {file_path}\n", "white")
        )
    else:
        suggestion_text = Text.assemble(
            ("\nSuggested Git Commands:\n", "bold cyan"),
            ("  git add .\n", "white"),
            ("  git commit -m \"Resolved merge conflicts\"\n", "white")
        )
        
    panel = Panel(suggestion_text, title="Next Steps", border_style="cyan")
    console.print(panel)

def progress_indicator(current: int, total: int):
    """Prints a progress indicator."""
    console.print(f"[[bold cyan]{current}/{total}[/bold cyan]] Resolving...", end="\r")

def print_success(message: str):
    """Prints a success message in bold green."""
    console.print(f"[success]{message}[/success]")

def display_file_list(files: list):
    """Displays a numbered list of conflicted files found."""
    text = Text()
    for i, f in enumerate(files, 1):
        text.append(f" [{i}] ", style="bold cyan")
        text.append(f"{f}\n", style="white")
    
    panel = Panel(text, title="Conflicted Files Found", border_style="info", padding=(1, 2))
    console.print(panel)

def display_file_progress(current: int, total: int, filename: str):
    """Displays a rich progress header for the current file being processed."""
    console.print("\n")
    console.rule(f"[bold yellow] Resolving file {current} of {total}: [bold white]{filename} [/bold yellow]", style="yellow")
    console.print("\n")

def display_all_mode_summary(total_files: int, total_conflicts: int, total_skipped: int):
    """Displays a final summary table for the --all mode run."""
    console.print("\n[bold]Batch Processing Summary[/bold]")
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Category", min_width=20)
    table.add_column("Count", justify="right")

    table.add_row("Total Files Processed", str(total_files))
    table.add_row("Total Conflicts Resolved", str(total_conflicts))
    table.add_row("Total Files Skipped", str(total_skipped))
    
    console.print(table)
