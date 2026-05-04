import argparse
import sys
import os
import subprocess
from rich.prompt import Confirm
from utils import (
    print_banner, print_error, print_info, print_warning,
    console, display_summary_table, display_git_suggestions, 
    display_code_panel, print_success, display_file_list,
    display_file_progress, display_all_mode_summary
)
from parser import parse_conflicts, validate_file_has_conflicts
from resolver import resolve_conflict_interactive, apply_resolutions, save_file

def get_conflicted_files():
    """Uses git to find all currently conflicted files."""
    try:
        result = subprocess.run(
            ['git', 'diff', '--name-only', '--diff-filter=U'],
            capture_output=True, text=True, check=True
        )
        files = result.stdout.strip().split('\n')
        return [f for f in files if f]
    except subprocess.CalledProcessError:
        print_error("Not a git repository (or git error).")
        return None
    except FileNotFoundError:
        print_error("Git is not installed. Please install Git to use --all mode.")
        return None

def process_single_file(file_path, args, current_file_num=None, total_files=None):
    """Processes a single file and returns the number of conflicts resolved."""
    if not os.path.exists(file_path):
        print_error(f"File '{file_path}' not found.")
        return 0, False

    if current_file_num and total_files:
        display_file_progress(current_file_num, total_files, file_path)
    else:
        print_info(f"Scanning: {file_path}")
    
    conflicts = parse_conflicts(file_path)
    
    if not conflicts:
        print_info(f"No merge conflicts found in '{file_path}'. Skipping.")
        return 0, True
        
    print_info(f"Found {len(conflicts)} conflict(s)")
    
    resolutions = []
    
    for i, conflict in enumerate(conflicts, 1):
        if args.auto:
            content = conflict.head_content
            label = "Keep current (Auto)"
        else:
            content, label = resolve_conflict_interactive(conflict, i, len(conflicts), file_path, ai_enabled=args.ai)
        
        resolutions.append({
            'content': content,
            'choice_label': label,
            'start': conflict.start_line,
            'end': conflict.end_line
        })
        print_success(f"Conflict #{i} resolved.")

    # Show summary for this file
    display_summary_table(resolutions)
    
    # Apply resolutions
    final_content = apply_resolutions(file_path, conflicts, resolutions)
    
    # Preview
    console.print("\n[bold]Final Merged File Preview:[/bold]")
    display_code_panel(final_content, "Full Merged Preview", "success", file_path)
    
    # Save
    output_path = args.output if args.output and not current_file_num else file_path
    
    if not args.auto:
        if not Confirm.ask(f"\nWrite changes to [success]{output_path}[/success]?", default=True):
            print_info(f"Aborted resolution for {file_path}.")
            return 0, False
            
    if save_file(final_content, output_path):
        print_success(f"File saved: {output_path}")
        if not current_file_num:
            display_git_suggestions(output_path)
        else:
            print_success(f"[OK] File {current_file_num} of {total_files} done")
        return len(conflicts), True
        
    return 0, False

def run_all_mode(args):
    """Detects and resolves all conflicted files in the repository."""
    files = get_conflicted_files()
    
    if files is None:
        return
        
    if not files:
        print_info("No conflicted files found in the repository. Everything looks clean!")
        return

    display_file_list(files)
    
    total_files = len(files)
    resolved_files_count = 0
    total_conflicts_resolved = 0
    skipped_files_count = 0
    
    for i, file_path in enumerate(files, 1):
        conflicts_count, success = process_single_file(file_path, args, i, total_files)
        if success:
            resolved_files_count += 1
            total_conflicts_resolved += conflicts_count
            if conflicts_count == 0:
                skipped_files_count += 1
        else:
            skipped_files_count += 1

    display_all_mode_summary(total_files, total_conflicts_resolved, skipped_files_count)
    display_git_suggestions()

def main():
    parser = argparse.ArgumentParser(description="Git Conflict Resolver CLI")
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("file_path", nargs="?", help="Path to the conflicted file")
    group.add_argument("--all", action="store_true", help="Auto-detect and resolve all conflicted files in the repo")
    
    parser.add_argument("--ai", action="store_true", help="Enable AI analysis for conflicts")
    parser.add_argument("--auto", action="store_true", help="Auto-select 'keep current' for all conflicts")
    parser.add_argument("--output", help="Save resolved content to a new file path (Single file mode only)")
    
    args = parser.parse_args()
    
    try:
        print_banner()
        
        if args.all:
            run_all_mode(args)
        else:
            process_single_file(args.file_path, args)
            
    except KeyboardInterrupt:
        print_error("\nAborted. No further changes were made.")
        sys.exit(1)
    except Exception as e:
        print_error(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
