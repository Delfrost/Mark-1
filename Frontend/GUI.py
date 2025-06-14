import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
from rich.console import Console
import logging

console = Console()

logging.basicConfig(
    filename="Data/delfrost_logs.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class DelfrostGUI(QMainWindow):
    def __init__(self, process_input, speech_to_text, speak_text):
        super().__init__()
        self.process_input = process_input
        self.speech_to_text = speech_to_text
        self.speak_text = speak_text
        self.voice_mode = False
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Jerry AI Assistant")
        self.setGeometry(100, 100, 600, 400)

        # Main widget and layout
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Chat display
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)

        # Input field
        self.input_field = QLineEdit()
        self.input_field.returnPressed.connect(self.send_command)
        layout.addWidget(self.input_field)

        # Send button
        send_button = QPushButton("Send")
        send_button.clicked.connect(self.send_command)
        layout.addWidget(send_button)

        # Voice button
        voice_button = QPushButton("Toggle Voice Mode")
        voice_button.clicked.connect(self.toggle_voice_mode)
        layout.addWidget(voice_button)

        # Speech input button
        speech_button = QPushButton("Speak Command")
        speech_button.clicked.connect(self.speech_command)
        layout.addWidget(speech_button)

    def send_command(self):
        user_input = self.input_field.text().strip()
        if user_input:
            self.chat_display.append(f"<b>You:</b> {user_input}")
            logging.info(f"GUI input: {user_input}")
            response, intent = self.process_input(user_input)
            self.chat_display.append(f"<b>Delfrost:</b> {response}")
            logging.info(f"GUI response: {response}")
            if self.voice_mode:
                self.speak_text(response)
            self.input_field.clear()
            # Update voice mode based on intent
            if intent == "voice":
                self.voice_mode = "enable" in user_input.lower()

    def speech_command(self):
        try:
            user_input = self.speech_to_text()
            if user_input in ["No speech detected.", "Could not understand audio."]:
                self.chat_display.append(f"<b>Error:</b> {user_input}")
                return
            if "error" in user_input.lower():
                self.chat_display.append(f"<b>Error:</b> {user_input}")
                return
            self.chat_display.append(f"<b>You:</b> {user_input}")
            logging.info(f"GUI speech input: {user_input}")
            response, intent = self.process_input(user_input)
            self.chat_display.append(f"<b>Delfrost:</b> {response}")
            logging.info(f"GUI speech response: {response}")
            if self.voice_mode:
                self.speak_text(response)
            # Update voice mode based on intent
            if intent == "voice":
                self.voice_mode = "enable" in user_input.lower()
        except Exception as e:
            self.chat_display.append(f"<b>Error:</b> Speech input error: {str(e)}")
            logging.error(f"GUI speech input error: {str(e)}")

    def toggle_voice_mode(self):
        self.voice_mode = not self.voice_mode
        status = "enabled" if self.voice_mode else "disabled"
        self.chat_display.append(f"<b>Jerry:</b> Voice mode {status}.")
        logging.info(f"Voice mode {status}")
        response, intent = self.process_input(f"{'enable' if self.voice_mode else 'disable'} voice")
        self.chat_display.append(f"<b>Jerry:</b> {response}")

def run_gui(process_input, speech_to_text, speak_text):
    app = QApplication(sys.argv)
    window = DelfrostGUI(process_input, speech_to_text, speak_text)
    window.show()
    sys.exit(app.exec_())