from .plot import Simulation
from .helpers import line_dist, find_side

hull = set()
lines = set()
sim = Simulation()

def quickhull_onside(points, p1, p2, side):
    """
    Find the points in the convex hull on one side of the line joining p1 and p2.
    """
    pmax = None
    max_dist = 0

    # find the point with max distance from the line on the specified side
    for p in points:
        dist = line_dist(p1, p2, p)
        tside = find_side(p1, p2, p)
        if tside == side and dist > max_dist:
            pmax = p
            max_dist = dist

    # if no point is found, add p1 and p2 to the convex hull
    if not pmax:
        hull.add(p1)
        hull.add(p2)
        if sim.mode:
            sim.step_sol(p1, p2)
        else:
            lines.add((p1, p2))
        return

    if sim.mode:
        line = sim.step_in(p1, p2, 'plotting line from {} to {}'.format(p1, p2))
        proj = sim.project(p1, p2, pmax)
        perp = sim.step_in(pmax, proj, 'partitioning line from {} to {}'.format(p1, p2))

    # find convex hull points on both sides of the line
    quickhull_onside(points, pmax, p1, -find_side(pmax, p1, p2))
    quickhull_onside(points, pmax, p2, -find_side(pmax, p2, p1))

    if sim.mode:
        sim.step_out(perp, 'removing partitioning of line from {} to {}'.format(p1, p2))
        sim.step_out(line, 'removing line from {} to {}'.format(p1, p2))

def quickhull(points):
    """
    Find the points in the convex hull, given a set of points of size n.
    """
    if len(points) < 3:
        print('convex hull not possible')
        return

    # find the points with min and max x coordinates
    min_x, max_x = points[0], points[0]
    for _, p in enumerate(points, 1):
        if p[0] < min_x[0]:
            min_x = p
        if p[0] > max_x[0]:
            max_x = p

    if sim.mode:
        line = sim.step_in(min_x, max_x, 'plotting line from {} to {}'.format(min_x, max_x))

    # find the points in the convex hull on both sides of the line joining min_x and max_x
    quickhull_onside(points, min_x, max_x,  1)
    quickhull_onside(points, min_x, max_x, -1)

    if sim.mode:
        sim.step_out(line, 'removing line from {} to {}'.format(min_x, max_x))

    return hull
