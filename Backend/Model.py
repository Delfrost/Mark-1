import os
print("Current working directory:", os.getcwd())
import cohere
from rich import print
from rich.console import Console
from dotenv import dotenv_values
import re
from functools import lru_cache
import logging

os.makedirs("Data", exist_ok=True)
logging.basicConfig(
    filename="Data/Jerry_logs.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Initialize import status flags for debugging
youtube_search_imported = False
automation_imported = False
image_generation_imported = False
text_to_speech_imported = False
speech_to_text_imported = False
chatbot_imported = False

try:
    from Backend.RealTimeSearchEngine import perform_youtube_search, perform_google_search
    youtube_search_imported = True
except ImportError as e:
    logging.error(f"Failed to import RealTimeSearchEngine: {str(e)}")
    def perform_youtube_search(query):
        return "YouTube search not implemented."
    def perform_google_search(query):
        return "Google search not implemented."

try:
    from Backend.Automation import open_application, close_application, play_media
    automation_imported = True
except ImportError as e:
    logging.error(f"Failed to import Automation: {str(e)}")
    def open_application(app_name):
        return "Application opening not implemented."
    def close_application(app_name):
        return "Application closing not implemented."
    def play_media(media):
        return "Media playback not implemented."

try:
    from Backend.ImageGeneration import generate_image
    image_generation_imported = True
except ImportError as e:
    logging.error(f"Failed to import ImageGeneration: {str(e)}")
    def generate_image(description):
        return "Image generation not implemented."

try:
    from Backend.TextToSpeech import speak_text
    text_to_speech_imported = True
except ImportError as e:
    logging.error(f"Failed to import TextToSpeech: {str(e)}")
    def speak_text(text):
        return "Text-to-speech not implemented."

try:
    from Backend.SpeechtoText import speech_to_text
    speech_to_text_imported = True
except ImportError as e:
    logging.error(f"Failed to import SpeechtoText: {str(e)}")
    def speech_to_text():
        return "Speech-to-text not implemented."

try:
    from Backend.Chatbot import process_chat_input
    chatbot_imported = True
except ImportError as e:
    logging.error(f"Failed to import Chatbot: {str(e)}")
    def process_chat_input(user_input):
        return "Chatbot not implemented."

# Log import status
console = Console()
console.print(f"[cyan]YouTube search imported: {youtube_search_imported}[/cyan]")
console.print(f"[cyan]Automation imported: {automation_imported}[/cyan]")
console.print(f"[cyan]Image generation imported: {image_generation_imported}[/cyan]")
console.print(f"[cyan]Text to speech imported: {text_to_speech_imported}[/cyan]")
console.print(f"[cyan]Speech to text imported: {speech_to_text_imported}[/cyan]")
console.print(f"[cyan]Chatbot imported: {chatbot_imported}[/cyan]")

env_vars = dotenv_values(".env")
CohereAPIKey = env_vars.get("CohereAPIKey")

if not CohereAPIKey:
    console.print("[bold red]Error: Cohere API key not found in .env.[/bold red]")
    logging.error("Cohere API key not found")
    raise ValueError("CohereAPIKey required")

try:
    co = cohere.Client(api_key=CohereAPIKey)
except Exception as e:
    console.print(f"[bold red]Cohere client error: {str(e)}[/bold red]")
    logging.error(f"Cohere client error: {str(e)}")
    raise

# Voice mode flag
voice_mode = False

funcs = [
    "exit", "general", "realtime", "open", "close", "play", "generate image",
    "google search", "youtube search", "system", "content", "reminder", "voice"
]

messages = []

preamble = """
You are Jerry, an AI assistant inspired by Iron Man, created by xAI. You are witty, helpful, and capable of performing tasks like searches, opening apps, and more. Respond concisely and professionally.
"""

@lru_cache(maxsize=100)
def classify_intent(user_input):
    user_input_lower = user_input.lower().strip()
    if user_input_lower in ["exit", "quit"]:
        return "exit"
    if re.search(r"\b(open|start)\s+[\w\s]*youtube[\w\s]*\b", user_input_lower):
        if re.search(r"\b(search|and\s+search)\b", user_input_lower):
            return "youtube search"
        return "open"
    if re.search(r"\b(open|start)\s+\w+\b", user_input_lower):
        return "open"
    if re.search(r"\bclose\s+\w+\b", user_input_lower):
        return "close"
    if re.search(r"\bplay\s+\w+\b", user_input_lower):
        return "play"
    if re.search(r"\bgenerate\s+image\b", user_input_lower):
        return "generate image"
    if re.search(r"\b(google\s+search|search\s+google)\b", user_input_lower):
        return "google search"
    if re.search(r"\b(youtube\s+search|search\s+youtube)\b", user_input_lower):
        return "youtube search"
    if re.search(r"\brealtime\s+news\b", user_input_lower):
        return "realtime"
    if re.search(r"\bsystem\s+(status|info)\b", user_input_lower):
        return "system"
    if re.search(r"\bwrite\s+(story|content)\b", user_input_lower):
        return "content"
    if re.search(r"\bset\s+reminder\b", user_input_lower):
        return "reminder"
    if re.search(r"\b(enable|disable)\s+voice\b", user_input_lower):
        return "voice"
    return "general"

def process_input(user_input):
    global voice_mode
    try:
        messages.append({"role": "user", "message": user_input})
        logging.info(f"User input: {user_input}")

        intent = classify_intent(user_input)
        logging.info(f"Classified intent: {intent}")

        if intent == "exit":
            return "Shutting down Jerry...", intent
        elif intent == "open":
            if "youtube" in user_input.lower():
                bot_response = perform_youtube_search("")
            else:
                app_name = re.sub(r"\b(open|start|hi\s+Jerry|kindly)\b", "", user_input, flags=re.IGNORECASE).strip()
                bot_response = open_application(app_name)
        elif intent == "close":
            app_name = re.sub(r"\bclose\b", "", user_input, flags=re.IGNORECASE).strip()
            bot_response = close_application(app_name)
        elif intent == "play":
            media = re.sub(r"\bplay\b", "", user_input, flags=re.IGNORECASE).strip()
            bot_response = play_media(media)
        elif intent == "generate image":
            description = re.sub(r"\bgenerate\s+image\b", "", user_input, flags=re.IGNORECASE).strip()
            bot_response = generate_image(description)
        elif intent == "google search":
            query = re.sub(r"\b(google\s+search|search\s+google|hi\s+Jerry|kindly)\b", "", user_input, flags=re.IGNORECASE).strip()
            bot_response = perform_google_search(query)
        elif intent == "youtube search":
            query = re.sub(r"\b(youtube\s+search|search\s+youtube|open\s+[\w\s]*youtube[\w\s]*\s+(and\s+search|search)|hi\s+Jerry|kindly)\b", "", user_input, flags=re.IGNORECASE).strip()
            bot_response = perform_youtube_search(query)
        elif intent == "realtime":
            bot_response = "Real-time news not implemented."
        elif intent == "system":
            bot_response = "System status not implemented."
        elif intent == "content":
            topic = re.sub(r"\bwrite\s+(story|content)\b", "", user_input, flags=re.IGNORECASE).strip()
            bot_response = f"Content generation for '{topic}' not implemented."
        elif intent == "reminder":
            reminder = re.sub(r"\bset\s+reminder\b", "", user_input, flags=re.IGNORECASE).strip()
            bot_response = f"Reminder for '{reminder}' not implemented."
        elif intent == "voice":
            if "enable" in user_input.lower():
                voice_mode = True
                bot_response = "Voice mode enabled."
            else:
                voice_mode = False
                bot_response = "Voice mode disabled."
        else:
            bot_response = process_chat_input(user_input)

        # Speak response if voice mode is enabled
        if voice_mode and text_to_speech_imported and bot_response:
            speak_text(bot_response)

        messages.append({"role": "Chatbot", "message": bot_response})
        logging.info(f"Jerry response: {bot_response}")
        return bot_response, intent
    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}[/bold red]")
        logging.error(f"Error: {str(e)}")
        return "Error occurred. Try again.", "general"

def main():
    global voice_mode
    console.print("[bold green]Jerry Initialized. Type 'exit' or speak to quit.[/bold green]")
    logging.info("Jerry Initialized")
    while True:
        if voice_mode and speech_to_text_imported:
            user_input = speech_to_text()
            if user_input in ["No speech detected.", "Could not understand audio."]:
                console.print(f"[yellow]{user_input}[/yellow]")
                continue
            if "error" in user_input.lower():
                console.print(f"[yellow]{user_input}[/yellow]")
                continue
            console.print(f"[bold green]You: {user_input}[/bold green]")
        else:
            user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            console.print("[bold green]Shutting down...[/bold green]")
            logging.info("Jerry shutdown")
            break
        response, intent = process_input(user_input)
        console.print(f"[bold blue]Jerry: {response}[/bold blue]")

if __name__ == "__main__":
    main()