import random


def generate_guess(code_length, number_of_colors):
    code = ""
    for _ in range(code_length):
        code += str(random.randint(0, number_of_colors - 1))
    return code
