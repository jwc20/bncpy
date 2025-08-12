from unittest.mock import Mock

import pytest

from bnc import Board, Player


class TestPlayerInitialization:
    def test_basic_initialization(self):
        board = Board()
        player = Player("Alice", board)
        assert player.name == "Alice"
        assert player.board is board

    def test_player_with_configured_board(self):
        board = Board(code_length=5, num_of_colors=8)
        player = Player("Bob", board)
        assert player.board.code_length == 5
        assert player.board.num_of_colors == 8


class TestPlayerProperties:
    def test_game_over_property(self):
        board = Board(secret_code="1234", num_of_guesses=1)
        player = Player("Alice", board)

        assert player.game_over is False
        player.make_guess("5555")
        assert player.game_over is True

    def test_game_won_property(self):
        board = Board(secret_code="1234")
        player = Player("Alice", board)

        assert player.game_won is False
        player.make_guess("1234")
        assert player.game_won is True

    def test_properties_delegation(self):
        board = Mock()
        board.game_over = True
        board.game_won = False

        player = Player("Alice", board)
        assert player.game_over is True
        assert player.game_won is False


class TestSetSecretCode:
    def test_set_secret_code(self):
        board = Board()
        player = Player("Alice", board)

        player.set_secret_code_to_board("1234")
        assert player.board.secret_code == "1234"

    def test_set_none_secret_code(self):
        board = Board()
        player = Player("Alice", board)

        with pytest.raises(ValueError, match="secret code cannot be None"):
            player.set_secret_code_to_board(None)


class TestMakeGuess:
    def test_successful_guess(self):
        board = Board(secret_code="1234")
        player = Player("Alice", board)

        player.make_guess("1234")
        assert player.game_won is True
        assert board.board[0].bulls == 4

    def test_incorrect_guess(self):
        board = Board(secret_code="1234")
        player = Player("Alice", board)

        player.make_guess("5555")
        assert player.game_won is False
        assert board.board[0].bulls == 0

    def test_multiple_guesses(self):
        board = Board(secret_code="1234")
        player = Player("Alice", board)

        player.make_guess("5555")
        player.make_guess("1111")
        player.make_guess("1234")

        assert board.board[0].guess == [5, 5, 5, 5]
        assert board.board[1].guess == [1, 1, 1, 1]
        assert board.board[2].guess == [1, 2, 3, 4]
        assert player.game_won is True

    def test_invalid_guess_format(self):
        board = Board(secret_code="1234")
        player = Player("Alice", board)

        with pytest.raises(ValueError, match="Code must contain only digits"):
            player.make_guess("12ab")

    def test_invalid_guess_length(self):
        board = Board(secret_code="1234")
        player = Player("Alice", board)

        with pytest.raises(ValueError, match="Code must be exactly 4 digits long"):
            player.make_guess("123")

    def test_invalid_guess_range(self):
        board = Board(secret_code="1234", num_of_colors=6)
        player = Player("Alice", board)

        with pytest.raises(ValueError, match="Digit 7 is out of range"):
            player.make_guess("1237")


class TestPlayerBoardInteraction:
    def test_board_state_tracking(self):
        board = Board(secret_code="1234")
        player = Player("Alice", board)

        assert board.current_board_row_index == 0
        player.make_guess("5555")
        assert board.current_board_row_index == 1
        player.make_guess("6666")
        assert board.current_board_row_index == 2

    def test_board_reference_not_copy(self):
        board = Board(secret_code="1234")
        player = Player("Alice", board)

        player.make_guess("5555")
        assert board.board[0].is_filled is True
        assert player.board.board[0].is_filled is True
        assert board is player.board
