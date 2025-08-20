import logging

from bncpy.bnc import GameConfig, GameMode, GameState
from bncpy.bnc.utils import generate_guess

logging.basicConfig(format="%(message)s", level=logging.INFO)


def first_example_to_2a_edit():
    """
    use GameState, GameConfig for Single Board mode
    """

    config = {
        "code_length": 4,
        "num_of_colors": 6,
        "num_of_guesses": 10,
        "secret_code": "1234",
    }
    config = GameConfig(**config)

    game_state = GameState(
        config=config, mode=GameMode.SINGLE_BOARD, players=["Benjamin", "Charlotte"]
    )

    for player in game_state.players:
        game_state.add_player(player)

    game = game_state.to_game()
    game.submit_guess(game.players[0], "1234")

    print(game.players[1].board.board)

    for _ in game.players[1].board.board:
        game.submit_guess(
            game.players[1], generate_guess(config.code_length, config.num_of_colors)
        )

    print(" ")
    print(" ")
    game.players[0].board.display_board()
    print(" ")
    game.players[1].board.display_board()
    print(" ")
    print(" ")
    print(game.state)
    print(" ")
    print(" ")

    # Check winners
    if game.winners:
        for winner in game.winners:
            print(f"Winner: {winner.name}")


def first_example_to_2b_edit():
    # Example 1: Direct bncpy usage (original style - still works)
    from bnc import Board, Game, Player, GameState, GameConfig
    from bnc.utils import generate_guess, get_random_number

    # Create players with boards
    # players = [
    #     Player(name="Benjamin", board=Board(**config)),
    #     Player(name="Charlotte", board=Board(**config)),
    # ]

    # Create game with secret code
    # secret_code = get_random_number(length=4, max_value=5)
    # game = Game(players, secret_code="1234")

    config = {
        "code_length": 4,
        "num_of_colors": 6,
        "num_of_guesses": 10,
        "secret_code": "1234",
    }
    config = GameConfig(**config)

    game_state = GameState(
        config=config, mode=GameMode.MULTI_BOARD, players=["Benjamin", "Charlotte"]
    )

    for player in game_state.players:
        game_state.add_player(player)

    game = game_state.to_game()

    # Submit guesses
    game.submit_guess(game.players[0], "1234")

    print(game.players[1].board.board)

    for _ in game.players[1].board.board:
        game.submit_guess(
            game.players[1], generate_guess(config.code_length, config.num_of_colors)
        )

    print(" ")
    print(" ")
    game.players[0].board.display_board()
    print(" ")
    game.players[1].board.display_board()
    print(" ")
    print(" ")
    print(game.state)
    print(" ")
    print(" ")

    # Check winners
    if game.winners:
        for winner in game.winners:
            print(f"Winner: {winner.name}")


def first_example():
    # Example 1: Direct bncpy usage (original style - still works)
    from bnc import Board, Game, Player
    from bnc.utils import generate_guess, get_random_number

    # Game configuration
    config = {"code_length": 4, "num_of_colors": 6, "num_of_guesses": 10}

    # Create players with boards
    players = [
        Player(name="Benjamin", board=Board(**config)),
        Player(name="Charlotte", board=Board(**config)),
    ]

    # Create game with secret code
    secret_code = get_random_number(length=4, max_value=5)
    game = Game(players, secret_code=secret_code)

    # Submit guesses
    game.submit_guess(players[0], "1234")
    game.submit_guess(
        players[1], generate_guess(config["code_length"], config["num_of_colors"])
    )

    # Check game state
    print(game.state)
    players[0].board.display_board()

    # Check winners
    if game.winners:
        for winner in game.winners:
            print(f"Winner: {winner.name}")


def second_single_example():

    # ================================================================================
    # Example 2: Using the State class for database-friendly operations
    # ================================================================================

    from bnc.state import GameState, GameConfig, GameMode
    from bnc.utils import generate_guess

    # Create configuration
    config = GameConfig(code_length=4, num_of_colors=6, num_of_guesses=10)

    # Example 2a: Single-player mode (collaborative)
    print("\n=== Single Player Mode ===")
    state_single = GameState(
        config=config,
        mode=GameMode.SINGLE_BOARD,
        players=["Jae", "Soo", "Benjamin", "Charlotte"],
    )

    # Convert to game for making moves
    game = state_single.to_game()
    game.submit_guess(game.players[0], "1234")

    # Convert back to state (this is what you'd save to database)
    state_single = GameState.from_game(
        game, config, GameMode.SINGLE_BOARD, state_single
    )

    # Add another guess with player attribution
    game = state_single.to_game()
    game.submit_guess(game.players[0], "2345")
    state_single = GameState.from_game(
        game, config, GameMode.SINGLE_BOARD, state_single
    )
    # Manually update the player name for the last guess (in single mode)
    state_single.all_guesses[-1].player = "Soo"

    # Save to database (JSON)
    json_data = state_single.to_json()
    print(f"JSON for database: {json_data[:100]}...")

    # Load from database
    loaded_state = GameState.from_json(json_data, config)
    print(f"Game over: {loaded_state.game_over}")
    print(f"Current row: {loaded_state.current_row}")
    print(f"Guesses: {[(g.guess, g.player) for g in loaded_state.all_guesses]}")


def second_multi_example():
    """Example 2b: Multi-player mode (competitive)"""

    from bnc.state import GameState, GameConfig, GameMode
    from bnc.utils import generate_guess

    # Create configuration
    config = GameConfig(code_length=4, num_of_colors=6, num_of_guesses=10)

    print("\n=== Multi Player Mode ===")
    state_multi = GameState(
        config=config,
        mode=GameMode.MULTI_BOARD,
        players=["Jae", "Soo", "Benjamin", "Charlotte"],
    )

    # Add players to the game
    for player_name in ["Jae", "Soo", "Benjamin", "Charlotte"]:
        state_multi.add_player(player_name)

    # Simulate some gameplay
    # Jae makes a guess
    game = state_multi.to_game()
    jae_player = next(p for p in game.players if p.name == "Jae")
    game.submit_guess(jae_player, "1234")
    game.submit_guess(jae_player, "1235")
    state_multi = GameState.from_game(game, config, GameMode.MULTI_BOARD, state_multi)
    print(state_multi.player_states["Jae"])

    # Benjamin makes a guess
    game = state_multi.to_game()
    benjamin_player = next(p for p in game.players if p.name == "Benjamin")
    game.submit_guess(benjamin_player, generate_guess(4, 6))
    state_multi = GameState.from_game(game, config, GameMode.MULTI_BOARD, state_multi)
    print(state_multi.player_states["Benjamin"])

    # Soo makes a guess
    game = state_multi.to_game()
    soo_player = next(p for p in game.players if p.name == "Soo")
    game.submit_guess(soo_player, generate_guess(4, 6))
    state_multi = GameState.from_game(game, config, GameMode.MULTI_BOARD, state_multi)
    print(state_multi)

    # Check individual player states
    for name, player_state in state_multi.player_states.items():
        print(
            f"{name}: {player_state.current_row} guesses, game_over: {player_state.game_over}"
        )


def third_example():
    # ================================================================================
    # Example 4: Advanced features with State class
    # ================================================================================

    print("\n=== Advanced State Features ===")

    # Create a game in progress
    state = GameState(
        config=GameConfig(code_length=4, num_of_colors=6, num_of_guesses=10),
        mode=GameMode.MULTI_BOARD,
    )

    # Add multiple players
    players = ["Alice", "Bob", "Charlie"]
    for p in players:
        state.add_player(p)

    # Simulate a few rounds
    test_guesses = ["1234", "2345", "3456", "4321"]
    for i, player_name in enumerate(players):
        if i < len(test_guesses):
            # Each player makes a guess
            game = state.to_game()
            player = next((p for p in game.players if p.name == player_name), None)
            if not player:
                # Create player if doesn't exist in game
                from bnc import Board, Player

                board = state._create_board()
                player = Player(name=player_name, board=board)
                game.players.append(player)

            game.submit_guess(player, test_guesses[i])
            state = GameState.from_game(game, state.config, state.mode, state)

    # Game statistics
    print(f"Total guesses made: {len(state.all_guesses)}")
    print(f"Active players: {state.players}")
    print(f"Game over: {state.game_over}")
    print(f"Winners: {state.winners}")

    # Reset for new game
    print("\n=== Resetting Game ===")
    state.reset()
    print(f"After reset - Guesses: {len(state.all_guesses)}")
    print(f"New secret code: {state.config.secret_code}")

    # Demonstrate state persistence
    json_state = state.to_json()
    print(f"\nState size (bytes): {len(json_state)}")

    # Load it back
    restored_state = GameState.from_json(json_state, state.config)
    print(
        f"Restored successfully: {restored_state.config.secret_code == state.config.secret_code}"
    )


########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################


if __name__ == "__main__":
    # first_example()
    # second_single_example()
    # second_multi_example()
    # third_example()

    first_example_to_2a_edit()
    # first_example_to_2b_edit()
