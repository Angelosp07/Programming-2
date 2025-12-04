from components import initialise_board ,legal_move, print_board, light, dark, none

def cli_coords_input():

    x = 0
    y = 0
    print("")
    print("Please input the coordinates of your move")
    print("")

    #check range
    while x < 1 or x > 8 :
        print("Input the x coordinate (1-8 inclusive)")

        try:
            x = int(input())
        except ValueError:
            print("Not an integer")
            print("")
            x = 0

    while y < 1 or y > 8:
        print("Input the y coordinate (1-8 inclusive)")

        try:
            y = int(input())
        except ValueError:
            print("Not an integer")
            print("")
            y = 0
        

    return (x,y)

def simple_game_loop():

    #start game with welcome message
    print("Welcome to Othello!")
    print("")
    print("Dark (*) goes first")

    #initialise the board, set first player
    board = initialise_board()
    current_colour = dark

    #setting move counter to 60
    move_counter = 60


    while move_counter > 0:
        print_board(board)
        print(current_colour, "is the current player.")

        #check legal move exists for current player, if not pass turn
        if legal_move_exists(board, current_colour) == False:
            print("No legal moves for", current_colour)
            print("Passing turn...")
            if current_colour == dark:
                current_colour = light
            else:
                current_colour = dark
            print("")
            print("Current colour is", current_colour)

            #check legal move exists for passed player, if not game over
            if legal_move_exists(board, current_colour) == False:
                print("No legal moves for either player...")
                print("")
                display_winner(board)
                break
            continue

        #make sure user enters legal move
        (x, y) = (0, 0)
        while legal_move(current_colour, (x, y), board) == False:

            (x, y) = cli_coords_input()
            if legal_move(current_colour, (x, y), board) == False:
                print("")
                print("ILLEGAL MOVE. TRY AGAIN")
                print("")
                print_board(board)
                print("")

        #flips pieces
        flip_pieces(current_colour, (x, y), board)
        move_counter -= 1

        if current_colour == dark:
            current_colour = light
        else:
            current_colour = dark
    
    
    display_winner(board)


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

def display_winner(board):
    light_num = 0
    dark_num = 0

    #
    for row in board:
        for square in row:
            if square == light:
                light_num += 1
            elif square == dark:
                dark_num += 1

    print_board(board)
    print("")
    print("GAME OVER")
    print("")
    print("THE WINNER IS")

    if light_num > dark_num:
        print("LIGHT!!!")
    elif dark_num > light_num:
        print("DARK!!!")
    else:
        print("NEITHER...")
        print("ITS A DRAW!!!")

    print(light_num)
    print(dark_num)


if __name__ == "__main__":
    simple_game_loop()





