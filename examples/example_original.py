import bncpy
from bncpy.bnc import Board, Game, Player
from bncpy.bnc.utils import generate_guess


# Game configuration
config = {"code_length": 4, "num_of_colors": 6, "num_of_guesses": 10}

# Create players with boards
players = [
    Player(name="Jae", board=Board(**config)),
    Player(name="Soo", board=Board(**config)),
    #   Player(name="Benjamin", board=Board(**config)),
    #   Player(name="Charlotte", board=Board(**config))
]

# Create game with secret code
# secret_code = get_random_number(length=4, max_value=5)  # Random 4-digit code
game = Game(players, secret_code="1234")

# Submit guesses
game.submit_guess(players[0], "1234")


# Check game state
print(game.state)
players[0].board.display_board()


# Player Soo
# game.submit_guess(players[1], generate_guess(config["code_length"], config["num_of_colors"]))  # Random guess


guesses = 0
while guesses < config["num_of_guesses"]:
    game.submit_guess(
        players[1], generate_guess(config["code_length"], config["num_of_colors"])
    )
    guesses += 1


print(game.state)
players[1].board.display_board()


# Check winners
if game.winners:
    for winner in game.winners:
        print(f"Winner: {winner.name}")
