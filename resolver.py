import sys
import os
from parser import Conflict
from utils import (
    console, display_conflict_header, display_code_panel, 
    print_info, print_error, print_success, display_summary_table
)
from ai_helper import analyze_conflict_with_ai, display_ai_analysis

def resolve_conflict_interactive(conflict: Conflict, current: int, total: int, filename: str, ai_enabled: bool = False):
    """Interactively resolve a single conflict."""
    display_conflict_header(current, total, conflict.start_line, conflict.end_line)
    
    display_code_panel(conflict.head_content, "HEAD (current)", "head", filename)
    display_code_panel(conflict.incoming_content, f"INCOMING ({conflict.branch_name})", "incoming", filename)
    
    # Removed automatic AI analysis from here
    
    while True:
        console.print("\nChoose resolution:")
        console.print("  [1] Keep current (HEAD)")
        console.print("  [2] Keep incoming (theirs)")
        console.print("  [3] Combine both (current first)")
        console.print("  [4] Skip this conflict")
        console.print("  [5] Ask Groq AI for analysis & suggestion")
        
        choice = input("\n> Your choice: ").strip()
        
        resolved_content = ""
        choice_label = ""
        
        if choice == '1':
            resolved_content = conflict.head_content
            choice_label = "Keep current"
        elif choice == '2':
            resolved_content = conflict.incoming_content
            choice_label = "Keep incoming"
        elif choice == '3':
            resolved_content = conflict.head_content + conflict.incoming_content
            choice_label = "Combine both"
        elif choice == '4':
            # Skip: Keep original markers
            resolved_content = (
                f"<<<<<<< HEAD\n"
                f"{conflict.head_content}"
                f"=======\n"
                f"{conflict.incoming_content}"
                f">>>>>>> {conflict.branch_name}\n"
            )
            choice_label = "Skipped"
        elif choice == '5':
            # On-demand AI analysis: Check for key BEFORE starting the spinner
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
        else:
            print_error("Invalid choice. Please pick 1-5.")
            continue
            
        # Preview
        if choice != '4':
            console.print("\n[bold]Preview:[/bold]")
            display_code_panel(resolved_content, "Resolved Block", "combined", filename)
        
        confirm = input("\nApply this resolution? (y/n/back): ").lower().strip()
        if confirm == 'y':
            return resolved_content, choice_label
        elif confirm == 'back':
            continue
        else:
            continue

def apply_resolutions(file_path: str, conflicts: list, resolutions: list) -> str:
    """Reconstructs the file with resolved content."""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    new_content = []
    last_idx = 0
    
    for i, conflict in enumerate(conflicts):
        # Lines before the conflict
        # Conflict start_line is 1-based index of <<<<<<< HEAD
        # So it's index start_line - 1 in lines list
        new_content.extend(lines[last_idx : conflict.start_line - 1])
        
        # Add the resolved content
        new_content.append(resolutions[i]['content'])
        
        # Move last_idx to after the conflict (end_line is 1-based index of >>>>>>> branch)
        last_idx = conflict.end_line
        
    # Lines after the last conflict
    new_content.extend(lines[last_idx:])
    
    return "".join(new_content)

def save_file(content: str, output_path: str):
    """Writes the resolved content to the specified path."""
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print_error(f"Failed to save file: {str(e)}")
        return False
