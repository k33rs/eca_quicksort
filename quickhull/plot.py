import matplotlib.pyplot as plt
import numpy as np

class Simulation:
    def __init__(self):
        self.mode = None

    def set_mode(self, interactive):
        self.mode = { 'interactive': interactive }

    def __ffw(self):
        self.set_mode(False)

    def project(self, p1, p2, p):
        """
        Compute the orthogonal projection of point p
        on the line joining points p1 and p2.
        """
        a1 = np.array(p2) - np.array(p1)
        a2 = a1.copy()[::-1]
        a2[0] = -a2[0]
        a = np.array([a1, a2])
        b = np.array([
            p[0] * (p2[0] - p1[0]) + p[1] * (p2[1] - p1[1]),
            p1[1] * (p2[0] - p1[0]) - p1[0] * (p2[1] - p1[1])
        ])
        return np.linalg.solve(a, b)

    @staticmethod
    def plot_points(points):
        """Plot a set of points."""
        plt.plot([p[0] for p in points], [p[1] for p in points], '.', color='crimson', zorder=20)

    @staticmethod
    def plot_line(p1, p2, color=None):
        """Plot a line between points p1 and p2."""
        line, = plt.plot([p1[0], p2[0]], [p1[1], p2[1]], '-', color=color, zorder=10)
        return line

    def plot_commit(self, print_msg=''):
        """Apply changes to plot."""
        if self.mode['interactive']:
            print(print_msg)
            inp = input('Press Enter to continue (q to quit): ')
            print()
            if inp == 'q':
                self.__ffw()
            plt.show()
        else:
            plt.pause(0.1)

    def step_in(self, p1, p2, print_msg, color=None):
        self.plot_commit(print_msg)
        return self.plot_line(p1, p2, color)

    def step_out(self, line, print_msg):
        self.plot_commit(print_msg)
        line.remove()

    def step_sol(self, p1, p2):
        self.plot_commit('{} and {} are in the convex hull'.format(p1, p2))
        self.plot_line(p1, p2, color='royalblue')
