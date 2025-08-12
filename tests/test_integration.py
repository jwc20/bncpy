import pytest
from unittest.mock import patch
from bnc import Board, Game, Player, GameConfig, GameMode, GameState
from bnc.utils import generate_guess, get_random_number


class TestSinglePlayerGame:
    def test_complete_game_win(self):
        board = Board(secret_code="1234")
        player = Player("Alice", board)
        game = Game([player])

        game.submit_guess(player, "5555")
        assert game.state.value == 1
        assert player.game_won is False

        game.submit_guess(player, "1234")
        assert player.game_won is True
        assert game.winner == player
        assert game.state.value == 2

    def test_complete_game_loss(self):
        board = Board(secret_code="1234", num_of_guesses=3)
        player = Player("Alice", board)
        game = Game([player])

        game.submit_guess(player, "5555")
        game.submit_guess(player, "6666")
        game.submit_guess(player, "5566")

        assert player.game_over is True
        assert player.game_won is False
        assert game.winner is None
        assert game.state.value == 2


class TestMultiPlayerGame:
    def test_two_player_competition(self):
        players = [
            Player("Alice", Board(secret_code="1234")),
            Player("Bob", Board(secret_code="1234")),
        ]
        game = Game(players)

        game.submit_guess(players[0], "5555")
        game.submit_guess(players[1], "1234")
        game.submit_guess(players[0], "1234")

        assert players[1].game_won is True
        assert players[0].game_won is True
        assert game.winner == players[1]
        assert len(game.winners) == 2

    def test_three_player_ranking(self):
        players = [
            Player("Alice", Board(secret_code="1234")),
            Player("Bob", Board(secret_code="1234")),
            Player("Charlie", Board(secret_code="1234")),
        ]
        game = Game(players)

        game.submit_guess(players[1], "1234")
        game.submit_guess(players[2], "1234")
        game.submit_guess(players[0], "1234")

        assert game.winners[0] == players[1]
        assert game.winners[1] == players[2]
        assert game.winners[2] == players[0]


class TestGameStateIntegration:
    def test_state_to_game_roundtrip(self):
        config = GameConfig(secret_code="1234")
        state = GameState(config, mode=GameMode.SINGLE_BOARD)

        state.submit_guess("Alice", "5555")
        state.submit_guess("Bob", "1234")

        game = state.to_game()
        assert game.players[0].board.board[0].bulls == 0
        assert game.players[0].board.board[1].bulls == 4

        new_state = GameState.from_game(game, config, GameMode.SINGLE_BOARD, state)
        assert len(new_state.all_guesses) == 2
        assert new_state.game_won is True

    def test_multi_board_state_integration(self):
        config = GameConfig(secret_code="1234", game_type=2)
        state = GameState(config, mode=GameMode.MULTI_BOARD)

        state.add_player("Alice")
        state.add_player("Bob")

        game = state.to_game()
        game.submit_guess(game.players[0], "1234")
        game.submit_guess(game.players[1], "5555")

        new_state = GameState.from_game(game, config, GameMode.MULTI_BOARD)
        assert new_state.player_states["Alice"].game_won is True
        assert new_state.player_states["Bob"].game_won is False


class TestEdgeCases:
    def test_empty_board_display(self, capsys):
        board = Board()
        board.display_board()
        captured = capsys.readouterr()
        assert "____" in captured.out

    def test_partial_board_display(self, capsys):
        board = Board(secret_code="1234")
        board.evaluate_guess(0, "5555")
        board.display_board()
        captured = capsys.readouterr()
        assert "5555" in captured.out
        assert "Bulls: 0" in captured.out

    def test_different_board_configs_error(self):
        players = [
            Player("Alice", Board(code_length=4)),
            Player("Bob", Board(code_length=5)),
        ]
        with pytest.raises(ValueError, match="same configuration"):
            Game(players)

    def test_game_continues_after_winner(self):
        players = [
            Player("Alice", Board(secret_code="1234")),
            Player("Bob", Board(secret_code="1234")),
        ]
        game = Game(players)

        game.submit_guess(players[0], "1234")
        assert players[0].game_won is True

        game.submit_guess(players[1], "5555")
        game.submit_guess(players[1], "1234")
        assert players[1].game_won is True
        assert len(game.winners) == 2


class TestComplexScenarios:
    def test_player_rejoining(self):
        config = GameConfig(secret_code="1234")
        state = GameState(config)

        state.add_player("Alice")
        state.submit_guess("Alice", "5555")
        state.remove_player("Alice")

        assert "Alice" not in state.players
        assert len(state.all_guesses) == 1

        state.add_player("Alice")
        assert "Alice" in state.players
        assert "Alice" in state.player_states

    def test_game_reset_mid_game(self):
        config = GameConfig(secret_code="1234")
        state = GameState(config)
        state.add_player("Alice")
        state.add_player("Bob")

        state.submit_guess("Alice", "5555")
        state.submit_guess("Bob", "6666")

        with patch("bnc.state.GameConfig.generate_secret_code", return_value="5678"):
            state.reset()

        assert state.config.secret_code == "5678"
        assert len(state.all_guesses) == 0
        assert state.player_states["Alice"].remaining_guesses == 10
        assert state.player_states["Bob"].remaining_guesses == 10

    def test_concurrent_guesses_same_answer(self):
        players = [
            Player("Alice", Board(secret_code="1234")),
            Player("Bob", Board(secret_code="1234")),
            Player("Charlie", Board(secret_code="1234")),
        ]
        game = Game(players)

        for player in players:
            game.submit_guess(player, "1234")

        assert all(p.game_won for p in players)
        assert len(game.winners) == 3
        assert game.winners[0] == players[0]
        assert game.winners[1] == players[1]
        assert game.winners[2] == players[2]

    def test_serialization_preserves_state(self):
        config = GameConfig(secret_code="1234")
        state1 = GameState(config)
        state1.add_player("Alice")
        state1.submit_guess("Alice", "5555")
        state1.submit_guess("Alice", "1234")

        json_data = state1.to_json()
        state2 = GameState.from_json(json_data, config)

        assert len(state2.all_guesses) == 2
        assert state2.all_guesses[0].guess == "5555"
        assert state2.all_guesses[1].guess == "1234"
        assert state2.game_won is True


class TestErrorHandling:
    def test_invalid_guess_recovery(self):
        board = Board(secret_code="1234")
        player = Player("Alice", board)
        game = Game([player])

        try:
            game.submit_guess(player, "12ab")
        except ValueError:
            pass

        game.submit_guess(player, "1234")
        assert player.game_won is True

    def test_multiple_validation_errors(self):
        errors = []

        try:
            Board(code_length=2)
        except ValueError as e:
            errors.append(str(e))

        try:
            Board(num_of_colors=4)
        except ValueError as e:
            errors.append(str(e))

        try:
            Board(num_of_guesses=0)
        except ValueError as e:
            errors.append(str(e))

        assert len(errors) == 3
        assert "code_length" in errors[0]
        assert "num_of_colors" in errors[1]
        assert "num_of_guesses" in errors[2]

    def test_state_recovery_from_invalid_data(self):
        config = GameConfig(secret_code="1234")
        state = GameState(config)

        result = state.submit_guess("Alice", "999")
        assert "error" in result
        assert "Code must be exactly 4 digits long" in result["error"]

        result = state.submit_guess("Alice", "1237")
        assert "error" in result
        assert "out of range" in result["error"]

        result = state.submit_guess("Alice", "1234")
        assert "error" not in result
        assert state.game_won is True


class TestPerformance:
    def test_large_number_of_players(self):
        players = [Player(f"Player{i}", Board(secret_code="1234")) for i in range(100)]
        game = Game(players)

        for i, player in enumerate(players):
            if i % 2 == 0:
                game.submit_guess(player, "1234")
            else:
                game.submit_guess(player, "5555")

        assert len(game.winners) == 50
        assert all(players[i] in game.winners for i in range(0, 100, 2))

    def test_many_guesses_single_player(self):
        board = Board(secret_code="1234", num_of_guesses=100)
        player = Player("Alice", board)
        game = Game([player])

        for i in range(99):
            guess = f"{(i % 6) + 1}{((i + 1) % 6) + 1}{((i + 2) % 6) + 1}{((i + 3) % 6) + 1}"
            game.submit_guess(player, guess)
            if player.game_won:
                break

        if not player.game_won:
            game.submit_guess(player, "1234")
            assert player.game_won is True


class TestBoundaryConditions:
    def test_minimum_valid_config(self):
        board = Board(code_length=3, num_of_colors=5, num_of_guesses=1)
        assert board.code_length == 3
        assert board.num_of_colors == 5
        assert board.num_of_guesses == 1

    def test_maximum_practical_config(self):
        board = Board(code_length=10, num_of_colors=9, num_of_guesses=100)
        assert board.code_length == 10
        assert board.num_of_colors == 9
        assert board.num_of_guesses == 100

    def test_single_guess_game(self):
        board = Board(secret_code="1234", num_of_guesses=1)
        player = Player("Alice", board)
        game = Game([player])

        game.submit_guess(player, "1234")
        assert player.game_won is True
        assert player.game_over is True

    def test_single_guess_loss(self):
        board = Board(secret_code="1234", num_of_guesses=1)
        player = Player("Alice", board)
        game = Game([player])

        game.submit_guess(player, "5555")
        assert player.game_won is False
        assert player.game_over is True
