from .plot import Simulation
from .helpers import line_dist_side, find_side, remove_triangle, project

lines = set()
sim = Simulation()

def quickhull_onside(points, p1, p2, side):
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

    # if no point is found, return
    if not pmax:
        if sim.demo:
            sim.step_sol(p1, p2)
        else:
            lines.add((p1, p2))
        return

    if sim.demo:
        line = sim.step_in(p1, p2, 'plotting line from {} to {}'.format(p1, p2))
        proj = project(p1, p2, pmax)
        perp = sim.step_in(pmax, proj, 'partitioning line from {} to {}'.format(p1, p2))

    # find convex hull points outside the triangle
    remove_triangle(points, pmax, p1, p2)
    quickhull_onside(points, pmax, p1, -find_side(pmax, p1, p2))
    quickhull_onside(points, pmax, p2, -find_side(pmax, p2, p1))

    if sim.demo:
        sim.step_out(perp, 'removing partitioning of line from {} to {}'.format(p1, p2))
        sim.step_out(line, 'removing line from {} to {}'.format(p1, p2))

def quickhull(points):
    """
    Find the points in the convex hull, given a set of points.
    """
    # find the points with min and max x coordinates
    rnd_elem = points.pop()
    min_x, max_x = rnd_elem, rnd_elem
    for p in points:
        if p[0] < min_x[0]:
            min_x = p
        if p[0] > max_x[0]:
            max_x = p

    # find the points in the convex hull on both sides of the line joining min_x and max_x
    quickhull_onside(points, min_x, max_x,  1)
    quickhull_onside(points, min_x, max_x, -1)
