import logging
import random
from collections import Counter

import httpx

logger = logging.getLogger(__name__)


def check_color(color: int, num_of_colors: int) -> bool:
    return 0 < color <= num_of_colors


def validate_code_input(code: str, code_length: int, num_of_colors: int) -> list[int]:
    if len(code) != code_length:
        raise ValueError(
            f"Code must be exactly {code_length} digits long, got '{code}'"
        )
    if not code.isdigit():
        raise ValueError("Code must contain only digits")

    digits: list[int] = list(map(int, code))
    for digit in digits:
        if not check_color(digit, num_of_colors):
            raise ValueError(
                f"Digit {digit} is out of range, must be between 1 and {num_of_colors}"
            )
    return digits


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
    number: int = 4,
    minimum: int | None = 1,
    maximum: int = 7,
    base: int = 10,
) -> str:
    """generates random number from minimum to maximum inclusive"""
    # response type should be a string since converting to int removes leading zeros (EX: 0000 -> 0)

    if minimum is None:
        minimum = 1

    if minimum < 1 and minimum >= maximum:
        raise ValueError("Minimum should be greater than one and less than the maximum")

    if maximum <= 0:
        raise ValueError("Maximum value must be greater than minimum")

    if base not in [2, 8, 10, 16]:
        raise ValueError("Base value must be 2, 8, 10, or 16")

    params = {
        "num": number,
        "min": minimum,
        "max": maximum,
        "col": 1,
        "base": base,
        "format": "plain",
        "rnd": "new",
    }
    try:
        response = httpx.get("https://www.random.org/integers/", params=params)
        response.raise_for_status()
        cleaned_response = response.text.replace("\n", "")

        if len(cleaned_response) != number:
            raise ValueError(
                "Random number generator returned a number with %s digits, expected %s",
                len(cleaned_response),
                number,
            )

        return cleaned_response
    except (httpx.RequestError, httpx.HTTPStatusError) as e:
        logger.warning(
            "Failed to get random number from API: %s, falling back to local generation",
            e,
        )
        # Fallback to local random generation
        return "".join(
            str(random.randint(minimum or 0, maximum - 1)) for _ in range(number)
        )
