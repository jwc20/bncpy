from bnc import Board, Player, Game

if __name__ == "__main__":
    board = Board()

    players = [
        Player("Jae", board),
        Player("Soo", board),
    ]

    game = Game(players, code="1234")
