import pygame
import os
from virtualgarden.constants import WIDTH, HEIGHT, SQUARE_SIZE
pygame.font.init()

FPS = 30

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Virtual Garden')

assets_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

BG = pygame.transform.scale(pygame.image.load(str(os.path.join(assets_path, "greenbg.jpg"))),
                            (WIDTH, HEIGHT))
tree = pygame.transform.scale(pygame.image.load(str(os.path.join(assets_path, "Regenwald_Baum.jpg"))),
                              (SQUARE_SIZE, SQUARE_SIZE))

FONT = pygame.font.SysFont("comicsans", 30)


def draw():
    WIN.blit(BG, (0, 0))
    WIN.blit(tree, (0, 0))
    welcome_text = FONT.render("Welcome", 1, "white")
    WIN.blit(welcome_text, (WIDTH/2 - welcome_text.get_width()/2,
                            HEIGHT/2 - welcome_text.get_height()/2))
    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)
        draw()
        pygame.time.delay(4000)
        break
        
    pygame.quit()


if __name__ == '__main__':
    main()
