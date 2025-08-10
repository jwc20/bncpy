import logging

from bnc.state import GameConfig, GameMode, GameState

logging.basicConfig(format="%(message)s", level=logging.INFO)


if __name__ == "__main__":
    # Test Examples

    print("=" * 60)
    print("EXAMPLE 1: SINGLE BOARD MODE (Collaborative)")
    print("=" * 60)

    config = GameConfig(code_length=4, num_of_colors=6, num_of_guesses=10)
    state = GameState(config=config, mode=GameMode.SINGLE_BOARD)

    # Add players
    state.add_player("Alice")
    state.add_player("Bob")
    state.add_player("Charlie")

    print(f"Secret code: {state.config.secret_code}")
    print(f"Players: {state.players}")

    # Players take turns guessing
    result = state.submit_guess("Alice", "1234")
    print(
        f"\nAlice guesses 1234: Bulls={result['guesses'][-1]['bulls']}, Cows={result['guesses'][-1]['cows']}"
    )

    result = state.submit_guess("Bob", "5432")
    print(
        f"Bob guesses 5432: Bulls={result['guesses'][-1]['bulls']}, Cows={result['guesses'][-1]['cows']}"
    )

    result = state.submit_guess("Charlie", "1111")
    print(
        f"Charlie guesses 1111: Bulls={result['guesses'][-1]['bulls']}, Cows={result['guesses'][-1]['cows']}"
    )

    print("\nGame status:")
    print(f"  - Current row: {state.current_row}")
    print(f"  - Remaining guesses: {state.remaining_guesses}")
    print(f"  - Game over: {state.game_over}")
    print(f"  - Game won: {state.game_won}")

    # Test JSON serialization
    json_data = state.to_json()
    print(f"\nJSON data: {json_data}")
    print(f"\nJSON length: {len(json_data)} bytes")

    # Test deserialization
    loaded_state = GameState.from_json(json_data, config)
    print("loaded_state:" + str(loaded_state))
    print(f"Loaded state has {len(loaded_state.all_guesses)} guesses")

    print("\n" + "=" * 60)
    print("EXAMPLE 2: MULTI BOARD MODE (Competitive)")
    print("=" * 60)

    config2 = GameConfig(code_length=4, num_of_colors=6, num_of_guesses=10)
    state2 = GameState(config=config2, mode=GameMode.MULTI_BOARD)

    # Add players
    state2.add_player("Player1")
    state2.add_player("Player2")

    print(f"Secret code: {state2.config.secret_code}")
    print(f"Players: {state2.players}")

    # Each player makes their own guesses
    state2.submit_guess("Player1", "1234")
    state2.submit_guess("Player1", "2345")
    state2.submit_guess("Player2", "3456")

    print("\nPlayer states:")
    for name, pstate in state2.player_states.items():
        print(
            f"  {name}: {pstate.current_row} guesses, remaining: {pstate.remaining_guesses}"
        )

    print("\n" + "=" * 60)
    print("EXAMPLE 3: MODE SWITCHING")
    print("=" * 60)

    config3 = GameConfig(code_length=4, num_of_colors=6, num_of_guesses=10)
    state3 = GameState(config=config3, mode=GameMode.SINGLE_BOARD)

    print(f"Initial mode: {state3.mode.value}")
