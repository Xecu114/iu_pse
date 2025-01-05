import unittest
import sqlite3
from PyQt6.QtWidgets import QApplication
from src.session import MainSession
from common.constants import WIDTH, HEIGHT
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
        self.main_session.start_time()
        self.assertEqual(self.main_session.time_manager.mode, "running")

    def test_pause_time(self):
        self.main_session.start_time()
        self.main_session.pause_time()
        self.assertEqual(self.main_session.time_manager.mode, "paused")
        self.main_session.pause_time()
        self.assertEqual(self.main_session.time_manager.mode, "running")

    def test_stop_time(self):
        self.main_session.start_time()
        self.main_session.stop_time()
        self.assertEqual(self.main_session.time_manager.mode, "stopped")

    def test_toggle_mode(self):
        self.main_session.toggle_mode()
        self.assertEqual(self.main_session.time_manager.selected_timer, "timer")
        self.main_session.toggle_mode()
        self.assertEqual(self.main_session.time_manager.selected_timer, "stopwatch")
        self.main_session.toggle_mode()
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