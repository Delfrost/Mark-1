import webbrowser
import urllib.parse
from rich import print
from rich.console import Console

console = Console()

def perform_youtube_search(query):
    try:
        if query:
            encoded_query = urllib.parse.quote(query)
            url = f"https://www.youtube.com/results?search_query={encoded_query}"
            console.print(f"[cyan]Opening YouTube with search: {query}[/cyan]")
        else:
            url = "https://www.youtube.com"
            console.print("[cyan]Opening YouTube homepage[/cyan]")
        webbrowser.open(url)
        return "Done!"
    except Exception as e:
        console.print(f"[yellow]Error opening YouTube: {str(e)}[/yellow]")
        return f"Failed to open YouTube: {str(e)}"

def perform_google_search(query):
    try:
        if query:
            encoded_query = urllib.parse.quote(query)
            url = f"https://www.google.com/search?q={encoded_query}"
            console.print(f"[cyan]Opening Google with search: {query}[/cyan]")
        else:
            url = "https://www.google.com"
            console.print("[cyan]Opening Google homepage[/cyan]")
        webbrowser.open(url)
        return "Done!"
    except Exception as e:
        console.print(f"[yellow]Error opening Google: {str(e)}[/yellow]")
        return f"Failed to open Google: {str(e)}"