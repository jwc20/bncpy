import asyncio
import logging

from bnc import Board, Game, Player
from bnc.utils import display_board, generate_guess, get_random_number

logging.basicConfig(format="%(message)s", level=logging.INFO)


if __name__ == "__main__":
    _code_length = 4
    _number_of_colors = 6
    # _secret_code = "1234"

    board = Board(code_length=_code_length, num_of_colors=_number_of_colors)

    players = [
        Player("Jae", board.create_new_board()),
        Player("Soo", board.create_new_board()),
        Player("Ben", board.create_new_board()),
        Player("Char", board.create_new_board()),
    ]

    _secret_code = asyncio.run(
        get_random_number(number=_code_length, maximum=_number_of_colors - 1)
    )
    print(_secret_code)
    # game = Game(players, secret_code=_secret_code)
    game = Game(players)
    # game.set_random_secret_code()

    print(game.state)
    print(" ")

    for _ in range(10):
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

    game.submit_guess(game.players[0], "1234")
    game.submit_guess(game.players[0], "1112")  # cannot guess since the game is over

    print(f"player: {game.players[0].name}")
    display_board(game.players[0].board)
    print(game.players[0].game_won)
    print(game.players[0].game_over)
    print("###############")
    print(" ")

    print(f"player: {game.players[1].name}")
    display_board(game.players[1].board)
    print(game.players[1].game_won)
    print(game.players[1].game_over)
    print("###############")
    print(" ")

    print(f"player: {game.players[2].name}")
    display_board(game.players[2].board)
    print("###############")
    print(game.players[2].game_won)
    print(game.players[2].game_over)
    print(" ")

    print(f"player: {game.players[3].name}")
    display_board(game.players[3].board)
    print(game.players[3].game_won)
    print(game.players[3].game_over)
    print("###############")
    print(" ")

    if game.winners:
        for player in game.winners:
            print(player.name)

    print(game.state)
