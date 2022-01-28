import argparse
import matplotlib.pyplot as plt
from .quickhull_py.data import cli_usage
from .quickhull_py.helpers import random_points
from .quickhull_py.quickhull import quickhull, lines, sim

# parse cli args
parser = argparse.ArgumentParser(description=cli_usage['description'])
for arg_name, arg_config in cli_usage['args'].items():
    parser.add_argument(arg_name, **arg_config)
parser.add_argument('--demo', action='store_true', help='run interactive demo')
args = parser.parse_args()

if args.demo:
    sim.set_mode(True)

# init plot
fig = plt.figure(num='quickhull')
ax = fig.add_subplot(111)
ax.set_aspect('equal', adjustable='box')
plt.tick_params(axis='x', which='both', bottom=True, top=False, labelbottom=True)
plt.tick_params(axis='y', which='both', left=True, right=False, labelleft=True)

if sim.demo:
    plt.ion()
    sim.plot_commit('plotting set of points')

# generate set of points and add to plot
points = random_points(args.n, args.a, args.b)
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
