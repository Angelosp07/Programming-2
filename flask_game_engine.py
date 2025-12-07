from flask import Flask, render_template, request
from components import initialise_board, flip_pieces, legal_move_exists, legal_move, calculate_winner, light, dark, none
import json

app = Flask(__name__)

board = initialise_board()
current_colour = dark
finished = False
game_file = "othello_game_file.json"

@app.route('/')
def index():
    return render_template('OthelloBoard.html', game_board = board)



#The function will go on to define how to get the x and y coordinate arguments and store them as variables,
# and then check that the move is legal, 
# and if so calculate the outcome of the move.

@app.route('/move')
def move():

    global board, current_colour, finished

    # get coords
    try:
        x = int(request.args.get("x"))
        y = int(request.args.get("y"))

    except:
        return {'status': 'fail', 'board': board, 'message': 'problem with coordinates'}

    #check legality of move
    if legal_move(current_colour, (x, y), board) == False:
        return {'status': 'fail', 'board': board, 'message': 'Illegal move!'}

    #flip pieces
    flip_pieces(current_colour, (x,y), board)

    #switch player
    if current_colour == dark:
        current_colour = light
    else:
        current_colour = dark

    #check legal move exists for current player, if not pass turn
    if legal_move_exists(board, current_colour) == False:

        #passing turn
        if current_colour == dark:
            current_colour = light
        else:
            current_colour = dark

        #check legal move exists for passed player, if not game over
        if legal_move_exists(board, current_colour) == False:
            finished = True
            light_num, dark_num, winner = calculate_winner(board)
            msg = "Winner is " + winner + " | Light: " + str(light_num) + " | Dark: " + str(dark_num)
            return {'finished': 'Game Over', 'board': board, 'message': msg}


    return {'status': 'success', 'board': board, 'player': current_colour}

#additional restart board functionality
@app.route('/restart')
def restart():
    global board, current_colour, finished
    board = initialise_board()
    current_colour = dark
    finished = False
    return {"status": "success", "board": board, "player": current_colour, "message": "Game state restarted"}

#save game state into json file
@app.route('/save')
def save():
    global board, current_colour

    data = {'board': board, 'current_colour': current_colour}
    with open(game_file, "w") as file:
        json.dump(data, file)
    return {'status': 'success', 'message': 'Game state saved'}

#attempt to load game state
@app.route('/load')
def load():
    global board, current_colour
    try:
        with open(game_file, "r") as file:
            data = json.load(file)
        board = data["board"]
        current_colour = data["current_colour"]
        return {'status': 'success', "board": board, "player": current_colour, 'message': 'Game state loaded'}
    except:
        return {'status': 'fail', 'message': 'Game state not found'}



if __name__ == "__main__":
    app.run(debug=True)
