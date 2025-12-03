def initialise_board(size=8):
    board = []

    for i in range(size):
        row = []

        for j in range(size):
            row.append("None ")
        board.append(row)


    board[3][3] = "Light"
    board[3][4] = "Dark "
    board[4][3] = "Dark "
    board[4][4] = "Light"
    return board


#Create a function called print_board that accepts a board as an argument and prints an ascii representation of the board state to the command line.

def print_board(board):

    for row in board:
        R = []

        for square in row:
            if square == "None ":
                R.append("[ ]")
            elif square == "Light":
                R.append("[O]")
            elif square == "Dark ":
                R.append("[*]")
        
        print("".join(R))


def legal_move(colour, coordinate, board):
    x = coordinate[0]
    y = coordinate[1]
    

#determine opponent
    if colour.strip() == "Dark":
        opponent = "Light"
    else:
        opponent = "Dark"

#represents vector translations
    vectors = [
        (-1,-1), (-1,0), (-1,1),
        (0, -1),         (0, 1),
        (1, -1), (1, 0), (1, 1)
        ]
    

#validate coordinates
    if x < 1 or x > 8 or y < 1 or y > 8:
        return False
    
#validate chosen square
    if board[x-1][y-1] != "None ":
        return False


#main part
    # for each vector transformation
    for (i, j) in vectors:

        #move in that direction
        row = x-1 + i
        col = y-1 + j
        found_opponent = False

        #while still inside board, check along the whole direction to see if flanking
        while row >= 0 and row < 8 and col >= 0 and col < 8:
            square = board[row][col].strip()

            #only three outcomes for each piece in direction:

            #if oppenent piece encountered
            if square == opponent:
                found_opponent = True
            
            #if own piece encountereed
            elif square == colour.strip():
                #(and flanking)
                if found_opponent == True:
                    return True
                break

            #if empty square
            else:
                break
        
            #move to next square in direction
            row += i
            col += j

    #if no directions flank the oppenent piece:
    return False


board = initialise_board()
test = legal_move("Light",(6,4),board)
print(test)