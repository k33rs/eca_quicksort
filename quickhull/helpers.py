def line_dist_signed(p1, p2, p):
    """
    Return the distance between the point p
    and the line joining the points p1 and p2.
    """
    return (p[1] - p1[1]) * (p2[0] - p1[0]) - (p2[1] - p1[1]) * (p[0] - p1[0])

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
