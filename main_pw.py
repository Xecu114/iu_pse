import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit
from PyQt6.QtCore import QTimer, QTime, Qt
from PyQt6.QtGui import QPainter, QColor

class CircleWithNumber(QWidget):
    def __init__(self, number, parent=None):
        super().__init__(parent)
        self.number = number

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw circle
        painter.setBrush(QColor(100, 150, 200))
        painter.setPen(QColor(0, 0, 0))
        painter.drawEllipse(10, 10, 100, 100)

        # Draw number in the circle
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(self.font())
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, str(self.number))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 Example")
        self.setGeometry(100, 100, 1280, 720)

        # Main layout with 3 columns
        main_layout = QHBoxLayout()

        # First column layout
        first_column_layout = QVBoxLayout()

        # Text Element
        text_label = QLabel("This is a text element")
        text_label.setStyleSheet("font-size: 16px;")
        first_column_layout.addWidget(text_label)

        # Circle with number
        circle = CircleWithNumber(42)
        circle.setFixedSize(120, 120)
        first_column_layout.addWidget(circle)

        # Button
        button = QPushButton("Garden")
        button.setStyleSheet("font-size: 18px; padding: 10px;")
        first_column_layout.addWidget(button)

        # Add spacer to push content to the top
        first_column_layout.addStretch()

        # Add the first column layout to the main layout
        first_column_container = QWidget()
        first_column_container.setLayout(first_column_layout)
        main_layout.addWidget(first_column_container, stretch=1)

        # Second column layout
        second_column_layout = QVBoxLayout()

        # Digital clock
        self.clock_label = QLabel("00:00:00")
        self.clock_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        second_column_layout.addWidget(self.clock_label)

        # Input field for number
        input_field = QLineEdit()
        input_field.setPlaceholderText("Enter a number")
        input_field.setStyleSheet("font-size: 16px; padding: 5px;")
        second_column_layout.addWidget(input_field)

        # Add spacer to push content to the top
        second_column_layout.addStretch()

        # Add the second column layout to the main layout
        second_column_container = QWidget()
        second_column_container.setLayout(second_column_layout)
        main_layout.addWidget(second_column_container, stretch=1)

        # Third column layout
        third_column_layout = QVBoxLayout()

        # Text "Projects"
        projects_label = QLabel("Projects")
        projects_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        third_column_layout.addWidget(projects_label)

        # Add spacer to push content to the top
        third_column_layout.addStretch()

        # Add the third column layout to the main layout
        third_column_container = QWidget()
        third_column_container.setLayout(third_column_layout)
        main_layout.addWidget(third_column_container, stretch=1)

        # Set central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Timer for clock
        self.time = QTime(0, 0, 0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # Update every second

    def update_time(self):
        self.time = self.time.addSecs(1)
        self.clock_label.setText(self.time.toString("hh:mm:ss"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
