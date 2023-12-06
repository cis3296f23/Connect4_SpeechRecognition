import pygame
import sys
import math
import pygame_gui
import random
from speechRecognition import SpeechRecognizer
from gameLogic import GameLogic

p1 = "Player 1"  # initialize with a default value
p2 = "Player 2"  # initialize with default value
dif = "easy"
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 139, 148)
YELLOW = (250, 238, 7)
BLUE = (0, 251, 255)
GREEN = (124, 252, 0)
colour_p1 = RED
colour_p1_sig = RED
colour_p2 = YELLOW
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
turn_count_p1 = 0
turn_count_p2 = 0
remaining_count_p1 = 21
remaining_count_p2 = 21
CLOCK = pygame.time.Clock()
winnername = str
gl = GameLogic(ROW_COUNT, COLUMN_COUNT)
sr = SpeechRecognizer()

num_dict = {
    'one': '1',
    'two': '2',
    'to': '2',
    'three': '3',
    'four': '4',
    'for': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
}

board = gl.create_board()
gl.print_board(board)
game_over = False
turn = 0

pygame.init()

width = (COLUMN_COUNT) * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

RADIUS = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode([width, height])
pygame.display.set_caption('Connect4')
fps = 60

timer = pygame.time.Clock()
screen_number = 0
font = pygame.font.Font('freesansbold.ttf', 24)

MANAGER = pygame_gui.UIManager((width, height))
TEXT_INPUT1 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((350, 105), (200, 50)), manager=MANAGER,
                                                  object_id="#first_text_entry")
TEXT_INPUT2 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((350, 205), (200, 50)), manager=MANAGER,
                                                  object_id="#second_text_entry")

def screen0():  # Main Menu
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill('dark blue')  # Updated background color

        # Title
        title_font = pygame.font.SysFont("calibri", 100, True)  # Larger and bold font for the title
        title_text = title_font.render("Connect4", True, 'gold')
        title_rect = title_text.get_rect(center=(width // 2, height // 2 - 150))
        screen.blit(title_text, title_rect)

        # Single Player button
        single_player_btn = pygame.draw.rect(screen, 'light yellow', [width // 2 - 130, height // 2 - 50, 260, 60], 0,
                                             5)
        pygame.draw.rect(screen, 'blue', [width // 2 - 130, height // 2 - 50, 260, 60], 5, 5)
        text_single_player = font.render('Single Player', True, 'black')
        text_single_player_rect = text_single_player.get_rect(center=single_player_btn.center)
        screen.blit(text_single_player, text_single_player_rect)

        # Multiplayer button
        multiplayer_btn = pygame.draw.rect(screen, 'light yellow', [width // 2 - 130, height // 2 + 50, 260, 60], 0, 5)
        pygame.draw.rect(screen, 'blue', [width // 2 - 130, height // 2 + 50, 260, 60], 5, 5)
        text_multiplayer = font.render('Multiplayer', True, 'black')
        text_multiplayer_rect = text_multiplayer.get_rect(center=multiplayer_btn.center)
        screen.blit(text_multiplayer, text_multiplayer_rect)

        # Developer Section
        developed_font = pygame.font.SysFont("", 25, False)
        developed_by_text = developed_font.render('Developed by:\n'
                                                  'Angelo Lim\n'
                                                  'Christopher Douglas\n'
                                                  'Jeswin James\n'
                                                  'Josh Sabio\n', True, 'white')
        developed_by_rect = developed_by_text.get_rect(bottomright=(width - 10, height - 10))
        screen.blit(developed_by_text, developed_by_rect)

        pygame.display.flip()

        if single_player_btn.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return 4  # Single Player option selected
        elif multiplayer_btn.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return 1  # Multiplayer option selected

        pygame.display.update()


def screen1(): # Multiplayer Menu
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
        menu_btn = pygame.draw.rect(screen, 'light gray', [230, 500, 260, 60], 0, 5)
        pygame.draw.rect(screen, 'dark gray', [230, 500, 260, 60], 5, 5)
        text = font.render('Start game', True, 'black')
        screen.blit(text, (295, 517))

        menu_btn_menu = pygame.draw.rect(screen, 'light gray', [230, 600, 260, 60], 0, 5)
        pygame.draw.rect(screen, 'dark gray', [230, 600, 260, 60], 5, 5)
        text = font.render('Back', True, 'black')
        screen.blit(text, (325, 617))

        if menu_btn.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return 2

        if menu_btn_menu.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            turn = 0
            remaining_count_p1 = 21
            remaining_count_p2 = 21
            board = gl.create_board()
            return 0

        pygame.display.update()


def screen2(): # Multiplayer Game
    global previous_screen
    previous_screen = 2
    # pygame.draw.rect(screen, 'black',[100,100,300,300])
    gl.draw_board(board, screen, RADIUS, height, colour_p1, colour_p2)
    pygame.display.update()

    myfont = pygame.font.SysFont("monospace", 75)
    game_over = False
    turn = 0

    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # pygame.draw.circle(screen, RED, (600, 25), RADIUS / 2)
            # pygame.draw.circle(screen, YELLOW, (650, 25), RADIUS / 2)

            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            # print(event.pos)
            # Ask for Player 1 Input
            if turn == 0:
                global turn_count_p1
                turn_count_p1 += 1
                global remaining_count_p1
                global winnername
                global winnercolor
                remaining_count_p1 -= 1
                print(remaining_count_p1)
                col = None
                while (col == None):
                    col = sr.speech_recognition_move(gl, board)
                posx = col * SQUARESIZE

                if gl.is_valid_location(board, col):
                    row = gl.get_next_open_row(board, col)
                    gl.drop_piece(board, row, col, 1)

                    if gl.winning_move(board, 1):
                        global turn_count
                        turn_count = str(turn_count_p1)
                        global winner
                        winner = p1
                        winnercolor = colour_p1
                        label = myfont.render(p1 + " wins!!", 1, colour_p1)
                        screen.blit(label, (100, 10))
                        game_over = True

            # Ask for Player 2 Input
            elif turn != 0:
                global turn_count_p2
                turn_count_p2 += 1
                global remaining_count_p2

                remaining_count_p2 -= 1
                print(remaining_count_p2)
                col = None
                while (col == None):
                    col = sr.speech_recognition_move(gl, board)
                posx = col * SQUARESIZE

                if gl.is_valid_location(board, col):
                    row = gl.get_next_open_row(board, col)
                    gl.drop_piece(board, row, col, 2)

                    if gl.winning_move(board, 2):
                        turn_count = str(turn_count_p2)
                        winner = p2
                        winnercolor = colour_p2
                        label = myfont.render(p2 + " wins!!", 1, colour_p2)
                        screen.blit(label, (100, 10))
                        game_over = True

            gl.print_board(board)
            gl.draw_board(board, screen, RADIUS, height, colour_p1, colour_p2)

            turn += 1
            turn = turn % 2

            if game_over:
                pygame.time.wait(2000)
                scr_no = 3
                screen_number = scr_no

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
    return 3, winner, winnercolor


def screen3(): # Win Screen
    global winnercolor
    global winner  # Declare winner as a global variable if it's not already passed as an argument
    text1 = font.render(winner + ' wins!', True, winnercolor)  # Ensure winner is a string
    screen.blit(text1, (225, 125))
    text2 = font.render('CONGRATULATIONS!!', True, 'white')
    screen.blit(text2, (225, 150))

    # Play again button
    menu_btn_again = pygame.draw.rect(screen, 'light gray', [230, 400, 260, 60], 0, 5)
    pygame.draw.rect(screen, 'dark gray', [230, 400, 260, 60], 5, 5)
    text = font.render('Play again', True, 'black')
    screen.blit(text, (300, 418))

    # QUIT button
    menu_btn_quit = pygame.draw.rect(screen, 'light gray', [230, 300, 260, 60], 0, 5)
    pygame.draw.rect(screen, 'dark gray', [230, 300, 260, 60], 5, 5)
    text = font.render('Quit', True, 'black')
    screen.blit(text, (325, 318))

    # MENU button
    menu_btn_menu = pygame.draw.rect(screen, 'light gray', [230, 200, 260, 60], 0, 5)
    pygame.draw.rect(screen, 'dark gray', [230, 200, 260, 60], 5, 5)
    text = font.render('Menu', True, 'black')
    screen.blit(text, (325, 218))

    if menu_btn_quit.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
        pygame.quit()
        sys.exit()

    if menu_btn_again.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
        global board
        global game_over
        global turn
        global remaining_count_p1
        global remaining_count_p2
        board = gl.create_board()
        game_over = False
        turn = 0
        remaining_count_p1 = 21
        remaining_count_p2 = 21

        if previous_screen == 2:
            return 2
        elif previous_screen == 5:
            return 5

    if menu_btn_menu.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
        turn = 0
        remaining_count_p1 = 21
        remaining_count_p2 = 21
        board = gl.create_board()
        return 0

    return 3


def screen4(): # Single Player Menu
    global previous_screen
    previous_screen = 5
    ai = True
    error_message = ""

    while ai:
        UI_REFRESH_RATE = CLOCK.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#first_text_entry":
                global p1
                p1 = event.text
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#second_text_entry":
                global dif
                dif = event.text

            MANAGER.process_events(event)
        MANAGER.update(UI_REFRESH_RATE)
        screen.fill('black')
        MANAGER.draw_ui(screen)
        global p2
        p2 = "AI"
        red_p1 = pygame.draw.rect(screen, RED, [560, 100, 100, 20], 0, 5)
        if red_p1.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            global colour_p1
            colour_p1 = RED

        green_p1 = pygame.draw.rect(screen, GREEN, [560, 120, 100, 20], 0, 5)
        if green_p1.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            colour_p1 = GREEN

        blue_p1 = pygame.draw.rect(screen, BLUE, [560, 140, 100, 20], 0, 5)
        if blue_p1.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            colour_p1 = BLUE

        player1_text = font.render('Enter Player 1 name: ', True, colour_p1)
        screen.blit(player1_text, (100, 117))
        player1_enter = font.render('(and press ENTER) ', True, colour_p1)
        screen.blit(player1_enter, (100, 147))

        dif_text = font.render('Enter difficulty level:', True, YELLOW)
        screen.blit(dif_text, (100, 217))
        dif_text = font.render('(easy, medium, hard)', True, YELLOW)
        screen.blit(dif_text, (100, 247))
        dif_enter = font.render('(and press ENTER) ', True, YELLOW)
        screen.blit(dif_enter, (100, 277))

        menu_btn = pygame.draw.rect(screen, 'light gray', [230, 500, 260, 60], 0, 5)
        pygame.draw.rect(screen, 'dark gray', [230, 500, 260, 60], 5, 5)
        text = font.render('Start game', True, 'black')
        screen.blit(text, (295, 517))

        menu_btn_menu = pygame.draw.rect(screen, 'light gray', [230, 600, 260, 60], 0, 5)
        pygame.draw.rect(screen, 'dark gray', [230, 600, 260, 60], 5, 5)
        text = font.render('Back', True, 'black')
        screen.blit(text, (325, 617))

        MANAGER.update(UI_REFRESH_RATE)
        MANAGER.draw_ui(screen)

        if error_message:
            error_text = font.render(error_message, True, RED)
            screen.blit(error_text, (100, 317))

        if menu_btn.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            if dif not in ["easy", "medium", "hard"]:
                error_message = ("Invalid difficulty level.\n"
                                 "Please enter 'easy', 'medium', or 'hard'.")
            else:
                ai = False
        if menu_btn_menu.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            turn = 0
            remaining_count_p1 = 21
            remaining_count_p2 = 21
            board = gl.create_board()
            return 0

        pygame.display.update()
    return 5


def computer_move():
    global dif
    global turn_count
    global winner
    global winnercolor
    global turn_count_p2
    global remaining_count_p2

    if dif == "easy":
        print("Difficulty: Easy\n")
        turn_count_p2 += 1
        remaining_count_p2 -= 1
        print(remaining_count_p2)

        col = random.randint(0, COLUMN_COUNT - 1)  # Generate a random column

        if gl.is_valid_location(board, col):
            row = gl.get_next_open_row(board, col)
            gl.drop_piece(board, row, col, 2)

        return False

    elif dif == "medium":
        print("Difficulty: Medium\n")
        turn_count_p2 += 1
        remaining_count_p2 -= 1
        print(remaining_count_p2)

        col = choose_medium_column(board)
        valid_columns = [col for col in range(COLUMN_COUNT) if gl.is_valid_location(board, col)]

        if gl.is_valid_location(board, col) and col is not None and valid_columns:
            row = gl.get_next_open_row(board, col)
            gl.drop_piece(board, row, col, 2)

        return False

    elif dif == "hard":
        print("Difficulty: Hard\n")
        turn_count_p2 += 1
        remaining_count_p2 -= 1
        print(remaining_count_p2)

        col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)
        valid_columns = [col for col in range(COLUMN_COUNT) if gl.is_valid_location(board, col)]

        if gl.is_valid_location(board, col) and col is not None and valid_columns:
            row = gl.get_next_open_row(board, col)
            gl.drop_piece(board, row, col, 2)

        return False


def choose_medium_column(board):
    # Check for potential winning moves
    for col in range(COLUMN_COUNT):
        temp_board = board.copy()
        if gl.is_valid_location(temp_board, col):
            row = gl.get_next_open_row(temp_board, col)
            gl.drop_piece(temp_board, row, col, 2)

            if gl.winning_move(temp_board, 2):
                return col

    # Check for opponent's potential winning moves and block them
    for col in range(COLUMN_COUNT):
        temp_board = board.copy()
        if gl.is_valid_location(temp_board, col):
            row = gl.get_next_open_row(temp_board, col)
            gl.drop_piece(temp_board, row, col, 1)

            if gl.winning_move(temp_board, 1):
                return col

    # If no winning or blocking move, choose a random valid column
    valid_columns = [col for col in range(COLUMN_COUNT) if gl.is_valid_location(board, col)]
    return random.choice(valid_columns)


def evaluate_board(board):
    # Constants for weights
    WINNING_SCORE = 1000
    BLOCKING_SCORE = 100
    TWO_IN_A_ROW_SCORE = 10
    ONE_IN_A_ROW_SCORE = 1

    score = 0

    # Check for winning moves
    if gl.winning_move(board, 2):  # Computer wins
        return WINNING_SCORE
    elif gl.winning_move(board, 1):  # Opponent wins
        return -WINNING_SCORE

    # Check for potential winning moves and blocking moves
    for col in range(COLUMN_COUNT):
        for row in range(ROW_COUNT):
            if board[row][col] == 0:  # Empty space
                # Check for potential winning move for the computer
                temp_board = [row[:] for row in board]  # Create a copy of the board
                gl.drop_piece(temp_board, row, col, 2)
                if gl.winning_move(temp_board, 2):
                    score += BLOCKING_SCORE

                # Check for potential winning move for the opponent
                temp_board = [row[:] for row in board]
                gl.drop_piece(temp_board, row, col, 1)
                if gl.winning_move(temp_board, 1):
                    score -= BLOCKING_SCORE

    # Check for two in a row and one in a row for the computer
    for col in range(COLUMN_COUNT - 1):
        for row in range(ROW_COUNT):
            if board[row][col] == 2 and board[row][col + 1] == 2:
                score += TWO_IN_A_ROW_SCORE
            elif board[row][col] == 2 and board[row][col + 1] == 0:
                score += ONE_IN_A_ROW_SCORE

    # Check for two in a row and one in a row for the opponent
    for col in range(COLUMN_COUNT - 1):
        for row in range(ROW_COUNT):
            if board[row][col] == 1 and board[row][col + 1] == 1:
                score -= TWO_IN_A_ROW_SCORE
            elif board[row][col] == 1 and board[row][col + 1] == 0:
                score -= ONE_IN_A_ROW_SCORE

    return score


def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = gl.get_valid_locations(board)
    is_terminal = gl.is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if gl.winning_move(board, 2):
                return (None, 100000000000000)
            elif gl.winning_move(board, 1):
                return (None, -10000000000000)
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, gl.score_position(board, 2))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = gl.get_next_open_row(board, col)
            b_copy = board.copy()
            gl.drop_piece(b_copy, row, col, 2)
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:  # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = gl.get_next_open_row(board, col)
            b_copy = board.copy()
            gl.drop_piece(b_copy, row, col, 1)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


def screen5(): # Single PLayer Game
    global winner
    global winnercolor

    gl.draw_board(board, screen, RADIUS, height, colour_p1, colour_p2)
    pygame.display.update()

    myfont = pygame.font.SysFont("monospace", 75)
    game_over = False
    player1_turn = True  # Flag to track if it's Player 1's turn

    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if not game_over:
                if player1_turn:  # Player 1's turn
                    col = sr.speech_recognition_move(gl, board)
                    if col is not None:
                        posx = col * SQUARESIZE
                        if gl.is_valid_location(board, col):
                            row = gl.get_next_open_row(board, col)
                            gl.drop_piece(board, row, col, 1)
                            gl.print_board(board)
                            gl.draw_board(board, screen, RADIUS, height, colour_p1, colour_p2)

                            if gl.winning_move(board, 1):
                                turn_count = str(turn_count_p1)
                                winner = p1
                                winnercolor = colour_p1
                                label = myfont.render(p1 + " wins!!", 1, colour_p1)
                                screen.blit(label, (100, 10))
                                game_over = True
                            else:
                                player1_turn = False  # Switch to Computer's turn
                else:  # Computer's turn
                    if not computer_move():
                        pygame.time.wait(2000)  # Wait before dropping piece
                        gl.print_board(board)
                        gl.draw_board(board, screen, RADIUS, height, colour_p1, colour_p2)
                        if gl.winning_move(board, 2):
                            turn_count = str(turn_count_p2)  # Update the turn count for the computer
                            winner = p2
                            winnercolor = colour_p2
                            label = myfont.render(p2 + " wins!!", 1, colour_p2)
                            screen.blit(label, (100, 10))
                            game_over = True
                        else:
                            player1_turn = True  # Switch back to Player 1's turn

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                if player1_turn:
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

        if game_over:
            pygame.time.wait(1000)  # Wait for a moment to display the victory message
            return 3, winner, winnercolor  # Transition to screen3

    return 5

run = True
while run:
    screen.fill('black')
    timer.tick(fps)
    if screen_number == 0:
        screen_number = screen0()
    elif screen_number == 1:
        screen_number = screen1()
    elif screen_number == 2:
        screen_number = screen2()
    elif screen_number == 4:
        screen_number = screen4()
    elif screen_number == 5:
        screen_number = screen5()
    else:
        screen_number = screen3()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

pygame.quit()
