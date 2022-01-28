from math import inf
from operator import gt, lt
from .plot import Simulation
from .helpers import line_dist_side, find_side, remove_triangle

lines = set()
sim = Simulation()

def reduce_op(t1, t2, op):
    """
    Choose one tuple by evaluating the given operator on the first items.
    """
    return t1 if op(t1[0], t2[0]) else t2

def quickhull_onside(points, p1, p2, side, comm):
    """
    Find the points in the convex hull on one side of the line joining p1 and p2.
    """
    pmax = None
    max_dist = 0
    # find point pₘ farthest from the line p₁-p₂
    for p in points:
        dist, tside = line_dist_side(p1, p2, p)
        if tside == side and dist > max_dist:
            pmax = p
            max_dist = dist

    max_dist, pmax = comm.allreduce((max_dist, pmax), lambda t1, t2: reduce_op(t1, t2, gt))
    # if no point is found, add p₁ and p₂ to the convex hull
    if not pmax:
        if comm.Get_rank() == 0:
            lines.add((p1, p2))
        return

    # find convex hull points outside the triangle
    remove_triangle(points, pmax, p1, p2)
    quickhull_onside(points, pmax, p1, -find_side(pmax, p1, p2), comm)
    quickhull_onside(points, pmax, p2, -find_side(pmax, p2, p1), comm)

def quickhull(points, comm):
    """
    Find the points in the convex hull, given a set of points.
    """
    # find points with min and max x-coordinates
    rnd_elem = points.pop() if len(points) > 0 else None
    min_x = rnd_elem if rnd_elem is not None else ( inf,  inf)
    max_x = rnd_elem if rnd_elem is not None else (-inf, -inf)
    for p in points:
        if p[0] < min_x[0]:
            min_x = p
        if p[0] > max_x[0]:
            max_x = p

    min_x = comm.allreduce(min_x, lambda p1, p2: reduce_op(p1, p2, lt))
    max_x = comm.allreduce(max_x, lambda p1, p2: reduce_op(p1, p2, gt))
    # find the points in the convex hull on both sides of the line joining min_x and max_x
    quickhull_onside(points, min_x, max_x,  1, comm)
    quickhull_onside(points, min_x, max_x, -1, comm)

    return comm.gather(points)
