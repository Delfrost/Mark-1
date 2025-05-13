from rich import print
from rich.console import Console
import subprocess
import os
import webbrowser
from RealTimeSearchEngine import perform_youtube_search

console = Console()

def open_application(app_name):
    try:
        if not app_name:
            return "No application name provided."
        app_name_lower = app_name.lower().strip()
        if "youtube" in app_name_lower:
            return perform_youtube_search("")
        app_name_clean = app_name_lower.replace(" ", "").replace("ms paint", "mspaint")
        app_map = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "browser": "msedge.exe",
            "mspaint": "mspaint.exe",
            "paint": "mspaint.exe",
            "spotify": "spotify",
        }
        executable = app_map.get(app_name_clean, app_name_clean)
        if executable == "spotify":
            try:
                webbrowser.open("spotify:")
                console.print(f"[cyan]Opening Spotify[/cyan]")
                return "Done!"
            except:
                spotify_path = os.path.expanduser("~/AppData/Roaming/Spotify/Spotify.exe")
                if os.path.exists(spotify_path):
                    subprocess.run([spotify_path], check=True)
                    console.print(f"[cyan]Opening Spotify[/cyan]")
                    return "Done!"
                return "Spotify not found. Ensure it is installed."
        if os.name == "nt":
            subprocess.run(["start", "", executable], shell=True, check=True)
        else:
            subprocess.run(["open", executable], check=True)
        console.print(f"[cyan]Opening application: {app_name}[/cyan]")
        return "Done!"
    except Exception as e:
        console.print(f"[yellow]Error opening {app_name}: {str(e)}[/yellow]")
        return f"Failed to open {app_name}: {str(e)}"

def close_application(app_name):
    try:
        if not app_name:
            return "No application name provided."
        app_name_clean = app_name.lower().replace(" ", "").replace("ms paint", "mspaint")
        app_map = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "browser": "msedge.exe",
            "mspaint": "mspaint.exe",
            "paint": "mspaint.exe",
            "spotify": "Spotify.exe",
        }
        executable = app_map.get(app_name_clean, app_name_clean)
        if os.name == "nt":
            subprocess.run(["taskkill", "/IM", executable, "/F"], check=True)
        else:
            subprocess.run(["pkill", executable], check=True)
        console.print(f"[cyan]Closing application: {app_name}[/cyan]")
        return "Done!"
    except Exception as e:
        console.print(f"[yellow]Error closing {app_name}: {str(e)}[/yellow]")
        return f"Failed to open {app_name}: {str(e)}"

def play_media(media):
    try:
        if not media:
            return "No media specified."
        console.print(f"[cyan]Playing media: {media}[/cyan]")
        return "Media playback not fully implemented."
    except Exception as e:
        console.print(f"[yellow]Error playing {media}: {str(e)}[/yellow]")
        return f"Failed to play {media}: {str(e)}"