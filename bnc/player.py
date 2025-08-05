from bnc import Board
from collections import Counter


class Player:
    def __init__(self, name: str, board: Board) -> None:
        self.name = name
        self.board = board

    def make_guess(self, guess: str) -> None:
        guess_digits = list(map(int, guess))
        self.board.evaluate_guess(guess_digits)
