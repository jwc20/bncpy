import random

import httpx


async def get_random_number(
    number: int | None = 4,
    maximum: int | None = 7,
    base: int | None = 10,
) -> str:
    # response type should be a string since converting to int removes leading zeros (EX: 0000 -> 0)

    if maximum <= 0:
        raise ValueError("Maximum value must be greater than minimum")

    if base not in [2, 8, 10, 16]:
        raise ValueError("Base value must be 2, 8, 10, or 16")

    params = {
        "num": number,
        "min": 0,
        "max": maximum,
        "col": 1,
        "base": base,
        "format": "plain",
        "rnd": "new",
    }

    async with httpx.AsyncClient() as client:
        response = await client.get("https://www.random.org/integers/", params=params)

    # response = httpx.get("https://www.random.org/integers/", params=params)
    cleaned_response = response.text.replace("\n", "")

    if len(cleaned_response) != number:
        raise ValueError(
            f"Random number generator returned a number with {len(cleaned_response)} digits, expected {number}"
        )

    return cleaned_response


def generate_guess(code_length: int, number_of_colors: int) -> str:
    code = ""
    for _ in range(code_length):
        code += str(random.randint(0, number_of_colors - 1))
    return code


def validate_code_input(code: str, expected_length: int, max_color: int) -> list[int]:
    if len(code) != expected_length:
        raise ValueError(
            f"Code must be exactly {expected_length} digits long, got '{code}'"
        )
    if not code.isdigit():
        raise ValueError("Code must contain only digits")

    digits: list[int] = list(map(int, code))
    for digit in digits:
        if not check_color(digit, max_color):
            raise ValueError(
                f"Digit {digit} is out of range, must be between 0 and {max_color - 1}"
            )
    return digits


def display_board(board) -> None:
    print("-" * 40)
    for i, row in enumerate(board.board):
        if row.is_filled:
            guess_str = "".join(map(str, row.guess))
            print(f"Guess {i + 1}: {guess_str} | Bulls: {row.bulls} | Cows: {row.cows}")
        else:
            print(f"Guess {i + 1}: {'_' * board.code_length}")


def validate_secret_code(
    secret_code: str, code_length: int, num_of_colors: int
) -> list[int]:
    if secret_code is None:
        raise ValueError("secret code cannot be None")
    secret_digits = validate_code_input(secret_code, code_length, num_of_colors)
    return secret_digits


def check_color(color: int, num_of_colors: int) -> bool:
    return 0 <= color < num_of_colors


def check_board_row_index(board_row_index: int, num_of_guesses: int) -> bool:
    return 0 <= board_row_index < num_of_guesses
