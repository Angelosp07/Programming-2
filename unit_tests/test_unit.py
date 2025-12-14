import unittest


from components import initialise_board, legal_move, flip_pieces, legal_move_exists
from components import  calculate_winner, ai_move, LIGHT, DARK, NONE


class TestInitialiseBoard(unittest.TestCase):

    def test_dimensions(self):
        board = initialise_board()

        self.assertEqual(len(board), 8)

        for row in board:
            self.assertEqual(len(row), 8)

    def test_center_pieces(self):
        board = initialise_board()
        
        self.assertEqual(board[3][3], LIGHT)
        self.assertEqual(board[3][4], DARK)
        self.assertEqual(board[4][3], DARK)
        self.assertEqual(board[4][4], LIGHT)

    def test_remaining_squares_empty(self):
        board = initialise_board()

        for i in range(8):
            for j in range(8):
                if (i, j) not in [(3,3), (3,4), (4,3), (4,4)]:
                    self.assertEqual(board[j][i], NONE)



class TestLegalMove(unittest.TestCase):
    #fresh board
    def setUp(self):
        self.board = initialise_board()

    def test_valid_first_move(self):
        self.assertTrue(legal_move(DARK, (4, 3), self.board))

    def test_occupied_move(self):
        self.assertFalse(legal_move(DARK, (4, 4), self.board))

    def test_out_of_bounds(self):
        self.assertFalse(legal_move(DARK, (0, 0), self.board))
        self.assertFalse(legal_move(DARK, (9, 9), self.board))

    def test_invalid_flanking(self):
        self.assertFalse(legal_move(DARK, (1, 1), self.board))


class TestFlipPieces(unittest.TestCase):
    #fresh board
    def setUp(self):
        self.board = initialise_board()

    def test_chosen_piece_placed(self):
        flip_pieces(DARK, (4, 3), self.board)

        self.assertEqual(self.board[2][3], DARK)

    def test_single_flip(self):
        flip_pieces(DARK, (4, 3), self.board)

        self.assertEqual(self.board[3][3], DARK)

    def test_multiple_flips(self):
        flip_pieces(DARK, (4, 3), self.board)
        flip_pieces(LIGHT, (3, 3), self.board)

        self.assertEqual(LIGHT, self.board[3][3])
        self.assertEqual(DARK, self.board[3][4])



class TestLegalMoveExists(unittest.TestCase):

    def test_moves_exist_at_start(self):
        board = initialise_board()

        self.assertTrue(legal_move_exists(board, DARK))

    def test_no_moves_available(self):
        board = []

        for _ in range(8):
            row = [DARK] * 8
            board.append(row)

        self.assertFalse(legal_move_exists(board, LIGHT))


class TestCalculateWinner(unittest.TestCase):

    def test_light(self):
        board = []
        for _ in range(8):
            row = [LIGHT] * 8
            board.append(row)

        light_num, dark_num, winner = calculate_winner(board)

        self.assertEqual(light_num, 64)
        self.assertEqual(dark_num, 0)
        self.assertEqual(winner, LIGHT)

    def test_dark(self):
        board = []
        for _ in range(8):
            row = [DARK] * 8
            board.append(row)
            light_num, dark_num, winner = calculate_winner(board)

        self.assertEqual(light_num, 0)
        self.assertEqual(dark_num, 64)
        self.assertEqual(winner, DARK)

    def test_draw(self):
        board = []

        for _ in range(8):
            board.append([LIGHT] * 4)
            board.append([DARK] * 4)

        light_num, dark_num, winner = calculate_winner(board)

        self.assertEqual(light_num, dark_num)
        self.assertEqual(winner, NONE)


class TestAIMove(unittest.TestCase):

    def test_ai_return(self):
        board = initialise_board()
        move = ai_move(board)

        self.assertTrue(move is None or isinstance(move, tuple))

    def test_ai_move_legal(self):
        board = initialise_board()
        move = ai_move(board)

        if move is not None:
            self.assertTrue(legal_move(LIGHT, move, board))


if __name__ == "__main__":
    unittest.main()
