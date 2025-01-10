class PointsSystem:
    def __init__(self):
        self.total_points = 0
        self.available_points = 0

    def add_points(self, points: int):
        """Add points to the total and available points."""
        self.total_points += points
        self.available_points += points
    
    def remove_points(self, points: int):
        """Remove points from the available points."""
        self.available_points -= points

    def set_points(self, total_points, available_points):
        self.total_points = total_points
        self.available_points = available_points

    def get_points(self):
        """Return the current points."""
        return self.total_points, self.available_points