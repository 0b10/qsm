import argparse
import sys
from qsm import __version__
from qsm.template import update


def get_parser():
    """
    Creates a new argument parser.
    """
    parser = argparse.ArgumentParser('qsm')
    version = '%(prog)s ' + __version__
    parser.add_argument("--version", "-v", action="version", version=version)
    parser.add_argument("target", help="a vm name, template name, or 'dom0'")

    # package manager: --update, --install
    pman_group = parser.add_mutually_exclusive_group()
    # pman_group.add_argument("-i", "--install", nargs="+", help="install packages on the target")
    pman_group.add_argument(
        "-u", "--update", action="store_true", help="update the target")

    return parser


def main(args=None):
    """
    Main entry point for your project.

    Args:
        args : list
            A of arguments as if they were input in the command line. Leave it
            None to use sys.argv.
    """
    parser = get_parser()
    args = parser.parse_args(args)

    if args.update:
        update(args.target)
        sys.exit(0)

    # if args.install:
    #     print("installing", args.install)
    #     sys.exit(0)


if __name__ == '__main__':
    main()
