from dataclasses import dataclass

from .utils import calculate_bulls_and_cows, validate_code_input


@dataclass
class BoardRow:
    guess: list[int]
    bulls: int = 0
    cows: int = 0
    is_filled: bool = False

    @property
    def is_winning_row(self):
        return self.is_filled and self.bulls == len(self.guess)


class Board:
    def __init__(
        self,
        code_length: int = 4,
        num_of_colors: int = 6,
        num_of_guesses: int = 10,
        secret_code: str | None = None,
    ) -> None:
        if code_length < 3:
            raise ValueError(f"code_length must be at least 3, got {code_length}")
        if num_of_colors < 5:
            raise ValueError(f"num_of_colors must be at least 5, got {num_of_colors}")
        if num_of_guesses < 1:
            raise ValueError(f"num_of_guesses must be at least 1, got {num_of_guesses}")

        self._secret_code = secret_code
        self._code_length = code_length
        self._num_of_colors = num_of_colors
        self._num_of_guesses = num_of_guesses
        self._secret_digits: list[int] = []
        self._board: list[BoardRow] = self._init_board()
        self._game_won = False
        self._game_over = False

    def _init_board(self):
        board = []
        if self._secret_code:
            self._secret_digits = self.validate_secret_code(self._secret_code)
        for _ in range(self._num_of_guesses):
            board.append(BoardRow([0] * self._code_length))
        return board

    @property
    def board(self):
        return self._board

    @property
    def num_of_guesses(self):
        return self._num_of_guesses

    @property
    def secret_code(self):
        return self._secret_code

    @secret_code.setter
    def secret_code(self, secret_code: str) -> None:
        self._secret_digits = self.validate_secret_code(secret_code)
        self._secret_code = secret_code

    @property
    def num_of_colors(self):
        return self._num_of_colors

    @property
    def code_length(self):
        return self._code_length

    @property
    def game_won(self):
        return self._game_won

    @property
    def game_over(self):
        return self._game_over

    @property
    def current_board_row_index(self) -> int:
        for i, row in enumerate(self._board):
            if not row.is_filled:
                return i
        return -1

    def create_new_board(self):
        return Board(
            code_length=self._code_length,
            num_of_colors=self._num_of_colors,
            num_of_guesses=self._num_of_guesses,
            secret_code=self._secret_code,
        )

    def set_board_row(
        self, bulls: int, cows: int, guess_digits: list[int], board_row_index: int
    ):
        self._board[board_row_index] = BoardRow(
            guess=guess_digits, bulls=bulls, cows=cows, is_filled=True
        )

    def display_board(self) -> None:
        print("-" * 40)
        for i, row in enumerate(self._board):
            if row.is_filled:
                guess_str = "".join(map(str, row.guess))
                print(
                    f"Guess {i + 1}: {guess_str} | Bulls: {row.bulls} | Cows: {row.cows}"
                )
            else:
                print(f"Guess {i + 1}: {'_' * self._code_length}")

    def check_board_row_index(self, board_row_index: int) -> bool:
        return 0 <= board_row_index < self._num_of_guesses

    def validate_secret_code(self, secret_code: str) -> list[int]:
        if secret_code is None:
            raise ValueError("secret code cannot be None")
        secret_digits = validate_code_input(
            secret_code, self._code_length, self._num_of_colors
        )
        return secret_digits

    def evaluate_guess(self, board_row_index: int, guess: str) -> None:
        if not self.check_board_row_index(board_row_index):
            raise ValueError("Row index is out of range")

        guess_digits = validate_code_input(
            guess, self._code_length, self._num_of_colors
        )
        bulls_count, cows_count = calculate_bulls_and_cows(
            self._secret_digits, guess_digits
        )

        self.set_board_row(bulls_count, cows_count, guess_digits, board_row_index)

        if self._board[board_row_index].is_winning_row:
            self._game_won = True
            self._game_over = True
        elif board_row_index == self._num_of_guesses - 1:
            self._game_over = True
