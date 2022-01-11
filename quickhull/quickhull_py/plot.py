import matplotlib.pyplot as plt

class Simulation:
    def __init__(self):
        self.demo = None

    def set_mode(self, interactive):
        self.demo = { 'interactive': interactive }

    def __ffw(self):
        self.set_mode(False)

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
        if self.demo['interactive']:
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
