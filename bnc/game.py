from .player import Player


class Game:
    def __init__(self, players: list[Player], secret_code: str | None = None) -> None:
        self._players = players
        if secret_code:
            self.set_secret_code(secret_code)

    @property
    def players(self) -> list[Player]:
        return self._players

    def set_secret_code(self, secret_code: str | None) -> None:
        for player in self._players:
            player.board.secret_code = secret_code

    def submit_guess(self, player: Player, guess: str) -> None:
        player.make_guess(guess)
