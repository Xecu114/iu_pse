import json
import os
import re
import sqlite3
import subprocess
from PyQt6.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, \
    QLineEdit, QPlainTextEdit, QComboBox, QDateEdit
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QPainter, QColor, QPaintEvent, QBrush
from PyQt6.QtCharts import QChart, QChartView, QPieSeries
from src.timemanagement import TimeManagement
from src.pointssystem import PointsSystem
from src.projectmanagement import ProjectManagement
# from main_vg import main
from src.constants import WIDTH, HEIGHT, \
    COLOR_BEIGE_HEX, COLOR_OCEANBAY_HEX, COLOR_OCEANBAY_RGB, COLOR_ROSE_RGB, COLOR_ROSE_HEX, COLOR_RED_HEX, \
    IMGDIR_GUI_FLOWER_MEADOW, COLOR_SOFTCORAL_HEX, JSON_FILE


class CircleWithNumber(QWidget):
    """
    Create a custom QWidget that displays a circle with a number centered inside.
    
    Parameters:
        number (int): The number to display inside the circle.
        w (int): The width of the widget.
        h (int): The height of the widget.
        color_circle (tuple): A tuple of three integers representing the RGB color of the circle.
        color_number (tuple): A tuple of three integers representing the RGB color of the number.
        parent (QWidget, optional): The parent widget. Defaults to None.
    
    Example:
        circle_widget = CircleWithNumber(
            number=5,
            w=100,
            h=100,
            color_circle=(255, 0, 0),
            color_number=(255, 255, 255)
        )
    """
    def __init__(self, number, w, h, color_circle: tuple, color_number: tuple, parent=None):
        super().__init__(parent)
        self.number = number
        self.w = w
        self.h = h
        self.color_circle = color_circle
        self.color_number = color_number
        self.setFixedSize(w, h)

    def paintEvent(self, event: QPaintEvent):   # type: ignore
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw circle
        r, g, b = self.color_circle
        painter.setBrush(QColor(r, g, b))
        painter.setPen(QColor(r, g, b))
        painter.drawEllipse((self.w//10), (self.h//10), (self.w-(self.w//5)), (self.h-(self.h//5)))

        # Draw number in the circle
        r, g, b = self.color_number
        painter.setPen(QColor(r, g, b))
        font = painter.font()
        font.setBold(True)
        font.setPointSize(14)
        painter.setFont(font)
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, str(self.number))
    
    def update_widget(self, new_number):
        self.number = new_number
        self.update()


class ProjectsOverviewPieChart:
    """
    Create and manage a pie chart that provides an overview of projects and their associated data.

    Attributes:
        chart (QChart): The main chart object.
        series (QPieSeries): The pie series object representing the data in the chart.
        chart_view (QChartView): The view for rendering the chart.
    
    Example:
        pie_chart = ProjectsOverviewPieChart()
        pie_chart.update_data(
            project_names=["Project A", "Project B"],
            time_tracked_list=[10, 20]
        )
    """
    def __init__(self):
        # Initialisierung der Diagrammkomponenten
        self.chart = QChart()
        self.chart.setTitle("")
        self.chart.setTheme(QChart.ChartTheme.ChartThemeBrownSand)
        self.chart.setBackgroundBrush(QBrush(QColor(COLOR_BEIGE_HEX)))

        self.series = QPieSeries()
        self.series.setPieSize(1)
        self.series.setHoleSize(0.5)

        self.chart.addSeries(self.series)

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.chart_view.setMinimumSize(WIDTH // 4, HEIGHT // 3)

        # self.layout = QVBoxLayout()  # Erstelle einen Layout-Container
        # self.layout.addWidget(self.chart_view)

    def update_data(self, project_names, time_tracked_list):
        """
        Update the pie chart with the latest project data.

        Parameters:
            project_names (list of str): A list of project names to be displayed on the pie chart.
            time_tracked_list (list of float or int): A list of time tracked values corresponding to each project.
        
        Example:
            pie_chart.update_data(
                project_names=["Project A", "Project B"],
                time_tracked_list=[10, 20]
            )
        """

        self.series.clear()  # Vorhandene Daten entfernen
        for i, name in enumerate(project_names):
            self.series.append(name, time_tracked_list[i])


class MainSession(QMainWindow):
    """
    Main application window, managing the PYQt6 user interface,
    data handling and periodic updates.

    Attributes:
        minute_counter (int): Counter for minutes elapsed.
        point_system (PointsSystem): Instance of the points management system.
        time_manager (TimeManagement): Instance of the time management system.
        conn (sqlite3.Connection): SQLite database connection.
        current_project (ProjectManagement): Instance of the project management system.
    
    Example:
        connection = sqlite3.connect("database.db")
        app = QApplication(sys.argv)
        main_session = MainSession(connection)
        main_session.show()
        sys.exit(app.exec_())
    """

    def __init__(self, connection: sqlite3.Connection):
        super().__init__()
        self.minute_counter = 0  # init local minute counter
        
        # Create class instances
        self.point_system = PointsSystem()
        self.time_manager = TimeManagement()
        self.conn = connection
        self.current_project = ProjectManagement(self.conn)
        
        # UI setup
        self.setWindowTitle("ProductivityGarden")
        self.setGeometry(100, 100, WIDTH, HEIGHT)
        self.setup_gui()
        
        # get user data from json
        self.load_json_data()
        
        # initial component updates
        self.update_high_frequency()
        self.update_low_frequency()
        
        # Timer for updating various components of the application at different frequencies
        self.update_timer_high_frequency = QTimer(self)
        self.update_timer_high_frequency.timeout.connect(self.update_high_frequency)
        self.update_timer_high_frequency.start(250)
        
        self.update_timer_low_frequency = QTimer(self)
        self.update_timer_low_frequency.timeout.connect(self.update_low_frequency)
        self.update_timer_low_frequency.start(2000)

    def setup_gui(self):
        """Setup the main UI layout and widgets."""
        # Main layout with 3 columns
        main_layout = QHBoxLayout()

        # Add first column
        first_column_container = self.gui_create_first_column()
        main_layout.addWidget(first_column_container, stretch=1)

        # Separator line
        separator1 = self.gui_create_separator()
        main_layout.addWidget(separator1)

        # Add second column
        second_column_container = self.gui_create_second_column()
        main_layout.addWidget(second_column_container, stretch=1)

        # Separator line
        separator2 = self.gui_create_separator()
        main_layout.addWidget(separator2)

        # Add third column
        third_column_container = self.gui_create_third_column()
        main_layout.addWidget(third_column_container, stretch=1)

        # Set central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        central_widget.setStyleSheet(f"background-color: {COLOR_BEIGE_HEX};")
        self.setCentralWidget(central_widget)

    def gui_create_first_column(self):
        """
        Create the first column with the points overview,
        "to the gardens" navigation button and an image of a meadow
        """
        layout = QVBoxLayout()
        
        # create point overview
        self.gui_draw_point_overview(layout)
        
        # create button to the gardens
        # button = self.gui_create_button("TO THE GARDENS", main)
        button_gardens = self.gui_create_button("TO THE GARDENS", COLOR_OCEANBAY_HEX, self.handle_open_virtualgardens)
        layout.addWidget(button_gardens)
        
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
        container.setStyleSheet(f"background-color: {COLOR_BEIGE_HEX};")
        return container

    def gui_create_second_column(self):
        """Create the second column with a clock label and input field."""
        layout = QVBoxLayout()

        self.gui_draw_time_management_area(layout)

        # Add spacer to push content to the top
        layout.addStretch()
        
        # Input field for text
        self.text_box = QPlainTextEdit()
        self.text_box.setPlaceholderText("Enter your text here...")
        self.text_box.setStyleSheet(f"font-size: 16px; padding: 5px; color: {COLOR_OCEANBAY_HEX};\
            border: 1px solid {COLOR_OCEANBAY_HEX};")
        font_metrics = self.text_box.fontMetrics()
        line_height = font_metrics.lineSpacing()
        self.text_box.setFixedHeight(8 * line_height + 10)
        layout.addWidget(self.text_box)

        container = QWidget()
        container.setLayout(layout)
        container.setStyleSheet(f"background-color: {COLOR_BEIGE_HEX};")
        return container

    def gui_create_third_column(self):
        """Create the third column with a projects label."""
        layout = QVBoxLayout()

        # Create project overview
        self.gui_draw_project_overview(layout)
        
        # Add spacer to push content to the top
        layout.addStretch()

        container = QWidget()
        container.setLayout(layout)
        container.setStyleSheet(f"background-color: {COLOR_BEIGE_HEX};")
        return container

    def gui_create_separator(self):
        """Create a separator line."""
        separator = QWidget()
        separator.setFixedWidth(1)
        separator.setStyleSheet(f"background-color: {COLOR_OCEANBAY_HEX};")
        return separator

    def gui_create_button(self, text, main_color: str, callback=None):
        """ Method helps create a button, so that each button has a similar style """
        button = QPushButton(text)
        button.setStyleSheet(f"""
            QPushButton{{
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
                color: {main_color};
                border: 1px solid {main_color};
                background-color: transparent;
            }}
            QPushButton:hover {{
                background-color: {COLOR_ROSE_HEX};
                color: {main_color};
            }}
            QPushButton:pressed {{
                background-color: {main_color};
                color: {main_color};
            }}
        """)
        if callback is not None:
            button.clicked.connect(callback)
        return button

    def gui_draw_point_overview(self, layout : QVBoxLayout):
        """ init and draw the whole "point overview" area """
        # Text Element
        points_label = QLabel("POINTS")
        points_label.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {COLOR_OCEANBAY_HEX}")
        points_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(points_label)

        # Horizontal layout for circle and text
        circle_and_text_layout_av = QHBoxLayout()
        
        # Circle with number (currently available points)
        self.circle_av = CircleWithNumber(self.point_system.get_points()[1], 60, 60,
                                          COLOR_ROSE_RGB, COLOR_OCEANBAY_RGB)
        circle_and_text_layout_av.addWidget(self.circle_av)
        
        # Label next to the circle
        circle_text_label = QLabel("available")
        circle_text_label.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {COLOR_OCEANBAY_HEX}")
        circle_and_text_layout_av.addWidget(circle_text_label)
        
        # Add the horizontal layout to the main layout
        layout.addLayout(circle_and_text_layout_av)
        
        # Horizontal layout for circle and text
        circle_and_text_layout_tot = QHBoxLayout()
        
        # Circle with number (total points collected)
        self.circle_tot = CircleWithNumber(self.point_system.get_points()[0], 60, 60,
                                           COLOR_ROSE_RGB, COLOR_OCEANBAY_RGB)
        circle_and_text_layout_tot.addWidget(self.circle_tot)
        
        # Label next to the circle
        circle_text_label = QLabel("total")
        circle_text_label.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {COLOR_OCEANBAY_HEX}")
        circle_and_text_layout_tot.addWidget(circle_text_label)
        
        # Add the horizontal layout to the main layout
        layout.addLayout(circle_and_text_layout_tot)

    def gui_draw_time_management_area(self, layout : QVBoxLayout):
        """ init and draw the whole "time management" area """
        # Display current timer mode
        self.timer_mode_label = QLabel(self.time_manager.selected_timer.upper())
        self.timer_mode_label.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {COLOR_OCEANBAY_HEX}")
        self.timer_mode_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.timer_mode_label)
        
        # Digital clock
        self.clock_label = QLabel("00:00:00")
        self.clock_label.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {COLOR_OCEANBAY_HEX}")
        self.clock_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.clock_label)
        
        # Buttons to control the various time functions
        buttons_layout = QHBoxLayout()
        start_button = self.gui_create_button("Start", COLOR_OCEANBAY_HEX, self.handle_start_time)
        buttons_layout.addWidget(start_button)

        self.pause_button = self.gui_create_button("-", COLOR_OCEANBAY_HEX, self.handle_pause_time)
        buttons_layout.addWidget(self.pause_button)
        
        stop_button = self.gui_create_button("Stop", COLOR_OCEANBAY_HEX, self.handle_stop_time)
        buttons_layout.addWidget(stop_button)
        
        layout.addLayout(buttons_layout)
        
        # Input field for pomodoro #1
        work_input_layout = QHBoxLayout()
        self.pomodoro_work_input = QLineEdit()
        self.pomodoro_work_input.setText("00:25:00")
        self.pomodoro_work_input.setStyleSheet(f"font-size: 16px; font-weight: bold; padding: 5px; \
            color: {COLOR_OCEANBAY_HEX};\
            border: 2px solid {COLOR_SOFTCORAL_HEX};")
        self.pomodoro_work_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pomodoro_work_input.setVisible(True)
        work_input_layout.addWidget(self.pomodoro_work_input)
        work_input_layout.addStretch()
        # Label next to the input box
        self.pomodoro_work_input_label = QLabel("set work time ")
        self.pomodoro_work_input_label.setStyleSheet(
            f"font-size: 16px; font-weight: bold; color: {COLOR_OCEANBAY_HEX}")
        work_input_layout.addWidget(self.pomodoro_work_input_label)
        layout.addLayout(work_input_layout)
        # Input field for pomodoro #2
        break_input_layout = QHBoxLayout()
        self.pomodoro_break_input = QLineEdit()
        self.pomodoro_break_input.setText("00:05:00")
        self.pomodoro_break_input.setStyleSheet(f"font-size: 16px; font-weight: bold; padding: 5px; \
            color: {COLOR_OCEANBAY_HEX};\
            border: 2px solid {COLOR_SOFTCORAL_HEX};")
        self.pomodoro_break_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pomodoro_break_input.setVisible(True)
        break_input_layout.addWidget(self.pomodoro_break_input)
        break_input_layout.addStretch()
        # Label next to the input box
        self.pomodoro_break_input_label = QLabel("set break time")
        self.pomodoro_break_input_label.setStyleSheet(
            f"font-size: 16px; font-weight: bold; color: {COLOR_OCEANBAY_HEX}")
        break_input_layout.addWidget(self.pomodoro_break_input_label)
        layout.addLayout(break_input_layout)
        
        # Input field for timer
        self.timer_input_field = QLineEdit()
        self.timer_input_field.setText("00:50:00")
        self.timer_input_field.setStyleSheet(f"font-size: 16px; font-weight: bold; padding: 5px; \
            color: {COLOR_OCEANBAY_HEX};\
            border: 2px solid {COLOR_SOFTCORAL_HEX};")
        self.timer_input_field.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_input_field.setVisible(False)
        layout.addWidget(self.timer_input_field)
        
        # Text element for errors
        self.input_error_label = QLabel("")
        self.input_error_label.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {COLOR_RED_HEX}")
        self.input_error_label.setVisible(False)
        layout.addWidget(self.input_error_label)
        
        # Toggle button for stopwatch/timer
        self.mode_toggle_button = self.gui_create_button("Switch to Timer", COLOR_OCEANBAY_HEX, self.handle_toggle_mode)
        layout.addWidget(self.mode_toggle_button)

    def gui_draw_project_overview(self, layout : QVBoxLayout):
        """ init and draw the whole "projects" area including the edit area """
        layout = layout
        
        # Text "Projects"
        projects_label = QLabel("PROJECTS")
        projects_label.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {COLOR_OCEANBAY_HEX}")
        projects_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(projects_label)
        
        # Drop-Down menu for projects
        self.projects_dropdown = QComboBox()
        self.projects_dropdown.setStyleSheet(f"font-size: 16px; font-weight: bold; padding: 5px; \
            color: {COLOR_OCEANBAY_HEX}; border: 1px solid {COLOR_OCEANBAY_HEX};")
        self.projects_dropdown.addItems(ProjectManagement.get_projects_name_list(self.conn))
        self.projects_dropdown.currentIndexChanged.connect(self.handle_select_project_from_dropdown)
        layout.addWidget(self.projects_dropdown)
        
        # Button to add a new project and one to delete the selected project
        buttons_layout = QHBoxLayout()
        add_button = self.gui_create_button("Add", COLOR_OCEANBAY_HEX, self.handle_add_new_project)
        buttons_layout.addWidget(add_button)
        del_button = self.gui_create_button("Delete", COLOR_OCEANBAY_HEX, self.handle_delete_project)
        buttons_layout.addWidget(del_button)
        layout.addLayout(buttons_layout)
        
        # Add edit info area
        self.gui_draw_project_info_area(layout)
        
        # Tracked time for the selected project (Circle with number)
        circle_and_text_layout = QHBoxLayout()
        self.circle_project_time = CircleWithNumber(self.current_project.get_time(), 60, 60,
                                                    COLOR_ROSE_RGB, COLOR_OCEANBAY_RGB)
        circle_and_text_layout.addWidget(self.circle_project_time)
        # Label next to the circle
        circle_text_label = QLabel("time tracked (min)")
        circle_text_label.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {COLOR_OCEANBAY_HEX}")
        circle_and_text_layout.addWidget(circle_text_label)
        # Add the horizontal layout to the main layout
        layout.addLayout(circle_and_text_layout)
        
        # Add pie chart for project time distribution
        self.projects_pie_chart = ProjectsOverviewPieChart()
        layout.addWidget(self.projects_pie_chart.chart_view)
        
        # add strecht to push content to the top and foloowing item to the bottom
        layout.addStretch()
        
        # Create items to manually add time
        layout_add_time = QHBoxLayout()
        # Button next to the input field
        pr_add_time_button = self.gui_create_button("Add time", COLOR_OCEANBAY_HEX, self.handle_add_time_to_project)
        # Input field
        self.pr_add_time = QLineEdit()
        self.pr_add_time.setText("")
        self.pr_add_time.setPlaceholderText("Add x minutes to the current project")
        self.pr_add_time.setStyleSheet(f"font-size: 14px; padding: 5px; font-weight: bold; \
            color: {COLOR_OCEANBAY_HEX}; border: 2px solid {COLOR_SOFTCORAL_HEX};")
        self.pr_add_time.setVisible(True)
        # Add to layout
        layout_add_time.addWidget(pr_add_time_button)
        layout_add_time.addWidget(self.pr_add_time)
        layout.addLayout(layout_add_time)

    def gui_draw_project_info_area(self, layout : QVBoxLayout):
        """ add project info (editable) area to the project overview with this method """
        # build layout for input fields
        inputh_layout = QHBoxLayout()
        inputv1_layout = QVBoxLayout()
        inputv2_layout = QVBoxLayout()
        # Label next to the input box
        self.pr_name_input_label = QLabel("Name")
        self.pr_name_input_label.setStyleSheet(
            f"font-size: 16px; font-weight: bold; color: {COLOR_OCEANBAY_HEX}")
        # Input field for name of the project
        self.pr_name_input = QLineEdit()
        self.pr_name_input.setText(self.current_project.name)
        self.pr_name_input.setPlaceholderText("Physics")
        self.pr_name_input.setStyleSheet(f"font-size: 14px; padding: 5px; font-weight: bold; \
            color: {COLOR_OCEANBAY_HEX}; border: 2px solid {COLOR_SOFTCORAL_HEX};")
        self.pr_name_input.setVisible(True)
        inputv1_layout.addWidget(self.pr_name_input_label)
        inputv2_layout.addWidget(self.pr_name_input)
        # connect to update dropdown menu
        self.pr_name_input.textChanged.connect(self.handle_update_project_name)
        
        # Label next to the input box
        self.pr_description_input_label = QLabel("Description")
        self.pr_description_input_label.setStyleSheet(
            f"font-size: 16px; font-weight: bold; color: {COLOR_OCEANBAY_HEX}")
        # Input field for description of the project
        self.pr_description_input = QLineEdit()
        self.pr_description_input.setText(self.current_project.description)
        self.pr_description_input.setPlaceholderText("Physics class")
        self.pr_description_input.setStyleSheet(f"font-size: 14px; padding: 5px; font-weight: bold; \
            color: {COLOR_OCEANBAY_HEX}; border: 2px solid {COLOR_SOFTCORAL_HEX};")
        self.pr_description_input.setVisible(True)
        inputv1_layout.addWidget(self.pr_description_input_label)
        inputv2_layout.addWidget(self.pr_description_input)
        
        # Label next to the input box
        self.pr_type_input_label = QLabel("Category")
        self.pr_type_input_label.setStyleSheet(
            f"font-size: 16px; font-weight: bold; color: {COLOR_OCEANBAY_HEX}")
        # Input field for type of the project
        self.pr_type_input = QLineEdit()
        self.pr_type_input.setText(self.current_project.type)
        self.pr_type_input.setPlaceholderText("Study")
        self.pr_type_input.setStyleSheet(f"font-size: 14px; padding: 5px; font-weight: bold; \
            color: {COLOR_OCEANBAY_HEX}; border: 2px solid {COLOR_SOFTCORAL_HEX};")
        self.pr_type_input.setVisible(True)
        inputv1_layout.addWidget(self.pr_type_input_label)
        inputv2_layout.addWidget(self.pr_type_input)
        inputh_layout.addLayout(inputv1_layout)
        inputh_layout.addLayout(inputv2_layout)
        layout.addLayout(inputh_layout)
        
        # Date input for the project start date
        start_date_layout = QHBoxLayout()
        self.project_start_date_label = QLabel("Start Date")
        self.project_start_date_label.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {COLOR_OCEANBAY_HEX}")
        self.project_start_date_edit = QDateEdit(self)
        self.project_start_date_edit.setCalendarPopup(True)  # Enable the calendar popup
        self.project_start_date_edit.setDate(self.current_project.start_date)  # Set default date
        self.project_start_date_edit.setStyleSheet(f"font-size: 14px; padding: 5px; font-weight: bold;\
            color: {COLOR_OCEANBAY_HEX}; border: 2px solid {COLOR_SOFTCORAL_HEX};")
        self.project_start_date_edit.dateChanged.connect(self.handle_start_date_changed)  # call ... if date changes
        start_date_layout.addWidget(self.project_start_date_label)
        start_date_layout.addWidget(self.project_start_date_edit)
        layout.addLayout(start_date_layout)
        
        # Date input for the project end date
        end_date_layout = QHBoxLayout()
        self.project_end_date_label = QLabel("End Date")
        self.project_end_date_label.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {COLOR_OCEANBAY_HEX}")
        self.project_end_date_edit = QDateEdit(self)
        self.project_end_date_edit.setCalendarPopup(True)  # Enable the calendar popup
        self.project_end_date_edit.setMinimumDate(self.project_start_date_edit.date())  # Set minimum date
        self.project_end_date_edit.setDate(self.current_project.end_date)  # Set default date
        self.project_end_date_edit.setStyleSheet(f"font-size: 14px; padding: 5px; font-weight: bold;\
            color: {COLOR_OCEANBAY_HEX}; border: 2px solid {COLOR_SOFTCORAL_HEX};")
        self.project_end_date_edit.dateChanged.connect(self.handle_end_date_changed)  # call ... if date changes
        end_date_layout.addWidget(self.project_end_date_label)
        end_date_layout.addWidget(self.project_end_date_edit)
        layout.addLayout(end_date_layout)
        
    def gui_show_error(self, text):
        """Show error on gui."""
        self.input_error_label.setText(text)
        self.input_error_label.setVisible(True)
    
    def handle_start_time(self):
        """Handle a click on the "Start" button."""
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

    def handle_pause_time(self):
        """Handle a click on the "Pause" button."""
        if self.time_manager.mode == "running":
            self.time_manager.pause()  # Pause the timer/stopwatch
        elif self.time_manager.mode == "paused":
            self.time_manager.resume()  # Resume the timer/stopwatch

    def handle_stop_time(self):
        """Handle a click on the "Stop" button."""
        self.time_manager.stop()
    
    def handle_toggle_mode(self):
        """
        Handle a click on "Switch to ..." button.
        Switches between Pomodoro-Timer, Timer and Stopwatch.
        """
        self.input_error_label.setVisible(False)  # reset error on gui
        if self.time_manager.selected_timer == "pomodoro":
            self.time_manager.set_timer_mode("timer")
        elif self.time_manager.selected_timer == "timer":
            self.time_manager.set_timer_mode("stopwatch")
        elif self.time_manager.selected_timer == "stopwatch":
            self.time_manager.set_timer_mode("pomodoro")
    
    def handle_add_new_project(self):
        """Handle a click on the "Add" new project button."""
        self.current_project.add_project()
        self.projects_dropdown.addItem(self.current_project.name)
        self.projects_dropdown.setCurrentIndex(self.projects_dropdown.count()-1)
        
    def handle_delete_project(self):
        """Handle a click on the "Delete" project button."""
        self.current_project.delete_project()
        self.projects_dropdown.removeItem(self.projects_dropdown.currentIndex())
        self.projects_dropdown.setCurrentIndex(0)
    
    def handle_select_project_from_dropdown(self):
        """Handle a click on another project in the projects dropdown menu."""
        self.current_project.id = ProjectManagement.get_id_by_name(self.projects_dropdown.currentText(), self.conn)
        self.current_project.load_data_from_sql()
        self.pr_name_input.setText(self.current_project.name)
        self.pr_description_input.setText(self.current_project.description)
        self.pr_type_input.setText(self.current_project.type)
        self.project_start_date_edit.setDate(self.current_project.start_date)
        self.project_end_date_edit.setDate(self.current_project.end_date)

    def handle_update_project_name(self):
        """
        Validate the user input for the project name and
        update the projects dropdown menu
        """
        text = self.pr_name_input.text()
        if len(text) > 40:
            # Truncate the text to 40 characters
            self.pr_name_input.setText(text[:40])
            self.pr_name_input.setCursorPosition(40)  # Set cursor to the end
        elif not text.strip():
            # Prevent empty input
            self.pr_name_input.setStyleSheet("font-size: 14px; padding: 5px; font-weight: bold; \
                color: red; border: 2px solid red;")
        else:
            # Restore original style if valid
            self.pr_name_input.setStyleSheet(f"font-size: 14px; padding: 5px; font-weight: bold; \
                color: {COLOR_OCEANBAY_HEX}; border: 2px solid {COLOR_SOFTCORAL_HEX};")
        self.projects_dropdown.setItemText(self.projects_dropdown.currentIndex(), self.pr_name_input.text())
 
    def handle_add_time_to_project(self):
        """Handle the manual add time to the current project input field"""
        self.input_error_label.setVisible(False)
        input = self.pr_add_time.text()
        self.pr_add_time.setText("")
        if input.isdigit():
            number = int(input)
            if 1 <= number <= 999:
                self.time_manager.productiv_minutes += number
            else:
                self.gui_show_error("Number must be between 1 and 999")
                print("Number must be between 1 and 999")  # debug message
        else:
            self.gui_show_error("Input must be a number")
            print(f"Input must be a number... input: {input}")  # debug message

    def handle_start_date_changed(self, new_date):
        """
        Is called as soon as the start date changes.
        Ensures that the end date >= start date.
        """
        self.project_end_date_edit.setMinimumDate(new_date)
        
        # If end date is earlier then new start date, set it to the start date
        if self.project_end_date_edit.date() < new_date:
            self.project_end_date_edit.setDate(new_date)

    def handle_end_date_changed(self, new_date):
        """
        Is called as soon as the end date changes.
        Ensures that it is not before the start date.
        """
        # If new end date is earlier then start date, set it to the start date
        if new_date < self.project_start_date_edit.date():
            self.project_end_date_edit.setDate(self.project_start_date_edit.date())
    
    def handle_open_virtualgardens(self):
        """Start virtualgardens.py and close this app."""
        self.close()
        subprocess.Popen(["python", "src\\virtualgardens.py"])
    
    def update_gui(self):
        """
        Update the GUI frequently.
        Only updates the time management area.
        Other areas are handled on demand or less frequent.
        """
        
        # update time management area -> handle switch between pomodoro, timer and stopwatch
        self.timer_mode_label.setText(self.time_manager.selected_timer.upper())
        if self.time_manager.selected_timer == "pomodoro":
            self.mode_toggle_button.setText("Switch to Timer")
            self.timer_input_field.setVisible(False)
            self.pomodoro_work_input.setVisible(True)
            self.pomodoro_work_input_label.setVisible(True)
            self.pomodoro_break_input.setVisible(True)
            self.pomodoro_break_input_label.setVisible(True)
            if self.time_manager.mode == "running":
                phase = "Work" if self.time_manager.is_work_phase else "Break"
                self.clock_label.setText(f"{phase}: {self.time_manager.remaining_time.toString('hh:mm:ss')}")
        if self.time_manager.selected_timer == "timer":
            self.mode_toggle_button.setText("Switch to Stopwatch")
            self.timer_input_field.setVisible(True)
            self.pomodoro_work_input.setVisible(False)
            self.pomodoro_work_input_label.setVisible(False)
            self.pomodoro_break_input.setVisible(False)
            self.pomodoro_break_input_label.setVisible(False)
            if self.time_manager.mode == "running":
                self.clock_label.setText(self.time_manager.remaining_time.toString("hh:mm:ss"))
        elif self.time_manager.selected_timer == "stopwatch":
            self.mode_toggle_button.setText("Switch to Pomodoro")
            self.timer_input_field.setVisible(False)
            self.pomodoro_work_input.setVisible(False)
            self.pomodoro_work_input_label.setVisible(False)
            self.pomodoro_break_input.setVisible(False)
            self.pomodoro_break_input_label.setVisible(False)
            if self.time_manager.mode == "running":
                self.clock_label.setText(self.time_manager.elapsed_time.toString("hh:mm:ss"))
        
        # update "Pause"/"Resume" button depending on current state
        if self.time_manager.mode == "running":
            self.pause_button.setText("Pause")
        elif self.time_manager.mode == "paused":
            self.pause_button.setText("Resume")
        elif self.time_manager.mode == "stopped":
            self.clock_label.setText("00:00:00")
            self.pause_button.setText("-")
    
    def sync_variables(self):
        """Update and synchronize various variables"""
        # get counter of productiv minutes from timemanagement
        # add the time to the local counter
        self.minute_counter += self.time_manager.productiv_minutes
        if self.minute_counter >= 10:  # add points to point system every 10 minutes
            self.point_system.add_points(self.minute_counter//10)
            self.minute_counter = self.minute_counter % 10
        
        # write project data from gui to the backend class
        self.current_project.add_time(self.time_manager.productiv_minutes)
        self.current_project.start_date = self.project_start_date_edit.date()
        self.current_project.end_date = self.project_end_date_edit.date()
        self.current_project.name = self.pr_name_input.text()
        self.current_project.description = self.pr_description_input.text()
        self.current_project.type = self.pr_type_input.text()
        
        self.time_manager.productiv_minutes = 0  # reset counter after reading

    def update_high_frequency(self):
        """Updates components of the application at high frequency (e.g., every 250ms)."""
        self.sync_variables()
        self.update_gui()
    
    def update_low_frequency(self):
        """Updates components of the application at low frequency (e.g., every 2000ms)."""
        # save data
        self.save_json_data()
        self.current_project.update_data_in_sql()
        
        # update Point Overview
        self.circle_av.update_widget(self.point_system.get_points()[1])
        self.circle_tot.update_widget(self.point_system.get_points()[0])
        
        # update Project Overview
        self.circle_project_time.update_widget(self.current_project.get_time())
        self.projects_pie_chart.update_data(
            ProjectManagement.get_projects_name_list(self.conn),
            ProjectManagement.get_projects_time_tracked_list(self.conn))
    
    def save_json_data(self):
        """Save user data to a json file"""
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
        with open(JSON_FILE, "w") as file:
            json.dump(data, file)
        
    def load_json_data(self):
        """Load user data from a json file"""
        if not os.path.exists(JSON_FILE):
            self.save_json_data()  # create file with default values
        else:
            with open(JSON_FILE, "r") as file:
                data = json.load(file)
                self.point_system.set_points(data["total_points"], data["available_points"])
                self.pomodoro_work_input.setText(data["pomodoro_work_input"])
                self.pomodoro_break_input.setText(data["pomodoro_break_input"])
                self.timer_input_field.setText(data["timer_input_field"])
                self.text_box.setPlainText(data["text_box"])

    def validate_timer_input(self, input_text):
        """
        Checks the timer time input field.
        Validates that the input string has the correct format and
        a reasonable value
        """
        # Regular expression for hh:mm:ss format
        regex = r"^\d{1,2}:[0-5]\d:[0-5]\d$"

        if not re.match(regex, input_text):
            self.gui_show_error("Invalid Time Format Use hh:mm:ss.")
            return False

        # Split the time into hours, minutes, and seconds
        hours, minutes, seconds = map(int, input_text.split(':'))
        total_seconds = hours * 3600 + minutes * 60 + seconds

        # Check if the time is between 1 minute and 24 hours
        if total_seconds < 60:
            self.gui_show_error("Time must be at least 1 minute.")
            return False
        elif total_seconds > 24 * 3600:
            self.gui_show_error("Time cannot exceed 24 hours.")
            return False
        return True