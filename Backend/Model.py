import cohere
from rich import print
from rich.console import Console
from dotenv import dotenv_values
import os
import re
from functools import lru_cache
import logging

os.makedirs("Data", exist_ok=True)
logging.basicConfig(
    filename="Data/delfrost_logs.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

try:
    from Backend.RealTimeSearchEngine import perform_youtube_search, perform_google_search
except ImportError:
    def perform_youtube_search(query):
        return "YouTube search not implemented."
    def perform_google_search(query):
        return "Google search not implemented."

try:
    from Backend.Automation import open_application, close_application, play_media
except ImportError:
    def open_application(app_name):
        return "Application opening not implemented."
    def close_application(app_name):
        return "Application closing not implemented."
    def play_media(media):
        return "Media playback not implemented."

try:
    from ImageGeneration import generate_image
except ImportError:
    def generate_image(description):
        return "Image generation not implemented."

try:
    from TextToSpeech import speak_text
except ImportError:
    def speak_text(text):
        return "Text-to-speech not implemented."

console = Console()

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

funcs = [
    "exit", "general", "realtime", "open", "close", "play", "generate image",
    "google search", "youtube search", "system", "content", "reminder"
]

messages = []

preamble = """
You are Delfrost, an AI assistant inspired by Iron Man, created by xAI. You are witty, helpful, and capable of performing tasks like searches, opening apps, and more. Respond concisely and professionally.
"""

ChatHistory = [
    {"role": "user", "message": "Hello"},
    {"role": "Chatbot", "message": "Hello! How can I assist you?"},
    {"role": "user", "message": "Tell me a joke"},
    {"role": "Chatbot", "message": "Why don't atoms trust each other? They make up everything!"},
]

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
    return "general"

def process_input(user_input):
    try:
        messages.append({"role": "user", "message": user_input})
        logging.info(f"User input: {user_input}")

        intent = classify_intent(user_input)
        logging.info(f"Classified intent: {intent}")

        if intent == "exit":
            return "Shutting down Delfrost...", intent
        elif intent == "open":
            if "youtube" in user_input.lower():
                bot_response = perform_youtube_search("")
            else:
                app_name = re.sub(r"\b(open|start|hi\s+delfrost|kindly)\b", "", user_input, flags=re.IGNORECASE).strip()
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
            query = re.sub(r"\b(google\s+search|search\s+google|hi\s+delfrost|kindly)\b", "", user_input, flags=re.IGNORECASE).strip()
            bot_response = perform_google_search(query)
        elif intent == "youtube search":
            query = re.sub(r"\b(youtube\s+search|search\s+youtube|open\s+[\w\s]*youtube[\w\s]*\s+(and\s+search|search)|hi\s+delfrost|kindly)\b", "", user_input, flags=re.IGNORECASE).strip()
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
        else:
            context = preamble + "\n\nRecent Chat History:\n"
            for msg in messages[-3:]:
                context += f"{msg['role']}: {msg['message']}\n"
            try:
                response = co.generate(
                    model="command-light",
                    prompt=f"{context}\nUser: {user_input}\nDelfrost:",
                    max_tokens=50,
                    temperature=0.7,
                    stop_sequences=["\n"]
                )
                bot_response = response.generations[0].text.strip()
            except cohere.error.CohereAPIError as api_err:
                console.print(f"[yellow]API Error: {str(api_err)}[/yellow]")
                logging.warning(f"Cohere API Error: {str(api_err)}")
                bot_response = "Trouble connecting to knowledge base."

        messages.append({"role": "Chatbot", "message": bot_response})
        logging.info(f"Delfrost response: {bot_response}")
        return bot_response, intent
    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}[/bold red]")
        logging.error(f"Error: {str(e)}")
        return "Error occurred. Try again.", "general"

def main():
    console.print("[bold green]Delfrost Initialized. Type 'exit' to quit.[/bold green]")
    logging.info("Delfrost Initialized")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            console.print("[bold green]Shutting down...[/bold green]")
            logging.info("Delfrost shutdown")
            break
        response, intent = process_input(user_input)
        console.print(f"[bold blue]Delfrost: {response}[/bold blue]")

if __name__ == "__main__":
    main()