import os
from groq import Groq
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from getpass import getpass

console = Console()

# In-memory storage for the API key if prompted during session
_SESSION_KEY = None

def get_groq_key():
    """Ensures a Groq API key is available."""
    global _SESSION_KEY
    
    # 1. Check for environment variable
    groq_key = os.environ.get("GROQ_API_KEY") or _SESSION_KEY
    if groq_key:
        return groq_key
        
    # 2. Prompt user if not found
    console.print("\n[bold yellow]No Groq API key found in environment.[/bold yellow]")
    try:
        user_key = getpass("Enter Groq API Key: ").strip()
        if user_key:
            _SESSION_KEY = user_key
            return user_key
    except EOFError:
        pass
        
    return None

def analyze_conflict_with_ai(head_content: str, incoming_content: str, branch_name: str, filename: str, api_key: str = None):
    """
    Uses the Groq API to analyze a Git conflict.
    """
    if not api_key:
        api_key = get_groq_key()
    
    if not api_key:
        return "Error: Groq API key missing. AI analysis cancelled."

    prompt = f"""
    Analyze this Git merge conflict in the file '{filename}'.
    
    HEAD (current) version:
    ```
    {head_content}
    ```
    
    INCOMING (from {branch_name}) version:
    ```
    {incoming_content}
    ```
    
    explain these following task like you are explaining to a donkey:
    Tasks:
    1. Explain the difference between these two versions.(keep it short and simple)
    2. Suggest which one is likely more correct or how they should be combined.
    3. Provide the final merged code block.
    
    Keep the explanation like you are explaining to a caveman.
    """

    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful git conflict resolution assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error during Groq AI analysis: {str(e)}"

def display_ai_analysis(analysis: str):
    """Displays the AI analysis in a styled panel."""
    from rich import box
    if analysis.startswith("Error:"):
        console.print(f"\n[bold red]{analysis}[/bold red]")
    else:
        md = Markdown(analysis)
        panel = Panel(
            md, 
            title="[bold magenta]Groq AI Conflict Analysis[/bold magenta]", 
            title_align="left",
            border_style="magenta", 
            padding=(1, 2),
            box=box.DOUBLE_EDGE
        )
        console.print("\n")
        console.print(panel)
