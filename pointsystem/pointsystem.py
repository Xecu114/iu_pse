

class PointSystem:
    def __init__(self):
        self.total_points = 0
        self.available_points = 0
        # self.filename = "data_pointsystem.json"
        # self.load_data()

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
    
    # def save_data(self):
    #     data = {"total_points": self.total_points, "available_points": self.available_points}
    #     with open(self.filename, "w") as file:
    #         json.dump(data, file)
    
    # def load_data(self):
    #     if not os.path.exists(self.filename):
    #         self.save_data()
    #     with open(self.filename, "r") as file:
    #         data = json.load(file)
    #     self.total_points = data["total_points"]
    #     self.available_points = data["available_points"]