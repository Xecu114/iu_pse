import sys
from PyQt6.QtWidgets import QApplication
from productivitywindow.mainwindow import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Create Main Window with all functionalities regarding productivity
    # like timemanagement, pointsystem, projectmanagement
    window = MainWindow()
    window.show()
    sys.exit(app.exec())