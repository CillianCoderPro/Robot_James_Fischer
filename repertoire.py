import chess
import chess.pgn
import random
from collections import defaultdict

# Global cache for opening moves
openings_cache = {}

# Load your games from the PGN file
def load_games_from_pgn(pgn_file_path):
    games = []
    with open(pgn_file_path) as pgn_file:
        while True:
            game = chess.pgn.read_game(pgn_file)
            if game is None:
                break
            games.append(game)
    return games

# Extract openings into a dictionary
def extract_openings(games):
    openings = defaultdict(lambda: defaultdict(int))

    for game in games:
        board = game.board()
        for move in game.mainline_moves():
            fen_before_move = board.fen()
            openings[fen_before_move][move] += 1  # Count each move occurrence for each FEN
            board.push(move)

    # Convert counts to a random-weighted selection
    weighted_openings = {}
    for fen, move_counts in openings.items():
        moves, weights = zip(*move_counts.items())  # Separate moves and their weights
        weighted_openings[fen] = random.choices(moves, weights=weights, k=1)[0]  # Choose a move based on weights

    return weighted_openings

# Get openings for a specific color, caching them
def get_openings_for_colour(colour):
    if colour not in openings_cache:
        pgn_file_path = f"GrafterChess-{colour}.pgn"
        games = load_games_from_pgn(pgn_file_path)
        openings_cache[colour] = extract_openings(games)
    return openings_cache[colour]

def colour_move(position, colour):
    openings = get_openings_for_colour(colour)
    return openings.get(position.fen(), None)
