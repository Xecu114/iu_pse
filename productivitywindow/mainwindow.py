from PyQt6.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, \
    QPlainTextEdit
from PyQt6.QtCore import Qt, QTime, QTimer
from PyQt6.QtGui import QPixmap, QPainter, QColor, QPaintEvent
from productivitywindow.timemanagement import TimeManagement
from common.constants import WIDTH, HEIGHT, \
    PASTEL_BEIGE_HEX, PASTEL_OCEANBAY_HEX, PASTEL_OCEANBAY_RGB, PASTEL_ROSE_RGB, PASTEL_ROSE_HEX, PASTEL_RED_HEX, \
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
        self.time_manager = TimeManagement()
        self.setup_ui()

        # Timer for updating the clock label
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_display)
        self.update_timer.start(200)

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
        """Create the first column with the points overview,
        "to the gardens" navigation button and an image of a meadow"""
        layout = QVBoxLayout()
        
        # create point overview
        self.draw_point_overview(layout)
        
        # create button to the gardens
        button = self.create_button("TO THE GARDENS")
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
        self.clock_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.clock_label)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        start_button = self.create_button("Start", self.start_time)
        buttons_layout.addWidget(start_button)

        self.pause_button = self.create_button("-", self.pause_time)
        buttons_layout.addWidget(self.pause_button)
        
        stop_button = self.create_button("Stop", self.stop_time)
        stop_button.clicked.connect(self.stop_time)
        buttons_layout.addWidget(stop_button)
        
        layout.addLayout(buttons_layout)
        
        # Input field for timer
        self.timer_input_field = QLineEdit()
        self.timer_input_field.setText("00:00:00")
        self.timer_input_field.setStyleSheet(f"font-size: 12px; padding: 5px; color: {PASTEL_OCEANBAY_HEX};\
            border: 1px solid {PASTEL_OCEANBAY_HEX};")
        self.timer_input_field.setVisible(False)
        layout.addWidget(self.timer_input_field)
        
        # Text element for errors
        self.input_error_label = QLabel("")
        self.input_error_label.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {PASTEL_RED_HEX}")
        self.input_error_label.setVisible(False)
        layout.addWidget(self.input_error_label)
        
        # Toggle button for stopwatch/timer
        self.mode_toggle_button = self.create_button("Switch to Timer", self.toggle_mode)
        layout.addWidget(self.mode_toggle_button)

        # Add spacer to push content to the top
        layout.addStretch()
        
        # Input field for text
        text_box = QPlainTextEdit()
        text_box.setPlaceholderText("Enter your text here...")
        text_box.setStyleSheet(f"font-size: 12px; padding: 5px; color: {PASTEL_OCEANBAY_HEX};\
            border: 1px solid {PASTEL_OCEANBAY_HEX};")
        font_metrics = text_box.fontMetrics()
        line_height = font_metrics.lineSpacing()
        text_box.setFixedHeight(8 * line_height + 10)
        layout.addWidget(text_box)

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

    def create_button(self, text, callback=None):
        button = QPushButton(text)
        button.setStyleSheet(f"""
            QPushButton{{
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
                color: {PASTEL_OCEANBAY_HEX};
                border: 1px solid {PASTEL_OCEANBAY_HEX};
                background-color: transparent;
            }}
            QPushButton:hover {{
                background-color: {PASTEL_ROSE_HEX};
                color: {PASTEL_OCEANBAY_HEX};
            }}
            QPushButton:pressed {{
                background-color: {PASTEL_OCEANBAY_HEX};
                color: {PASTEL_OCEANBAY_HEX};
            }}
        """)
        if callback:
            button.clicked.connect(callback)
        return button

    def draw_point_overview(self, layout):
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
    
    def update_display(self):
        """Update the displayed time on the GUI."""
        if self.time_manager.mode == "running":
            if self.time_manager.target_time != QTime(0, 0, 0):
                # Timer mode
                self.clock_label.setText(self.time_manager.target_time.toString("hh:mm:ss"))
            else:
                # Stopwatch mode
                self.clock_label.setText(self.time_manager.elapsed_time.toString("hh:mm:ss"))
            self.pause_button.setText("Pause")
        elif self.time_manager.mode == "paused":
            self.pause_button.setText("Resume")
        elif self.time_manager.mode == "stopped":
            # Default to "00:00:00" if stopped
            self.clock_label.setText("00:00:00")
            self.pause_button.setText("-")

    def start_time(self):
        """Start the stopwatch or timer."""
        self.input_error_label.setVisible(False)  # reset error on gui
        if self.time_manager.is_stopwatch:
            self.time_manager.start_stopwatch()
        else:
            # Parse the input field for timer duration
            time_text = self.timer_input_field.text()
            try:
                hours, minutes, seconds = map(int, time_text.split(":"))
                self.time_manager.set_timer(hours, minutes, seconds)
                self.time_manager.start_timer()
            except ValueError:
                # show error on gui
                self.input_error_label.setText("Invalid Time Format")
                self.input_error_label.setVisible(True)
                print(f"Error: Invalid time format provided for timer: {time_text}")  # Debug message
        
    def pause_time(self):
        """Pause or resume the timer/stopwatch."""
        if self.time_manager.mode == "running":
            self.time_manager.pause()  # Pause the timer/stopwatch
        elif self.time_manager.mode == "paused":
            self.time_manager.resume()  # Resume the timer/stopwatch

    def stop_time(self):
        self.time_manager.stop()
    
    def toggle_mode(self):
        """Switch between Stopwatch and Timer."""
        self.input_error_label.setVisible(False)  # reset error on gui
        if self.time_manager.is_stopwatch:
            self.time_manager.set_mode("timer")
            self.mode_toggle_button.setText("Switch to Stopwatch")
            self.timer_input_field.setVisible(True)
        else:
            self.time_manager.set_mode("stopwatch")
            self.mode_toggle_button.setText("Switch to Timer")
            self.timer_input_field.setVisible(False)