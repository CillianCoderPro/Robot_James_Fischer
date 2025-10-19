import chess
from sys import exit
import pygame
from bot import bot_turn
pygame.init()

screen_width = 640
screen_height = 640
square_size = screen_width // 8

screen = pygame.display.set_mode((screen_width, screen_height ),pygame.RESIZABLE)
pygame.display.set_caption("Robot James Fischer")
Clock = pygame.time.Clock()


board = chess.Board()

def mouse_square():
    mouse_pos = pygame.mouse.get_pos()
    file = mouse_pos[0] // square_size
    rank = 7 - (mouse_pos[1] // square_size)

    square = chess.square(file, rank)
    return square

def draw_board():

    light_square = pygame.Surface((square_size, square_size))
    light_square.fill((255, 248, 220))
    dark_square = pygame.Surface((square_size, square_size))
    dark_square.fill((210, 180, 140))

    for n in range(8):
        for i in range(8):
            if (i + n) % 2 == 0:
                screen.blit(light_square, (i * square_size, n * square_size))
            elif (i + n) % 2 == 1:
                screen.blit(dark_square, (i * square_size, n * square_size))



def draw_pieces(hovered_square):
    piece_pos = {}
    for square in chess.SQUARES:

        if square == hovered_square:
            piece_size = 70
        else:
            piece_size = 60

        piece = board.piece_at(square)

        file = chess.square_file(square)
        rank = chess.square_rank(square)

        if piece:
            if piece.color:
                piece_image = pygame.image.load(f'images/white pieces/{piece.symbol()}.png').convert_alpha()
                piece_image = pygame.transform.scale(piece_image, (piece_size, piece_size))

            else:
                piece_image = pygame.image.load(f'images/black pieces/{piece.symbol()}.png').convert_alpha()
                piece_image = pygame.transform.scale(piece_image, (piece_size, piece_size))

            piece_rect = piece_image.get_rect()
            piece_rect.center = ( file * square_size + square_size // 2, (7 - rank) * square_size + square_size //2 )
            screen.blit(piece_image, piece_rect)

            piece_pos[(file,rank)] = piece_rect

def cursor(width, colour, selected_piece):

    # mouse position
    mouse_pos = pygame.mouse.get_pos()

    # snaps the cursor square to the grid
    cursor_x = mouse_pos[0] // square_size * square_size
    cursor_y = mouse_pos[1] // square_size * square_size

    # draw cursor
    draw_board()
    draw_pieces(mouse_square())
    pygame.draw.rect(screen, colour, ( cursor_x, cursor_y, square_size, square_size ), width)
    """"
    if selected_piece:
        piece_image = pygame.image.load(f'images/black pieces/{selected_piece}.png').convert_alpha()
        piece_image = pygame.transform.scale(piece_image, (70, 70))
        piece_rect = piece_image.get_rect()
        piece_rect.center = mouse_pos[0], mouse_pos[1]
        screen.blit(piece_image, piece_rect)
    """

    pygame.display.update()

def user_turn(square1):
    square2 = None
    print("Click on two squares")

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                cursor(1, "black", "b")

                square = chess.square_name(mouse_square())

                # Check if this is the first or second square being clicked
                if square1 is None:
                    square1 = square
                    print(f"First square: {square1}")
                else:
                    square2 = square
                    print(f"Second square: {square2}")

                    # Check if both squares are selected
                    if square1 and square2:
                        move = square1 + square2  # e.g., 'e2e4'
                        try:
                            #play the move if it's legal
                            chess_move = chess.Move.from_uci(move)
                            if chess_move in board.legal_moves:
                                board.push(chess_move)
                                return
                            # play the move if queen promotion makes it legal
                            chess_move = chess.Move.from_uci(move+"q")
                            if chess_move in board.legal_moves:
                                board.push(chess_move)
                                return
                            else:
                                return user_turn(square2)  # Reset and try again

                        except Exception as e:
                            print(f"Move failed: {e}, try again")
                            return user_turn(square2)  # Reset and try again
            else:
                cursor(1, "black", None)




while not board.is_game_over():


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    draw_board()
    print(board)
    draw_pieces(None)
    pygame.display.update()

    #If the game isn't over
    if not board.is_game_over():
        #board.push(bot_turn(board, 4))
        user_turn(None)

    draw_board()
    print(board)
    draw_pieces(None)
    pygame.display.update()

    #If the game isn't over
    if not board.is_game_over():
        board.push(bot_turn(board, 4))
        #user_turn(None)


    Clock.tick(60)

outcome = board.outcome()
print("result = ", outcome.result())


