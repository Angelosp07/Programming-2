import random

light = "Light"
dark = "Dark "
none = "None "

def initialise_board(size=8):
    board = []

    for i in range(size):
        row = []

        for j in range(size):
            row.append(none)
        board.append(row)


    board[3][3] = light
    board[3][4] = dark 
    board[4][3] = dark
    board[4][4] = light
    return board

def legal_move(colour, coordinate, board):
    x = coordinate[0] - 1
    y = coordinate[1] - 1
    
#validate coordinates
    if x < 0 or x > 7 or y < 0 or y > 7:
        return False

#determine opponent
    if colour == dark:
        opponent = light
    else:
        opponent = dark

#represents vector translations
    vectors = [
        (-1,-1), (-1,0), (-1,1),
        (0, -1),         (0, 1),
        (1, -1), (1, 0), (1, 1)
        ]

#validate chosen square
    if board[y][x] != none:
        return False

#main part
    # for each vector transformation
    for (i, j) in vectors:

        #move in that direction
        xx = x + i
        yy = y + j
        found_opponent = False

        #while still inside board, check along the whole direction to see if flanking
        while xx >= 0 and xx < 8 and yy >= 0 and yy < 8:
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
    x = coordinate[0] - 1
    y = coordinate[1] - 1

    #determine opponent
    if colour == dark:
        opponent = light
    else:
        opponent = dark
   
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
        while xx >= 0 and xx < 8 and yy >= 0 and yy < 8:
            square = board[yy][xx]
            #only three outcomes for each piece in direction:

            #if oppenent piece encountered: record locattion in flank line
            if square == opponent:
                flank_line.append((xx,yy))
            
            #if own piece encountered
            elif square == colour:
                #flip pieces recorded in flank line list
                for (a, b) in flank_line:
                    board[b][a] = colour
                #move onto next possible vector flank
                break

#if empty square
            else:

                break
        
#move to next square in direction
            xx += i
            yy += j

def legal_move_exists(board, colour):
    length = len(board)

    #checks whole board for legal moves
    for x in range(length):
        for y in range(length):
            if legal_move(colour, (x + 1, y + 1), board):
                return True
    return False

def calculate_winner(board):
    light_num = 0
    dark_num = 0
    winner = ""
    
    for row in board:
        for square in row:
            if square == light:
                light_num += 1
            elif square == dark:
                dark_num += 1

    if light_num > dark_num:
        winner = light
    elif dark_num > light_num:
        winner = dark
    else:
        winner = none

    return light_num, dark_num, winner

# AI MOVES SECTION

def find_possible_squares(board, colour=light):
    possible_squares = []
    for x in range(1, 9):
        for y in range(1, 9):
            if legal_move(colour, (x, y), board):
                possible_squares.append((x, y))
    return possible_squares

def count_flipped(board_before, board_after, colour=light):
    flipped = 0
    for x in range(8):
        for y in range(8):
            #counts flipped pieces, ignoring "none " squares
            if board_before[y][x] != colour and board_after[y][x] == colour:
                flipped += 1
    return flipped

def ai_move(board, colour=light):
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

