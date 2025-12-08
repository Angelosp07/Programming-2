"""Module providing game logic for flask_game_engine.py"""
import random

LIGHT = "Light"
DARK = "Dark "
NONE = "None "

def initialise_board(size=8):
    """
    Initialises board.

    Args:
        size (int, optional): length of rows. Defaults to 8

    Returns: 
        list of lists representing board.
    """
    board = []

    for _ in range(size):
        row = []
        for _ in range(size):
            row.append(NONE)
        board.append(row)

    board[3][3] = LIGHT
    board[3][4] = DARK
    board[4][3] = DARK
    board[4][4] = LIGHT
    return board

def legal_move(colour, coordinate, board):
    """
    Checks if colour provided has a legal move at coordinates of board
    
    Args:
        colour (str): colour of player who made the move
        coordinate (tuple[int, int]): location (row, col) of said move
        board (list[list]): current playing board

    Returns:
        bool: True if move is legal, vice versa

    """
    x = coordinate[0] - 1
    y = coordinate[1] - 1

#validate coordinates
    if x < 0 or x > 7 or y < 0 or y > 7:
        return False

#determine opponent
    if colour == DARK:
        opponent = LIGHT
    else:
        opponent = DARK

#represents vector translations
    vectors = [
        (-1,-1), (-1,0), (-1,1),
        (0, -1),         (0, 1),
        (1, -1), (1, 0), (1, 1)
        ]

#validate chosen square
    if board[y][x] != NONE:
        return False

#main part
    # for each vector transformation
    for (i, j) in vectors:

        #move in that direction
        xx = x + i
        yy = y + j
        found_opponent = False

        #while still inside board, check along the whole direction to see if flanking
        while 0 <= xx < 8 and 0 <= yy < 8:
            square = board[yy][xx]

            #only three outcomes for each piece in direction:

            #if oppenent piece encountered
            if square == opponent:
                found_opponent = True

            #if own piece encountereed
            elif square == colour:
                #(and flanking)
                if found_opponent:
                    return True
                break

            #if empty square
            else:
                break
            #move to next square in direction
            xx += i
            yy += j

    #if no directions flank the oppenent piece:
    return False

def flip_pieces(colour, coordinate, board):
    """
    Flips all possible pieces of opponent based on the parameters provided
    
    Args:
        colour (str): colour of player who placed the piece
        coordinate (tuple[int, int]): location (row, col) of said piece
        board (list[list]): current playing board

    Returns:
        None: global board is modified
    """
    x = coordinate[0] - 1
    y = coordinate[1] - 1

    #determine opponent
    if colour == DARK:
        opponent = LIGHT
    else:
        opponent = DARK

    #represents vector translations
    vectors = [
        (-1,-1), (-1,0), (-1,1),
        (0, -1),         (0, 1),
        (1, -1), (1, 0), (1, 1)
        ]

    #place first piece
    board[y][x] = colour

    # for each vector transformation
    for (i, j) in vectors:
        #record flank line for current vector
        flank_line = []
        #move in that direction
        xx = x + i
        yy = y + j
        #while still inside board, check along the whole flank line to see if flanking
        # flip pieces if so
        while 0 <= xx < 8 and 0 <= yy < 8:
            square = board[yy][xx]

            #if oppenent piece encountered: record location in flank line
            if square == opponent:
                flank_line.append((xx,yy))
            #if own piece encountered flip pieces recorded in flank line list
            elif square == colour:
                for (a, b) in flank_line:
                    board[b][a] = colour
                #move onto next possible vector flank
                break
            #break if empty square
            else:
                break
            #move to next square in direction
            xx += i
            yy += j

def legal_move_exists(board, colour):
    """
    Analyses whole board square by square for prescence of possible moves for a certain colour

    Args:
        board (list[list]): current playing board
        colour (str): colour of current player

    Returns:
        bool: True if moves exists, else False
    """
    length = len(board)
    for x in range(length):
        for y in range(length):
            if legal_move(colour, (x + 1, y + 1), board):
                return True
    return False

def calculate_winner(board):
    """
    Calculates winner when the game is finished by counting each colour's pieces and comparing

    Args:
        board (list[list]): playing board at end of the game

    Returns:
        light_num (int): number of light pieces
        dark_num (int): number of dark pieces
        winner (str): whichever colour has most pieces, NONE if draw
    """
    light_num = 0
    dark_num = 0
    winner = ""

    for row in board:
        for square in row:
            if square == LIGHT:
                light_num += 1
            elif square == DARK:
                dark_num += 1

    if light_num > dark_num:
        winner = LIGHT
    elif dark_num > light_num:
        winner = DARK
    else:
        winner = NONE

    return light_num, dark_num, winner

def find_possible_squares(board, colour=LIGHT):
    """
    Creates list of possible legal moves for the ai by checking each square and appending if legal
    
    Args:
        board (list[list]): current playing board
        colour (str, optional): colour of ai's pieces. Defaults to LIGHT

    Returns:
        possible_squares (list[tuple[x, y]]): list of coordinates (row, col) with legal squares
    """
    possible_squares = []
    for x in range(1, 9):
        for y in range(1, 9):
            if legal_move(colour, (x, y), board):
                possible_squares.append((x, y))
    return possible_squares

def count_flipped(board_before, board_after, colour=LIGHT):
    """
    Counts the number of flipped pieces for the ai's move. 
    Done square by square with respect to a board before the flips occured and a board after.
    
    Args:
        board_before (list[list]): playing board before pieces were flipped
        board_after (list[list]): playing board after pieces were flipped
        colour (str, optional): colour of ai's pieces. Defaults to LIGHT

    Returns:
        flipped (int): number of flipped pieces
    """
    flipped = 0
    for x in range(8):
        for y in range(8):
            #counts flipped pieces, ignoring "None " squares
            if board_before[y][x] != colour and board_after[y][x] == colour:
                flipped += 1
    return flipped

def ai_move(board, colour=LIGHT):
    """
    Counts the number of flipped pieces a given legal square would flip.
    Adds a random number 0-1 to the flipped number to give the human an advantage.
    Returns the square with the highest score (may not be best move).
        
    Args:
        board (list[list]): current playing board
        colour (str, optional): colour of ai's pieces. Defaults to LIGHT

    Returns:
        best_square (tuple[x, y]): coordinates of ai's predicted best move
    """
    possible_squares = find_possible_squares(board)

    if len(possible_squares) == 0:
        return None

    best_square = None
    best_score = 0

    #evaluate move for each possible square
    for square in possible_squares:

        #create copy of board
        new_board = []
        for row in board:
            new_row = list(row)
            new_board.append(new_row)

        #apply move
        flip_pieces(colour, square, new_board)

        flipped = count_flipped(board, new_board)

        #change score randomly by (0-1), giving player a slight advantage
        current_score = flipped + random.random()

        #record best score and corresponding square
        if current_score > best_score:
            best_score = current_score
            best_square = square

    return best_square
