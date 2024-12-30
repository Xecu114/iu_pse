import random
from PyQt6.QtCore import QDate


class ProjectManagement:
    def __init__(self, name: str, description: str, type: str,
                 start_date: QDate, end_date: QDate):
        self.id = self.create_project_id()
        self.name = name
        self.description = description
        self.type = type
        self.time_tracked = 0
        self.start_date = start_date
        self.end_date = end_date
        self.status = "active"
        self.save_data_to_sql()
    
    def create_project_id(self):
        return random.randint(1000, 9999)
    
    def add_time(self, minutes: int):
        self.time_tracked += minutes
    
    def get_time(self):
        return self.time_tracked

    def save_data_to_sql(self):
        """Create the current project data in the database."""
        pass
    
    def update_data_in_sql(self):
        """Update the current project data in the database."""
        # currently called in "session.save_data()"

        pass
    
    def load_data_from_sql(self):
        """Load the current project data from the database."""
        pass