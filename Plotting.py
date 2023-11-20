from typing import Optional

import matplotlib.pyplot as plt
import numpy as np

from ProjectEnums import GraphPlot
from Generators import random_coordinate_generator

# Plot multiple clients on same graph


class Plotter:
    def __init__(self):
        self.axes = {}
        plt.ion()
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot()

    def display_point(self, x_: float, y_: float, graph_id: int, graph_type: Optional[GraphPlot], graph_color: str):
        if graph_id not in self.axes:  # use get
            x = np.array([x_])
            y = np.array([y_])
            self.axes[graph_id] = {'x': x, 'y': y, 'color': graph_color, 'type': graph_type}
        else:
            x = np.append(self.axes[graph_id]['x'], [x_])
            y = np.append(self.axes[graph_id]['y'], [y_])
            self.axes[graph_id]['x'] = x
            self.axes[graph_id]['y'] = y

        self.add_plots()

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def add_plots(self):
        for _, plot in self.axes.items():
            graph_type = plot['type']
            graph_color = plot['color']
            x = plot['x']
            y = plot['y']

            if not graph_type or graph_type == GraphPlot.plot:
                self.ax.plot(x, y, color=graph_color)
            elif graph_type == GraphPlot.scatter:
                self.ax.scatter(x, y, color=graph_color)
            elif graph_type == GraphPlot.bar:
                self.ax.bar(x, y, color=graph_color)
            elif graph_type == GraphPlot.stairs:
                self.ax.stairs(y, color=graph_color)
            elif graph_type == GraphPlot.stem:
                self.ax.stem(x, y, linefmt=graph_color, markerfmt=graph_color)
            else:
                raise ValueError('Unsupported graph type was provided.')


if __name__ == '__main__':
    plat = Plotter()
    for point in random_coordinate_generator(50):
        plat.display_point(point['x'], point['y'], GraphPlot.scatter, 'y')
