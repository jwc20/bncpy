from .player import Player


class Game:
    def __init__(self, players: list[Player], secret_code: str | None = None) -> None:
        self._players = players

    def set_secret_code(self, secret_code: str) -> None:
        for player in self._players:
            player.board.set_secret_code(secret_code)
