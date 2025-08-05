class Board:
    def __init__(
        self,
        code_length: int = 4,
        num_of_colors: int = 6,
        num_of_guesses: int = 10,
    ) -> None:
        self._code_length = code_length
        self._num_of_colors = num_of_colors
        self._num_of_guesses = num_of_guesses
        self._board = []
        self._init_board()

    def _init_board(self):
        for _ in range(self._num_of_guesses):
            self._board.append([0] * self._code_length)

    def display_board(self):
        for i, row in enumerate(self._board):
            print(f"{i}: {row}")
