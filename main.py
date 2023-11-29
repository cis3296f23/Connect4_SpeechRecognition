import pygame
import numpy as np
import sys
import math
import pygame_gui
import speech_recognition as sr


p1 = "Player 1" # initialize with a default value
p2 = "Player 2" # initialize with default value
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255,139,148)
YELLOW = (250, 238, 7)
BLUE=(64,144,245)
GREEN=(124,252,0)
colour_p1=RED
colour_p2=YELLOW
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
turn_count_p1=0
turn_count_p2=0
remaining_count_p1=21
remaining_count_p2=21
CLOCK = pygame.time.Clock()
winnername = str
connect4_positions = ["Column 1", "Column 2", "Column 3", "Column 4", "Column 5", "Column 6", "Column 7",
                      "Drop in column 1", "Drop in column 2", "Drop in column 3", "Drop in column 4",
                      "Drop in column 5", "Drop in column 6", "Drop in column 7", "Place it in column 1",
                      "Place it in column 2", "Place it in column 3", "Place it in column 4",
                      "Place it in column 5", "Place it in column 6", "Place it in column 7",
                      "Put a chip in column 1", "Put a chip in column 2", "Put a chip in column 3",
                      "Put a chip in column 4", "Put a chip in column 5", "Put a chip in column 6",
                      "Put a chip in column 7"]

def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece):
    global winner  # Declare winner as a global variable
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                winner = p1 if piece == 1 else p2
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                winner = p1 if piece == 1 else p2
                return True

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                winner = p1 if piece == 1 else p2
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                winner = p1 if piece == 1 else p2
                return True



def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, WHITE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (
            int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, colour_p1, (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, colour_p2, (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    #pygame.draw.circle(screen, RED, (600, 25), RADIUS/2)
    #pygame.draw.circle(screen, YELLOW, (650, 25), RADIUS / 2)
    pygame.display.update()


board = create_board()
print_board(board)
game_over = False
turn = 0

pygame.init()

width = (COLUMN_COUNT) * SQUARESIZE
height = (ROW_COUNT) * SQUARESIZE

RADIUS = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode([width, height])
pygame.display.set_caption('Connect4')
fps = 60

timer = pygame.time.Clock()
screen_number = 1
font = pygame.font.Font('freesansbold.ttf', 24)

MANAGER = pygame_gui.UIManager((width, height))
TEXT_INPUT1 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((350, 105), (200, 50)), manager=MANAGER,
                                                  object_id="#first_text_entry")
TEXT_INPUT2 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((350, 205), (200, 50)), manager=MANAGER,
                                                  object_id="#second_text_entry")


def screen1():
    selected_colors = {'p1': RED, 'p2': YELLOW}
    while True:
        UI_REFRESH_RATE = CLOCK.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#first_text_entry":
                global p1
                p1 = event.text
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#second_text_entry":
                global p2
                p2 = event.text

            MANAGER.process_events(event)
        MANAGER.update(UI_REFRESH_RATE)
        screen.fill('black')
        MANAGER.draw_ui(screen)

        red_p1 = pygame.draw.rect(screen, RED, [560, 90, 100, 20], 0, 5)
        if red_p1.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            global colour_p1
            if selected_colors['p2'] != RED:
                selected_colors['p1'] = RED
                colour_p1 = RED
        yellow_p1 = pygame.draw.rect(screen, YELLOW, [560, 110, 100, 20], 0, 5)
        if yellow_p1.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            if selected_colors['p2'] != YELLOW:
                selected_colors['p1'] = YELLOW
                colour_p1 = YELLOW
        blue_p1 = pygame.draw.rect(screen, BLUE, [560, 130, 100, 20], 0, 5)
        if blue_p1.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            if selected_colors['p2'] != BLUE:
                selected_colors['p1'] = BLUE
                colour_p1 = BLUE
        green_p1 = pygame.draw.rect(screen, GREEN, [560, 150, 100, 20], 0, 5)
        if green_p1.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            if selected_colors['p2'] != GREEN:
                selected_colors['p1'] = GREEN
                colour_p1 = GREEN

        red_p2 = pygame.draw.rect(screen, RED, [560, 200, 100, 20], 0, 5)
        if red_p2.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            global colour_p2
            if selected_colors['p1'] != RED:
                selected_colors['p2'] = RED
                colour_p2 = RED
        yellow_p2 = pygame.draw.rect(screen, YELLOW, [560, 220, 100, 20], 0, 5)
        if yellow_p2.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            if selected_colors['p1'] != YELLOW:
                selected_colors['p2'] = YELLOW
                colour_p2 = YELLOW
        blue_p2 = pygame.draw.rect(screen, BLUE, [560, 240, 100, 20], 0, 5)
        if blue_p2.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            if selected_colors['p1'] != BLUE:
                selected_colors['p2'] = BLUE
                colour_p2 = BLUE
        green_p2 = pygame.draw.rect(screen, GREEN, [560, 260, 100, 20], 0, 5)
        if green_p2.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            if selected_colors['p1'] != GREEN:
                selected_colors['p2'] = GREEN
                colour_p2 = GREEN

        player1_text = font.render('Enter Player 1 name: ', True, colour_p1)
        screen.blit(player1_text, (100, 117))
        player1_enter = font.render('(and press ENTER) ', True, colour_p1)
        screen.blit(player1_enter, (100, 147))
        player2_text = font.render('Enter Player 2 name: ', True, colour_p2)
        screen.blit(player2_text, (100, 217))
        player2_enter = font.render('(and press ENTER) ', True, colour_p2)
        screen.blit(player2_enter, (100, 247))
        menu_btn = pygame.draw.rect(screen, 'light gray', [230, 300, 260, 60], 0, 5)
        pygame.draw.rect(screen, 'dark gray', [230, 300, 260, 60], 5, 5)
        text = font.render('Start game', True, 'black')
        screen.blit(text, (295, 317))
        if menu_btn.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return 2

        pygame.display.update()

def screen2():
    global remaining_count_p1
    global remaining_count_p2
    global player_turn

    # pygame.draw.rect(screen, 'black',[100,100,300,300])
    draw_board(board)
    pygame.display.update()

    myfont = pygame.font.SysFont("monospace", 75)
    game_over = False
    turn = 0
    player_turn = 1  # Initialize player_turn

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # Voice recognition
                move = speak_to_drop_chip()
                if move is not None:
                    # Check if the move is valid and update the game state
                    move = move.lower()
                    if move in connect4_positions:
                        col = connect4_positions.index(move)
                        if board[0][col] == 0:
                            row = next((i for i in range(ROW_COUNT - 1, -1, -1) if board[i][col] == 0), None)
                            if row is not None:
                                drop_piece(board, row, col, player_turn)
                                player_turn = 3 - player_turn  # Switch players (assuming 1 and 2 players)
                                remaining_count_p1 -= 1 if player_turn == 1 else 0
                                remaining_count_p2 -= 1 if player_turn == 2 else 0
                                print_board(board)
                                draw_board(board)

                                # Check for a winner
                                if winning_move(board, player_turn):
                                    turn_count = turn_count_p1 if player_turn == 1 else turn_count_p2
                                    winner = p1 if player_turn == 1 else p2
                                    winnercolor = colour_p1 if player_turn == 1 else colour_p2
                                    label = myfont.render(winner + " wins!!", 1, winnercolor)
                                    screen.blit(label, (100, 10))
                                    game_over = True

                                # Check for a tie
                                elif all(board[0][col] != 0 for col in range(COLUMN_COUNT)):
                                    label = myfont.render("It's a tie!", 1, WHITE)
                                    screen.blit(label, (165, 10))
                                    game_over = True

                print_board(board)
                draw_board(board)

                turn += 1
                turn = turn % 2

                if game_over:
                    pygame.time.wait(2000)
                    scr_no = 3
                    screen_number = scr_no

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, colour_p1, (628, 25), RADIUS / 2)
                    pygame.draw.circle(screen, colour_p2, (675, 25), RADIUS / 2)
                    text_rem = font.render('Remaining coins:', True, 'white')
                    screen.blit(text_rem, (396, 13))
                    text_rem_p1 = font.render(str(remaining_count_p1), True, 'black')
                    screen.blit(text_rem_p1, (616, 15))
                    text_rem_p1 = font.render(str(remaining_count_p2), True, 'black')
                    screen.blit(text_rem_p1, (663, 15))
                    pygame.draw.circle(screen, colour_p1, (posx, int(SQUARESIZE / 2)), RADIUS)
                else:
                    pygame.draw.circle(screen, colour_p1, (628, 25), RADIUS / 2)
                    pygame.draw.circle(screen, colour_p2, (675, 25), RADIUS / 2)
                    text_rem = font.render('Remaining coins:', True, 'white')
                    screen.blit(text_rem, (396, 13))
                    text_rem_p1 = font.render(str(remaining_count_p1), True, 'black')
                    screen.blit(text_rem_p1, (616, 15))
                    text_rem_p1 = font.render(str(remaining_count_p2), True, 'black')
                    screen.blit(text_rem_p1, (663, 15))
                    pygame.draw.circle(screen, colour_p2, (posx, int(SQUARESIZE / 2)), RADIUS)
            pygame.display.update()


def screen3():
    global winnercolor
    global winner  # Declare winner as a global variable if it's not already passed as an argument
    text1 = font.render(winner + ' wins!', True, winnercolor) # Ensure winner is a string
    screen.blit(text1, (225, 150))
    text2 = font.render('CONGRATULATIONS!!', True, 'white')
    screen.blit(text2, (235, 175))

    # Play again button
    menu_btn_3 = pygame.draw.rect(screen, 'light gray', [230, 400, 260, 60], 0, 5)
    pygame.draw.rect(screen, 'dark gray', [230, 400, 260, 60], 5, 5)
    text = font.render('Play again', True, 'black')
    screen.blit(text, (300, 418))

    # QUIT button
    menu_btn_quit = pygame.draw.rect(screen, 'light gray', [230, 300, 260, 60], 0, 5)
    pygame.draw.rect(screen, 'dark gray', [230, 300, 260, 60], 5, 5)
    text = font.render('QUIT', True, 'black')
    screen.blit(text, (325, 318))
    if menu_btn_quit.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
        pygame.quit()
        sys.exit()


    if menu_btn_3.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
        global board
        global game_over
        global turn
        global remaining_count_p1
        global remaining_count_p2
        board = create_board()
        game_over = False
        turn = 0
        remaining_count_p1 = 21
        remaining_count_p2 = 21
        selected_colors = {'p1': RED, 'p2': YELLOW}
        return 1

    return 3

def speak_to_drop_chip():
    r = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source)
        except ValueError:
            print("Please say it again")
            audio = r.listen(source)
        except IndexError:
            print("Please say it again")
            audio = r.listen(source)

        result = r.recognize_google(audio)
        print(result)

        # Extract numbers from the recognized words
        numbers = [word for word in result.split() if word.isdigit()]

        if not numbers:
            return None

        # Check if any extracted number is a valid column number
        for number in numbers:
            if is_valid_column(number):
                return number

        return None

def is_valid_column(number):
    return 1 <= int(number) <= 7

run = True
while run:
    screen.fill('black')
    timer.tick(fps)
    if screen_number == 1:
        screen_number = screen1()
    elif screen_number == 2:
        screen_number = screen2()
    else:
        screen_number = screen3()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()
pygame.quit()

