from dataclasses import dataclass, field
from enum import Enum
import jsonpickle
from datetime import datetime


from bnc import Board, Game, Player
from bnc.utils import generate_guess, get_random_number


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
        return get_random_number(number=self.code_length, maximum=self.num_of_colors)


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
        self.config = config
        self.config.validate()
        self._mode = mode
        self._players = players or []
        self._player_states = player_states or {}
        self._all_guesses = all_guesses or []
        self._winners = winners or []

        if not self.config.secret_code:
            self.config.secret_code = self.config.generate_secret_code()

    @property
    def game_over(self):
        if self._mode == GameMode.SINGLE_BOARD:
            # single mode
            return len(self._all_guesses) >= self.config.num_of_guesses or any(
                g.bulls == self.config.code_length for g in self._all_guesses
            )
        else:
            # multi mode, game is over when all players are done
            return all(ps.game_over for ps in self._player_states.values())

    @property
    def game_won(self):
        if self._mode == GameMode.SINGLE_BOARD:
            return any(g.bulls == self.config.code_length for g in self._all_guesses)
        else:
            return any(ps.game_won for ps in self._player_states.values())

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

    # TODO: TEMPORARY, replace with prototype(?)
    def _create_board(self) -> Board:
        """Create a new Board with current configuration."""
        return Board(
            code_length=self.config.code_length,
            num_of_colors=self.config.num_of_colors,
            num_of_guesses=self.config.num_of_guesses,
            secret_code=self.config.secret_code,
        )

    def to_game(self) -> Game:
        if self._mode == GameMode.SINGLE_BOARD:
            # Create a single shared board
            board = self._create_board()

            # Replay all guesses on the board
            for guess_entry in self._all_guesses:
                if board.current_board_row_index >= 0:
                    board.evaluate_guess(
                        board.current_board_row_index, guess_entry.guess
                    )

            player = Player(name="Shared", board=board)
            return Game([player], secret_code=self.config.secret_code)

        else:
            pass

    # @classmethod
    # def from_game(cls, state: GameState) -> Game:
    #     pass


if __name__ == "__main__":

    # Board config
    config = GameConfig(code_length=4, num_of_colors=6, num_of_guesses=10)

    print("\n=== Single Player Mode ===")
    state_single = GameState(
        config=config,
        mode=GameMode.SINGLE_BOARD,
        players=["Jae", "Soo", "Benjamin", "Charlotte"],
    )

    # Convert to game for making moves
    game = state_single.to_game()
    game.submit_guess(game.players[0], "1234")

    # Convert back to state (this is what you'd save to database)
    state_single = GameState.from_game(
        game, config, GameMode.SINGLE_BOARD, state_single
    )

    print("\n=== Multi Player Mode ===")
    state_multi = GameState(
        config=config,
        mode=GameMode.MULTI,
        players=["Jae", "Soo", "Benjamin", "Charlotte"],
    )
