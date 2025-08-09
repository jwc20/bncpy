from __future__ import annotations

import jsonpickle
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum

from . import Board, Game, Player
from .utils import get_random_number


class GameMode(Enum):
    SINGLE_BOARD = "SINGLE_BOARD"
    MULTI_BOARD = "MULTI_BOARD"


@dataclass
class PlayerGuess:
    guess: str
    bulls: int
    cows: int
    player: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "guess": self.guess,
            "bulls": self.bulls,
            "cows": self.cows,
            "player": self.player,
            "timestamp": self.timestamp.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict):
        timestamp = data.get("timestamp")
        if timestamp and isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)
        elif not timestamp:
            timestamp = datetime.now(timezone.utc)

        return cls(
            guess=data["guess"],
            bulls=data["bulls"],
            cows=data["cows"],
            player=data["player"],
            timestamp=timestamp,
        )


@dataclass
class PlayerState:
    name: str
    guesses: list[PlayerGuess] = field(default_factory=list)
    current_row: int = 0
    game_over: bool = False
    game_won: bool = False
    remaining_guesses: int = 10

    def to_dict(self):
        return {
            "name": self.name,
            "guesses": [g.to_dict() for g in self.guesses],
            "current_row": self.current_row,
            "game_over": self.game_over,
            "game_won": self.game_won,
            "remaining_guesses": self.remaining_guesses,
        }

    @classmethod
    def from_dict(cls, data: dict):
        guesses = [PlayerGuess.from_dict(g) for g in data.get("guesses", [])]
        return cls(
            name=data["name"],
            guesses=guesses,
            current_row=data.get("current_row", 0),
            game_over=data.get("game_over", False),
            game_won=data.get("game_won", False),
            remaining_guesses=data.get("remaining_guesses", 10),
        )


@dataclass
class GameConfig:
    code_length: int = 4
    num_of_colors: int = 6
    num_of_guesses: int = 10
    secret_code: str | None = None

    def validate(self):
        if self.code_length < 3:
            raise ValueError(f"code_length must be at least 3, got {self.code_length}")
        if self.num_of_colors < 5:
            raise ValueError(
                f"num_of_colors must be at least 5, got {self.num_of_colors}"
            )
        if self.num_of_guesses < 1:
            raise ValueError(
                f"num_of_guesses must be at least 1, got {self.num_of_guesses}"
            )
        if self.secret_code and len(self.secret_code) != self.code_length:
            raise ValueError(f"secret_code must be {self.code_length} digits long")

    def generate_secret_code(self) -> str:
        return get_random_number(
            number=self.code_length, maximum=self.num_of_colors - 1
        )

    def to_dict(self) -> dict:
        return {
            "code_length": self.code_length,
            "num_of_colors": self.num_of_colors,
            "num_of_guesses": self.num_of_guesses,
            "secret_code": self.secret_code,
        }

    @classmethod
    def from_dict(cls, data: dict) -> GameConfig:
        return cls(
            code_length=data.get("code_length", 4),
            num_of_colors=data.get("num_of_colors", 6),
            num_of_guesses=data.get("num_of_guesses", 10),
            secret_code=data.get("secret_code"),
        )

    def to_json(self) -> str:
        return jsonpickle.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> GameConfig:
        data = jsonpickle.loads(json_str)
        print(data)
        return cls.from_dict(data)


class GameState:
    def __init__(
        self,
        config: GameConfig,
        mode: GameMode = GameMode.SINGLE_BOARD,
        players: list[str] | None = None,
        player_states: dict[str, PlayerState] | None = None,
        all_guesses: list[PlayerGuess] | None = None,
        winners: list[str] | None = None,
        game_started: bool = False,
    ) -> None:
        self.config = config
        self.config.validate()
        self.mode = mode
        self.players = players or []
        self.player_states = player_states or {}
        self.all_guesses = all_guesses or []
        self.winners = winners or []
        self.game_started = game_started

        if not self.config.secret_code:
            self.config.secret_code = self.config.generate_secret_code()

    @property
    def game_over(self):
        if self.mode == GameMode.SINGLE_BOARD:
            return len(self.all_guesses) >= self.config.num_of_guesses or any(
                g.bulls == self.config.code_length for g in self.all_guesses
            )
        else:
            if not self.player_states:
                return False
            return all(ps.game_over for ps in self.player_states.values())

    @property
    def game_won(self):
        if self.mode == GameMode.SINGLE_BOARD:
            return any(g.bulls == self.config.code_length for g in self.all_guesses)
        else:
            return any(ps.game_won for ps in self.player_states.values())

    @property
    def current_row(self):
        return len(self.all_guesses)

    @property
    def remaining_guesses(self):
        return self.config.num_of_guesses - self.current_row

    def add_player(self, player_name: str) -> None:
        if player_name not in self.players:
            self.players.append(player_name)

            if (
                self.mode == GameMode.MULTI_BOARD
                and player_name not in self.player_states
            ):
                self.player_states[player_name] = PlayerState(
                    name=player_name, remaining_guesses=self.config.num_of_guesses
                )

    def remove_player(self, player_name: str) -> None:
        if player_name in self.players:
            self.players.remove(player_name)

    def reset(self) -> None:
        self.config.secret_code = self.config.generate_secret_code()
        self.all_guesses = []
        self.player_states = {}
        self.winners = []
        self.game_started = False

        if self.mode == GameMode.MULTI_BOARD:
            for player_name in self.players:
                self.player_states[player_name] = PlayerState(
                    name=player_name, remaining_guesses=self.config.num_of_guesses
                )

    def _create_board(self) -> Board:
        return Board(
            code_length=self.config.code_length,
            num_of_colors=self.config.num_of_colors,
            num_of_guesses=self.config.num_of_guesses,
            secret_code=self.config.secret_code,
        )

    def to_game(self) -> Game:
        if self.mode == GameMode.SINGLE_BOARD:
            board = self._create_board()

            for guess_entry in self.all_guesses:
                if board.current_board_row_index >= 0:
                    board.evaluate_guess(
                        board.current_board_row_index, guess_entry.guess
                    )

            player = Player(name="Shared", board=board)
            return Game([player], secret_code=self.config.secret_code)

        else:
            players = []

            for player_name, player_state in self.player_states.items():
                board = self._create_board()

                for guess_entry in player_state.guesses:
                    if board.current_board_row_index >= 0:
                        board.evaluate_guess(
                            board.current_board_row_index, guess_entry.guess
                        )

                player = Player(name=player_name, board=board)
                players.append(player)

            if not players:
                board = self._create_board()
                players = [Player(name="Default", board=board)]

            return Game(players, secret_code=self.config.secret_code)

    @classmethod
    def from_game(
        cls,
        game: Game,
        config: GameConfig,
        mode: GameMode = GameMode.SINGLE_BOARD,
        existing_state: GameState | None = None,
    ) -> GameState:
        all_guesses = []
        player_states = {}
        winners = [winner.name for winner in game.winners]

        if mode == GameMode.SINGLE_BOARD:
            player = game.players[0]
            board = player.board

            for i, row in enumerate(board.board):
                if row.is_filled:
                    player_name = "Anonymous"
                    if existing_state and i < len(existing_state.all_guesses):
                        player_name = existing_state.all_guesses[i].player

                    all_guesses.append(
                        PlayerGuess(
                            guess="".join(map(str, row.guess)),
                            bulls=row.bulls,
                            cows=row.cows,
                            player=player_name,
                        )
                    )
        else:
            for player in game.players:
                board = player.board
                player_guesses = []

                for row in board.board:
                    if row.is_filled:
                        guess_entry = PlayerGuess(
                            guess="".join(map(str, row.guess)),
                            bulls=row.bulls,
                            cows=row.cows,
                            player=player.name,
                        )
                        player_guesses.append(guess_entry)
                        all_guesses.append(guess_entry)

                player_states[player.name] = PlayerState(
                    name=player.name,
                    guesses=player_guesses,
                    current_row=len(player_guesses),
                    game_over=board.game_over,
                    game_won=board.game_won,
                    remaining_guesses=config.num_of_guesses - len(player_guesses),
                )

        players = existing_state.players if existing_state else []
        if not players:
            players = [
                p.name
                for p in game.players
                if p.name != "Shared" and p.name != "Default"
            ]

        return cls(
            config=config,
            mode=mode,
            players=players,
            player_states=player_states,
            all_guesses=all_guesses,
            winners=winners,
            game_started=True,
        )

    def submit_guess(self, player_name: str, guess: str) -> dict:
        if self.game_over:
            return {"error": "Game is already over"}

        if not self.game_started:
            self.game_started = True

        game = self.to_game()

        if self.mode == GameMode.SINGLE_BOARD:
            player = game.players[0]
        else:
            player = None
            for p in game.players:
                if p.name == player_name:
                    player = p
                    break

            if not player:
                board = self._create_board()
                player = Player(name=player_name, board=board)
                game.players.append(player)
                self.add_player(player_name)

        try:
            prev_guess_count = len(self.all_guesses)
            game.submit_guess(player, guess)

            new_state = GameState.from_game(game, self.config, self.mode, self)

            if self.mode == GameMode.SINGLE_BOARD and prev_guess_count < len(
                new_state.all_guesses
            ):
                new_state.all_guesses[-1].player = player_name

            self.all_guesses = new_state.all_guesses
            self.player_states = new_state.player_states
            self.winners = new_state.winners

            return self.to_dict()

        except ValueError as e:
            return {"error": str(e)}

    def to_json(self) -> str:
        return jsonpickle.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str, config: GameConfig | None = None) -> GameState:
        data = jsonpickle.loads(json_str)
        return cls.from_dict(data, config)

    def to_dict(self):
        base_dict = {
            "config": self.config.to_dict(),  # Add config serialization
            "mode": self.mode.value,
            "players": self.players,
            "guesses": [g.to_dict() for g in self.all_guesses],
            "game_over": self.game_over,
            "game_won": self.game_won,
            "winners": self.winners,
            "game_started": self.game_started,
            "current_row": self.current_row,
            "remaining_guesses": self.remaining_guesses,
            "secret_code": self.config.secret_code if self.game_over else None,
        }

        if self.mode == GameMode.MULTI_BOARD:
            base_dict["players_data"] = {
                name: state.to_dict() for name, state in self.player_states.items()
            }

        return base_dict

    @classmethod
    def from_dict(cls, data: dict, config: GameConfig | None = None) -> GameState:
        # If config is in the data, use it; otherwise use the provided config
        if "config" in data:
            config = GameConfig.from_dict(data["config"])
        elif config is None:
            # If no config provided and not in data, use defaults
            config = GameConfig()

        mode = GameMode(data.get("mode", "SINGLE_BOARD"))
        players = data.get("players", [])
        all_guesses = [PlayerGuess.from_dict(g) for g in data.get("guesses", [])]
        winners = data.get("winners", [])
        game_started = data.get("game_started", False)

        player_states = {}
        if mode == GameMode.MULTI_BOARD and "players_data" in data:
            for name, player_data in data["players_data"].items():
                player_states[name] = PlayerState.from_dict(player_data)

        return cls(
            config=config,
            mode=mode,
            players=players,
            player_states=player_states,
            all_guesses=all_guesses,
            winners=winners,
            game_started=game_started,
        )
