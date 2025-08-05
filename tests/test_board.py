from bnc import Board


class TestBoard:
    def test_init_board(self):
        board1 = Board()
        # default: code_length=4, num_of_colors=6, num_of_guesses=10
        expected_board1 = [[0, 0, 0, 0] for _ in range(10)]
        assert board1._board == expected_board1

        board2 = Board(code_length=5, num_of_guesses=11)
        expected_board2 = [[0, 0, 0, 0, 0] for _ in range(11)]
        assert board2._board == expected_board2
