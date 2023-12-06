import numpy as np
import math
import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (64, 144, 245)
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
                pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
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

    def is_terminal_node(self, board):
        return self.winning_move(board, 1) or self.winning_move(board, 2) or len(self.get_valid_locations(board)) == 0

    def get_valid_locations(self, board):
        valid_locations = []
        for col in range(self.col):
            if self.is_valid_location(board, col):
                valid_locations.append(col)
        return valid_locations

    def evaluate_window(self, window, piece):
        score = 0
        opp_piece = 1
        if piece == 1:
            opp_piece = 2

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(0) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(0) == 2:
            score += 2

        if window.count(opp_piece) == 3 and window.count(0) == 1:
            score -= 4

        return score
    def score_position(self, board, piece):
        score = 0

        # Score center column
        center_array = [int(i) for i in list(board[:, self.col // 2])]
        center_count = center_array.count(piece)
        score += center_count * 3

        # Score Horizontal
        for r in range(self.row):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(self.col - 3):
                window = row_array[c:c + 4]
                score += self.evaluate_window(window, piece)

        # Score Vertical
        for c in range(self.col):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(self.row - 3):
                window = col_array[r:r + 4]
                score += self.evaluate_window(window, piece)

        # Score posiive sloped diagonal
        for r in range(self.row - 3):
            for c in range(self.col - 3):
                window = [board[r + i][c + i] for i in range(4)]
                score += self.evaluate_window(window, piece)

        for r in range(self.row - 3):
            for c in range(self.col - 3):
                window = [board[r + 3 - i][c + i] for i in range(4)]
                score += self.evaluate_window(window, piece)

        return score
