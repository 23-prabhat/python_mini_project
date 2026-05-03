import os
import google.generativeai as genai
from groq import Groq
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from getpass import getpass

console = Console()

# In-memory storage for the API keys if prompted during session
_SESSION_KEYS = {
    "GEMINI": None,
    "GROQ": None
}

def get_provider_and_key():
    """Determines which AI provider to use and ensures an API key is available."""
    global _SESSION_KEYS
    
    # 1. Check for Groq environment variable
    groq_key = os.environ.get("GROQ_API_KEY") or _SESSION_KEYS["GROQ"]
    if groq_key:
        return "GROQ", groq_key
        
    # 2. Check for Gemini environment variable
    gemini_key = os.environ.get("GEMINI_API_KEY") or _SESSION_KEYS["GEMINI"]
    if gemini_key:
        return "GEMINI", gemini_key
        
    # 3. Prompt user to choose if neither is found
    console.print("\n[bold yellow]No AI API key found in environment.[/bold yellow]")
    console.print("Which AI provider would you like to use?")
    console.print(" [1] Gemini (Google)")
    console.print(" [2] Groq")
    
    choice = input("\nSelect provider [1/2]: ").strip()
    
    provider = "GEMINI" if choice == "1" else "GROQ" if choice == "2" else None
    if not provider:
        return None, None
        
    try:
        user_key = getpass(f"Enter {provider} API Key: ").strip()
        if user_key:
            _SESSION_KEYS[provider] = user_key
            return provider, user_key
    except EOFError:
        pass
        
    return None, None

def analyze_conflict_with_ai(head_content: str, incoming_content: str, branch_name: str, filename: str):
    """
    Uses the selected AI provider to analyze a Git conflict.
    """
    provider, api_key = get_provider_and_key()
    
    if not provider or not api_key:
        return "Error: No API provider selected or key missing. AI analysis cancelled."

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
    
    Tasks:
    1. Explain the difference between these two versions.
    2. Suggest which one is likely more correct or how they should be combined.
    3. Provide the final merged code block.
    
    Keep the explanation concise and professional.
    """

    try:
        if provider == "GEMINI":
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            return response.text
        elif provider == "GROQ":
            client = Groq(api_key=api_key)
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
            )
            return completion.choices[0].message.content
    except Exception as e:
        return f"Error during {provider} AI analysis: {str(e)}"

def display_ai_analysis(analysis: str):
    """Displays the AI analysis in a styled panel."""
    if analysis.startswith("Error:"):
        console.print(f"\n[bold red]{analysis}[/bold red]")
    else:
        md = Markdown(analysis)
        panel = Panel(md, title="AI Conflict Analysis", border_style="magenta", padding=(1, 2))
        console.print("\n")
        console.print(panel)
