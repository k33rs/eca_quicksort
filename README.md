# Quickhull implementation

## Run sequential Quickhull

    $ python3 -m quickhull 100

N.B.: the argument is the number of points *n*.

## Run sequential Quickhull with interactive demo

    $ python3 -m quickhull 100 --demo

## Run distributed Quickhull

Running the parallel version requires *mpi4py*:

    $ pip3 install mpi4py
    $ cd quickhull
    $ mpiexec -n 4 python3 mpi_main.py 1000 -100 100

N.B.: the *-n* argument specifies the number of processes to run; the last two arguments are the limits in the 2D domain.

## Run scaling analysis

Run **plot.sh** on 2 compute nodes with 32 processes and 16 max processes per node.

For example, with slurm:

    sbatch -N 2 -n 32 --ntasks-per-node=16 --exclusive plot.sh
