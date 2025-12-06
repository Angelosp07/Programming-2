from flask import Flask, render_template, request
from components import initialise_board, flip_pieces, legal_move_exists, legal_move,  light, dark, none

app = Flask(__name__)

board = initialise_board()
current_colour = dark
finished = False

@app.route('/')
def index():
    return render_template('OthelloBoard.html', game_board = board)



#The function will go on to define how to get the x and y coordinate arguments and store them as variables,
# and then check that the move is legal, 
# and if so calculate the outcome of the move.

@app.route('/move')
def move():

    global board, current_colour, finished

    if finished:
        return {'status': 'fail', 'message': 'Game is finished.', 'board': board}

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
            return {'finished': 'Game Over', 'board': board}

    return {'status': 'success', 'board': board, 'player': current_colour}


if __name__ == "__main__":
    app.run(debug=True)
