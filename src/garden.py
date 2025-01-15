import os
import pygame
from constants import SQUARE_SIZE, ROWS, COLS
from gardenobjects import PlacedObject


class Garden:
    """
    The garden manages the map data (self.garden_map) and
    a list of all currently placed objects (self.placed_objects).
    """
    def __init__(self, map_file, garden_objects):
        self.map_file = map_file
        self.garden_objects = garden_objects
        self.garden_map = []
        self.placed_objects = []
        self.init_garden_map()

    def init_garden_map(self):
        # clear list first
        self.placed_objects.clear()
        self.garden_map.clear()

        if os.path.isfile(self.map_file):
            with open(self.map_file, 'r') as f:
                lines = f.read().splitlines()
            for line in lines:
                row_data = [int(ch) for ch in line]
                self.garden_map.append(row_data)
        else:
            # If no .map file exists: Empty map (zeros only)
            for _ in range(ROWS):
                row_data = [0] * COLS
                self.garden_map.append(row_data)

        self.update_garden_map()

    def update_garden_map(self):
        """
        Reconstructs the PlacedObject instances from the garden_map.
        Everything > 0 => is placed as an object.
        """
        self.placed_objects.clear()  # erst mal leeren
        for y, row in enumerate(self.garden_map):
            for x, element in enumerate(row):
                if element != 0:
                    PlacedObject(
                        self,
                        self.garden_objects[element],
                        (x * SQUARE_SIZE, y * SQUARE_SIZE)
                    )

    def draw_garden_map(self, win):
        # 1) Boden (Index 0) in jede Zelle
        ground_object = self.garden_objects[0]  # index 0 ist der Boden
        for y in range(ROWS):
            for x in range(COLS):
                win.blit(ground_object.image, (x * SQUARE_SIZE, y * SQUARE_SIZE))

        # 2) Alle platzierten Objekte zeichnen
        for obj in self.placed_objects:
            obj.draw(win)

    def save_garden_map(self):
        with open(self.map_file, 'w') as f:
            for row in self.garden_map:
                f.write("".join(map(str, row)) + "\n")

    def place_object(self, object_index):
        """
        Places an object (object_index) at the current mouse position.
        Call `update_garden_map()` afterwards to recreate the PlacedObject list (or add it directly).
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        row = mouse_y // SQUARE_SIZE
        col = mouse_x // SQUARE_SIZE
        self.garden_map[row][col] = object_index
