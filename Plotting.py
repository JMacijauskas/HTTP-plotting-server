import matplotlib.pyplot as plt
import numpy as np


class Plotter:
    def __init__(self):
        self.x_points = np.array([11])
        self.y_points = np.array([23])
        plt.ion()
        # self.fig, self.ax = plt.subplots()
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot()
        self.line, = self.ax.plot(self.x_points, self.y_points)
        # self.fig.canvas.draw()

    def display_point(self, x: int, y: int):
        np.append(self.x_points, x)
        np.append(self.y_points, y)
        self.line.set_xdata(self.x_points)
        self.line.set_ydata(self.y_points)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
