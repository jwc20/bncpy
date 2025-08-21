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
        code += str(random.randint(1, number_of_colors))
    return code


async def get_random_number_async(
    length: int = 4,
    min_value: int = 1,
    max_value: int = 7,
    base: int = 10,
) -> str:
    if length <= 0:
        raise ValueError("Length must be a positive integer.")

    if min_value >= max_value:
        raise ValueError(
            f"min_value ({min_value}) must be less than max_value ({max_value})."
        )

    if base not in [2, 8, 10, 16]:
        raise ValueError("Base value must be 2, 8, 10, or 16.")

    if min_value < 0:
        raise ValueError("min_value cannot be negative for this implementation.")

    numbers: list[int]
    params = {
        "num": length,
        "min": min_value,
        "max": max_value,
        "col": 1,
        "base": 10,
        "format": "plain",
        "rnd": "new",
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                "https://www.random.org/integers/", params=params, timeout=5.0
            )
            response.raise_for_status()
            numbers_str = response.text.strip().split()
            if len(numbers_str) != length:
                raise ValueError(
                    f"API returned {len(numbers_str)} numbers, expected {length}"
                )
            numbers = [int(n) for n in numbers_str]
        except (httpx.RequestError, httpx.HTTPStatusError, ValueError) as e:
            # fallback
            logger.warning(
                "Failed to get random number from API: %s, falling back to local generation",
                e,
            )
            numbers = [random.randint(min_value, max_value) for _ in range(length)]

        return "".join(map(str, numbers))


def get_random_number(
    length: int = 4,
    min_value: int = 1,
    max_value: int = 7,
    base: int = 10,
) -> str:
    if length <= 0:
        raise ValueError("Length must be a positive integer.")

    if min_value >= max_value:
        raise ValueError(
            f"min_value ({min_value}) must be less than max_value ({max_value})."
        )

    if base not in [2, 8, 10, 16]:
        raise ValueError("Base value must be 2, 8, 10, or 16.")

    if min_value < 0:
        raise ValueError("min_value cannot be negative for this implementation.")

    numbers: list[int]
    params = {
        "num": length,
        "min": min_value,
        "max": max_value,
        "col": 1,
        "base": 10,
        "format": "plain",
        "rnd": "new",
    }

    try:
        response = httpx.get(
            "https://www.random.org/integers/", params=params, timeout=5.0
        )
        response.raise_for_status()
        numbers_str = response.text.strip().split()
        if len(numbers_str) != length:
            raise ValueError(
                f"API returned {len(numbers_str)} numbers, expected {length}"
            )
        numbers = [int(n) for n in numbers_str]

    except (httpx.RequestError, httpx.HTTPStatusError, ValueError) as e:
        # fallback
        logger.warning(
            "Failed to get random number from API: %s, falling back to local generation",
            e,
        )
        numbers = [random.randint(min_value, max_value) for _ in range(length)]

    return "".join(map(str, numbers))
