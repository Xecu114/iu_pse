import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit
from PyQt6.QtCore import QTimer, QTime, Qt
from PyQt6.QtGui import QPainter, QColor, QPaintEvent
from common.constants import PASTEL_BEIGE_HEX, PASTEL_GREEN_HEX


class CircleWithNumber(QWidget):
    def __init__(self, number, w, h, parent=None):
        super().__init__(parent)
        self.number = number
        self.w = w
        self.h = h
        self.setFixedSize(w, h)

    def paintEvent(self, event: QPaintEvent):   # type: ignore
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw circle
        painter.setBrush(QColor(132, 165, 158))
        painter.setPen(QColor(0, 0, 0))
        painter.drawEllipse((self.w//10), (self.h//10), (self.w-(self.w//5)), (self.h-(self.h//5)))

        # Draw number in the circle
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(self.font())
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, str(self.number))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 Example")
        self.setGeometry(100, 100, 1280, 720)

        # Set up UI
        self.setup_ui()

        # Timer for clock
        self.time = QTime(0, 0, 0)
        self.setup_timer()

    def setup_ui(self):
        """Setup the main UI layout and widgets."""
        # Main layout with 3 columns
        main_layout = QHBoxLayout()

        # Add first column
        first_column_container = self.create_first_column()
        main_layout.addWidget(first_column_container, stretch=1)

        # Separator line
        separator1 = self.create_separator()
        main_layout.addWidget(separator1)

        # Add second column
        second_column_container = self.create_second_column()
        main_layout.addWidget(second_column_container, stretch=1)

        # Separator line
        separator2 = self.create_separator()
        main_layout.addWidget(separator2)

        # Add third column
        third_column_container = self.create_third_column()
        main_layout.addWidget(third_column_container, stretch=1)

        # Set central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        central_widget.setStyleSheet(f"background-color: {PASTEL_BEIGE_HEX};")
        self.setCentralWidget(central_widget)

    def create_first_column(self):
        """Create the first column with a text label, circle, and button."""
        layout = QVBoxLayout()

        # Text Element
        text_label = QLabel("This is a text element")
        text_label.setStyleSheet(f"font-size: 16px; color: {PASTEL_GREEN_HEX}")
        layout.addWidget(text_label)

        # Circle with number
        circle = CircleWithNumber(42, 60, 60)
        layout.addWidget(circle)

        # Button
        button = QPushButton("Garden")
        button.setStyleSheet(f"font-size: 18px; padding: 10px; color: {PASTEL_GREEN_HEX}; border: 1px solid #84a59e; \
            background-color: transparent;")
        layout.addWidget(button)

        # Add spacer to push content to the top
        layout.addStretch()

        container = QWidget()
        container.setLayout(layout)
        container.setStyleSheet(f"background-color: {PASTEL_BEIGE_HEX};")
        return container

    def create_second_column(self):
        """Create the second column with a clock label and input field."""
        layout = QVBoxLayout()

        # Digital clock
        self.clock_label = QLabel("00:00:00")
        self.clock_label.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {PASTEL_GREEN_HEX}")
        layout.addWidget(self.clock_label)

        # Input field for number
        input_field = QLineEdit()
        input_field.setPlaceholderText("Enter a number")
        input_field.setStyleSheet(f"font-size: 16px; padding: 5px; color: {PASTEL_GREEN_HEX};\
            border: 1px solid {PASTEL_GREEN_HEX};")
        layout.addWidget(input_field)

        # Add spacer to push content to the top
        layout.addStretch()

        container = QWidget()
        container.setLayout(layout)
        container.setStyleSheet(f"background-color: {PASTEL_BEIGE_HEX};")
        return container

    def create_third_column(self):
        """Create the third column with a projects label."""
        layout = QVBoxLayout()

        # Text "Projects"
        projects_label = QLabel("Projects")
        projects_label.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {PASTEL_GREEN_HEX}")
        layout.addWidget(projects_label)

        # Add spacer to push content to the top
        layout.addStretch()

        container = QWidget()
        container.setLayout(layout)
        container.setStyleSheet(f"background-color: {PASTEL_BEIGE_HEX};")
        return container

    def create_separator(self):
        """Create a separator line."""
        separator = QWidget()
        separator.setFixedWidth(1)
        separator.setStyleSheet(f"background-color: {PASTEL_GREEN_HEX};")
        return separator

    def setup_timer(self):
        """Setup the timer to update the clock label."""
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
