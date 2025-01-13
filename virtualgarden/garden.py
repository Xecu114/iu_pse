import os
import pygame
from common.constants import SQUARE_SIZE, ROWS, COLS
from virtualgarden.gardenobjects import PlacedObject


class Garden:
    def __init__(self, map_file, garden_objects):
        self.map_file = map_file
        self.garden_objects = garden_objects
        self.garden_map = []
        self.init_garden_map()

    def init_garden_map(self):
        # Leere zunächst die globale Liste platzierter Objekte
        placed_objects.clear()

        # Prüfe, ob es die Datei schon gibt
        if os.path.isfile(self.map_file):
            with open(self.map_file, 'r') as f:
                lines = f.read().splitlines()
            for line in lines:
                row_data = [int(ch) for ch in line]
                self.garden_map.append(row_data)
        else:
            # Falls nein, erstelle einen leeren Garten (nur 0)
            for _ in range(ROWS):
                row_data = [0] * COLS
                self.garden_map.append(row_data)

        self.update_garden_map()

    def update_garden_map(self):
        """
        Re-creates PlacedObject instances based on the garden_map.
        We only create them for indices > 0 (everything that's NOT ground).
        """
        placed_objects.clear()
        for y, row in enumerate(self.garden_map):
            for x, element in enumerate(row):
                if element != 0:
                    PlacedObject(
                        self.garden_objects[element],
                        (x * SQUARE_SIZE, y * SQUARE_SIZE)
                    )

    def draw_garden_map(self, win):
        # 1) Draw ground for every cell
        for y in range(ROWS):
            for x in range(COLS):
                ground_object = self.garden_objects[0]  # index 0 is ground
                win.blit(ground_object.image, (x * SQUARE_SIZE, y * SQUARE_SIZE))

        # 2) Draw placed objects (these are all indices > 0)
        for o in placed_objects:
            o.draw(win)

    def save_garden_map(self):
        with open(self.map_file, 'w') as f:
            for row in self.garden_map:
                f.write("".join(map(str, row)) + "\n")

    def place_object(self, object_index):
        """
        Platziert das Objekt (object_index) an der aktuellen Mausposition.
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        row = mouse_y // SQUARE_SIZE
        col = mouse_x // SQUARE_SIZE
        self.garden_map[row][col] = object_index