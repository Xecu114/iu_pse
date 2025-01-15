# import pyautogui
import os

# screen resolution
# screen_width, screen_height = pyautogui.size()

# GUI / PyQt
WIDTH, HEIGHT = 1280, 720
# int(screen_width/1.5), int(screen_height/1.5)

# VG / Pygame
GAME_WIDTH, GAME_HEIGHT = 1250, 700  # 1875, 1050
SQUARE_SIZE = 50  # 75
ROWS, COLS = HEIGHT // SQUARE_SIZE, WIDTH // SQUARE_SIZE

# colors
COLOR_BEIGE_HEX = '#f7ede3'
COLOR_BEIGE_RGB = (247, 237, 227)
COLOR_OCEANBAY_HEX = '#648181'
COLOR_OCEANBAY_RGB = (100, 129, 129)
COLOR_ROSE_HEX = '#f5cac2'
COLOR_ROSE_RGB = (245, 202, 194)
COLOR_RED_HEX = '#f28582'
COLOR_SOFTCORAL_HEX = '#edc3ae'
COLOR_SOFTCORAL_RGB = (237, 195, 174)
# unused
COLOR_TURQUOISE_HEX = '#c1e7e3'
COLOR_BABYBLUE_HEX = '#dfebeb'
COLOR_BABYBLUE_RGB = (223, 235, 235)
COLOR_BLUE_HEX = '#1f3855'
COLOR_BLUE_RGB = (31, 56, 85)

# file paths
RESOURCES_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resources")
ASSETS_PATH = os.path.join(RESOURCES_PATH, "assets\\")
JSON_FILE = os.path.join(RESOURCES_PATH, "data.json")
DB_FILE = os.path.join(RESOURCES_PATH, "projects.db")
MAP_FOLDER_PATH = os.path.join(RESOURCES_PATH, "gardens\\")
MAPDATA_FILE_PATH = os.path.join(MAP_FOLDER_PATH, "gardens_data.json")
IMGDIR_GUI_FLOWER_MEADOW = str(os.path.join(ASSETS_PATH, "Gemini_flower_meadow.jpg"))