import pyautogui
import os

# Bildschirmauflösung abrufen
screen_width, screen_height = pyautogui.size()

WIDTH, HEIGHT = 1280, 720
# int(screen_width/1.5), int(screen_height/1.5)
SQUARE_SIZE = 50
ROWS, COLS = HEIGHT//SQUARE_SIZE, WIDTH//SQUARE_SIZE

# colors
COLOR_BEIGE_HEX = '#f7ede3'
COLOR_BEIGE_RGB = (247, 237, 227)
COLOR_OCEANBAY_HEX = '#648181'
COLOR_OCEANBAY_RGB = (100, 129, 129)
COLOR_ROSE_HEX = '#f5cac2'
COLOR_ROSE_RGB = (245, 202, 194)
COLOR_RED_HEX = '#f28582'
# unused
COLOR_SOFTCORAL_HEX = '#edc3ae'
COLOR_SOFTCORAL_RGB = (237, 195, 174)
COLOR_TURQUOISE_HEX = '#c1e7e3'
COLOR_BABYBLUE_HEX = '#dfebeb'
COLOR_BABYBLUE_RGB = (223, 235, 235)
COLOR_BLUE_HEX = '#1f3855'
COLOR_BLUE_RGB = (31, 56, 85)

assets_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")

IMGDIR_GRASS = str(os.path.join(assets_path, "grass.png"))
IMGDIR_TREE = str(os.path.join(assets_path, "Regenwald_Baum.jpg"))
IMGDIR_GUI_FLOWER_MEADOW = str(os.path.join(assets_path, "Gemini_flower_meadow.jpg"))