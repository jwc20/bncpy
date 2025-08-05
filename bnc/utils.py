import random


def generate_guess(code_length, number_of_colors):
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

    digits = list(map(int, code))
    for digit in digits:
        if not check_color(digit, max_color):
            raise ValueError(
                f"Digit {digit} is out of range, must be between 0 and {max_color - 1}"
            )

    return digits


def display_board(board):
    for row in board.board:
        print(row)


def check_secret_code(secret_code: str, code_length, num_of_colors):
    if secret_code is None:
        raise ValueError("secret code cannot be None")

    secret_digits = validate_code_input(secret_code, code_length, num_of_colors)
    return secret_digits


def check_color(color: int, num_of_colors) -> bool:
    return 0 <= color < num_of_colors


def check_board_row_index(board_row_index: int, num_of_guesses) -> bool:
    return 0 <= board_row_index < num_of_guesses
