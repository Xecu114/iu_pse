import pyautogui
import os

# Bildschirmauflösung abrufen
screen_width, screen_height = pyautogui.size()

WIDTH, HEIGHT = 2000, 1000
# int(screen_width/1.5), int(screen_height/1.5)
SQUARE_SIZE = 50
ROWS, COLS = HEIGHT//SQUARE_SIZE, WIDTH//SQUARE_SIZE

# rgb
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)
GREEN = (0, 200, 0)
GREEN_LIGHTER = (0, 255, 50)

assets_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")

IMGDIR_GRASS = str(os.path.join(assets_path, "grass.png"))
IMGDIR_TREE = str(os.path.join(assets_path, "Regenwald_Baum.jpg"))