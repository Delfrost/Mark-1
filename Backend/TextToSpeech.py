import edge_tts
import asyncio
from rich import print
from rich.console import Console

console = Console()

async def _speak_async(text):
    """
    Internal async function to speak text using edge-tts.
    """
    try:
        communicate = edge_tts.Communicate(text, voice="en-US-GuyNeural")
        await communicate.save("Data/output.mp3")
        console.print(f"[cyan]Speaking: {text}[/cyan]")
        return "Done!"
    except Exception as e:
        console.print(f"[yellow]Error in text-to-speech: {str(e)}[/yellow]")
        return f"Failed to speak: {str(e)}"

def speak_text(text):
    """
    Speak the given text using edge-tts.
    Returns a success message or error details.
    """
    if not text:
        return "No text provided."
    return asyncio.run(_speak_async(text))