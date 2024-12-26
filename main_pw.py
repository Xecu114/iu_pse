import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit
from PyQt6.QtCore import QTimer, QTime, Qt
from PyQt6.QtGui import QPainter, QColor, QPaintEvent, QPixmap
from common.constants import WIDTH, HEIGHT, \
    PASTEL_BEIGE_HEX, PASTEL_OCEANBAY_HEX, PASTEL_OCEANBAY_RGB, PASTEL_ROSE_RGB, \
    IMGDIR_GUI_FLOWER_MEADOW


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
        r, g, b = PASTEL_ROSE_RGB
        painter.setBrush(QColor(r, g, b))
        painter.setPen(QColor(r, g, b))
        painter.drawEllipse((self.w//10), (self.h//10), (self.w-(self.w//5)), (self.h-(self.h//5)))

        # Draw number in the circle
        r, g, b = PASTEL_OCEANBAY_RGB
        painter.setPen(QColor(r, g, b))
        font = painter.font()
        font.setBold(True)
        font.setPointSize(14)
        painter.setFont(font)
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, str(self.number))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ProductivityGarden")
        self.setGeometry(100, 100, WIDTH, HEIGHT)

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
        points_label = QLabel("Points")
        points_label.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {PASTEL_OCEANBAY_HEX}")
        layout.addWidget(points_label)

        # Horizontal layout for circle and text
        circle_and_text_layout_av = QHBoxLayout()
        
        # Circle with number
        circle_av = CircleWithNumber(12, 60, 60)
        circle_and_text_layout_av.addWidget(circle_av)
        
        # Label next to the circle
        circle_text_label = QLabel("available")
        circle_text_label.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {PASTEL_OCEANBAY_HEX}")
        circle_and_text_layout_av.addWidget(circle_text_label)
        
        # Add the horizontal layout to the main layout
        layout.addLayout(circle_and_text_layout_av)
        
        # Horizontal layout for circle and text
        circle_and_text_layout_tot = QHBoxLayout()
        
        circle_tot = CircleWithNumber(42, 60, 60)
        circle_and_text_layout_tot.addWidget(circle_tot)
        
        # Label next to the circle
        circle_text_label = QLabel("total")
        circle_text_label.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {PASTEL_OCEANBAY_HEX}")
        circle_and_text_layout_tot.addWidget(circle_text_label)
        
        # Add the horizontal layout to the main layout
        layout.addLayout(circle_and_text_layout_tot)

        # Button
        button = QPushButton("TO THE GARDENS")
        button.setStyleSheet(f"font-size: 16px; font-weight: bold; padding: 10px; color: {PASTEL_OCEANBAY_HEX};\
            border: 1px solid #84a59e; background-color: transparent;")
        layout.addWidget(button)
        
        # Image
        image_label = QLabel()
        pixmap = QPixmap(IMGDIR_GUI_FLOWER_MEADOW)  # Get image
        scaled_pixmap = pixmap.scaled((WIDTH//3), (HEIGHT*2//3), Qt.AspectRatioMode.IgnoreAspectRatio)  # Scale image
        image_label.setPixmap(scaled_pixmap)    # Assign the scaled image
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(image_label)

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
        self.clock_label.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {PASTEL_OCEANBAY_HEX}")
        layout.addWidget(self.clock_label)

        # Input field for number
        input_field = QLineEdit()
        input_field.setPlaceholderText("Enter a number")
        input_field.setStyleSheet(f"font-size: 16px; padding: 5px; color: {PASTEL_OCEANBAY_HEX};\
            border: 1px solid {PASTEL_OCEANBAY_HEX};")
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
        projects_label.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {PASTEL_OCEANBAY_HEX}")
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
        separator.setStyleSheet(f"background-color: {PASTEL_OCEANBAY_HEX};")
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
