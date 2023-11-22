# gui.py
import sys
import pygame
import pygame_gui
import math
import numpy as np
from logic import Connect4Game

class Connect4GUI:
    def __init__(self, game):
        self.game = game
        pygame.init()

        self.width = 800
        self.height = 600
        self.SQUARESIZE = 100
        self.RADIUS = int(self.SQUARESIZE / 2 - 5)
        self.screen = pygame.display.set_mode([self.width, self.height])
        pygame.display.set_caption('Connect4')
        self.fps = 60
        self.timer = pygame.time.Clock()
        self.font = pygame.font.Font('freesansbold.ttf', 24)
        self.turn_count_p1 = 0
        self.turn_count_p2 = 0
        self.remaining_count_p1 = 21
        self.remaining_count_p2 = 21

        self.MANAGER = pygame_gui.UIManager((self.width, self.height))
        self.TEXT_INPUT1 = pygame_gui.elements.UITextEntryLine(
            relative_rect = pygame.Rect((350, 105), (200, 50)),
            manager = self.MANAGER,
            object_id = "#first_text_entry"
        )
        self.TEXT_INPUT2 = pygame_gui.elements.UITextEntryLine(
            relative_rect = pygame.Rect((350, 205), (200, 50)),
            manager = self.MANAGER,
            object_id = "#second_text_entry"
        )

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 139, 148)
        self.YELLOW = (250, 238, 7)
        self.BLUE = (64, 144, 245)
        self.GREEN = (124, 252, 0)
        self.colour_p1 = self.RED
        self.colour_p2 = self.YELLOW

    def screen1(self):
        selected_colors = {'p1': self.game.colour_p1, 'p2': self.game.colour_p2}
        while True:
            UI_REFRESH_RATE = self.timer.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#first_text_entry":
                    self.game.p1 = event.text
                if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#second_text_entry":
                    self.game.p2 = event.text

                self.MANAGER.process_events(event)
            self.MANAGER.update(UI_REFRESH_RATE)
            self.screen.fill('black')
            self.MANAGER.draw_ui(self.screen)

            red_p1 = pygame.draw.rect(self.screen, self.RED, [560, 90, 100, 20], 0, 5)
            if red_p1.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                if selected_colors['p2'] != self.RED:
                    selected_colors['p1'] = self.RED
                    self.game.colour_p1 = self.RED

            yellow_p1 = pygame.draw.rect(self.screen, self.YELLOW, [560, 110, 100, 20], 0, 5)
            if yellow_p1.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                if selected_colors['p2'] != self.YELLOW:
                    selected_colors['p1'] = self.YELLOW
                    self.game.colour_p1 = self.YELLOW

            blue_p1 = pygame.draw.rect(self.screen, self.BLUE, [560, 130, 100, 20], 0, 5)
            if blue_p1.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                if selected_colors['p2'] != self.BLUE:
                    selected_colors['p1'] = self.BLUE
                    self.game.colour_p1 = self.BLUE

            green_p1 = pygame.draw.rect(self.screen, self.GREEN, [560, 150, 100, 20], 0, 5)
            if green_p1.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                if selected_colors['p2'] != self.GREEN:
                    selected_colors['p1'] = self.GREEN
                    self.game.colour_p1 = self.GREEN

            red_p2 = pygame.draw.rect(self.screen, self.RED, [560, 200, 100, 20], 0, 5)
            if red_p2.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                if selected_colors['p1'] != self.RED:
                    selected_colors['p2'] = self.RED
                    self.game.colour_p2 = self.RED

            yellow_p2 = pygame.draw.rect(self.screen, self.YELLOW, [560, 220, 100, 20], 0, 5)
            if yellow_p2.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                if selected_colors['p1'] != self.YELLOW:
                    selected_colors['p2'] = self.YELLOW
                    self.game.colour_p2 = self.YELLOW

            blue_p2 = pygame.draw.rect(self.screen, self.BLUE, [560, 240, 100, 20], 0, 5)
            if blue_p2.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                if selected_colors['p1'] != self.BLUE:
                    selected_colors['p2'] = self.BLUE
                    self.game.colour_p2 = self.BLUE

            green_p2 = pygame.draw.rect(self.screen, self.GREEN, [560, 260, 100, 20], 0, 5)
            if green_p2.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                if selected_colors['p1'] != self.GREEN:
                    selected_colors['p2'] = self.GREEN
                    self.game.colour_p2 = self.GREEN

            player1_text = self.font.render('Enter Player 1 name: ', True, self.game.colour_p1)
            self.screen.blit(player1_text, (100, 117))
            player1_enter = self.font.render('(and press ENTER) ', True, self.game.colour_p1)
            self.screen.blit(player1_enter, (100, 147))
            player2_text = self.font.render('Enter Player 2 name: ', True, self.game.colour_p2)
            self.screen.blit(player2_text, (100, 217))
            player2_enter = self.font.render('(and press ENTER) ', True, self.game.colour_p2)
            self.screen.blit(player2_enter, (100, 247))
            menu_btn = pygame.draw.rect(self.screen, 'light gray', [230, 300, 260, 60], 0, 5)
            pygame.draw.rect(self.screen, 'dark gray', [230, 300, 260, 60], 5, 5)
            text = self.font.render('Start game', True, 'black')
            self.screen.blit(text, (295, 317))
            if menu_btn.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                return 2

            pygame.display.update()

    def screen2(self):
        # pygame.draw.rect(screen, 'black',[100,100,300,300])
        self.game.draw_board(self.screen)
        pygame.display.update()

        myfont = pygame.font.SysFont("monospace", 75)
        game_over = False
        turn = 0

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 3

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(self.screen, self.BLACK, (0, 0, self.width, self.SQUARESIZE))

                    # Ask for Player 1 Input
                    if turn == 0:
                        self.turn_count_p1 += 1
                        self.remaining_count_p1 -= 1
                        print(self.remaining_count_p1)
                        posx = event.pos[0]
                        col = int(math.floor(posx / self.SQUARESIZE))

                        if self.game.is_valid_location(col):
                            row = self.game.get_next_open_row(col)
                            self.game.drop_piece(row, col, 1)

                            if self.game.winning_move(1):
                                self.game.turn_count = self.turn_count_p1
                                self.game.winner = self.game.p1
                                self.game.winnercolor = self.game.colour_p1
                                label = myfont.render(self.game.p1 + " wins!!", True, self.game.colour_p1)
                                self.screen.blit(label, (100, 10))
                                game_over = True

                    # Ask for Player 2 Input
                    else:
                        self.turn_count_p2 += 1
                        self.remaining_count_p2 -= 1
                        print(self.remaining_count_p2)
                        posx = event.pos[0]
                        col = int(math.floor(posx / self.SQUARESIZE))

                        if self.game.is_valid_location(col):
                            row = self.game.get_next_open_row(col)
                            self.game.drop_piece(row, col, 2)

                            if self.game.winning_move(2):
                                self.game.turn_count = self.turn_count_p2
                                self.game.winner = self.game.p2
                                self.game.winnercolor = self.game.colour_p2
                                label = myfont.render(self.game.p2 + " wins!!", True, self.game.colour_p2)
                                self.screen.blit(label, (100, 10))
                                game_over = True

                    self.game.print_board()
                    self.game.draw_board(self.screen)

                    turn += 1
                    turn = turn % 2

                    if game_over:
                        pygame.time.wait(2000)
                        return 3

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(self.screen, self.BLACK, (0, 0, self.width, self.SQUARESIZE))
                    posx = event.pos[0]
                    if turn == 0:
                        pygame.draw.circle(self.screen, self.game.colour_p1, (628, 25), self.RADIUS / 2)
                        pygame.draw.circle(self.screen, self.game.colour_p2, (675, 25), self.RADIUS / 2)
                        text_rem = self.font.render('Remaining coins:', True, 'white')
                        self.screen.blit(text_rem, (396, 13))
                        text_rem_p1 = self.font.render(str(self.remaining_count_p1), True, 'black')
                        self.screen.blit(text_rem_p1, (616, 15))
                        text_rem_p1 = self.font.render(str(self.remaining_count_p2), True, 'black')
                        self.screen.blit(text_rem_p1, (663, 15))
                        pygame.draw.circle(self.screen, self.game.colour_p1, (posx, int(self.SQUARESIZE / 2)),
                                           self.RADIUS)
                    else:
                        pygame.draw.circle(self.screen, self.game.colour_p1, (628, 25), self.RADIUS / 2)
                        pygame.draw.circle(self.screen, self.game.colour_p2, (675, 25), self.RADIUS / 2)
                        text_rem = self.font.render('Remaining coins:', True, 'white')
                        self.screen.blit(text_rem, (396, 13))
                        text_rem_p1 = self.font.render(str(self.remaining_count_p1), True, 'black')
                        self.screen.blit(text_rem_p1, (616, 15))
                        text_rem_p1 = self.font.render(str(self.remaining_count_p2), True, 'black')
                        self.screen.blit(text_rem_p1, (663, 15))
                        pygame.draw.circle(self.screen, self.game.colour_p2, (posx, int(self.SQUARESIZE / 2)),
                                           self.RADIUS)
                pygame.display.update()

    def screen3(self):
        text1 = self.game.font.render(self.game.winner + ' wins!', True, self.game.winnercolor)
        self.screen.blit(text1, (225, 150))
        text2 = self.game.font.render('CONGRATULATIONS!!', True, 'white')
        self.screen.blit(text2, (235, 175))

        # Play again button
        menu_btn_3 = pygame.draw.rect(self.screen, 'light gray', [230, 400, 260, 60], 0, 5)
        pygame.draw.rect(self.screen, 'dark gray', [230, 400, 260, 60], 5, 5)
        text = self.game.font.render('Play again', True, 'black')
        self.screen.blit(text, (300, 418))

        # QUIT button
        menu_btn_quit = pygame.draw.rect(self.screen, 'light gray', [230, 300, 260, 60], 0, 5)
        pygame.draw.rect(self.screen, 'dark gray', [230, 300, 260, 60], 5, 5)
        text = self.game.font.render('QUIT', True, 'black')
        self.screen.blit(text, (325, 318))

        if menu_btn_quit.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            pygame.quit()
            sys.exit()

        if menu_btn_3.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            self.game.board = self.game.create_board()
            self.game.game_over = False
            self.game.turn = 0
            self.game.remaining_count_p1 = 21
            self.game.remaining_count_p2 = 21
            self.game.selected_colors = {'p1': self.game.RED, 'p2': self.game.YELLOW}
            return 1

        return 3

