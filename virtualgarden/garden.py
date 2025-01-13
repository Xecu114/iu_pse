import os
import pygame
from common.constants import SQUARE_SIZE, ROWS, COLS
from virtualgarden.gardenobjects import PlacedObject


class Garden:
    """
    Der Garten verwaltet die Map-Daten (self.garden_map) und
    eine Liste aller aktuell platzierten Objekte (self.placed_objects).
    """
    def __init__(self, map_file, garden_objects):
        self.map_file = map_file
        self.garden_objects = garden_objects
        self.garden_map = []
        self.placed_objects = []  # => keine globale placed_objects mehr
        self.init_garden_map()

    def init_garden_map(self):
        # Liste immer erstmal leeren
        self.placed_objects.clear()
        self.garden_map.clear()

        if os.path.isfile(self.map_file):
            with open(self.map_file, 'r') as f:
                lines = f.read().splitlines()
            for line in lines:
                row_data = [int(ch) for ch in line]
                self.garden_map.append(row_data)
        else:
            # Falls keine .map-Datei existiert: Leere Map (nur Nullen)
            for _ in range(ROWS):
                row_data = [0] * COLS
                self.garden_map.append(row_data)

        # Damit direkt PlacedObjects erzeugt werden
        self.update_garden_map()

    def update_garden_map(self):
        """
        Rekonstruiert die PlacedObject-Instanzen aus der garden_map.
        Alles > 0 => wird als Objekt platziert.
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
        Platziert ein Objekt (object_index) an der aktuellen Mausposition.
        Anschließend musst du `update_garden_map()` aufrufen, damit die
        PlacedObject-Liste neu erstellt wird (oder du fügst es direkt hinzu).
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        row = mouse_y // SQUARE_SIZE
        col = mouse_x // SQUARE_SIZE
        self.garden_map[row][col] = object_index
