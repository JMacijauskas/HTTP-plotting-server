from time import sleep
from typing import Optional
import matplotlib.pyplot as plt
import numpy as np
from ProjectEnums import GraphPlot
from Generators import random_coordinate_generator


class Plotter:
    def __init__(self):
        self.axes = {}
        plt.ion()
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot()

    def display_point(self, x_: float, y_: float, graph_id: int, graph_type: Optional[GraphPlot], graph_color: str):
        graph_axes = self.axes.get(graph_id)
        if graph_axes:
            graph_axes['x'] = np.append(graph_axes['x'], [x_])
            graph_axes['y'] = np.append(graph_axes['y'], [y_])
        else:
            self.axes[graph_id] = {'x': np.array([x_]), 'y': np.array([y_]), 'color': graph_color, 'type': graph_type}

        self.add_existing_plots()

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def add_existing_plots(self):
        for plot in self.axes.values():
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


class PeriodicPlotter:
    def __init__(self, data: dict):
        self.axes = data
        plt.ion()
        self.refresh_interval = 0.5
        self.fig, self.ax = plt.subplots(2, 3)
        self.plot_map = {
            GraphPlot.plot.value: {'axis': self.ax[0, 0], 'plot_func': self.ax[0, 0].plot},
            GraphPlot.scatter.value: {'axis': self.ax[0, 1], 'plot_func': self.ax[0, 1].scatter},
            GraphPlot.bar.value: {'axis': self.ax[0, 2], 'plot_func': self.ax[0, 2].bar},
            GraphPlot.stairs.value: {'axis': self.ax[1, 0], 'plot_func': self.ax[1, 0].stairs},
            GraphPlot.stem.value: {'axis': self.ax[1, 1], 'plot_func': self.ax[1, 1].stem},
        }
        for plot_type in self.plot_map:
            self.plot_map[plot_type]['axis'].set_title(f'{plot_type} graph')

    def cycle_display(self):
        while True:
            sleep(self.refresh_interval)
            self.add_existing_plots()

            self.fig.canvas.draw()
            self.fig.canvas.flush_events()

    def add_existing_plots(self):
        for unique_plot_data in self.axes.values():
            for graph_type in self.plot_map:
                self.plot_graph(unique_plot_data, graph_type)

    def plot_graph(self, user_data: dict, graph_type: str):
        graph_data = user_data.get(graph_type)
        if graph_data:
            if graph_type == GraphPlot.stairs.value:
                coordinates = (graph_data['y'],)
            else:
                coordinates = (graph_data['x'], graph_data['y'])
            self.plot_map[graph_type]['plot_func'](*coordinates, color=user_data['color'])


if __name__ == '__main__':
    plat = Plotter()
    for point in random_coordinate_generator(50):
        plat.display_point(point['x'], point['y'], 999, GraphPlot.scatter, 'y')
