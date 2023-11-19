import random
from typing import Callable

COORD_RANGE = (-1000, 1000)


def random_coordinate_generator(num: int) -> dict[str, float]:
    for i in range(num):
        yield {'x': random.randint(*COORD_RANGE) / 10, 'y': random.randint(*COORD_RANGE) / 10}


def function_point_generator(num: int, func: Callable) -> dict[str, float]:
    for i in range(num):
        yield {'x': i, 'y': func(i)}
