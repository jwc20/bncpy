from collections import Counter


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
        self._init_board()

    def _init_board(self):
        for _ in range(self._num_of_guesses):
            self._board.append([0] * self._code_length)

    @property
    def secret_code(self):
        return self._secret_code

    @secret_code.setter
    def secret_code(self, secret_code: str):
        self._secret_digits = list(map(int, secret_code))
        self._secret_code = secret_code

    def evaluate_guess(self, guess_digits: list[int]):
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
        return bulls_count, cows_count

    def display_board(self):
        for i, row in enumerate(self._board):
            print(f"{i}: {row}")

    def copy(self):
        return Board(
            code_length=self._code_length,
            num_of_colors=self._num_of_colors,
            num_of_guesses=self._num_of_guesses,
        )
