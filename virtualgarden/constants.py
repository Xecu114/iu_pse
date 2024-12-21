import pyautogui

# Bildschirmauflösung abrufen
screen_width, screen_height = pyautogui.size()

WIDTH, HEIGHT = screen_width/1.5, screen_height/1.5
SQUARE_SIZE = 100
ROWS, COLS = HEIGHT//SQUARE_SIZE, WIDTH//SQUARE_SIZE

# rgb
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)
