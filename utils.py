from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
from rich.theme import Theme
from rich.align import Align
from rich.box import ROUNDED, HEAVY, DOUBLE_EDGE, HEAVY_EDGE
import sys
import platform

# Define a custom theme for the application
custom_theme = Theme({
    "info": "bold cyan",
    "warning": "bold yellow",
    "error": "bold red",
    "success": "bold green",
    "head": "bold green",
    "incoming": "bold red",
    "combined": "bold blue",
    "dim": "bright_black",
    "highlight": "bold magenta",
})

if platform.system() == "Windows":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "strict")
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.buffer, "strict")
    console = Console(theme=custom_theme, legacy_windows=False)
else:
    console = Console(theme=custom_theme)

def print_banner():
    """Prints a futuristic terminal-style banner for the tool."""
    # Neon Green ASCII Art for "G C R" (Git Conflict Resolver)
    # Designed with a segmented/blocky aesthetic
    ascii_art = """
    [bold #39FF14]
     ________  ________  ________      
    |  ______|/  _____/ |  __   \\     
    | |  ____|  |      | |__|  |     
    | | |_  ||  |      |  _  _/      
    | |___| ||  |_____ | | \\ \\       
    |_______|\\_______/ |_|  \\_\\      
    [/bold #39FF14]
    """
    
    subtitle = Text("Development — Productivity — Innovation", style="#39FF14")
    
    # Render the elements with center alignment
    console.print("\n")
    console.print(Align.center(ascii_art))
    console.print(Align.center(subtitle))
    console.print(Align.center(Text("—" * 50, style="dim #39FF14")))
    console.print("\n")

def print_error(message: str):
    """Prints an error message in bold red."""
    console.print(f"[error]✘ Error:[/error] {message}")

def print_warning(message: str):
    """Prints a warning message in yellow."""
    console.print(f"[warning]⚠ Warning:[/warning] {message}")

def print_info(message: str):
    """Prints an info message in cyan."""
    console.print(f"[info]ℹ[/info] {message}")

def print_success(message: str):
    """Prints a success message in bold green."""
    console.print(f"[success]✔[/success] {message}")

def display_conflict_header(current: int, total: int, start_line: int, end_line: int):
    """Displays a header for a specific conflict."""
    console.print("\n")
    console.rule(f"[bold white]Conflict [highlight]#{current}[/highlight] of [highlight]{total}[/highlight] [/bold white]", style="dim")
    console.print(Align.center(f"[dim]Lines {start_line} to {end_line}[/dim]"))
    console.print()

def display_code_panel(code: str, title: str, style: str, filename: str):
    """Displays code in a syntax-highlighted panel."""
    lexer = Syntax.guess_lexer(filename)
    syntax = Syntax(code, lexer, theme="monokai", line_numbers=True, background_color="default")
    panel = Panel(
        syntax,
        title=f"[bold]{title}[/bold]",
        border_style=style,
        padding=(0, 1),
        box=HEAVY_EDGE
    )
    console.print(panel)

def display_summary_table(resolutions: list):
    """Displays a summary table of all resolutions."""
    console.print("\n[bold highlight]Resolution Summary[/bold highlight]")
    table = Table(show_header=True, header_style="bold magenta", box=DOUBLE_EDGE)
    table.add_column("#", style="dim", width=4, justify="center")
    table.add_column("Choice", min_width=20)
    table.add_column("Lines", justify="right")

    for i, res in enumerate(resolutions, 1):
        style = "success" if res['choice_label'] != "Skipped" else "warning"
        table.add_row(
            str(i),
            f"[{style}]{res['choice_label']}[/{style}]",
            f"[dim]{res['start']}–{res['end']}[/dim]"
        )
    console.print(table)

def display_git_suggestions(file_path: str = None):
    """Displays suggested Git commands after resolution."""
    suggestion_text = Text()
    if file_path:
        suggestion_text.append("\nFinalized file: ", style="bold white")
        suggestion_text.append(f"{file_path}\n", style="success")
        suggestion_text.append("\nSuggested Next Steps:\n", style="bold highlight")
        suggestion_text.append(f"  ➜ git add {file_path}\n", style="info")
        suggestion_text.append(f"  ➜ git commit -m \"Resolved conflicts in {file_path}\"\n", style="info")
    else:
        suggestion_text.append("\nAll conflicts resolved! 🎉\n", style="bold success")
        suggestion_text.append("\nSuggested Next Steps:\n", style="bold highlight")
        suggestion_text.append("  ➜ git add .\n", style="info")
        suggestion_text.append("  ➜ git commit -m \"Merge branch '...' into ...\"\n", style="info")
        
    panel = Panel(suggestion_text, title="Next Steps", border_style="highlight", box=HEAVY, padding=(1, 2))
    console.print(panel)

def display_file_list(files: list):
    """Displays a numbered list of conflicted files found."""
    table = Table(title="[bold yellow]Conflicted Files Found[/bold yellow]", box=HEAVY_EDGE, show_header=False)
    table.add_column("Index", style="bold cyan", width=4)
    table.add_column("File Path", style="white")
    
    for i, f in enumerate(files, 1):
        table.add_row(str(i), f)
    
    console.print(table)

def display_file_progress(current: int, total: int, filename: str):
    """Displays a rich progress header for the current file being processed."""
    console.print("\n")
    title = Text.assemble(
        (" Processing File ", "bold white"),
        (f"{current}/{total} ", "highlight"),
        ("➜ ", "dim"),
        (f"{filename} ", "bold yellow")
    )
    console.rule(title, style="dim")

def display_all_mode_summary(total_files: int, total_conflicts: int, total_skipped: int):
    """Displays a final summary table for the --all mode run."""
    console.print("\n[bold highlight]Batch Processing Summary[/bold highlight]")
    table = Table(show_header=True, header_style="bold magenta", box=DOUBLE_EDGE)
    table.add_column("Category", min_width=25)
    table.add_column("Count", justify="right", style="bold")

    table.add_row("Total Files Processed", f"[info]{total_files}[/info]")
    table.add_row("Conflicts Resolved", f"[success]{total_conflicts}[/success]")
    table.add_row("Files Skipped/Aborted", f"[warning]{total_skipped}[/warning]")
    
    console.print(table)
