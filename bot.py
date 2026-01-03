import chess
import chess.pgn
import repertoire
from operator import itemgetter
import math
import chess




# this is the whole function that will end up choosing what move to play
def bot_turn(board, depth):

    # reverses tuples
    def reverse(tuple):
        return tuple[::-1]

    """
    # values of pieces
    pawn_value = 10
    knight_value = 30
    bishop_value = 30
    rook_value = 50
    queen_value = 100
    """

    # map of where the pieces should go
    white_piece_map = {
        chess.PAWN: (
            10, 10, 10, 10, 10, 10, 10, 10,
            10, 10, 10, 10, 10, 10, 10, 10,
            20, 12, 10, 10, 10, 10, 12, 10,
            11, 11, 5, 15, 15, 5, 11, 11,
            12, 12, 12, 14, 14, 12, 12, 12,
            14, 14, 11, 13, 13, 11, 14, 14,
            16, 16, 16, 16, 16, 16, 16, 16,
            10, 10, 10, 10, 10, 10, 10, 10
        ),
        chess.KNIGHT: (
            30, 30, 30, 30, 30, 30, 30, 30,
            30, 30, 30, 30, 30, 30, 30, 30,
            28, 30, 32, 30, 30, 32, 30, 28,
            29, 30, 30, 32, 32, 30, 30, 29,
            30, 32, 32, 33, 33, 32, 32, 30,
            34, 34, 34, 34, 34, 34, 34, 34,
            30, 30, 30, 30, 30, 30, 30, 30,
            30, 30, 30, 30, 30, 30, 30, 30
        ),
        chess.BISHOP: (
            30, 30, 30, 30, 30, 30, 30, 30,
            30, 33, 30, 30, 30, 30, 33, 30,
            30, 30, 30, 31, 31, 30, 30, 30,
            30, 30, 33, 30, 30, 33, 30, 30,
            30, 33, 30, 30, 30, 30, 33, 30,
            30, 30, 30, 30, 30, 30, 30, 30,
            30, 30, 30, 30, 30, 30, 30, 30,
            30, 30, 30, 30, 30, 30, 30, 30
        ),
        chess.ROOK: (
            50, 50, 50, 50, 50, 50, 50, 50,
            50, 50, 50, 50, 50, 50, 50, 50,
            50, 50, 50, 50, 50, 50, 50, 50,
            50, 50, 50, 50, 50, 50, 50, 50,
            50, 50, 50, 50, 50, 50, 50, 50,
            50, 50, 50, 50, 50, 50, 50, 50,
            50, 50, 50, 50, 50, 50, 50, 50,
            50, 50, 50, 50, 50, 50, 50, 50
        ),
        chess.QUEEN: (
            100, 100, 100, 100, 100, 100, 100, 100,
            100, 103, 100, 100, 100, 100, 103, 100,
            100, 100, 100, 101, 101, 100, 100, 100,
            100, 100, 103, 100, 100, 103, 100, 100,
            100, 103, 100, 100, 100, 100, 103, 100,
            100, 100, 100, 100, 100, 100, 100, 100,
            100, 100, 100, 100, 100, 100, 100, 100,
            100, 100, 100, 100, 100, 100, 100, 100
        ),
        chess.KING: (
            103, 102, 99, 99, 99, 99, 102, 103,
            100, 100, 100, 100, 100, 100, 100, 100,
            100, 100, 100, 100, 100, 100, 100, 100,
            100, 100, 100, 100, 100, 100, 100, 100,
            100, 100, 100, 100, 100, 100, 100, 100,
            100, 100, 100, 100, 100, 100, 100, 100,
            95, 100, 100, 100, 100, 100, 100, 95,
            90, 95, 100, 100, 100, 100, 95, 90
        )
    }

    # creates a symmetrical map of the white map
    black_piece_map = {chess.PAWN: reverse(white_piece_map[chess.PAWN]),
                       chess.KNIGHT: reverse(white_piece_map[chess.KNIGHT]),
                       chess.BISHOP: reverse(white_piece_map[chess.BISHOP]),
                       chess.ROOK: reverse(white_piece_map[chess.ROOK]),
                       chess.QUEEN: reverse(white_piece_map[chess.QUEEN]),
                       chess.KING: reverse(white_piece_map[chess.KING]),
    }

    # uses the piece values and map to evaluate the position

    def mobility(board, square):
        number_of_moves = 0
        for move in board.legal_moves:
            if move.from_square == square:
                number_of_moves += 1
                if board.is_capture(move):
                    number_of_moves += 1
        print(number_of_moves)
        return math.sqrt(number_of_moves)


    def evaluate(board):

        """
        if board.can_claim_threefold_repetition:
            return 0
        """

        white_sum = 0
        black_sum = 0

        if len(list(board.legal_moves)) == 0:
            if board.is_check():
                if board.turn:
                    # White loss
                    return -100000000000000000000000000000000
                else:
                    # Black loss
                    return 100000000000000000000000000000000
            else:
                # draw
                return 0

        for square in board.piece_map():
            piece = board.piece_at(square)
            if piece:
                """
                if piece.piece_type == chess.PAWN:
                    value = pawn_value
                elif piece.piece_type == chess.KNIGHT:
                    value = knight_value
                elif piece.piece_type == chess.BISHOP:
                    value = bishop_value
                elif piece.piece_type == chess.ROOK:
                    value = rook_value
                elif piece.piece_type == chess.QUEEN:
                    value = queen_value
                else:
                    value = 0
                """

                if piece.color == 1:
                    value = white_piece_map[piece.piece_type][square]
                    white_sum += value # + mobility(board, square)
                elif piece.color == 0:
                    value = black_piece_map[piece.piece_type][square]
                    black_sum +=  value # + mobility(board, square)



        return white_sum - black_sum



    def get_ordered_moves(position):
        moves = []
        for move in position.legal_moves:
            position.push(move)
            score = evaluate(position)
            moves.append((move, score))
            position.pop()
        moves.sort(key=itemgetter(1), reverse=position.turn)  # Sort moves by evaluation, descending for maximizing
        return [move for move, score in moves]

    ###########################################################################################################

    def minimax(position, depth, alpha, beta, maximizing_player):
        #legal_moves = position.legal_moves
        best_move = None

        if depth == 0 or position.is_game_over():
            return evaluate(position), best_move

        if maximizing_player:
            max_eval = -float("inf")
            for move in get_ordered_moves(position):
                position.push(move)
                if position.is_capture(move):
                    evaluation, _ = minimax(position, depth - 1, alpha, beta, False)
                else:
                    evaluation = evaluate(position)
                position.pop()
                if evaluation > max_eval:
                    max_eval = evaluation
                    best_move = move
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            return max_eval, best_move

        else:
            min_eval = float("inf")
            for move in get_ordered_moves(position):
                position.push(move)
                if position.is_capture(move):
                    evaluation, _ = minimax(position, depth - 1, alpha, beta, True)
                else:
                    evaluation = evaluate(position)
                position.pop()
                if evaluation < min_eval:
                    min_eval = evaluation
                    best_move = move
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            return min_eval, best_move


    """
    if board.turn:
        best_move = repertoire.colour_move(board, "white")
        if best_move == None:
            _, best_move = minimax(board, depth, -float("inf"), float("inf"), True)
    else:
        best_move = repertoire.colour_move(board, "black")
        if best_move == None:
            _, best_move = minimax(board, depth, -float("inf"), float("inf"), False)

    board.push(best_move)
    return best_move"""


    if board.turn:
        _, best_move = minimax(board, depth, -float("inf"), float("inf"), True)
    else:
        _, best_move = minimax(board, depth, -float("inf"), float("inf"), False)
    return best_move



##########################################    Lichess     ##################################################