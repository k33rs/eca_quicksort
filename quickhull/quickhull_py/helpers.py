import random
import numpy as np
import numpy.linalg as la

def line_dist(p1, p2, p):
    """
    Return the distance between the point p
    and the line joining points p1 and p2.
    """
    p1v, p2v, pv = np.array(p1), np.array(p2), np.array(p)
    return la.det([p2v - p1v, pv - p1v])

def find_side(p1, p2, p):
    """
    Return the side of point p
    wrt the line joining points p1 and p2.
    """
    dist = line_dist(p1, p2, p)

    if dist > 0:
        return 1
    if dist < 0:
        return -1
    return 0

def line_dist_side(p1, p2, p):
    """
    Return the absolute distance and the side of point p
    wrt the line joining points p1 and p2.
    """
    dist = line_dist(p1, p2, p)

    side = 0
    if dist > 0:
        side = 1
    if dist < 0:
        side = -1

    return abs(dist), side

def remove_triangle(points, p0, p1, p2):
    """
    Remove points that are inside the triangle p0, p1, p2
    from the given set of points.
    """
    v0 = np.array(p2)
    v1 = np.array(p0) - v0
    v2 = np.array(p1) - v0

    d = la.det([v1, v2])
    if d == 0:
        return

    for p in list(points):
        v = np.array(p)
        a = (la.det([v, v2]) - la.det([v0, v2])) / d
        b = - (la.det([v, v1]) - la.det([v0, v1])) / d

        if a > 0 and b > 0 and a + b < 1:
            points.remove(p)

def random_points(n, a, b):
    """Generate n uniformly random points in [a,b]"""
    res = set()
    for _ in range(n):
        res.add((random.uniform(a, b), random.uniform(a, b)))
    return res

def project(p1, p2, p):
    """
    Compute the orthogonal projection of point p
    on the line joining points p1 and p2.
    """
    p1v, p2v, pv = np.array(p1), np.array(p2), np.array(p)
    a = ((pv-p1v) @ (p2v-p1v)) / la.norm(p2v-p1v)**2
    return (1-a)*p1v + a*p2v
