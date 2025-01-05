import unittest
import sqlite3
from PyQt6.QtCore import QDate
from src.projectmanagement import ProjectManagement, DB_FILE


class TestProjectManagement(unittest.TestCase):
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
        self.project = ProjectManagement(self.conn)

    def tearDown(self):
        # Clean up the test database
        self.cursor.execute('DROP TABLE IF EXISTS projects')
        self.conn.commit()
        self.conn.close()

    def test_add_time_and_get_time(self):
        self.project.time_tracked = 0
        self.project.add_time(30)
        self.assertEqual(self.project.get_time(), 30)

    def test_save_data_to_sql(self):
        self.project.id = 1
        self.project.name = "Test Project"
        self.project.description = "Test Description"
        self.project.type = "Test Type"
        self.project.time_tracked = 60
        self.project.start_date = QDate.currentDate()
        self.project.end_date = QDate.currentDate()
        self.project.status = "active"
        self.project.save_data_to_sql()

        self.cursor.execute('SELECT * FROM projects WHERE id = 1')
        row = self.cursor.fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row[1], "Test Project")

    def test_update_data_in_sql(self):
        self.project.id = 1
        self.project.name = "Test Project"
        self.project.description = "Test Description"
        self.project.type = "Test Type"
        self.project.time_tracked = 60
        self.project.start_date = QDate.currentDate()
        self.project.end_date = QDate.currentDate()
        self.project.status = "active"
        self.project.save_data_to_sql()

        self.project.name = "Updated Project"
        self.project.update_data_in_sql()

        self.cursor.execute('SELECT * FROM projects WHERE id = 1')
        row = self.cursor.fetchone()
        self.assertEqual(row[1], "Updated Project")

    def test_load_data_from_sql(self):
        self.cursor.execute('''
            INSERT INTO projects (id, name, description, type, time_tracked, start_date, end_date, status)
            VALUES (1, "Test Project", "Test Description", "Test Type", 60, "2023-01-01", "2023-01-01", "active")
        ''')
        self.conn.commit()

        self.project.id = 1
        self.project.load_data_from_sql()
        self.assertEqual(self.project.name, "Test Project")
        self.assertEqual(self.project.time_tracked, 60)

    def test_add_project(self):
        self.project.add_project()
        self.cursor.execute('SELECT * FROM projects WHERE id = ?', (self.project.id,))
        row = self.cursor.fetchone()
        self.assertIsNotNone(row)

    def test_delete_project(self):
        self.cursor.execute('''
            INSERT INTO projects (id, name, description, type, time_tracked, start_date, end_date, status)
            VALUES (1, "Test Project", "Test Description", "Test Type", 60, "2023-01-01", "2023-01-01", "active")
        ''')
        self.conn.commit()

        self.project.name = "Test Project"
        self.project.delete_project()
        self.cursor.execute('SELECT * FROM projects WHERE name = "Test Project"')
        row = self.cursor.fetchone()
        self.assertIsNone(row)

    def test_get_projects_name_list(self):
        self.cursor.execute('''
            INSERT INTO projects (id, name, description, type, time_tracked, start_date, end_date, status)
            VALUES (1, "Test Project", "Test Description", "Test Type", 60, "2023-01-01", "2023-01-01", "active")
        ''')
        self.conn.commit()

        names = ProjectManagement.get_projects_name_list(self.conn)
        self.assertIn("Test Project", names)

    def test_get_id_by_name(self):
        self.cursor.execute('''
            INSERT INTO projects (id, name, description, type, time_tracked, start_date, end_date, status)
            VALUES (1, "Test Project", "Test Description", "Test Type", 60, "2023-01-01", "2023-01-01", "active")
        ''')
        self.conn.commit()

        project_id = ProjectManagement.get_id_by_name("Test Project", self.conn)
        self.assertEqual(project_id, 1)

    def test_get_projects_time_tracked_list(self):
        self.cursor.execute('''
            INSERT INTO projects (id, name, description, type, time_tracked, start_date, end_date, status)
            VALUES (1, "Test Project", "Test Description", "Test Type", 60, "2023-01-01", "2023-01-01", "active")
        ''')
        self.conn.commit()

        time_tracked_list = ProjectManagement.get_projects_time_tracked_list(self.conn)
        self.assertIn(60, time_tracked_list)


if __name__ == '__main__':
    unittest.main()