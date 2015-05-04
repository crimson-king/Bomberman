import math


def abs_ceil(number) -> int:
    """
    Returns absolute ceil. This is smallest integral value that following
    is True: abs(value) >= abs(number)
    """
    return math.floor(number) if number < 0 else math.ceil(number)
