class PointSystem:
    def __init__(self):
        self.total_minutes = 0
        self.points = 0

    def add_minutes(self, minutes: int):
        """Add minutes to the total and recalculate points."""
        self.total_minutes += minutes
        self.points = self.total_minutes // 1

    def get_points(self):
        """Return the current points."""
        return self.points
