from time import sleep

import requests

from Generators import random_coordinate_generator, function_point_generator
from ProjectEnums import GraphPlot

"""
run HTTP server (socket)
each user sends point to extend their graph
use matplotlib for displaying data
have queue for multiple clients to display data one after other (possibly capture more than one current point addition per refresh tick)
display in tkinter? or web
limit request format per graph and user
constantly update display for users
"""

"""
User POST coordinate -> multi thread server -> Queue -> parse coordinate -> add to plot -> display in main view
"""

# Client class -> param generator (coordinates)
# Generator as func (yield) and class (dunders)
# decide plotting graph type and plot type on init (x:timestamp, y:data)


class Client:
    def __init__(self, target_url: str, data_generator):
        self.generator = data_generator
        self.url = target_url
        self.single_connection = requests.Session()

    def send_point(self, plot_type: GraphPlot) -> None:
        print(post_coord := self.generator.__next__())
        print(self.single_connection.post(url=self.url, headers={'Graph-Type': plot_type.value}, data=post_coord))


if __name__ == '__main__':
    client = Client('http://localhost:7789', function_point_generator((-50, 50), lambda x: x ** 3 - x ** 2))
    for i in range(100):
        sleep(0.5)
        client.send_point(GraphPlot.stairs)
