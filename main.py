import pygame
import numpy as np
import sys
import math
import pygame_gui


p1 = str # initialize with a default value
p2 = str # initialize with default value
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
    selected_colors = set()
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
            if RED not in selected_colors:
                colour_p1 = RED
                selected_colors.add(RED)
        yellow_p1 = pygame.draw.rect(screen, YELLOW, [560, 110, 100, 20], 0, 5)
        if yellow_p1.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            if YELLOW not in selected_colors:
                colour_p1 = YELLOW
                selected_colors.add(YELLOW)
        blue_p1 = pygame.draw.rect(screen, BLUE, [560, 130, 100, 20], 0, 5)
        if blue_p1.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            if BLUE not in selected_colors:
                colour_p1 = BLUE
                selected_colors.add(BLUE)
        green_p1 = pygame.draw.rect(screen, GREEN, [560, 150, 100, 20], 0, 5)
        if green_p1.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            if GREEN not in selected_colors:
                colour_p1 = GREEN
                selected_colors.add(GREEN)

        red_p2 = pygame.draw.rect(screen, RED, [560, 200, 100, 20], 0, 5)
        if red_p2.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            global colour_p2
            if RED not in selected_colors:
                colour_p2 = RED
                selected_colors.add(RED)
        yellow_p2 = pygame.draw.rect(screen, YELLOW, [560, 220, 100, 20], 0, 5)
        if yellow_p2.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            if YELLOW not in selected_colors:
                colour_p2 = YELLOW
                selected_colors.add(YELLOW)
        blue_p2 = pygame.draw.rect(screen, BLUE, [560, 240, 100, 20], 0, 5)
        if blue_p2.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            if BLUE not in selected_colors:
                colour_p2 = BLUE
                selected_colors.add(BLUE)
        green_p2 = pygame.draw.rect(screen, GREEN, [560, 260, 100, 20], 0, 5)
        if green_p2.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            if GREEN not in selected_colors:
                colour_p2 = GREEN
                selected_colors.add(GREEN)

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
    # pygame.draw.rect(screen, 'black',[100,100,300,300])
    draw_board(board)
    pygame.display.update()

    myfont = pygame.font.SysFont("monospace", 75)
    game_over = False
    turn = 0

    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            #pygame.draw.circle(screen, RED, (600, 25), RADIUS / 2)
            #pygame.draw.circle(screen, YELLOW, (650, 25), RADIUS / 2)



            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                # print(event.pos)
                # Ask for Player 1 Input
                if turn == 0:
                    global turn_count_p1
                    turn_count_p1+=1
                    global remaining_count_p1
                    global winnername
                    global winnercolor
                    remaining_count_p1 -=1
                    print(remaining_count_p1)
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)

                        if winning_move(board, 1):
                            global turn_count
                            turn_count=str(turn_count_p1)
                            global winner
                            winner = p1
                            winnercolor = colour_p1
                            label = myfont.render(p1 + " wins!!", 1, colour_p1)
                            screen.blit(label, (100, 10))
                            game_over = True

                # # Ask for Player 2 Input
                else:
                    global turn_count_p2
                    turn_count_p2 += 1
                    global remaining_count_p2

                    remaining_count_p2-=1
                    print(remaining_count_p2)
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)

                        if winning_move(board, 2):
                            turn_count=str(turn_count_p2)
                            winner = p2
                            winnercolor = colour_p2
                            label = myfont.render(p2 + " wins!!", 1, colour_p2)
                            screen.blit(label, (100, 10))
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


    #if menu_btn_3.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
        #screen1()
        #return 1


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