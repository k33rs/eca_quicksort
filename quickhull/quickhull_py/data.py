from mpi4py import MPI

cli_usage = {
    'description': 'Run the Quickhull algorithm on a set of n random points (x,y) ∈ [a,b]',
    'args': {
        'n': {
            'metavar': 'n',
            'type': int,
            'help': 'the number of points in the set'
        },
        'a': {
            'metavar': 'a',
            'type': int,
            'help': 'left endpoint of interval [a,b]'
        },
        'b': {
            'metavar': 'b',
            'type': int,
            'help': 'right endpoint of inverval [a,b]'
        },
    }
}

class Discretization:
    """Simple class to hold discretization specifics"""
    def __init__(self, startx, starty, nx, ny) -> None:
        self._startx = startx
        self._starty = starty
        self._nx = nx
        self._ny = ny

    @property
    def startx(self):
        return self._startx

    @property
    def starty(self):
        return self._starty

    @property
    def nx(self):
        return self._nx

    @property
    def ny(self):
        return self._ny

class Domain:
    """Simple class to hold two-dimensional subdomain specifics"""
    def __init__(self, comm, discretization) -> None:
        # set communicator
        self._comm = comm
        # get size & rank
        self._size = comm.Get_size()
        self._rank = comm.Get_rank()
        # compute a distribution of processes per coordinate direction
        self._dims = [0, 0]
        self._dims = MPI.Compute_dims(self._size, self._dims)
        # create two-dimensional non-periodic Cartesian topology
        self._periods = [False, False]
        self._comm_cart = self._comm.Create_cart(self._dims, periods=self._periods)
        # get rank's coordinates in the topology
        self._coords = self._comm_cart.Get_coords(self._rank)
        # global start/end index in (sub)domain discretization
        chunky = discretization.ny // self._dims[0]
        self._starty = discretization.starty + chunky * self._coords[0]
        if self._coords[0] == self._dims[0] - 1:
            self._endy = discretization.starty + discretization.ny
        else:
            self._endy = self._starty + chunky
        chunkx = discretization.nx // self._dims[1]
        self._startx = discretization.startx + chunkx * self._coords[1]
        if self._coords[1] == self._dims[1] - 1:
            self._endx = discretization.startx + discretization.nx
        else:
            self._endx = self._startx + chunkx

    @property
    def comm(self):
        """MPI communicator"""
        return self._comm

    @property
    def size(self):
        """MPI size"""
        return self._size

    @property
    def rank(self):
        """MPI rank"""
        return self._rank

    @property
    def dims(self):
        """"Number of processes in x and y dimension"""
        return self._dims

    @property
    def comm_cart(self):
        """MPI Cartesian topology communicator"""
        return self._comm_cart

    @property
    def coords(self):
        """Rank's Cartesian coordinates in Cartesian topology"""
        return self._coords

    @property
    def startx(self):
        return self._startx

    @property
    def starty(self):
        return self._starty

    @property
    def endx(self):
        return self._endx

    @property
    def endy(self):
        return self._endy

    def includes(self, p):
        """Find whether point p is in the subdomain"""
        x, y = p
        inx = x >= self._startx and x < self._endx
        iny = y >= self._starty and y < self._endy
        return inx and iny

    def print(self):
        """Print domain decomposition specifics"""
        if self._rank == 0:
            print(
                "{:d} processes decomposed into a".format(self._size),
                "{:d} x {:d} Cartesian topology".format(self._dims[0], self._dims[1]),
                flush=True
            )
        self._comm.Barrier()
        for irank in range(self._size):
            self._comm.Barrier()
            if self._rank == irank:
                print(
                    MPI.Get_processor_name(),
                    "rank {:2d}/{:2d} :".format(self._rank, self._size),
                    "coords ({:2d},{:2d})".format(self._coords[0], self._coords[1]),
                    "start ({:4d},{:4d})".format(self._startx, self._starty),
                    "end ({:4d},{:4d})".format(self._endx, self._endy),
                    flush=True
                )
