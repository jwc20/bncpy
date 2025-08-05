import logging

from bnc import Board

from .utils import validate_code_input

logger = logging.getLogger(__name__)


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
            logger.info("%s has no more guesses.", self.name)
            return

        guess_digits = validate_code_input(
            guess, self._board.code_length, self._board.num_of_colors
        )
        self._board.evaluate_guess(self._board.current_board_row_index, guess_digits)
