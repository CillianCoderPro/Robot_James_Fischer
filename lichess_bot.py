import chess.pgn
import chess.engine
import berserk
import time
from bot import *

TOKEN = "lip_Shsk362V2cpVncZwYLuP"
session = berserk.TokenSession(TOKEN)
client = berserk.Client(session)


def handle_game_event(event):
    game_id = event['game']['id']
    board = chess.Board(event.get('fen', chess.STARTING_FEN))
    applied_moves = set()

    while True:
        try:
            for state in client.bots.stream_game_state(game_id):
                if state['type'] in ['gameFull', 'gameState']:
                    moves = state.get('moves', '')
                    for move in moves.split():
                        if move not in applied_moves:
                            board.push_uci(move)
                            applied_moves.add(move)

                    move = bot_turn(board, 4)
                    if move:
                        client.bots.make_move(game_id, move.uci())
                        time.sleep(1)
        except Exception as e:
            time.sleep(1)
            move = bot_turn(board, 4)  # Generate a move using your bot's logic
            print(f"Bot's move: {move.uci()}")
            print(board)  # Log the board state before the move
            if move:
                try:
                    # Ensure the move is legal before sending it to Lichess
                    client.bots.make_move(game_id, move.uci())  # Send the move to Lichess
                    print(f"Played move {move.uci()}")
                    time.sleep(1)  # Add a delay between moves
                except Exception as e:
                    print(f"Error making move: {e}")
            else:
                print("No valid moves found!")
        else:
            print(f"Unhandled state type: {state['type']}")

# Listen to incoming challenges
for event in client.bots.stream_incoming_events():
    if event['type'] == 'challenge':
        client.bots.accept_challenge(event['challenge']['id'])
        print(f"Challenge accepted: {event['challenge']['id']}")
    elif event['type'] == 'gameStart':
        handle_game_event(event)
