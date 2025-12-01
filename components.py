def initialise_board(size=8):
    L = "Light"
    D = "Dark "
    N = "None "

    board = [[]]

    for i in range(size):
        row = []

        for j in range(size):

            row.append(N)
            board.append(row)

b = initialise_board()
print(b)