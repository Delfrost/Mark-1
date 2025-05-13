import sys
import os
import logging
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# Import Model.py for AI processing
try:
    from Backend.Model import process_input
except ImportError:
    print("Error: Model.py not found in Backend folder.")
    raise

# Set up logging to Data folder
os.makedirs("Data", exist_ok=True)
logging.basicConfig(
    filename="Data/delfrost_logs.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class DelfrostWindow(QMainWindow):
    """
    Main window for the Delfrost GUI.
    """
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """
        Initialize the GUI components.
        """
        self.setWindowTitle("Delfrost AI Assistant")
        self.setGeometry(100, 100, 600, 400)

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Header
        header = QLabel("Delfrost: Your AI Assistant")
        header.setFont(QFont("Arial", 16, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        # Chat output area (read-only)
        self.chat_output = QTextEdit()
        self.chat_output.setReadOnly(True)
        self.chat_output.setFont(QFont("Arial", 12))
        layout.addWidget(self.chat_output)

        # Input area
        input_layout = QHBoxLayout()
        
        self.input_field = QLineEdit()
        self.input_field.setFont(QFont("Arial", 12))
        self.input_field.setPlaceholderText("Type your command (e.g., 'open youtube')")
        self.input_field.returnPressed.connect(self.send_input)
        input_layout.addWidget(self.input_field)

        send_button = QPushButton("Send")
        send_button.setFont(QFont("Arial", 12))
        send_button.clicked.connect(self.send_input)
        input_layout.addWidget(send_button)

        layout.addLayout(input_layout)

        # Control buttons
        control_layout = QHBoxLayout()
        
        clear_button = QPushButton("Clear Chat")
        clear_button.setFont(QFont("Arial", 12))
        clear_button.clicked.connect(self.clear_chat)
        control_layout.addWidget(clear_button)

        exit_button = QPushButton("Exit")
        exit_button.setFont(QFont("Arial", 12))
        exit_button.clicked.connect(self.close)
        control_layout.addWidget(exit_button)

        layout.addLayout(control_layout)

        # Log GUI initialization
        logging.info("Delfrost GUI initialized")

    def send_input(self):
        """
        Process user input and display the response.
        """
        user_input = self.input_field.text().strip()
        if not user_input:
            return

        # Display user input
        self.chat_output.append(f"<b>You:</b> {user_input}")
        logging.info(f"GUI User input: {user_input}")

        # Process input using Model.py
        try:
            response, intent = process_input(user_input)
            self.chat_output.append(f"<b>Delfrost:</b> {response}")
            logging.info(f"GUI Response: {response}, Intent: {intent}")
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.chat_output.append(f"<b>Delfrost:</b> {error_msg}")
            logging.error(f"GUI Error: {error_msg}")

        # Clear input field
        self.input_field.clear()

        # Scroll to bottom
        self.chat_output.verticalScrollBar().setValue(self.chat_output.verticalScrollBar().maximum())

    def clear_chat(self):
        """
        Clear the chat output area.
        """
        self.chat_output.clear()
        logging.info("GUI Chat cleared")

def run_gui():
    """
    Launch the Delfrost GUI application.
    """
    app = QApplication(sys.argv)
    window = DelfrostWindow()
    window.show()
    sys.exit(app.exec_())