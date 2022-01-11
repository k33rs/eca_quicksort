import random
import numpy as np
import numpy.linalg as la

def line_dist_signed(p1, p2, p):
    """
    Return the distance between the point p
    and the line joining the points p1 and p2.
    """
    p1v, p2v, pv = np.array(p1), np.array(p2), np.array(p)
    return la.det([p2v - p1v, pv - p1v])

def find_side(p1, p2, p):
    """
    Return the side of point p with respect to line
    joining points p1 and p2.
    """
    dist = line_dist_signed(p1, p2, p)

    if dist > 0:
        return 1
    if dist < 0:
        return -1
    return 0

def line_dist(p1, p2, p):
    """
    Return the absolute distance between the point p
    and the line joining the points p1 and p2.
    """
    return abs(line_dist_signed(p1, p2, p))

def random_points(n, a, b):
    """Generate n uniformly random points in [a,b]"""
    res = []
    for _ in range(n):
        res.append((random.uniform(a, b), random.uniform(a, b)))
    return res

def project(p1, p2, p):
    """
    Compute the orthogonal projection of point p
    on the line joining points p1 and p2.
    """
    p1v, p2v, pv = np.array(p1), np.array(p2), np.array(p)
    a1 = p2v - p1v
    a2 = a1.copy()[::-1]
    a2[0] = -a2[0]

    a = [a1, a2]
    b = [pv @ a1, la.det([a1, p1v])]

    return la.solve(a, b)
