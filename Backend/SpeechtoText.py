import speech_recognition as sr
from rich.console import Console
import logging

console = Console()

logging.basicConfig(
    filename="Data/delfrost_logs.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        console.print("[cyan]Listening for your command...[/cyan]")
        logging.info("Listening for speech input")
        try:
            # Adjust for ambient noise and listen for up to 5 seconds
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            console.print("[cyan]Processing speech...[/cyan]")
            # Use Google Speech Recognition
            text = recognizer.recognize_google(audio)
            logging.info(f"Transcribed speech: {text}")
            return text
        except sr.WaitTimeoutError:
            logging.warning("Speech recognition timed out: No speech detected")
            return "No speech detected."
        except sr.UnknownValueError:
            logging.warning("Speech recognition failed: Could not understand audio")
            return "Could not understand audio."
        except sr.RequestError as e:
            logging.error(f"Speech recognition error: {str(e)}")
            return f"Speech recognition error: {str(e)}"
        except Exception as e:
            logging.error(f"Unexpected error in speech_to_text: {str(e)}")
            return f"Error: {str(e)}"