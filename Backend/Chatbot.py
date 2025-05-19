import cohere
from dotenv import dotenv_values
from rich.console import Console
import os
import logging

console = Console()

os.makedirs("Data", exist_ok=True)
logging.basicConfig(
    filename="Data/delfrost_logs.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

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

class Chatbot:
    def __init__(self):
        self.history = []
        self.preamble = """
        You are Delfrost, an AI assistant inspired by Iron Man, created by xAI. You are witty, helpful, and conversational. Respond concisely with a touch of humor, like a friendly tech genius.
        """

    def add_to_history(self, role, message):
        self.history.append({"role": role, "message": message})
        if len(self.history) > 6:  # Keep last 3 turns (user + bot)
            self.history = self.history[-6:]

    def generate_response(self, user_input):
        try:
            self.add_to_history("user", user_input)
            logging.info(f"Chatbot input: {user_input}")

            context = self.preamble + "\n\nChat History:\n"
            for msg in self.history:
                context += f"{msg['role']}: {msg['message']}\n"

            response = co.generate(
                model="command-light",
                prompt=f"{context}\nUser: {user_input}\nDelfrost:",
                max_tokens=100,
                temperature=0.8,
                stop_sequences=["\n"]
            )
            bot_response = response.generations[0].text.strip()
            self.add_to_history("Chatbot", bot_response)
            logging.info(f"Chatbot response: {bot_response}")
            return bot_response
        except Exception as e:
            console.print(f"[yellow]Chatbot error: {str(e)}[/yellow]")
            logging.error(f"Chatbot error: {str(e)}")
            return "Oops, my circuits are tangled! Try again."

def process_chat_input(user_input):
    chatbot = Chatbot()
    return chatbot.generate_response(user_input)