from time import sleep

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
User POST coordinate -> multi thread server -> Queue -> parse coordinate -> add to plot -> display in main view
"""

COORD_RANGE = (-100, 100)


def coordinate_generator():
    return {'x': random.randint(*COORD_RANGE), 'y': random.randint(*COORD_RANGE)}

# Client class -> param generator (coordinates)
# Generator as func (yield) and class (dunders)
# decide plotting graph type and plot type on init (x:timestamp, y:data)
def send_point(session, endpoint: str | bytes) -> None:
    print(post_coord := coordinate_generator())
    print(session.post(url=endpoint, data=post_coord))


if __name__ == '__main__':
    single_connection = requests.Session()
    for i in range(50):
        sleep(0.5)
        send_point(single_connection, 'http://localhost:7789')
