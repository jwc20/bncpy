from bnc import Board, Game, Player
from bnc.utils import generate_guess
import logging


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

if __name__ == "__main__":
    _code_length = 4
    _number_of_colors = 3
    _secret_code = "1111"

    board = Board(code_length=_code_length, num_of_colors=_number_of_colors)

    players = [
        Player("Jae", board.copy()),
        Player("Soo", board.copy()),
        Player("Ben", board.copy()),
        Player("Char", board.copy()),
    ]

    game = Game(players, secret_code=_secret_code)
    print(game.state)
    print("###############")
    print("###############")
    print(" ")

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

    print(game.state)

    game.submit_guess(game.players[0], "1111")
    game.submit_guess(game.players[0], "1112")  # cannot guess since the game is over

    print(game.state)

    print(f"player: {game.players[0].name}")
    game.players[0].board.display_board()
    print(game.players[0].game_won)
    print(game.players[0].game_over)
    print("###############")
    print(" ")

    print(f"player: {game.players[1].name}")
    game.players[1].board.display_board()
    print(game.players[1].game_won)
    print(game.players[1].game_over)
    print("###############")
    print(" ")

    print(f"player: {game.players[2].name}")
    game.players[2].board.display_board()
    print("###############")
    print(game.players[2].game_won)
    print(game.players[2].game_over)
    print(" ")

    print(f"player: {game.players[3].name}")
    game.players[3].board.display_board()
    print(game.players[3].game_won)
    print(game.players[3].game_over)
    print("###############")
    print(" ")

    if game.winners:
        for player in game.winners:
            print(player.name)

    print(game.state)
