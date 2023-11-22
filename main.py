from time import sleep
import threading
import requests
from Generators import function_point_generator
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
        self.generator_initialized = None
        self.url = target_url
        self.single_connection = requests.Session()
        self.generator_params = generator_params
        self.plot_type = plot_type

    def send_points(self) -> None:
        for coordinate in self.generator(*self.generator_params):
            print(self.single_connection.post(url=self.url, headers={'Graph-Type': self.plot_type.value}, data=coordinate))

    def send_point(self) -> None:
        if not self.generator_initialized:
            self.generator_initialized = self.generator(*self.generator_params)
        try:
            print(self.single_connection.post(url=self.url, headers={'Graph-Type': self.plot_type.value}, data=self.generator_initialized.__next__()))
        except StopIteration:
            return

    def send_points_threaded(self):
        client_thread = threading.Thread(target=self.send_points)
        client_thread.start()


if __name__ == '__main__':
    client1 = Client('http://localhost:7789', GraphPlot.plot, function_point_generator, ((-10, 10), lambda x: 2*x))
    client2 = Client('http://localhost:7789', GraphPlot.scatter, function_point_generator, ((-50, 50), lambda x: 2*x + 20))
    client3 = Client('http://localhost:7789', GraphPlot.bar, function_point_generator, ((-100, 100), lambda x: 1 / (0.1 *x + 2.1)))
    client4 = Client('http://localhost:7789', GraphPlot.stairs, function_point_generator, ((-50, 50), lambda x: 2 * x ** 2))
    # for i in range(200):
    #     sleep(0.2)
    #     client1.send_point()
    #     client2.send_point()
    #     client3.send_point()
    #     client4.send_point()

    client1.send_points_threaded()
    client2.send_points_threaded()
    client3.send_points_threaded()
    client4.send_points_threaded()
