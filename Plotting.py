import matplotlib.pyplot as plt
import numpy as np

from main import coordinate_generator


class Plotter:
    def __init__(self):
        self.x_points = np.array([])
        self.y_points = np.array([])
        plt.ion()
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot()
        # self.ax.plot(self.x_points, self.y_points)

    def display_point(self, x_: int, y_: int):
        self.x_points = np.append(self.x_points, [x_])
        self.y_points = np.append(self.y_points, [y_])
        self.ax.plot(self.x_points, self.y_points)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()


if __name__ == '__main__':
    plat = Plotter()
    for x in range(50):
        point = coordinate_generator()
        plat.display_point(point['x'], point['y'])
