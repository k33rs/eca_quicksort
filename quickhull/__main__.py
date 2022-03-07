import argparse
import pickle
import matplotlib.pyplot as plt
from .quickhull_py.data import cli_usage
from .quickhull_py.quickhull import quickhull, lines, sim

# parse cli args
parser = argparse.ArgumentParser(description=cli_usage['description'])
parser.add_argument('n', metavar='n', type=int, help='the number of points in the set')
parser.add_argument('--demo', action='store_true', help='run interactive demo')
args = parser.parse_args()

if args.demo:
    sim.set_mode(True)

# init plot
fig = plt.figure(num='quickhull')
ax = fig.add_subplot(111)
ax.set_aspect('equal', adjustable='box')
plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
plt.tick_params(axis='y', which='both', left=False, right=False, labelleft=False)

if sim.demo:
    plt.ion()
    sim.plot_commit('plotting set of points')

# read set of points from file and add to plot
with open('./quickhull/data/{}.data'.format(args.n), 'rb') as file:
    points = pickle.load(file)

sim.plot_points(points)

# run algorithm
quickhull(points)
print("The points in the convex hull are:\n")
print(points, '\n')

# plot results
if sim.demo is None:
    for p1, p2 in lines:
        sim.plot_line(p1, p2, color='royalblue')
    plt.savefig('convex-hull.png')

if sim.demo:
    plt.ioff()
    plt.show()
