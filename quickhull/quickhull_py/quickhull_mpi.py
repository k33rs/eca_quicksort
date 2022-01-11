import math
from .plot import Simulation
from .helpers import line_dist, find_side

hull = set()
lines = set()
sim = Simulation()

def max_f(t1, t2):
    """
    Return the one tuple with greater second item.
    """
    d1, d2 = t1[1], t2[1]
    return t1 if d1 > d2 else t2

def quickhull_onside(points, p1, p2, side, comm):
    """
    Find the points in the convex hull on one side of the line joining p1 and p2.
    """
    pmax = None
    max_dist = 0
    # find point pₘ farthest from the line p₁-p₂
    for p in points:
        dist = line_dist(p1, p2, p)
        tside = find_side(p1, p2, p)
        if tside == side and dist > max_dist:
            pmax = p
            max_dist = dist

    pmax, max_dist = comm.allreduce((pmax, max_dist), max_f)
    # if no point is found, add p₁ and p₂ to the convex hull
    if not pmax:
        if comm.Get_rank() == 0:
            hull.add(p1)
            hull.add(p2)
            lines.add((p1, p2))
        return

    # find convex hull points outside the triangle
    quickhull_onside(points, pmax, p1, -find_side(pmax, p1, p2), comm)
    quickhull_onside(points, pmax, p2, -find_side(pmax, p2, p1), comm)

def quickhull(points, comm):
    """
    Find the points in the convex hull, given a set of points.
    """
    # find points with min and max x-coordinates
    min_x = points[0] if len(points) > 0 else ( math.inf,  math.inf)
    max_x = points[0] if len(points) > 0 else (-math.inf, -math.inf)
    for _, p in enumerate(points, 1):
        if p[0] < min_x[0]:
            min_x = p
        if p[0] > max_x[0]:
            max_x = p

    min_x = comm.allreduce(min_x, lambda p1, p2: p1 if p1[0] < p2[0] else p2)
    max_x = comm.allreduce(max_x, lambda p1, p2: p1 if p1[0] > p2[0] else p2)
    # find the points in the convex hull on both sides of the line joining min_x and max_x
    quickhull_onside(points, min_x, max_x,  1, comm)
    quickhull_onside(points, min_x, max_x, -1, comm)
