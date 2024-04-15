import string
from random import choice


def generate_code(digits: int = 6) -> str:
    return "".join(choice(string.digits) for _ in range(digits))
