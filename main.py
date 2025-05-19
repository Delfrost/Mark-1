import argparse
import os
from rich.console import Console
import logging
from dotenv import dotenv_values
from Backend.Model import process_input
from Backend.SpeechtoText import speech_to_text
from Backend.TextToSpeech import speak_text

# Initialize console and logging
console = Console()
os.makedirs("Data", exist_ok=True)
logging.basicConfig(
    filename="Data/delfrost_logs.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Load environment variables
env_vars = dotenv_values(".env")
CohereAPIKey = env_vars.get("CohereAPIKey")
if not CohereAPIKey:
    console.print("[bold red]Error: Cohere API key not found in .env.[/bold red]")
    logging.error("Cohere API key not found")
    raise ValueError("CohereAPIKey required")

# Voice mode flag
voice_mode = False

def run_console_mode():
    global voice_mode
    console.print("[bold green]Jerry Console Mode Initialized. Type 'exit' or speak to quit.[/bold green]")
    logging.info("Jerry Console Mode Initialized")
    while True:
        if voice_mode:
            try:
                user_input = speech_to_text()
                if user_input in ["No speech detected.", "Could not understand audio."]:
                    console.print(f"[yellow]{user_input}[/yellow]")
                    continue
                if "error" in user_input.lower():
                    console.print(f"[yellow]{user_input}[/yellow]")
                    continue
                console.print(f"[bold green]You: {user_input}[/bold green]")
            except Exception as e:
                console.print(f"[yellow]Speech input error: {str(e)}[/yellow]")
                continue
        else:
            user_input = input("You: ").strip()
        
        if user_input.lower() in ["exit", "quit"]:
            console.print("[bold green]Shutting down...[/bold green]")
            logging.info("Jerry shutdown")
            break
        
        response, intent = process_input(user_input)
        console.print(f"[bold blue]Jerry: {response}[/bold blue]")
        # Update voice_mode based on intent
        if intent == "voice":
            voice_mode = "enable" in user_input.lower()

def run_gui_mode():
    from Frontend.GUI import run_gui
    console.print("[bold green]Starting Jerry GUI Mode...[/bold green]")
    logging.info("Delfrost GUI Mode Initialized")
    run_gui(process_input, speech_to_text, speak_text)

def main():
    parser = argparse.ArgumentParser(description="Delfrost AI Assistant")
    parser.add_argument("--mode", choices=["console", "gui"], default="console", help="Run mode: console or gui")
    args = parser.parse_args()

    if args.mode == "console":
        run_console_mode()
    elif args.mode == "gui":
        run_gui_mode()

if __name__ == "__main__":
    main()