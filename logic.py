# logic.py
import pygame
import numpy as np
import sys
import math
import pygame_gui

class Connect4Game:

    def __init__(self):
        self.board = np.zeros((6, 7))
        self.winner = None
        self.p1 = "Player 1"
        self.p2 = "Player 2"
        self.turn_count_p1 = 0
        self.turn_count_p2 = 0
        self.remaining_count_p1 = 21
        self.remaining_count_p2 = 21
        self.SQUARESIZE = 100
        self.RADIUS = int(self.SQUARESIZE / 2 - 5)
        self.ROW_COUNT = 6
        self.COLUMN_COUNT = 7
        self.width = (self.COLUMN_COUNT) * self.SQUARESIZE
        self.height = (self.ROW_COUNT) * self.SQUARESIZE
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 139, 148)
        self.YELLOW = (250, 238, 7)
        self.BLUE = (64, 144, 245)
        self.GREEN = (124, 252, 0)
        self.colour_p1 = self.RED
        self.colour_p2 = self.YELLOW

        self.font = pygame.font.SysFont("monospace", 75)

    def create_board(self):
        board = np.zeros((self.ROW_COUNT, self.COLUMN_COUNT))
        return board

    def drop_piece(self, row, col, piece):
        self.board[row][col] = piece

    def is_valid_location(self, col):
        return self.board[self.ROW_COUNT - 1][col] == 0

    def get_next_open_row(self, col):
        for r in range(self.ROW_COUNT):
            if self.board[r][col] == 0:
                return r

    def print_board(self):
        print(np.flip(self.board, 0))

    def winning_move(self, piece):
        # Check horizontal locations for win
        for c in range(7 - 3):
            for r in range(6):
                if (
                    self.board[r][c] == piece
                    and self.board[r][c + 1] == piece
                    and self.board[r][c + 2] == piece
                    and self.board[r][c + 3] == piece
                ):
                    self.winner = self.p1 if piece == 1 else self.p2
                    return True

        # Check vertical locations for win
        for c in range(7):
            for r in range(6 - 3):
                if (
                    self.board[r][c] == piece
                    and self.board[r + 1][c] == piece
                    and self.board[r + 2][c] == piece
                    and self.board[r + 3][c] == piece
                ):
                    self.winner = self.p1 if piece == 1 else self.p2
                    return True

        # Check positively sloped diagonals
        for c in range(7 - 3):
            for r in range(6 - 3):
                if (
                    self.board[r][c] == piece
                    and self.board[r + 1][c + 1] == piece
                    and self.board[r + 2][c + 2] == piece
                    and self.board[r + 3][c + 3] == piece
                ):
                    self.winner = self.p1 if piece == 1 else self.p2
                    return True

        # Check negatively sloped diagonals
        for c in range(7 - 3):
            for r in range(3, 6):
                if (
                    self.board[r][c] == piece
                    and self.board[r - 1][c + 1] == piece
                    and self.board[r - 2][c + 2] == piece
                    and self.board[r - 3][c + 3] == piece
                ):
                    self.winner = self.p1 if piece == 1 else self.p2
                    return True

        return False

    def is_board_full(self):
        return np.all(self.board != 0)

    def get_winner(self):
        return self.winner

    def switch_players(self):
        self.turn_count_p1, self.turn_count_p2 = self.turn_count_p2, self.turn_count_p1
        self.remaining_count_p1, self.remaining_count_p2 = self.remaining_count_p2, self.remaining_count_p1
        self.p1, self.p2 = self.p2, self.p1

    def reset_game(self):
        self.create_board()
        self.winner = None
        self.turn_count_p1 = 0
        self.turn_count_p2 = 0
        self.remaining_count_p1 = 21
        self.remaining_count_p2 = 21

    def draw_board(self, screen):
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT):
                pygame.draw.rect(screen, self.WHITE,
                                 (c * self.SQUARESIZE, r * self.SQUARESIZE + self.SQUARESIZE, self.SQUARESIZE,
                                  self.SQUARESIZE))
                pygame.draw.circle(screen, self.BLACK, (
                    int(c * self.SQUARESIZE + self.SQUARESIZE / 2),
                    int(r * self.SQUARESIZE + self.SQUARESIZE + self.SQUARESIZE / 2)),
                                   self.RADIUS)

        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT):
                if self.board[r][c] == 1:
                    pygame.draw.circle(screen, self.colour_p1, (
                        int(c * self.SQUARESIZE + self.SQUARESIZE / 2),
                        self.height - int(r * self.SQUARESIZE + self.SQUARESIZE / 2)),
                                       self.RADIUS)
                elif self.board[r][c] == 2:
                    pygame.draw.circle(screen, self.colour_p2, (
                        int(c * self.SQUARESIZE + self.SQUARESIZE / 2),
                        self.height - int(r * self.SQUARESIZE + self.SQUARESIZE / 2)),
                                       self.RADIUS)

        pygame.display.update()
