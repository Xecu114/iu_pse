import json
import os
import re
from PyQt6.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, \
    QLineEdit, QPlainTextEdit
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QPainter, QColor, QPaintEvent
from src.timemanagement import TimeManagement
from src.pointssystem import PointsSystem
# from main_vg import main
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
    
    def update_widget(self, new_number):
        self.number = new_number
        self.update()


class MainSession(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data_filename = "data.json"
        
        # Create class instances
        self.point_system = PointsSystem()
        self.time_manager = TimeManagement()
        
        # UI
        self.setWindowTitle("ProductivityGarden")
        self.setGeometry(100, 100, WIDTH, HEIGHT)
        self.setup_ui()
        
        self.load_data()
        self.update_app()
        
        # Timer for updating the clock label
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_app)
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
        # button = self.create_button("TO THE GARDENS", main)
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

        self.draw_time_management_area(layout)

        # Add spacer to push content to the top
        layout.addStretch()
        
        # Input field for text
        self.text_box = QPlainTextEdit()
        self.text_box.setPlaceholderText("Enter your text here...")
        self.text_box.setStyleSheet(f"font-size: 16px; padding: 5px; color: {PASTEL_OCEANBAY_HEX};\
            border: 1px solid {PASTEL_OCEANBAY_HEX};")
        font_metrics = self.text_box.fontMetrics()
        line_height = font_metrics.lineSpacing()
        self.text_box.setFixedHeight(8 * line_height + 10)
        layout.addWidget(self.text_box)

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
        if callback is not None:
            button.clicked.connect(callback)
        return button

    def draw_point_overview(self, layout : QVBoxLayout):
        # Text Element
        points_label = QLabel("Points")
        points_label.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {PASTEL_OCEANBAY_HEX}")
        layout.addWidget(points_label)

        # Horizontal layout for circle and text
        circle_and_text_layout_av = QHBoxLayout()
        
        # Circle with number (currently available points)
        self.circle_av = CircleWithNumber(self.point_system.get_points()[1], 60, 60)
        circle_and_text_layout_av.addWidget(self.circle_av)
        
        # Label next to the circle
        circle_text_label = QLabel("available")
        circle_text_label.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {PASTEL_OCEANBAY_HEX}")
        circle_and_text_layout_av.addWidget(circle_text_label)
        
        # Add the horizontal layout to the main layout
        layout.addLayout(circle_and_text_layout_av)
        
        # Horizontal layout for circle and text
        circle_and_text_layout_tot = QHBoxLayout()
        
        # Circle with number (total points collected)
        self.circle_tot = CircleWithNumber(self.point_system.get_points()[0], 60, 60)
        circle_and_text_layout_tot.addWidget(self.circle_tot)
        
        # Label next to the circle
        circle_text_label = QLabel("total")
        circle_text_label.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {PASTEL_OCEANBAY_HEX}")
        circle_and_text_layout_tot.addWidget(circle_text_label)
        
        # Add the horizontal layout to the main layout
        layout.addLayout(circle_and_text_layout_tot)

    def draw_time_management_area(self, layout : QVBoxLayout):
        # Display current timer mode
        self.timer_mode_label = QLabel(self.time_manager.selected_timer.upper())
        self.timer_mode_label.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {PASTEL_OCEANBAY_HEX}")
        self.timer_mode_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.timer_mode_label)
        
        # Digital clock
        self.clock_label = QLabel("00:00:00")
        self.clock_label.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {PASTEL_OCEANBAY_HEX}")
        self.clock_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.clock_label)
        
        # Buttons to control the various time functions
        buttons_layout = QHBoxLayout()
        start_button = self.create_button("Start", self.start_time)
        buttons_layout.addWidget(start_button)

        self.pause_button = self.create_button("-", self.pause_time)
        buttons_layout.addWidget(self.pause_button)
        
        stop_button = self.create_button("Stop", self.stop_time)
        stop_button.clicked.connect(self.stop_time)
        buttons_layout.addWidget(stop_button)
        
        layout.addLayout(buttons_layout)
        
        # Input field for pomodoro #1
        work_input_layout = QHBoxLayout()
        self.pomodoro_work_input = QLineEdit()
        self.pomodoro_work_input.setText("00:25:00")
        self.pomodoro_work_input.setStyleSheet(f"font-size: 16px; padding: 5px; color: {PASTEL_OCEANBAY_HEX};\
            border: 1px solid {PASTEL_OCEANBAY_HEX};")
        self.pomodoro_work_input.setVisible(True)
        work_input_layout.addWidget(self.pomodoro_work_input)
        # Label next to the input box
        self.pomodoro_work_input_label = QLabel("set work time ")
        self.pomodoro_work_input_label.setStyleSheet(
            f"font-size: 16px; font-weight: bold; color: {PASTEL_OCEANBAY_HEX}")
        work_input_layout.addWidget(self.pomodoro_work_input_label)
        layout.addLayout(work_input_layout)
        # Input field for pomodoro #2
        break_input_layout = QHBoxLayout()
        self.pomodoro_break_input = QLineEdit()
        self.pomodoro_break_input.setText("00:05:00")
        self.pomodoro_break_input.setStyleSheet(f"font-size: 16px; padding: 5px; color: {PASTEL_OCEANBAY_HEX};\
            border: 1px solid {PASTEL_OCEANBAY_HEX};")
        self.pomodoro_break_input.setVisible(True)
        break_input_layout.addWidget(self.pomodoro_break_input)
        # Label next to the input box
        self.pomodoro_break_input_label = QLabel("set break time")
        self.pomodoro_break_input_label.setStyleSheet(
            f"font-size: 16px; font-weight: bold; color: {PASTEL_OCEANBAY_HEX}")
        break_input_layout.addWidget(self.pomodoro_break_input_label)
        layout.addLayout(break_input_layout)
        
        # Input field for timer
        self.timer_input_field = QLineEdit()
        self.timer_input_field.setText("00:50:00")
        self.timer_input_field.setStyleSheet(f"font-size: 16px; padding: 5px; color: {PASTEL_OCEANBAY_HEX};\
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

    def validate_timer_input(self, input_text):
        # Regular expression for hh:mm:ss format
        regex = r"^\d{1,2}:[0-5]\d:[0-5]\d$"

        if not re.match(regex, input_text):
            self.show_error("Invalid Time Format Use hh:mm:ss.")
            return False

        # Split the time into hours, minutes, and seconds
        hours, minutes, seconds = map(int, input_text.split(':'))
        total_seconds = hours * 3600 + minutes * 60 + seconds

        # Check if the time is between 1 minute and 24 hours
        if total_seconds < 60:
            self.show_error("Time must be at least 1 minute.")
            return False
        elif total_seconds > 24 * 3600:
            self.show_error("Time cannot exceed 24 hours.")
            return False
        return True
    
    def show_error(self, text):
        """Show error on gui."""
        self.input_error_label.setText(text)
        self.input_error_label.setVisible(True)
    
    def start_time(self):
        """Start the stopwatch or timer."""
        self.input_error_label.setVisible(False)  # reset error on gui
        if self.time_manager.selected_timer == "stopwatch":
            self.time_manager.start_stopwatch()
        elif self.time_manager.selected_timer == "pomodoro":
            if self.validate_timer_input(self.pomodoro_work_input.text()) and \
               self.validate_timer_input(self.pomodoro_break_input.text()):
                # Parse the input field for the work and break timer duration
                work_text = self.pomodoro_work_input.text()
                break_text = self.pomodoro_break_input.text()
                wh, wm, ws = map(int, work_text.split(":"))
                bh, bm, bs = map(int, break_text.split(":"))
                self.time_manager.set_pomodoro_time(wh, wm, ws, bh, bm, bs)
                self.time_manager.start_pomodoro()
        elif self.time_manager.selected_timer == "timer":
            if self.validate_timer_input(self.timer_input_field.text()):
                # Parse the input field for timer duration
                time_text = self.timer_input_field.text()
                h, m, s = map(int, time_text.split(":"))
                self.time_manager.set_timer(h, m, s)
                self.time_manager.start_timer()

    def pause_time(self):
        """Pause or resume the timer/stopwatch."""
        if self.time_manager.mode == "running":
            self.time_manager.pause()  # Pause the timer/stopwatch
        elif self.time_manager.mode == "paused":
            self.time_manager.resume()  # Resume the timer/stopwatch

    def stop_time(self):
        self.time_manager.stop()
    
    def toggle_mode(self):
        """Switch between Pomodoro-Timer, Timer and Stopwatch."""
        self.input_error_label.setVisible(False)  # reset error on gui
        if self.time_manager.selected_timer == "pomodoro":
            self.time_manager.set_timer_mode("timer")
        elif self.time_manager.selected_timer == "timer":
            self.time_manager.set_timer_mode("stopwatch")
        elif self.time_manager.selected_timer == "stopwatch":
            self.time_manager.set_timer_mode("pomodoro")
        
    def update_gui(self):
        """Update the displayed time on the GUI."""
        self.timer_mode_label.setText(self.time_manager.selected_timer.upper())
        
        # Point Overview
        self.circle_av.update_widget(self.point_system.get_points()[1])
        self.circle_tot.update_widget(self.point_system.get_points()[0])
        
        # Time Management
        if self.time_manager.selected_timer == "pomodoro":
            self.mode_toggle_button.setText("Switch to Timer")
            self.timer_input_field.setVisible(False)
            self.pomodoro_work_input.setVisible(True)
            self.pomodoro_work_input_label.setVisible(True)
            self.pomodoro_break_input.setVisible(True)
            self.pomodoro_break_input_label.setVisible(True)
            if self.time_manager.mode == "running":
                phase = "Work" if self.time_manager.is_work_phase else "Break"
                self.clock_label.setText(f"{phase}: {self.time_manager.target_time.toString('hh:mm:ss')}")
        if self.time_manager.selected_timer == "timer":
            self.mode_toggle_button.setText("Switch to Stopwatch")
            self.timer_input_field.setVisible(True)
            self.pomodoro_work_input.setVisible(False)
            self.pomodoro_work_input_label.setVisible(False)
            self.pomodoro_break_input.setVisible(False)
            self.pomodoro_break_input_label.setVisible(False)
            if self.time_manager.mode == "running":
                self.clock_label.setText(self.time_manager.target_time.toString("hh:mm:ss"))
        elif self.time_manager.selected_timer == "stopwatch":
            self.mode_toggle_button.setText("Switch to Pomodoro")
            self.timer_input_field.setVisible(False)
            self.pomodoro_work_input.setVisible(False)
            self.pomodoro_work_input_label.setVisible(False)
            self.pomodoro_break_input.setVisible(False)
            self.pomodoro_break_input_label.setVisible(False)
            if self.time_manager.mode == "running":
                self.clock_label.setText(self.time_manager.elapsed_time.toString("hh:mm:ss"))
        
        if self.time_manager.mode == "running":
            self.pause_button.setText("Pause")
        elif self.time_manager.mode == "paused":
            self.pause_button.setText("Resume")
        elif self.time_manager.mode == "stopped":
            self.clock_label.setText("00:00:00")
            self.pause_button.setText("-")
            if self.time_manager.timer_elapsed:
                # TODO insert timer-elapsed-action here
                pass

    def sync_variables(self):
        # get counter of productiv minutes from timemanagement
        self.point_system.add_points(self.time_manager.productiv_minutes//1)
        self.time_manager.productiv_minutes = 0  # reset counter after reading

    def update_app(self):
        self.sync_variables()
        self.update_gui()
        self.save_data()
        
    def save_data(self):
        total_points, available_points = self.point_system.get_points()
        pomodoro_work_input = self.pomodoro_work_input.text()
        pomodoro_break_input = self.pomodoro_break_input.text()
        timer_input_field = self.timer_input_field.text()
        text_box = self.text_box.toPlainText()
        data = {
            "total_points": total_points,
            "available_points": available_points,
            "pomodoro_work_input": pomodoro_work_input,
            "pomodoro_break_input": pomodoro_break_input,
            "timer_input_field": timer_input_field,
            "text_box": text_box
            }
        with open(self.data_filename, "w") as file:
            json.dump(data, file)

    def load_data(self):
        if not os.path.exists(self.data_filename):
            self.save_data()
        with open(self.data_filename, "r") as file:
            data = json.load(file)
            self.point_system.set_points(data["total_points"], data["available_points"])
            self.pomodoro_work_input.setText(data["pomodoro_work_input"])
            self.pomodoro_break_input.setText(data["pomodoro_break_input"])
            self.timer_input_field.setText(data["timer_input_field"])
            self.text_box.setPlainText(data["text_box"])