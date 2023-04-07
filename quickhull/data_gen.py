from argparse import ArgumentParser
import pickle
from quickhull_py.data import cli_usage
from quickhull_py.helpers import random_points

if __name__ == "__main__":
    parser = ArgumentParser(description=cli_usage['description'])
    for arg_name, arg_config in cli_usage['args'].items():
        parser.add_argument(arg_name, **arg_config)
    args = parser.parse_args()

    points = random_points(args.n, args.a, args.b)

    with open(f'data/{args.n}.data', 'wb') as file:
        pickle.dump(points, file)
