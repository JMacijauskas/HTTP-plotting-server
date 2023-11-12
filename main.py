import requests
import random

"""
run HTTP server (socket)
each user sends point to extend graph
use matplotlib for displaying data
have queue for multiple clients to display data one after other
display time duration, if queue exists?
display in tkinter? or web
identifier?
constantly update display for users?
"""

"""
User POST coordinate -> server -> Queue -> parse coordinate -> add to plot -> display in main view
"""

COORD_RANGE = (-100, 100)


def coordinate_generator():
    return {'x': random.randint(*COORD_RANGE), 'y': random.randint(*COORD_RANGE)}


def send_point(endpoint: str | bytes) -> None:
    post_coord = coordinate_generator()
    print(requests.post(url=endpoint, data=post_coord))


if __name__ == '__main__':
    send_point('http://localhost:7789')
    send_point('http://localhost:7789')
