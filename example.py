from bnc import Board, Game, Player
import random

if __name__ == "__main__":
    board = Board()
    players = [
        Player("Jae", board.copy()),
        Player("Soo", board.copy()),
    ]
    game = Game(players, secret_code="1234")

    # players[0].make_guess("1234")

    print(players[0].board.display_board())

    for i in range(10):
        game.submit_guess(game.players[1], str(random.randint(1000, 9999)))
    print(players[1].board.display_board())
