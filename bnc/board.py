# ./bnc/board.py

from collections import Counter
from dataclasses import dataclass
from .utils import validate_code_input


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
        self._secret_code = secret_code
        self._code_length = code_length
        self._num_of_colors = num_of_colors
        self._num_of_guesses = num_of_guesses
        self._board = []
        self._secret_digits: list[int] = []
        self._game_won = False
        self._game_over = False
        self._init_board()

    def _init_board(self):
        for _ in range(self._num_of_guesses):
            self._board.append(BoardRow([0] * self._code_length))

    @property
    def num_of_guesses(self):
        return self._num_of_guesses

    @property
    def secret_code(self):
        return self._secret_code

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

    def check_secret_code(self, secret_code: str | None = None):
        if secret_code is None:
            raise ValueError("secret code cannot be None")

        secret_digits = validate_code_input(
            secret_code, self._code_length, self._num_of_colors
        )
        return secret_digits

    # @secret_code.setter
    # def secret_code(self, secret_code: str):
    #     if secret_code is not None:
    #         self.check_secret_code(secret_code)
    #         self._secret_code = secret_code
    #         self._secret_digits = list(map(int, secret_code))
    @secret_code.setter
    def secret_code(self, secret_code: str):
        if secret_code is not None:
            self._secret_digits = self.check_secret_code(secret_code)
            self._secret_code = secret_code

    @property
    def current_board_row_index(self) -> int:
        for i, row in enumerate(self._board):
            if not row.is_filled:
                return i
        return self._num_of_guesses

    def set_bnc_row(
        self, bulls: int, cows: int, guess_digits: list[int], board_row_index: int
    ):
        self._board[board_row_index] = BoardRow(
            guess=guess_digits, bulls=bulls, cows=cows, is_filled=True
        )

    def check_color(self, color: int) -> bool:
        return 0 <= color < self._num_of_colors

    def check_board_row_index(self, board_row_index: int) -> bool:
        return 0 <= board_row_index < self._num_of_guesses

    def evaluate_guess(self, board_row_index: int, guess_digits: list[int]) -> None:
        if not self.check_board_row_index(board_row_index):
            raise ValueError("Row index is out of range")

        bulls_count = 0
        for i in range(len(self._secret_digits)):
            if self._secret_digits[i] == guess_digits[i]:
                bulls_count += 1

        secret_counter = Counter(self._secret_digits)
        guess_counter = Counter(guess_digits)

        total_matches = 0
        for digit in guess_counter:
            if digit in secret_counter:
                total_matches += min(guess_counter[digit], secret_counter[digit])

        cows_count = total_matches - bulls_count
        self.set_bnc_row(bulls_count, cows_count, guess_digits, board_row_index)

        if self._board[board_row_index].is_winning_row:
            self._game_won = True
            self._game_over = True
        elif board_row_index == self._num_of_guesses - 1:
            self._game_over = True

    def display_board(self):
        for i, row in enumerate(self._board):
            print(f"{i}: {row}")

    def copy(self):
        return Board(
            code_length=self._code_length,
            num_of_colors=self._num_of_colors,
            num_of_guesses=self._num_of_guesses,
            secret_code=self._secret_code,
        )
