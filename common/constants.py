import pyautogui
import os

# Bildschirmauflösung abrufen
screen_width, screen_height = pyautogui.size()

WIDTH, HEIGHT = 1280, 720
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
PASTEL_BEIGE_HEX = '#f7ede3'
PASTEL_BEIGE_RGB = (247, 237, 227)
PASTEL_OCEANBAY_HEX = '#648181'
PASTEL_OCEANBAY_RGB = (100, 129, 129)
PASTEL_ROSE_HEX = '#f5cac2'
PASTEL_ROSE_RGB = (245, 202, 194)
PASTEL_RED_HEX = '#f28582'
PASTEL_SOFTCORAL_HEX = '#edc3ae'
PASTEL_TURQUOISE_HEX = '#c1e7e3'

assets_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")

IMGDIR_GRASS = str(os.path.join(assets_path, "grass.png"))
IMGDIR_TREE = str(os.path.join(assets_path, "Regenwald_Baum.jpg"))
IMGDIR_GUI_FLOWER_MEADOW = str(os.path.join(assets_path, "Gemini_flower_meadow.jpg"))