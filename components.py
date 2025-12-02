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





print_board(initialise_board())