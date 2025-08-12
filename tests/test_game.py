from unittest.mock import patch

import pytest

from bnc import Board, Game, Player
from bnc.game import CurrentGameStatus


class TestGameInitialization:
    def test_empty_players(self):
        with pytest.raises(ValueError, match="Players cannot be empty"):
            Game([])

    def test_single_player(self):
        player = Player("Alice", Board(secret_code="1234"))
        game = Game([player])
        assert len(game.players) == 1
        assert game.state == CurrentGameStatus.SETUP

    def test_multiple_players(self):
        players = [Player("Alice", Board()), Player("Bob", Board())]
        game = Game(players, secret_code="1234")
        assert len(game.players) == 2

    def test_inconsistent_board_configs(self):
        players = [
            Player("Alice", Board(code_length=4)),
            Player("Bob", Board(code_length=5)),
        ]
        with pytest.raises(
            ValueError, match="All players must have boards with same configuration"
        ):
            Game(players)

    def test_different_num_colors(self):
        players = [
            Player("Alice", Board(num_of_colors=6)),
            Player("Bob", Board(num_of_colors=7)),
        ]
        with pytest.raises(
            ValueError, match="All players must have boards with same configuration"
        ):
            Game(players)


class TestSecretCodeManagement:
    def test_set_secret_code_for_all(self):
        players = [Player("Alice", Board()), Player("Bob", Board())]
        game = Game(players, secret_code="1234")

        for player in game.players:
            assert player.board.secret_code == "1234"


class TestGameState:
    def test_in_progress_state(self):
        player = Player("Alice", Board(secret_code="1234"))
        game = Game([player])
        game.submit_guess(player, "5555")
        assert game.state == CurrentGameStatus.IN_PROGRESS

    def test_finished_state_all_players(self):
        players = [
            Player("Alice", Board(secret_code="1234", num_of_guesses=1)),
            Player("Bob", Board(secret_code="1234", num_of_guesses=1)),
        ]
        game = Game(players)

        game.submit_guess(players[0], "5555")
        game.submit_guess(players[1], "5555")

        assert game.state == CurrentGameStatus.FINISHED


class TestSubmitGuess:
    def test_successful_guess(self):
        player = Player("Alice", Board(secret_code="1234"))
        game = Game([player])

        game.submit_guess(player, "1234")
        assert player.game_won is True
        assert game.winner == player

    def test_unsuccessful_guess(self):
        player = Player("Alice", Board(secret_code="1234"))
        game = Game([player])

        game.submit_guess(player, "5555")
        assert player.game_won is False
        assert game.winner is None

    def test_player_game_over(self):
        player = Player("Alice", Board(secret_code="1234", num_of_guesses=1))
        game = Game([player])

        game.submit_guess(player, "5555")
        assert player.game_over is True

        game.submit_guess(player, "1234")
        assert player.game_won is False

    def test_multiple_winners(self):
        players = [
            Player("Alice", Board(secret_code="1234")),
            Player("Bob", Board(secret_code="1234")),
            Player("Charlie", Board(secret_code="1234")),
        ]
        game = Game(players)

        game.submit_guess(players[0], "1234")
        game.submit_guess(players[1], "1234")
        game.submit_guess(players[2], "1234")

        assert len(game.winners) == 3
        assert game.winners[0] == players[0]
        assert game.winners[1] == players[1]
        assert game.winners[2] == players[2]


class TestWinnerTracking:
    def test_no_winner_initially(self):
        player = Player("Alice", Board(secret_code="1234"))
        game = Game([player])
        assert game.winner is None
        assert len(game.winners) == 0

    def test_single_winner(self):
        player = Player("Alice", Board(secret_code="1234"))
        game = Game([player])
        game.submit_guess(player, "1234")

        assert game.winner == player
        assert len(game.winners) == 1

    def test_winner_order(self):
        players = [
            Player("Alice", Board(secret_code="1234")),
            Player("Bob", Board(secret_code="1234")),
        ]
        game = Game(players)

        game.submit_guess(players[1], "1234")
        game.submit_guess(players[0], "1234")

        assert game.winner == players[1]
        assert game.winners[0] == players[1]
        assert game.winners[1] == players[0]


class TestLogging:
    @patch("bnc.game.logger")
    def test_winner_logging(self, mock_logger):
        player = Player("Alice", Board(secret_code="1234"))
        game = Game([player])
        game.submit_guess(player, "1234")

        mock_logger.info.assert_called_with(
            "%s won the game in %s place!", "Alice", "first"
        )

    @patch("bnc.game.logger")
    def test_player_already_won_logging(self, mock_logger):
        player = Player("Alice", Board(secret_code="1234"))
        game = Game([player])

        game.submit_guess(player, "1234")
        mock_logger.reset_mock()

        game.submit_guess(player, "5555")
        mock_logger.info.assert_called_with("%s already won the game", "Alice")

    @patch("bnc.game.logger")
    def test_no_more_guesses_logging(self, mock_logger):
        player = Player("Alice", Board(secret_code="1234", num_of_guesses=1))
        game = Game([player])

        game.submit_guess(player, "5555")
        mock_logger.info.assert_called_with("%s has no more guesses.", "Alice")
