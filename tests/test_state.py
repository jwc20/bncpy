import pytest
from unittest.mock import patch, Mock
from datetime import datetime, timezone
from bnc import Board, Game, Player
from bnc.state import GameConfig, GameMode, GameState, PlayerGuess, PlayerState


class TestPlayerGuess:
    def test_initialization(self):
        guess = PlayerGuess("1234", 2, 1, "Alice")
        assert guess.guess == "1234"
        assert guess.bulls == 2
        assert guess.cows == 1
        assert guess.player == "Alice"
        assert isinstance(guess.timestamp, datetime)
        
    def test_to_dict(self):
        guess = PlayerGuess("1234", 2, 1, "Alice")
        data = guess.to_dict()
        assert data["guess"] == "1234"
        assert data["bulls"] == 2
        assert data["cows"] == 1
        assert data["player"] == "Alice"
        assert "timestamp" in data
        
    def test_from_dict(self):
        timestamp = datetime.now(timezone.utc)
        data = {
            "guess": "5678",
            "bulls": 3,
            "cows": 0,
            "player": "Bob",
            "timestamp": timestamp.isoformat()
        }
        guess = PlayerGuess.from_dict(data)
        assert guess.guess == "5678"
        assert guess.bulls == 3
        assert guess.cows == 0
        assert guess.player == "Bob"
        
    def test_from_dict_no_timestamp(self):
        data = {"guess": "1234", "bulls": 1, "cows": 1, "player": "Alice"}
        guess = PlayerGuess.from_dict(data)
        assert isinstance(guess.timestamp, datetime)


class TestPlayerState:
    def test_initialization(self):
        state = PlayerState("Alice")
        assert state.name == "Alice"
        assert state.guesses == []
        assert state.current_row == 0
        assert state.game_over is False
        assert state.game_won is False
        assert state.remaining_guesses == 10
        
    def test_with_guesses(self):
        guesses = [
            PlayerGuess("1234", 2, 1, "Alice"),
            PlayerGuess("5678", 0, 2, "Alice")
        ]
        state = PlayerState("Alice", guesses=guesses, current_row=2)
        assert len(state.guesses) == 2
        assert state.current_row == 2
        
    def test_to_dict(self):
        state = PlayerState("Alice", game_won=True, remaining_guesses=5)
        data = state.to_dict()
        assert data["name"] == "Alice"
        assert data["game_won"] is True
        assert data["remaining_guesses"] == 5
        
    def test_from_dict(self):
        data = {
            "name": "Bob",
            "guesses": [{"guess": "1234", "bulls": 1, "cows": 1, "player": "Bob"}],
            "current_row": 1,
            "game_over": False,
            "game_won": False,
            "remaining_guesses": 9
        }
        state = PlayerState.from_dict(data)
        assert state.name == "Bob"
        assert len(state.guesses) == 1
        assert state.current_row == 1


class TestGameConfig:
    def test_default_values(self):
        config = GameConfig()
        assert config.code_length == 4
        assert config.num_of_colors == 6
        assert config.num_of_guesses == 10
        assert config.secret_code is None
        assert config.game_type == 1
        
    def test_custom_values(self):
        config = GameConfig(code_length=5, num_of_colors=8, secret_code="12345")
        assert config.code_length == 5
        assert config.num_of_colors == 8
        assert config.secret_code == "12345"
        
    def test_validation_code_length(self):
        config = GameConfig(code_length=2)
        with pytest.raises(ValueError, match="code_length must be at least 3"):
            config.validate()
            
    def test_validation_num_colors(self):
        config = GameConfig(num_of_colors=3)
        with pytest.raises(ValueError, match="num_of_colors must be at least 4"):
            config.validate()
            
    def test_validation_num_guesses(self):
        config = GameConfig(num_of_guesses=0)
        with pytest.raises(ValueError, match="num_of_guesses must be at least 1"):
            config.validate()
            
    def test_validation_secret_code_length(self):
        config = GameConfig(code_length=4, secret_code="123")
        with pytest.raises(ValueError, match="secret_code must be 4 digits long"):
            config.validate()
            
    def test_generate_secret_code(self):
        config = GameConfig(code_length=5, num_of_colors=7)
        with patch('bnc.state.get_random_number', return_value="12345"):
            code = config.generate_secret_code()
            assert code == "12345"
            
    def test_to_dict(self):
        config = GameConfig(secret_code="1234")
        data = config.to_dict()
        assert data["code_length"] == 4
        assert data["secret_code"] == "1234"
        assert "game_type" in data
        
    def test_from_dict(self):
        data = {
            "code_length": 5,
            "num_of_colors": 7,
            "num_of_guesses": 12,
            "secret_code": "12345",
            "game_type": 2
        }
        config = GameConfig.from_dict(data)
        assert config.code_length == 5
        assert config.game_type == 2
        
    def test_json_serialization(self):
        config = GameConfig(code_length=5, secret_code="12345")
        json_str = config.to_json()
        restored = GameConfig.from_json(json_str)
        assert restored.code_length == 5
        assert restored.secret_code == "12345"


class TestGameState:
    def test_initialization_single_board(self):
        config = GameConfig()
        state = GameState(config, mode=GameMode.SINGLE_BOARD)
        assert state.mode == GameMode.SINGLE_BOARD
        assert state.players == []
        assert state.game_started is False
        
    def test_initialization_multi_board(self):
        config = GameConfig()
        state = GameState(config, mode=GameMode.MULTI_BOARD)
        assert state.mode == GameMode.MULTI_BOARD
        
    def test_auto_generate_secret(self):
        config = GameConfig()
        with patch('bnc.state.GameConfig.generate_secret_code', return_value="1234"):
            state = GameState(config)
            assert state.config.secret_code == "1234"
            
    def test_game_over_single_board_max_guesses(self):
        config = GameConfig(num_of_guesses=2, secret_code="1234")
        state = GameState(config, mode=GameMode.SINGLE_BOARD)
        state.all_guesses = [
            PlayerGuess("5555", 0, 0, "Alice"),
            PlayerGuess("6666", 0, 0, "Alice")
        ]
        assert state.game_over is True
        
    def test_game_over_single_board_won(self):
        config = GameConfig(secret_code="1234")
        state = GameState(config, mode=GameMode.SINGLE_BOARD)
        state.all_guesses = [PlayerGuess("1234", 4, 0, "Alice")]
        assert state.game_over is True
        assert state.game_won is True
        
    def test_game_over_multi_board(self):
        config = GameConfig(secret_code="1234")
        state = GameState(config, mode=GameMode.MULTI_BOARD)
        state.player_states = {
            "Alice": PlayerState("Alice", game_over=True),
            "Bob": PlayerState("Bob", game_over=True)
        }
        assert state.game_over is True
        
    def test_add_player(self):
        config = GameConfig()
        state = GameState(config)
        state.add_player("Alice")
        assert "Alice" in state.players
        assert "Alice" in state.player_states
        
    def test_add_duplicate_player(self):
        config = GameConfig()
        state = GameState(config)
        state.add_player("Alice")
        state.add_player("Alice")
        assert state.players.count("Alice") == 1
        
    def test_remove_player(self):
        config = GameConfig()
        state = GameState(config)
        state.add_player("Alice")
        state.remove_player("Alice")
        assert "Alice" not in state.players
        
    def test_reset(self):
        config = GameConfig(secret_code="1234")
        state = GameState(config)
        state.add_player("Alice")
        state.all_guesses = [PlayerGuess("5555", 0, 0, "Alice")]
        state.game_started = True
        
        with patch('bnc.state.GameConfig.generate_secret_code', return_value="5678"):
            state.reset()
            
        assert state.config.secret_code == "5678"
        assert state.all_guesses == []
        assert state.game_started is False
        
    def test_submit_guess_success(self):
        config = GameConfig(secret_code="1234")
        state = GameState(config)
        
        result = state.submit_guess("Alice", "1324")
        assert "error" not in result
        assert len(state.all_guesses) == 1
        assert state.all_guesses[0].bulls == 2
        assert state.all_guesses[0].cows == 2
        
    def test_submit_guess_game_over(self):
        config = GameConfig(secret_code="1234", num_of_guesses=1, game_type=1)
        state = GameState(config)
        state.all_guesses = [PlayerGuess("5555", 0, 0, "Alice")]
        
        result = state.submit_guess("Alice", "1234")
        assert result == {"error": "Game is already over"}
        
    def test_submit_guess_invalid(self):
        config = GameConfig(secret_code="1234")
        state = GameState(config)
        
        result = state.submit_guess("Alice", "12ab")
        assert "error" in result
        
    def test_to_game_single_board(self):
        config = GameConfig(secret_code="1234")
        state = GameState(config, mode=GameMode.SINGLE_BOARD)
        state.all_guesses = [
            PlayerGuess("5555", 0, 0, "Alice"),
            PlayerGuess("1234", 4, 0, "Bob")
        ]
        
        game = state.to_game()
        assert len(game.players) == 1
        assert game.players[0].name == "Shared"
        
    def test_to_game_multi_board(self):
        config = GameConfig(secret_code="1234")
        state = GameState(config, mode=GameMode.MULTI_BOARD)
        
        alice_state = PlayerState("Alice")
        alice_state.guesses = [PlayerGuess("5555", 0, 0, "Alice")]
        state.player_states["Alice"] = alice_state
        
        game = state.to_game()
        assert len(game.players) == 1
        assert game.players[0].name == "Alice"
        
    def test_from_game_single_board(self):
        board = Board(secret_code="1234")
        board.evaluate_guess(0, "5555")
        player = Player("Shared", board)
        game = Game([player])
        config = GameConfig(secret_code="1234")
        
        state = GameState.from_game(game, config, GameMode.SINGLE_BOARD)
        assert len(state.all_guesses) == 1
        assert state.all_guesses[0].bulls == 0
        
    def test_from_game_multi_board(self):
        boards = [
            Board(secret_code="1234"),
            Board(secret_code="1234")
        ]
        boards[0].evaluate_guess(0, "1234")
        boards[1].evaluate_guess(0, "5555")
        
        players = [
            Player("Alice", boards[0]),
            Player("Bob", boards[1])
        ]
        game = Game(players)
        config = GameConfig(secret_code="1234")
        
        state = GameState.from_game(game, config, GameMode.MULTI_BOARD)
        assert "Alice" in state.player_states
        assert "Bob" in state.player_states
        assert state.player_states["Alice"].game_won is True
        assert state.player_states["Bob"].game_won is False
        
    def test_json_serialization(self):
        config = GameConfig(secret_code="1234")
        state = GameState(config)
        state.add_player("Alice")
        state.submit_guess("Alice", "5555")
        
        json_str = state.to_json()
        restored = GameState.from_json(json_str, config)
        
        assert len(restored.all_guesses) == 1
        assert "Alice" in restored.players