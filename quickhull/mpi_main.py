from argparse import ArgumentParser
from matplotlib import pyplot as plt
from mpi4py import MPI
import pickle
import time
from quickhull_py.data import cli_usage, Discretization, Domain
from quickhull_py.quickhull_mpi import quickhull, lines, sim

if __name__ == "__main__":
    # parse cli args
    parser = ArgumentParser(description=cli_usage['description'])
    for arg_name, arg_config in cli_usage['args'].items():
        parser.add_argument(arg_name, **arg_config)
    args = parser.parse_args()
    # init MPI communicator, size and rank
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()
    # init discretization and domain
    start, end = args.a, args.b
    nx = end - start
    discretization = Discretization(start, start, nx, nx)
    domain = Domain(comm, discretization)
    domain.print()
    # read set of points from file
    with open(f'./data/{args.n}.data', 'rb') as file:
        points_global = pickle.load(file)
    points_global = comm.bcast(points_global)
    points_local = set(filter(lambda p: domain.includes(p), points_global))
    # run algorithm - measure time (sec)
    timespent = - time.perf_counter()
    hull = quickhull(points_local, comm)
    timespent += time.perf_counter()
    # plot results
    if rank == 0:
        print("The points in the convex hull are:\n", hull, '\n')

        fig = plt.figure(num='quickhull')
        ax = fig.add_subplot(111)
        ax.set_aspect('equal', adjustable='box')
        plt.tick_params(axis='x', which='both', bottom=True, top=False, labelbottom=True)
        plt.tick_params(axis='y', which='both', left=True, right=False, labelleft=True)

        sim.plot_points(points_global)
        for p1, p2 in lines:
            sim.plot_line(p1, p2, color='royalblue')

        plt.savefig('convex-hull.png')

        file = open('plot.data', 'a')
        file.write(f'{size} {timespent}\n')
        file.close()
