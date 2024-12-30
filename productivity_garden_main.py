import sys
from PyQt6.QtWidgets import QApplication
from src.session import MainSession


if __name__ == "__main__":
    # Initialize the qt application instance
    # This is the main application object required for any PyQt application.
    app = QApplication(sys.argv)
    
    # Create an instance of MainSession
    # This object represents the primary functionality of the application.
    # It includes features like time management, a points system, and project management.
    session = MainSession()
    #  Display the main window (application's GUI)
    session.show()
    
    # Start the application event loop
    # This keeps the application running and responsive to user input until the window is closed.
    sys.exit(app.exec())
    