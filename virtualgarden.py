import pygame
import os

assets_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
WIDTH, HEIGHT = 1280, 720
SQUARE_SIZE = 50
ROWS, COLS = HEIGHT//SQUARE_SIZE, WIDTH//SQUARE_SIZE
IMGDIR_GRASS = str(os.path.join(assets_path, "grass.png"))
IMGDIR_TREE = str(os.path.join(assets_path, "Regenwald_Baum.jpg"))

pygame.init()
# FONT = pygame.font.SysFont("comicsans", 30)
FPS = 30
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Virtual Garden')

placed_objects = []
loaded_images = {}


class GardenObject:
    def __init__(self, name, image):
        self.name = name
        if image in loaded_images:
            self.image = loaded_images[image]
        else:
            self.image = pygame.transform.scale(pygame.image.load(image),
                                                (SQUARE_SIZE, SQUARE_SIZE))
            loaded_images[image] = self.image


class PlacedObject:
    def __init__(self, garden_object, location):
        self.garden_object = garden_object
        self.location = location
        placed_objects.append(self)

    def delete(self):
        placed_objects.remove(self)
        
    def draw(self, win):
        win.blit(self.garden_object.image, self.location)


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


def main():
    running = True
    is_mouse_clicked = False
    clock = pygame.time.Clock()
    garden_objects = [
        GardenObject("grass", IMGDIR_GRASS),
        GardenObject("tree", IMGDIR_TREE)
    ]
    # TODO add way more objects (incl. textures) and different vegetations / floras
    garden0 = Garden("virtualgarden\\gardens\\garden0.map", garden_objects)
    
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.dict['button'] == 1:
                    is_mouse_clicked = True
                    
            # if event.type == pygame.MOUSEMOTION:
            # TODO add object moving with move if picked up
            
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    running = False
            
            if event.type == pygame.QUIT:
                running = False
                    
        if is_mouse_clicked:
            garden0.place_object()

        is_mouse_clicked = False
        garden0.update_garden_map()
        garden0.draw_garden_map(WIN)

    garden0.save_garden_map()
    pygame.quit()
    

if __name__ == '__main__':
    main()
