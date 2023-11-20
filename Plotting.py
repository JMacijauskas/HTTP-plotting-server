from typing import Optional

import matplotlib.pyplot as plt
import numpy as np

from ProjectEnums import GraphPlot
from Generators import random_coordinate_generator

# Plot multiple clients on same graph


class Plotter:
    def __init__(self):
        self.x_points = np.array([])
        self.y_points = np.array([])
        plt.ion()
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot()
        # self.ax.plot(self.x_points, self.y_points)

    def display_point(self, x_: float, y_: float, graph_type: Optional[GraphPlot], graph_color: str):
        self.x_points = np.append(self.x_points, [x_])
        self.y_points = np.append(self.y_points, [y_])
        if not graph_type or graph_type == GraphPlot.plot:
            self.ax.plot(self.x_points, self.y_points, color=graph_color)
        elif graph_type == GraphPlot.scatter:
            self.ax.scatter(self.x_points, self.y_points, color=graph_color)
        elif graph_type == GraphPlot.bar:
            self.ax.bar(self.x_points, self.y_points, color=graph_color)
        elif graph_type == GraphPlot.stairs:
            self.ax.stairs(self.y_points, color=graph_color)
        elif graph_type == GraphPlot.stem:
            self.ax.stem(self.x_points, self.y_points, linefmt=graph_color, markerfmt=graph_color)
        else:
            raise ValueError('Unsupported graph type was provided.')

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()


if __name__ == '__main__':
    plat = Plotter()
    for point in random_coordinate_generator(50):
        plat.display_point(point['x'], point['y'], GraphPlot.scatter, 'y')
