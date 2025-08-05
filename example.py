from bnc import Board, Game, Player
from bnc.utils import generate_guess

if __name__ == "__main__":
    _code_length = 4
    _number_of_colors = 8
    _secret_code = "1337"

    board = Board(code_length=_code_length, num_of_colors=_number_of_colors)

    players = [
        Player("Jae", board.copy()),
        Player("Soo", board.copy()),
        Player("Ben", board.copy()),
        Player("Char", board.copy()),
    ]

    game = Game(players, secret_code=_secret_code)

    game.submit_guess(game.players[0], "1111")
    game.submit_guess(game.players[0], "1112")  # cannot guess since the game is over
    print(players[0].board.display_board())

    for i in range(10):
        game.submit_guess(
            game.players[1], generate_guess(_code_length, _number_of_colors)
        )
        game.submit_guess(
            game.players[2], generate_guess(_code_length, _number_of_colors)
        )
        game.submit_guess(
            game.players[3], generate_guess(_code_length, _number_of_colors)
        )

    print(players[1].board.display_board())
    print(players[2].board.display_board())
    print(players[3].board.display_board())

    print(game.winner.name)
