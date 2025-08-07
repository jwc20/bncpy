import random

import httpx

from collections import Counter


def calculate_bulls_and_cows(
    secret_digits: list[int], guess_digits: list[int]
) -> tuple[int, int]:
    if not secret_digits:
        raise ValueError("Secret code must be set before calculating bulls and cows")

    bulls_count = 0
    for i in range(len(secret_digits)):
        if secret_digits[i] == guess_digits[i]:
            bulls_count += 1

    secret_counter = Counter(secret_digits)
    guess_counter = Counter(guess_digits)

    total_matches = 0
    for digit in guess_counter:
        if digit in secret_counter:
            total_matches += min(guess_counter[digit], secret_counter[digit])

    cows_count = total_matches - bulls_count
    return bulls_count, cows_count


def generate_guess(code_length: int, number_of_colors: int) -> str:
    code = ""
    for _ in range(code_length):
        code += str(random.randint(0, number_of_colors - 1))
    return code


def get_random_number(
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

    response = httpx.get("https://www.random.org/integers/", params=params)
    cleaned_response = response.text.replace("\n", "")

    if len(cleaned_response) != number:
        raise ValueError(
            f"Random number generator returned a number with {len(cleaned_response)} digits, expected {number}"
        )

    return cleaned_response
