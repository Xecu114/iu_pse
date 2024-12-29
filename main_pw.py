import sys
from PyQt6.QtWidgets import QApplication
from productivitysession.session import MainSession

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Create MainSession with all functionalities regarding productivity
    # like timemanagement, pointsystem, projectmanagement
    session = MainSession()
    session.show()
    sys.exit(app.exec())