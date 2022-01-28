# Quickhull implementation

## Run sequential Quickhull

    $ python3 -m quickhull 100 -10 10

N.B.: arguments are a number of points *n* and the endpoints of the interval [*a*, *b*]. An input set of *n* 2D points (*x*, *y*) is randomly generated,
with *x* and *y* in [*a*, *b*].

## Run sequential Quickhull with interactive demo

    $ python3 -m quickhull 100 -10 10 --demo

## Run distributed Quickhull

Running the parallel version requires *mpi4py*:

    $ pip3 install mpi4py
    $ cd quickhull
    $ mpiexec -n 4 python3 mpi_main.py 1000 -100 100

N.B.: the *-n* argument specifies the number of processes to run.
