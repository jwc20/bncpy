import random


def generate_guess(code_length, number_of_colors):
    code = ""
    for _ in range(code_length):
        code += str(random.randint(0, number_of_colors - 1))
    return code


def validate_code_input(code: str, expected_length: int, max_color: int) -> list[int]:
    if len(code) != expected_length:
        raise ValueError(f"Code must be exactly {expected_length} digits long")
    if not code.isdigit():
        raise ValueError("Code must contain only digits")

    digits = list(map(int, code))
    for digit in digits:
        if not (0 <= digit < max_color):
            raise ValueError(f"Digit {digit} is out of range (0-{max_color - 1})")

    return digits
