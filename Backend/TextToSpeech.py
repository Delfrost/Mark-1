import edge_tts
import asyncio
import logging
import pyttsx3
from rich import print
from rich.console import Console

console = Console()

logging.basicConfig(
    filename="Data/delfrost_logs.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


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
    try:
        engine = pyttsx3.init()
        # Set properties (optional: adjust rate, volume, voice)
        engine.setProperty("rate", 150)  # Speed of speech
        engine.setProperty("volume", 0.9)  # Volume (0.0 to 1.0)
        console.print(f"[cyan]Speaking: {text}[/cyan]")
        
        logging.info(f"Speaking text: {text}")
        engine.say(text)
        engine.runAndWait()
        return "Speech completed."
    except Exception as e:
        console.print(f"[yellow]Text-to-speech error: {str(e)}[/yellow]")
        logging.error(f"Text-to-speech error: {str(e)}")
        return f"Text-to-speech error: {str(e)}"