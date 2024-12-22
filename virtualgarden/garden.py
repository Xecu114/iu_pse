import pygame
from ..common.constants import ROWS, COLS, SQUARE_SIZE
from virtualgarden.gardenobjects import PlacedObject, placed_objects


class Garden:
    def __init__(self, map_file, garden_objects):
        self.map_file = map_file
        self.garden_objects = garden_objects
        self.garden_map = []
        self.init_garden_map()
    
    def init_garden_map(self):
        # TODO CHECK if file exists and if not create board
        for row in range(ROWS):
            self.garden_map.append([])
            for col in range(COLS):
                self.garden_map[row].append(0)
        self.update_garden_map()
    
    def update_garden_map(self):
        for y, row in enumerate(self.garden_map):
            for x, element in enumerate(row):
                PlacedObject(self.garden_objects[element], (x*SQUARE_SIZE, y*SQUARE_SIZE))

    def draw_garden_map(self, win):
        # win.fill(GREEN)
        for o in placed_objects:
            o.draw(win)
        pygame.display.update()
    
    def save_garden_map(self):
        with open(self.map_file, 'w') as f:
            for row in self.garden_map:
                f.write("".join(map(str, row))+"\n")
    
    def place_object(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.garden_map[mouse_y//SQUARE_SIZE][mouse_x//SQUARE_SIZE] = 1