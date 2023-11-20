import random
from typing import Callable, Iterator
from matplotlib.colors import BASE_COLORS

COORD_RANGE = (-1000, 1000)


def random_coordinate_generator(num: int) -> Iterator[dict[str, float]]:
    for i in range(num):
        yield {'x': random.randint(*COORD_RANGE) / 10, 'y': random.randint(*COORD_RANGE) / 10}


def function_point_generator(range_interval: tuple[int, int], func: Callable) -> Iterator[dict[str, float]]:
    for i in range(*range_interval):
        yield {'x': i, 'y': func(i)}


def color_generator():
    while True:
        yield from BASE_COLORS.keys()
