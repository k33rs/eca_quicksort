import matplotlib.pyplot as plt
import argparse
import sys
from .quickhull import quickhull, sim, lines
from .helpers import random_points

parser = argparse.ArgumentParser(description='Run the Quickhull algorithm on a set of n random points (x,y) ∈ [a,b]')
parser.add_argument('n', metavar='n', type=int, help='the number of points in the set')
parser.add_argument('a', metavar='a', type=int, help='left endpoint of interval [a,b]')
parser.add_argument('b', metavar='b', type=int, help='right endpoint of inverval [a,b]')
parser.add_argument('--demo', action='store_true', help='run interactive demo')
args = parser.parse_args()

if args.demo:
    sim.set_mode(True)

fig = plt.figure(num='quickhull')
ax = fig.add_subplot(111)
ax.set_aspect('equal', adjustable='box')
plt.tick_params(axis='x', which='both', bottom=True, top=False, labelbottom=True)
plt.tick_params(axis='y', which='both', left=True, right=False, labelleft=True)

if sim.demo:
    plt.ion()
    sim.plot_commit('plotting set of points')

points = random_points(args.n, args.a, args.b)
sim.plot_points(points)

hull = quickhull(points)
if hull is None:
    sys.exit(1)

print("The points in the convex hull are:\n")
print(hull, '\n')

if not sim.demo:
    for p1, p2 in lines:
        sim.plot_line(p1, p2, color='royalblue')

plt.savefig('convex-hull.png')

if sim.demo:
    plt.ioff()
    plt.show()
