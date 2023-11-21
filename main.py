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
    def __init__(self, target_url: str, plot_type: GraphPlot, data_generator, generator_params: tuple):
        self.generator = data_generator
        self.url = target_url
        self.single_connection = requests.Session()
        self.generator_params = generator_params
        self.plot_type = plot_type

    def send_points(self, ) -> None:
        for coordinate in self.generator(*self.generator_params):
            print(self.single_connection.post(url=self.url, headers={'Graph-Type': self.plot_type.value}, data=coordinate))


if __name__ == '__main__':
    client = Client('http://localhost:7789', GraphPlot.stairs, function_point_generator, ((-50, 50), lambda x: x ** 3 - x ** 2))
    client.send_points()
