import argparse
import os
import logging
from datetime import datetime
from dotenv import dotenv_values
from rich.console import Console
from rich import print

# Import Model.py for AI processing
try:
    from Backend.Model import process_input
except ImportError:
    print("[bold red]Error: Model.py not found in Backend folder.[/bold red]")
    raise

# Import GUI.py for GUI mode
try:
    from Frontend.GUI import run_gui
except ImportError:
    print("[bold red]Error: GUI.py not found in Frontend folder.[/bold red]")
    raise

# Initialize rich console for formatted output
console = Console()

# Set up logging to Data folder
os.makedirs("Data", exist_ok=True)
logging.basicConfig(
    filename="Data/delfrost_logs.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def load_config():
    """
    Load environment variables and validate configuration.
    Returns the Cohere API key.
    """
    env_vars = dotenv_values(".env")
    cohere_api_key = env_vars.get("CohereAPIKey")
    if not cohere_api_key:
        console.print("[bold red]Error: Cohere API key not found in .env file.[/bold red]")
        logging.error("Cohere API key not found in .env")
        raise ValueError("CohereAPIKey is required in .env")
    return cohere_api_key

def run_console_mode():
    """
    Run Delfrost in console mode, similar to Model.py's main() function.
    """
    console.print("[bold green]Delfrost Model Initialized (Console Mode). Type 'exit' to quit.[/bold green]")
    logging.info("Delfrost initialized in console mode")
    
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            console.print("[bold green]Shutting down Delfrost...[/bold green]")
            logging.info("Shutting down Delfrost")
            break
        
        # Process input using Model.py
        response, intent = process_input(user_input)
        console.print(f"[bold blue]Delfrost: {response}[/bold blue]")
        logging.info(f"Intent: {intent}")

def run_gui_mode():
    """
    Run Delfrost in GUI mode using GUI.py.
    """
    console.print("[bold green]Starting Delfrost in GUI mode...[/bold green]")
    logging.info("Delfrost initialized in GUI mode")
    run_gui()

def main():
    """
    Main entry point for the Delfrost application.
    Parses arguments and starts the appropriate mode.
    """
    parser = argparse.ArgumentParser(description="Delfrost AI Assistant")
    parser.add_argument(
        "--mode",
        choices=["console", "gui"],
        default="console",
        help="Run Delfrost in console or GUI mode (default: console)"
    )
    args = parser.parse_args()

    # Load configuration
    try:
        cohere_api_key = load_config()
        logging.info("Configuration loaded successfully")
    except Exception as e:
        console.print(f"[bold red]Failed to load configuration: {str(e)}[/bold red]")
        logging.error(f"Failed to load configuration: {str(e)}")
        return

    # Start the application in the specified mode
    try:
        if args.mode == "console":
            run_console_mode()
        elif args.mode == "gui":
            run_gui_mode()
    except Exception as e:
        console.print(f"[bold red]Error running Delfrost: {str(e)}[/bold red]")
        logging.error(f"Error running Delfrost: {str(e)}")

if __name__ == "__main__":
    main()