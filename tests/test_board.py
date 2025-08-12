import pytest

from bnc import Board
from bnc.board import BoardRow


class TestBoardRow:
    def test_winning_row(self):
        row = BoardRow(guess=[1, 2, 3, 4], bulls=4, cows=0, is_filled=True)
        assert row.is_winning_row is True

    def test_non_winning_row(self):
        row = BoardRow(guess=[1, 2, 3, 4], bulls=2, cows=1, is_filled=True)
        assert row.is_winning_row is False

    def test_unfilled_row(self):
        row = BoardRow(guess=[1, 2, 3, 4], bulls=4, cows=0, is_filled=False)
        assert row.is_winning_row is False


class TestBoardInitialization:
    def test_default_initialization(self):
        board = Board()
        assert board.code_length == 4
        assert board.num_of_colors == 6
        assert board.num_of_guesses == 10
        assert board.secret_code is None

    def test_custom_initialization(self):
        board = Board(code_length=5, num_of_colors=8, num_of_guesses=12)
        assert board.code_length == 5
        assert board.num_of_colors == 8
        assert board.num_of_guesses == 12

    def test_with_secret_code(self):
        board = Board(secret_code="1234")
        assert board.secret_code == "1234"

    def test_invalid_code_length(self):
        with pytest.raises(ValueError, match="code_length must be at least 3"):
            Board(code_length=2)

    def test_invalid_num_colors(self):
        with pytest.raises(ValueError, match="num_of_colors must be at least 5"):
            Board(num_of_colors=4)

    def test_invalid_num_guesses(self):
        with pytest.raises(ValueError, match="num_of_guesses must be at least 1"):
            Board(num_of_guesses=0)


class TestBoardProperties:
    def test_current_board_row_index_empty(self):
        board = Board()
        assert board.current_board_row_index == 0

    def test_current_board_row_index_partial(self):
        board = Board(secret_code="1234")
        board.evaluate_guess(0, "5555")
        assert board.current_board_row_index == 1

    def test_current_board_row_index_full(self):
        board = Board(num_of_guesses=2, secret_code="1234")
        board.evaluate_guess(0, "5555")
        board.evaluate_guess(1, "6666")
        assert board.current_board_row_index == -1

    def test_game_states(self):
        board = Board(secret_code="1234")
        assert board.game_won is False
        assert board.game_over is False

        board.evaluate_guess(0, "1234")
        assert board.game_won is True
        assert board.game_over is True


class TestSecretCode:
    def test_set_secret_code(self):
        board = Board()
        board.secret_code = "1234"
        assert board.secret_code == "1234"

    def test_invalid_secret_code_none(self):
        board = Board()
        with pytest.raises(ValueError, match="secret code cannot be None"):
            board.secret_code = None

    def test_invalid_secret_code_length(self):
        board = Board(code_length=4)
        with pytest.raises(ValueError, match="Code must be exactly 4 digits long"):
            board.secret_code = "123"

    def test_invalid_secret_code_format(self):
        board = Board()
        with pytest.raises(ValueError, match="Code must contain only digits"):
            board.secret_code = "12ab"

    def test_invalid_secret_code_range(self):
        board = Board(num_of_colors=6)
        with pytest.raises(ValueError, match="Digit 7 is out of range"):
            board.secret_code = "1237"


class TestEvaluateGuess:
    def test_all_bulls(self):
        board = Board(secret_code="1234")
        board.evaluate_guess(0, "1234")
        row = board.board[0]
        assert row.bulls == 4
        assert row.cows == 0
        assert board.game_won is True

    def test_all_cows(self):
        board = Board(secret_code="1234")
        board.evaluate_guess(0, "4321")
        row = board.board[0]
        assert row.bulls == 0
        assert row.cows == 4

    def test_mixed_bulls_cows(self):
        board = Board(secret_code="1234")
        board.evaluate_guess(0, "1324")
        row = board.board[0]
        assert row.bulls == 2
        assert row.cows == 2

    def test_no_matches(self):
        board = Board(secret_code="1234")
        board.evaluate_guess(0, "5566")
        row = board.board[0]
        assert row.bulls == 0
        assert row.cows == 0

    def test_duplicate_digits_secret(self):
        board = Board(secret_code="1123")
        board.evaluate_guess(0, "1111")
        row = board.board[0]
        assert row.bulls == 2
        assert row.cows == 0

    def test_duplicate_digits_guess(self):
        board = Board(secret_code="1234")
        board.evaluate_guess(0, "1144")
        row = board.board[0]
        assert row.bulls == 2
        assert row.cows == 0

    def test_evaluate_without_secret(self):
        board = Board()
        with pytest.raises(ValueError, match="Secret code must be set"):
            board.evaluate_guess(0, "1234")

    def test_evaluate_invalid_row_index(self):
        board = Board(secret_code="1234", num_of_guesses=5)
        with pytest.raises(ValueError, match="Row index is out of range"):
            board.evaluate_guess(5, "1234")

    def test_game_over_on_last_guess(self):
        board = Board(secret_code="1234", num_of_guesses=2)
        board.evaluate_guess(0, "5555")
        board.evaluate_guess(1, "6666")
        assert board.game_over is True
        assert board.game_won is False


class TestBoardMethods:
    def test_check_board_row_index(self):
        board = Board(num_of_guesses=5)
        assert board.check_board_row_index(0) is True
        assert board.check_board_row_index(4) is True
        assert board.check_board_row_index(5) is False
        assert board.check_board_row_index(-1) is False

    def test_create_new_board(self):
        board1 = Board(code_length=5, num_of_colors=7, secret_code="12345")
        board2 = board1.create_new_board()

        assert board2.code_length == board1.code_length
        assert board2.num_of_colors == board1.num_of_colors
        assert board2.num_of_guesses == board1.num_of_guesses
        assert board2.secret_code == board1.secret_code
        assert board2 is not board1

    def test_set_board_row(self):
        board = Board()
        board.set_board_row(2, 1, [1, 2, 3, 4], 3)

        row = board.board[3]
        assert row.bulls == 2
        assert row.cows == 1
        assert row.guess == [1, 2, 3, 4]
        assert row.is_filled is True
