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


#Create a function called print_board that accepts a board as an argument and prints an ascii representation of the board state to the command line.

def print_board(board):
    top_nums = " |"
    for i in range(1, len(board) + 1):
        top_nums += "[" + str(i) + "]"
    
    print(top_nums)

    side_nums = 1
    for row in board:
        R = ""

        for square in row:
            if square == none:
                R += "[ ]"
            elif square == light:
                R += "[O]"
            elif square == dark:
                R += "[*]"
        
        print(str(side_nums)+"|" + R)
        side_nums +=1


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
