import pygame
from .constants import ROWS, COLS, SQUARE_SIZE, GREEN, GREEN_LIGHTER, TREE


class Garden:
    def __init__(self, win):
        self.board = []
        self.create_board()
        self.draw_board(win)
    
    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                self.board[row].append(0)
        
    def draw_board(self, win):
        win.fill(GREEN)
        self.board[0][3] = 1
        self.board[5][6] = 1
        # for row in range(ROWS):
        #     for col in range(row % 2, COLS, 2):
        for i, row in enumerate(self.board):
            for j, element in enumerate(row):
                print(f"row:{i},col:{j}")
                if element != 0:
                    win.blit(TREE, (j*SQUARE_SIZE, i*SQUARE_SIZE))
                    # pygame.draw.rect(win, GREEN_LIGHTER,
                    #                  (j*SQUARE_SIZE, i*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                    pygame.draw.rect
        pygame.display.update()
