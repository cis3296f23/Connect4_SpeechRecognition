import numpy as np
import math
import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SQUARESIZE = 100
class GameLogic:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.winner = None
    def create_board(self):
        return np.zeros((self.row, self.col))

    def drop_piece(self, board, row, col, piece):
        board[row][col] = piece

    def is_valid_location(self, board, col):
        return board[self.row - 1][col] == 0

    def get_next_open_row(self, board, col):
        for r in range(self.row):
            if board[r][col] == 0:
                return r

    def print_board(self, board):
        print(np.flip(board, 0))

    def winning_move(self, board, piece):
        global winner  # Declare winner as a global variable
        # Check horizontal locations for win
        for c in range(self.col - 3):
            for r in range(self.row):
                if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                    c + 3] == piece:
                    self.winner = piece
                    return True

        # Check vertical locations for win
        for c in range(self.col):
            for r in range(self.row - 3):
                if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                    c] == piece:
                    self.winner = piece
                    return True

        # Check positively sloped diagonals
        for c in range(self.col - 3):
            for r in range(self.row - 3):
                if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and \
                        board[r + 3][
                            c + 3] == piece:
                    self.winner = piece
                    return True

        # Check negatively sloped diagonals
        for c in range(self.col - 3):
            for r in range(3, self.row):
                if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and \
                        board[r - 3][
                            c + 3] == piece:
                    self.winner = piece
                    return True

    def draw_board(self, board, screen, radius, height, colour_p1, colour_p2):
        for c in range(self.col):
            for r in range(self.row):
                pygame.draw.rect(screen, WHITE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
                pygame.draw.circle(screen, BLACK, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), radius)

        for c in range(self.col):
            for r in range(self.row):
                if board[r][c] == 1:
                    pygame.draw.circle(screen, colour_p1, (
                        int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), radius)
                elif board[r][c] == 2:
                    pygame.draw.circle(screen, colour_p2, (
                        int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), radius)
        # pygame.draw.circle(screen, RED, (600, 25), radius/2)
        # pygame.draw.circle(screen, YELLOW, (650, 25), radius / 2)
        pygame.display.update()