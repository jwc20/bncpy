from bnc import Board


class Player:
    def __init__(self, name: str, board: Board) -> None:
        self.name = name
        self._board = board

    @property
    def board(self):
        return self._board

    @property
    def game_over(self):
        return self._board.game_over

    @property
    def game_won(self):
        return self._board.game_won

    def make_guess(self, guess: str) -> None:
        if self.game_over:
            print("Game over")
            return

        if len(guess) != self._board.code_length:
            raise ValueError(
                f"guess must be exactly {self._board.code_length} characters"
            )

        if not guess.isdigit():
            raise ValueError("guess must be a number")

        guess_digits = list(map(int, guess))

        for digit in guess_digits:
            if not self._board.check_color(digit):
                raise ValueError(
                    f"Digit {digit} is out of color range (0-{self._board.num_of_colors - 1})"
                )

        self._board.evaluate_guess(self._board.current_board_row_index, guess_digits)
