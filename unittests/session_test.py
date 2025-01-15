import unittest
import sqlite3
from PyQt6.QtWidgets import QApplication
from src.session import MainSession
from src.constants import WIDTH, HEIGHT
from src.projectmanagement import DB_FILE


class TestMainSession(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    def setUp(self):
        # Set up a test database
        self.conn = sqlite3.connect(DB_FILE)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY,
                name TEXT,
                description TEXT,
                type TEXT,
                time_tracked INTEGER,
                start_date TEXT,
                end_date TEXT,
                status TEXT
            )
        ''')
        self.conn.commit()
        self.cursor.execute('''
            INSERT INTO projects (id, name, description, type, time_tracked, start_date, end_date, status)
            VALUES (1, "Test Project", "Test Description", "Test Type", 60, "2023-01-01", "2023-01-01", "active")
        ''')
        self.conn.commit()
        self.main_session = MainSession(self.conn)

    def tearDown(self):
        # Clean up the test database
        self.cursor.execute('DROP TABLE IF EXISTS projects')
        self.conn.commit()
        self.conn.close()
    
    def test_initial_ui_setup(self):
        self.assertEqual(self.main_session.windowTitle(), "ProductivityGarden")
        self.assertEqual(self.main_session.width(), WIDTH)
        self.assertEqual(self.main_session.height(), HEIGHT)

    def test_point_overview_initialization(self):
        total_points, available_points = self.main_session.point_system.get_points()
        self.assertEqual(self.main_session.circle_av.number, available_points)
        self.assertEqual(self.main_session.circle_tot.number, total_points)

    def test_timer_mode_initialization(self):
        self.assertEqual(self.main_session.time_manager.selected_timer, "pomodoro")
        self.assertEqual(self.main_session.clock_label.text(), "00:00:00")

    def test_validate_timer_input(self):
        self.assertTrue(self.main_session.validate_timer_input("01:00:00"))
        self.assertFalse(self.main_session.validate_timer_input("25:00:00"))
        self.assertFalse(self.main_session.validate_timer_input("00:00:59"))
        self.assertFalse(self.main_session.validate_timer_input("invalid"))

    def test_start_time(self):
        self.main_session.pomodoro_work_input.setText("00:25:00")
        self.main_session.pomodoro_break_input.setText("00:05:00")
        self.main_session.handle_start_time()
        self.assertEqual(self.main_session.time_manager.mode, "running")

    def test_pause_time(self):
        self.main_session.handle_start_time()
        self.main_session.handle_pause_time()
        self.assertEqual(self.main_session.time_manager.mode, "paused")
        self.main_session.handle_pause_time()
        self.assertEqual(self.main_session.time_manager.mode, "running")

    def test_stop_time(self):
        self.main_session.handle_start_time()
        self.main_session.handle_stop_time()
        self.assertEqual(self.main_session.time_manager.mode, "stopped")

    def test_toggle_mode(self):
        self.main_session.handle_toggle_mode()
        self.assertEqual(self.main_session.time_manager.selected_timer, "timer")
        self.main_session.handle_toggle_mode()
        self.assertEqual(self.main_session.time_manager.selected_timer, "stopwatch")
        self.main_session.handle_toggle_mode()
        self.assertEqual(self.main_session.time_manager.selected_timer, "pomodoro")

    def test_save_and_load_data(self):
        self.main_session.point_system.set_points(10, 5)
        self.main_session.pomodoro_work_input.setText("00:30:00")
        self.main_session.pomodoro_break_input.setText("00:10:00")
        self.main_session.timer_input_field.setText("01:00:00")
        self.main_session.text_box.setPlainText("Test text")
        self.main_session.save_json_data()

        new_session = MainSession(self.conn)
        new_session.load_json_data()
        total_points, available_points = new_session.point_system.get_points()
        self.assertEqual(total_points, 10)
        self.assertEqual(available_points, 5)
        self.assertEqual(new_session.pomodoro_work_input.text(), "00:30:00")
        self.assertEqual(new_session.pomodoro_break_input.text(), "00:10:00")
        self.assertEqual(new_session.timer_input_field.text(), "01:00:00")
        self.assertEqual(new_session.text_box.toPlainText(), "Test text")
    
    """ not needed - gui tests are covered manually
    
    def test_circle_with_number_initialization(self):
        circle = CircleWithNumber(5, 60, 60, (255, 0, 0), (0, 0, 0))
        self.assertEqual(circle.number, 5)
        self.assertEqual(circle.w, 60)
        self.assertEqual(circle.h, 60)
        self.assertEqual(circle.color_circle, (255, 0, 0))
        self.assertEqual(circle.color_number, (0, 0, 0))

    def test_circle_with_number_update_widget(self):
        circle = CircleWithNumber(5, 60, 60, (255, 0, 0), (0, 0, 0))
        circle.update_widget(10)
        self.assertEqual(circle.number, 10)

    def test_projects_overview_pie_chart_initialization(self):
        pie_chart = ProjectsOverviewPieChart()
        self.assertIsInstance(pie_chart.chart, QChart)
        self.assertIsInstance(pie_chart.series, QPieSeries)
        self.assertIsInstance(pie_chart.chart_view, QChartView)

    def test_projects_overview_pie_chart_update_data(self):
        pie_chart = ProjectsOverviewPieChart()
        pie_chart.update_data(["Project 1", "Project 2"], [30, 70])
        self.assertEqual(len(pie_chart.series.slices()), 2)

    def test_main_session_initialization(self):
        session = MainSession(self.conn)
        self.assertEqual(session.windowTitle(), "ProductivityGarden")
        self.assertEqual(session.width(), WIDTH)
        self.assertEqual(session.height(), HEIGHT)

    def test_main_session_setup_ui(self):
        session = MainSession(self.conn)
        session.setup_ui()
        self.assertIsNotNone(session.centralWidget())

    def test_main_session_create_first_column(self):
        session = MainSession(self.conn)
        first_column = session.create_first_column()
        self.assertIsInstance(first_column, QWidget)

    def test_main_session_create_second_column(self):
        session = MainSession(self.conn)
        second_column = session.create_second_column()
        self.assertIsInstance(second_column, QWidget)

    def test_main_session_create_third_column(self):
        session = MainSession(self.conn)
        third_column = session.create_third_column()
        self.assertIsInstance(third_column, QWidget)

    def test_main_session_create_separator(self):
        session = MainSession(self.conn)
        separator = session.create_separator()
        self.assertIsInstance(separator, QWidget)

    def test_main_session_create_button(self):
        session = MainSession(self.conn)
        button = session.create_button("Test Button", COLOR_OCEANBAY_HEX)
        self.assertIsInstance(button, QPushButton)
        self.assertEqual(button.text(), "Test Button")

    def test_main_session_draw_point_overview(self):
        session = MainSession(self.conn)
        layout = QVBoxLayout()
        session.draw_point_overview(layout)
        self.assertEqual(layout.count(), 2)

    def test_main_session_draw_time_management_area(self):
        session = MainSession(self.conn)
        layout = QVBoxLayout()
        session.draw_time_management_area(layout)
        self.assertEqual(layout.count(), 6)

    def test_main_session_draw_project_overview(self):
        session = MainSession(self.conn)
        layout = QVBoxLayout()
        session.draw_project_overview(layout)
        self.assertEqual(layout.count(), 8)

    def test_main_session_draw_project_info_area(self):
        session = MainSession(self.conn)
        layout = QVBoxLayout()
        session.draw_project_info_area(layout)
        self.assertEqual(layout.count(), 5)

    def test_main_session_show_error(self):
        session = MainSession(self.conn)
        session.show_error("Test Error")
        self.assertEqual(session.input_error_label.text(), "Test Error")
        self.assertTrue(session.input_error_label.isVisible())

    def test_main_session_add_new_project(self):
        session = MainSession(self.conn)
        initial_count = session.projects_dropdown.count()
        session.add_new_project()
        self.assertEqual(session.projects_dropdown.count(), initial_count + 1)

    def test_main_session_del_selected_project(self):
        session = MainSession(self.conn)
        session.add_new_project()
        initial_count = session.projects_dropdown.count()
        session.del_selected_project()
        self.assertEqual(session.projects_dropdown.count(), initial_count - 1)

    def test_main_session_select_project_from_dropdown(self):
        session = MainSession(self.conn)
        session.select_project_from_dropdown()
        self.assertEqual(session.pr_name_input.text(), session.current_project.name)

    def test_main_session_update_projects_dropdown_menu(self):
        session = MainSession(self.conn)
        session.pr_name_input.setText("Updated Project")
        session.update_projects_dropdown_menu()
        self.assertEqual(session.projects_dropdown.currentText(), "Updated Project")

    def test_main_session_add_time_to_project(self):
        session = MainSession(self.conn)
        session.pr_add_time.setText("10")
        session.add_time_to_project()
        self.assertEqual(session.time_manager.productiv_minutes, 10)

    def test_main_session_update_gui(self):
        session = MainSession(self.conn)
        session.update_gui()
        self.assertEqual(session.timer_mode_label.text(), session.time_manager.selected_timer.upper())
    """