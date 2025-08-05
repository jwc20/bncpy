from .player import Player
from enum import Enum
from collections import deque
import logging

logger = logging.getLogger(__name__)


class GameState(Enum):
    SETUP = 0
    IN_PROGRESS = 1
    FINISHED = 2


class Game:
    def __init__(
        self,
        players: list[Player],
        secret_code: str | None = None,
    ) -> None:
        self._players = players
        self._winners = deque()
        if secret_code:
            self.set_secret_code(secret_code)

    def set_secret_code(self, secret_code: str | None) -> None:
        for player in self._players:
            player.board.secret_code = secret_code

    @property
    def players(self) -> list[Player]:
        return self._players

    @property
    def winner(self) -> Player | None:
        """get first place winner"""
        if not self._winners:
            return None
        return self._winners[0]

    @property
    def winners(self) -> deque[Player] | None:
        if not self._winners:
            return None
        return self._winners

    @property
    def state(self) -> GameState:
        if all(player.game_over for player in self._players):
            return GameState.FINISHED
        if all(player.board.current_board_row_index == 0 for player in self._players):
            return GameState.SETUP
        return GameState.IN_PROGRESS

    def submit_guess(self, player: Player, guess: str) -> None:
        if player in self._winners:
            # print(f"{player.name} already won the game")
            # logger.info(f"{player.name} already won the game")
            # logger.info(player.name, " already won the game")
            logger.info("%s already won the game", player.name)
            return

        player.make_guess(guess)

        if player.game_won and player not in self._winners:
            self._winners.append(player)
            position = len(self._winners)
            position_text = {1: "first", 2: "second", 3: "third"}.get(
                position, f"{position}th"
            )
            # print(f"{player.name} won the game in {position_text} place!")
            # logger.info(player.name, " won the game in ", position_text, " place!")
            # logger.info(
            #     "'{0}' won the game in {1} place!".format(player.name, position_text)
            # )
            logger.info("%s won the game in %s place!", player.name, position_text)
        elif player.game_over and not player.game_won:
            # print(f"{player.name} has no more guesses.")
            # logger.info(f"{player.name} has no more guesses.")
            # logger.info(player.name, " has no more guesses.")
            # logger.info("'{0}' has no more guesses.".format(player.name))
            logger.info("%s has no more guesses.", player.name)
