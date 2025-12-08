"""
Module providing web server functionality for Othello/Reversi using flask

Imports game logic from components such as:
- Board initialisation
- Flipping pieces
- Checking legal moves
- Calculating the winner
- AI move generation

Imports constants:
- LIGHT
- DARK

Dependencies: 
- Flask
"""
import json
import time
from flask import Flask, render_template, request
from components import initialise_board, flip_pieces, legal_move_exists, legal_move
from components import calculate_winner, ai_move, LIGHT, DARK

app = Flask(__name__)

board = initialise_board()
CURRENT_COLOUR = DARK
FINISHED = False
GAME_FILE = "othello_game_file.json"

@app.route('/')
def index():
    """
    Displays current state of the board using the OthelloBoard.html file

    Returns:
        HTML page of the board state
    """
    return render_template('OthelloBoard.html', game_board = board)

@app.route('/move')
def move():
    """
    Retrieves (x,y) coords of clicked square, checks if move is legal,
    applies it if legal and updates the game state.
    If the game isn't over the ai makes a move after the player,
    checks to see if game is over and calculates winner if so.

    Returns:
        dict: JSON:
            - status (str, optional): "success" or "fail" depending on move legality or input
            - board (list[list]): new state of the board
            - player (str, optional): player after the move
            - message (str, optional): info about move legality, errors, or outcomes
            - finished (str, optional): passed only if game is over
    """
    global board, CURRENT_COLOUR, FINISHED

    # get coords
    try:
        x = int(request.args.get("x"))
        y = int(request.args.get("y"))
    except (TypeError, ValueError):
        return {'status': 'fail',
                'board': board,
                'message': 'problem with coordinates'
                }

    #check legality of move
    if not legal_move(CURRENT_COLOUR, (x, y), board):
        return {'status': 'fail',
                'board': board,
                'message': 'Illegal move!'
                }
    flip_pieces(CURRENT_COLOUR, (x,y), board)
    CURRENT_COLOUR = LIGHT

    #if game still in play do ai's turn
    if not FINISHED:
        ai_square = ai_move(board)
        if ai_square is not None:
            time.sleep(0.20)
            flip_pieces(LIGHT, ai_square, board)
            #switch players if ai makes move
            CURRENT_COLOUR = DARK

    #check legal move exists for human if not check ai
    if not legal_move_exists(board, DARK):
        #check legal move exists for ai, if not game over
        if not legal_move_exists(board, CURRENT_COLOUR):
            FINISHED = True
            light_num, dark_num, winner = calculate_winner(board)
            msg = "Winner is " + winner
            msg += " | Light: " + str(light_num) + " | Dark: " + str(dark_num)
            return {'finished': 'Game Over',
                    'board': board,
                    'message': msg
                    }
        #if ai can move it has another turn
        CURRENT_COLOUR = LIGHT
    else:
        # human's turn
        CURRENT_COLOUR = DARK
    return {'status': 'success',
            'board': board,
            'player': CURRENT_COLOUR
            }

@app.route('/restart')
def restart():
    """
    Sets the board to its initial state, current player to dark, FINISHED as False

    Returns:
        dict: 
            - status (str): "success"
            - board (list[list]): board that was reset
            - player (str): new current player after restart
            - message (str): "Game state restarted"
    """
    global board, CURRENT_COLOUR, FINISHED
    board = initialise_board()
    CURRENT_COLOUR = DARK
    FINISHED = False
    return {'status': 'success',
            'board': board,
            'player': CURRENT_COLOUR, 
            'message': 'Game state restarted'
            }

@app.route('/save')
def save():
    """
    Saves the current game state to a .json file.

    Returns:
        dict: JSON:
            - status (str): 'success'
            - message (str): 'Game state saved'
    """
    global board, CURRENT_COLOUR

    data = {'board': board, 'current_colour': CURRENT_COLOUR}
    with open(GAME_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file)
    return {'status': 'success',
            'message': 'Game state saved'
            }

@app.route('/load')
def load():
    """
    Saves the current game state to a .json file.

    Returns:
        dict: JSON:
            - status (str): 'success'
            - board (list[list], optional): board state in file, passed upon success
            - player (str, optional): current player saved in file, passed upon success
            - message (str): 'Game state loaded'

    """
    global board, CURRENT_COLOUR
    try:
        with open(GAME_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
        board = data["board"]
        CURRENT_COLOUR = data["current_colour"]
        return {'status': 'success',
                'board': board, 
                'player': CURRENT_COLOUR, 
                'message': 'Game state loaded'
                }
    except FileNotFoundError:
        return {'status': 'fail',
                'message': 'Game state not found'
                }

if __name__ == "__main__":
    app.run(debug=True)
