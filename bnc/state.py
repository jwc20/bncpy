"""
https://github.com/faif/python-patterns/blob/master/patterns/behavioral/state.py
"""

from dataclasses import dataclass
from enum import Enum
import json
from datetime import datetime

from bncpy import Board, Game, Player, PlayerGuess, PlayerState
from bncpy.utils import generate_guess, get_random_number

from aifc import data


class GameMode(Enum):
    """
    SINGLE_BOARD: all players play on the same board
    MULTI_BOARD: each player has their own board
    """

    SINGLE_BOARD = 1
    MULTI_BOARD = 2


@dataclass
class PlayerGuess:
    guess: str
    bulls: int
    cows: int
    player: str
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class PlayerState:
    name: str
    guesses: list[PlayerGuess] = field(default_factory=list)
    current_row: int = 0
    game_over: bool = False
    game_won: bool = False
    remaining_guesses: int = 10


@dataclass
class GameConfig:
    code_length: int = 4
    num_of_colors: int = 6
    num_of_guesses: int = 10
    secret_code: str | None = None

    def validate(self) -> None:
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

    def generate_secret_code(self) -> str:
        return get_random_number(self.num_of_colors, self.code_length)


class GameState:
    def __init__(
        self,
        config: GameConfig,
        mode: GameMode = GameMode.SINGLE_BOARD,
        players: list[str] | None = None,
        player_states: dict[str, PlayerState] | None = None,
        all_guesses: list[PlayerGuess] | None = None,
        winners: list[str] | None = None,
    ) -> None:
        self._config = config
        self._config.validate()
        self._mode = mode
        self._players = players or []
        self._player_states = player_states or {}
        self._all_guesses = all_guesses or []
        self._winners = winners or []

    @property
    def game_over(self):
        pass

    @property
    def game_won(self):
        pass

    @property
    def current_row(self):
        pass

    @property
    def remaining_guesses(self):
        pass

    def add_player(self, player_name: str) -> None:
        pass

    def remove_player(self, player_name: str) -> None:
        pass

    def reset(self) -> None:
        pass


if __name__ == "__main__":
    game_config = GameConfig()
    game_state = GameState()

    board = Board()
    player = Player()
    game = Game()
