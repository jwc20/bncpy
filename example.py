import logging

from bnc import Board, Game, Player
from bnc.utils import generate_guess, get_random_number

logging.basicConfig(format="%(message)s", level=logging.INFO)


if __name__ == "__main__":
    _code_length = 4
    _number_of_colors = 6
    _num_of_guesses = 10
    player_names = ["Soo", "Benjamin", "Charlotte"]

    # Either set the secret code as number string
    # _secret_code = "1234"

    # Or generate a random number string
    _secret_code = get_random_number(number=_code_length, maximum=_number_of_colors - 1)

    # There multiple ways to set the secret code
    # Option 1: Set the secret code in the Board class (for all players)
    # Option 2: Set the secret code in the Player class (for individual player)
    # Option 3: Set the secret code in the Game class (for all players)

    config = {
        "code_length": _code_length,
        "num_of_colors": _number_of_colors,
        "num_of_guesses": _num_of_guesses,
        # "secret_code": _secret_code,              # Option 1
    }

    _players = [Player(name=name, board=Board(**config)) for name in player_names]

    # Option 2
    player_jae = Player(name="Jae", board=Board(**config))
    player_jae.set_secret_code_to_board("1234")
    players = _players + [player_jae]

    # Option 3
    game = Game(players, secret_code=_secret_code)

    # leave secret_code as None to generate a random secret code
    # game = Game(players)

    # to generate new random secret code
    # game.set_random_secret_code()

    print(game.state)
    print(" ")

    for _ in range(10):
        game.submit_guess(
            game.players[0], generate_guess(_code_length, _number_of_colors)
        )
        game.submit_guess(
            game.players[1], generate_guess(_code_length, _number_of_colors)
        )
        game.submit_guess(
            game.players[2], generate_guess(_code_length, _number_of_colors)
        )

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

    game.submit_guess(game.players[3], "1234")
    game.submit_guess(game.players[3], "1112")  # cannot guess since the game is over

    print(f"player: {game.players[3].name}")
    game.players[3].board.display_board()
    print(game.players[3].game_won)
    print(game.players[3].game_over)
    print("###############")
    print(" ")

    if game.winners:
        for player in game.winners:
            print(player.name)

    for player in game.players:
        print(player.board.secret_code)

    print(game.state)
