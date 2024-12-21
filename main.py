import pygame
from virtualgarden.constants import WIDTH, HEIGHT
from virtualgarden.garden import Garden
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
    garden = Garden(WIN)
    
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    running = False
        
    pygame.quit()


if __name__ == '__main__':
    main()
