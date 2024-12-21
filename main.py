import pygame
from virtualgarden.constants import WIDTH, HEIGHT, IMGDIR_TREE, IMGDIR_GRASS
from virtualgarden.garden import Garden
from virtualgarden.gardenobjects import GardenObject
pygame.init()

FPS = 30

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Virtual Garden')

# FONT = pygame.font.SysFont("comicsans", 30)


def draw_text():
    # welcome_text = FONT.render("Welcome", 1, "white")
    # WIN.blit(welcome_text, (WIDTH/2 - welcome_text.get_width()/2, HEIGHT/2 - welcome_text.get_height()/2))
    pygame.display.update()


def main():
    running = True
    clock = pygame.time.Clock()
    garden_objects = [
        GardenObject("grass", IMGDIR_GRASS),
        GardenObject("tree", IMGDIR_TREE)
    ]
    garden0 = Garden("virtualgarden\\gardens\\garden0.map", garden_objects)
    garden0.garden_map[8][10] = 1
    garden0.garden_map[9][10] = 1
    garden0.garden_map[8][11] = 1
    garden0.garden_map[9][11] = 1
    
    while running:
        clock.tick(FPS)

        garden0.update_garden_map()
        garden0.draw_garden_map(WIN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    running = False
            
            # TODO add Tree by clicking on a Tile

    garden0.save_garden_map()
    pygame.quit()
    

if __name__ == '__main__':
    main()
