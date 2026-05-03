import argparse
import sys
import os
from utils import (
    print_banner, print_error, print_info, print_warning,
    console, display_summary_table, display_git_suggestions, display_code_panel
)
from parser import parse_conflicts, validate_file_has_conflicts
from resolver import resolve_conflict_interactive, apply_resolutions, save_file, print_success

def main():
    parser = argparse.ArgumentParser(description="Git Conflict Resolver CLI")
    parser.add_argument("file_path", help="Path to the conflicted file")
    parser.add_argument("--ai", action="store_true", help="Future AI analysis hook")
    parser.add_argument("--auto", action="store_true", help="Auto-select 'keep current' for all conflicts")
    parser.add_argument("--output", help="Save resolved content to a new file path")
    
    args = parser.parse_args()
    
    try:
        print_banner()
        
        if not os.path.exists(args.file_path):
            print_error(f"File '{args.file_path}' not found.")
            sys.exit(1)
            
        print_info(f"Scanning: {args.file_path}")
        
        conflicts = parse_conflicts(args.file_path)
        
        if not conflicts:
            print_info(f"No merge conflicts found in '{args.file_path}'. File looks clean!")
            sys.exit(0)
            
        print_info(f"Found {len(conflicts)} conflict(s)")
        
        resolutions = []
        
        for i, conflict in enumerate(conflicts, 1):
            if args.auto:
                content = conflict.head_content
                label = "Keep current (Auto)"
            else:
                content, label = resolve_conflict_interactive(conflict, i, len(conflicts), args.file_path, ai_enabled=args.ai)
            
            resolutions.append({
                'content': content,
                'choice_label': label,
                'start': conflict.start_line,
                'end': conflict.end_line
            })
            print_success(f"Conflict #{i} resolved.")

        # Summary Table
        display_summary_table(resolutions)
        
        # Apply resolutions to full content
        final_content = apply_resolutions(args.file_path, conflicts, resolutions)
        
        # Preview Final File
        console.print("\n[bold]Final Merged File Preview:[/bold]")
        display_code_panel(final_content, "Full Merged Preview", "success", args.file_path)
        
        # Save Confirmation
        output_path = args.output if args.output else args.file_path
        
        if not args.auto:
            confirm = input(f"\nWrite changes to file? (y/n): ").lower().strip()
            if confirm != 'y':
                print_info("Aborted. No changes were made.")
                sys.exit(0)
        
        if save_file(final_content, output_path):
            print_success(f"File saved: {output_path}")
            display_git_suggestions(output_path)
        
    except KeyboardInterrupt:
        print_error("\nAborted. No changes were made.")
        sys.exit(1)
    except Exception as e:
        print_error(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
