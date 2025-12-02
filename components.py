def initialise_board(size=8):
    L = "Light"
    D = "Dark "
    N = "None "

    board = []

    for i in range(size):
        row = []

        for j in range(size):

            row.append(N)
        board.append(row)


    board[3][3] = L
    board[3][4] = D
    board[4][3] = D
    board[4][4] = L
    return board

b = initialise_board()
print(b)