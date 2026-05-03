import re
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Conflict:
    start_line: int
    separator_line: int
    end_line: int
    head_content: str
    incoming_content: str
    branch_name: str

def parse_conflicts(file_path: str) -> List[Conflict]:
    """
    Parses a file for Git conflict markers and returns a list of Conflict objects.
    
    Markers:
    <<<<<<< HEAD
    [head_content]
    =======
    [incoming_content]
    >>>>>>> branch_name
    """
    conflicts = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        return []
    except Exception:
        return []

    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith('<<<<<<< HEAD'):
            start_idx = i
            sep_idx = -1
            end_idx = -1
            branch_name = "incoming"
            
            # Look for =======
            j = i + 1
            while j < len(lines):
                if lines[j].startswith('======='):
                    sep_idx = j
                    break
                j += 1
            
            if sep_idx == -1:
                # Malformed: no separator
                i += 1
                continue
                
            # Look for >>>>>>>
            k = sep_idx + 1
            while k < len(lines):
                if lines[k].startswith('>>>>>>>'):
                    end_idx = k
                    branch_name = lines[k].strip().split(' ', 1)[1] if ' ' in lines[k] else lines[k].strip()[8:]
                    break
                k += 1
            
            if end_idx == -1:
                # Malformed: no end marker
                i += 1
                continue
            
            head_content = "".join(lines[start_idx + 1 : sep_idx])
            incoming_content = "".join(lines[sep_idx + 1 : end_idx])
            
            conflicts.append(Conflict(
                start_line=start_idx + 1,
                separator_line=sep_idx + 1,
                end_line=end_idx + 1,
                head_content=head_content,
                incoming_content=incoming_content,
                branch_name=branch_name
            ))
            
            i = end_idx + 1
        else:
            i += 1
            
    return conflicts

def validate_file_has_conflicts(file_path: str) -> bool:
    """Quickly check if a file contains any conflict markers."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            return '<<<<<<< HEAD' in content and '>>>>>>>' in content
    except Exception:
        return False
