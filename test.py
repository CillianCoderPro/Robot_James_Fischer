import math
from chess import *

"""test file for test functions"""


# returns the square root of the number of moves a piece can make + counted double if move is a capture
def mobility(board, square):
    number_of_moves = 0
    for move in board.legal_moves:
        if move.from_square == square:
            number_of_moves += 1
            if board.is_capture(move):
                number_of_moves += 1
    return math.sqrt(number_of_moves)