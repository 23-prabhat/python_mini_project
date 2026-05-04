import sys
import os
from parser import Conflict
from utils import (
    console, display_conflict_header, display_code_panel, 
    print_info, print_error, print_success, display_summary_table
)
from ai_helper import analyze_conflict_with_ai, display_ai_analysis
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.table import Table
from rich.panel import Panel
from rich.box import ROUNDED

def resolve_conflict_interactive(conflict: Conflict, current: int, total: int, filename: str, ai_enabled: bool = False):
    """Interactively resolve a single conflict."""
    display_conflict_header(current, total, conflict.start_line, conflict.end_line)
    
    display_code_panel(conflict.head_content, "HEAD (current)", "head", filename)
    display_code_panel(conflict.incoming_content, f"INCOMING ({conflict.branch_name})", "incoming", filename)
    
    while True:
        menu_table = Table(show_header=False, box=None, padding=(0, 2))
        menu_table.add_row("[bold cyan]1.[/bold cyan] Keep [head]HEAD[/head] (current)")
        menu_table.add_row("[bold cyan]2.[/bold cyan] Keep [incoming]INCOMING[/incoming] (theirs)")
        menu_table.add_row("[bold cyan]3.[/bold cyan] [combined]Combine[/combined] both (current first)")
        menu_table.add_row("[bold cyan]4.[/bold cyan] [warning]Skip[/warning] this conflict")
        menu_table.add_row("[bold cyan]5.[/bold cyan] Ask [highlight]Groq AI[/highlight] for analysis")
        
        console.print("\n[bold]Select an action:[/bold]")
        console.print(Panel(menu_table, border_style="dim", box=ROUNDED))
        
        choice = IntPrompt.ask("\n> Option", choices=["1", "2", "3", "4", "5"], default=1)
        
        resolved_content = ""
        choice_label = ""
        
        if choice == 1:
            resolved_content = conflict.head_content
            choice_label = "Keep HEAD"
        elif choice == 2:
            resolved_content = conflict.incoming_content
            choice_label = "Keep INCOMING"
        elif choice == 3:
            resolved_content = conflict.head_content + conflict.incoming_content
            choice_label = "Combined Both"
        elif choice == 4:
            resolved_content = (
                f"<<<<<<< HEAD\n"
                f"{conflict.head_content}"
                f"=======\n"
                f"{conflict.incoming_content}"
                f">>>>>>> {conflict.branch_name}\n"
            )
            choice_label = "Skipped"
        elif choice == 5:
            from ai_helper import get_groq_key
            if not get_groq_key():
                continue

            with console.status("[bold magenta]Asking Groq AI for insights..."):
                analysis = analyze_conflict_with_ai(
                    conflict.head_content, 
                    conflict.incoming_content, 
                    conflict.branch_name, 
                    filename
                )
            display_ai_analysis(analysis)
            continue
            
        # Preview
        if choice != 4:
            console.print("\n[bold]Preview of Resolution:[/bold]")
            display_code_panel(resolved_content, "Preview", "combined", filename)
            
            if not Confirm.ask("Apply this resolution?", default=True):
                continue
                
        return resolved_content, choice_label

def apply_resolutions(file_path: str, conflicts: list, resolutions: list) -> str:
    """Reconstructs the file with resolved content."""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    new_content = []
    last_idx = 0
    
    for i, conflict in enumerate(conflicts):
        # Lines before the conflict
        new_content.extend(lines[last_idx : conflict.start_line - 1])
        
        # Add the resolved content
        new_content.append(resolutions[i]['content'])
        
        # Move last_idx to after the conflict
        last_idx = conflict.end_line
        
    # Lines after the last conflict
    new_content.extend(lines[last_idx:])
    
    return "".join(new_content)

def save_file(content: str, output_path: str):
    """Writes the resolved content to the specified path."""
    try:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print_error(f"Failed to save file: {str(e)}")
        return False
