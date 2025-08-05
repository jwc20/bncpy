from bnc import Board


class Player:
    def __init__(self, name: str, board: Board) -> None:
        self.name = name
        self._board = board

    @property
    def board(self):
        return self._board

    def make_guess(self, guess: str) -> None:
        guess_digits = list(map(int, guess))
        self._board.evaluate_guess(self._board.current_guess_index, guess_digits)
