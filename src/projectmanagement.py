import random
import sqlite3
from PyQt6.QtCore import QDate

DB_FILE = "projects.db"


class ProjectManagement:
    def __init__(self, ):
        project_names = ProjectManagement.get_projects_name_list()
        if project_names:
            self.id = ProjectManagement.get_id_by_name(project_names[0])
            self.load_data_from_sql()
        else:
            self.add_project()
    
    def add_time(self, minutes: int):
        self.time_tracked += minutes
    
    def get_time(self):
        return self.time_tracked

    def save_data_to_sql(self):
        """Create the current project data in the database."""
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            # Create table if it does not exist
            cursor.execute('''
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

            # Insert the project data
            cursor.execute('''
                INSERT INTO projects (id, name, description, type, time_tracked, start_date, end_date, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (self.id, self.name, self.description, self.type, self.time_tracked,
                  self.start_date.toString("yyyy-MM-dd"), self.end_date.toString("yyyy-MM-dd"), self.status))
            conn.commit()
    
    def update_data_in_sql(self):
        """Update the current project data in the database."""
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE projects
                SET name = ?, description = ?, type = ?, time_tracked = ?,
                    start_date = ?, end_date = ?, status = ?
                WHERE id = ?
            ''', (self.name, self.description, self.type, self.time_tracked,
                  self.start_date.toString("yyyy-MM-dd"), self.end_date.toString("yyyy-MM-dd"), self.status, self.id))
            conn.commit()
    
    def load_data_from_sql(self):
        """Load the current project data from the database."""
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT name, description, type, time_tracked, start_date, end_date, status
                FROM projects
                WHERE id = ?
            ''', (self.id,))
            row = cursor.fetchone()
            if row:
                self.name, self.description, self.type, self.time_tracked, start_date, end_date, self.status = row
                self.start_date = QDate.fromString(start_date, "yyyy-MM-dd")
                self.end_date = QDate.fromString(end_date, "yyyy-MM-dd")
            else:
                raise ValueError(f"No project found with ID {self.id}")
    
    def add_project(self):
        """Add a new project to the database."""
        self.id = random.randint(1000, 9999)
        self.name = ""
        self.description = ""
        self.type = ""
        self.time_tracked = 0
        self.start_date = QDate.currentDate()
        self.end_date = QDate.currentDate()
        self.status = "active"
        self.save_data_to_sql()
        print("New project added successfully!")

    def delete_project(self):
        """Delete a project from the database by its name."""
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM projects WHERE name = ?
            ''', (self.name,))
            if cursor.rowcount > 0:
                print(f"Project '{self.name}' deleted successfully!")
            else:
                print(f"No project found with the name '{self.name}'.")
    
    @staticmethod
    def get_projects_name_list():
        """Retrieve all project names from the database and return a list of names."""
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT name FROM projects
            ''')
            names = [row[0] for row in cursor.fetchall()]
        return names
    
    @staticmethod
    def get_id_by_name(name_to_check: str):
        """Check if a project name exists and return its ID if found."""
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id FROM projects WHERE name = ?
            ''', (name_to_check,))
            row = cursor.fetchone()
        return row[0] if row else None

    @staticmethod
    def get_projects_time_tracked_list():
        """Retrieve all project time_tracked from the database and return a list."""
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT time_tracked FROM projects
            ''')
            time_tracked_list = [row[0] for row in cursor.fetchall()]
        return time_tracked_list