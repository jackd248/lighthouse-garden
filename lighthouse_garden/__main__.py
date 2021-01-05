#!/usr/bin/env python3
# -*- coding: future_fstrings -*-

import argparse, sys, os
from collections import defaultdict
# Workaround for ModuleNotFoundError
sys.path.append(os.getcwd())
from lighthouse_garden import illuminate


def main(args={}):
    """
    Main entry point for the command line. Parse the arguments and call to the main process.
    :param args:
    :return:
    """
    args = get_arguments(args)
    illuminate.Lighthouse(
        verbose=args.verbose,
        config_file=args.config,
        clear=args.clear
    )


def get_arguments(args):
    """
    Parses and returns script arguments
    :param args:
    :return:
    """
    parser = argparse.ArgumentParser(prog='lighthouse_garden', description='Monitoring performance data by lighthouse.')
    parser.add_argument('-v', '--verbose',
                        help='Enable extended console output',
                        required=False,
                        action='store_true')
    parser.add_argument('-c', '--config',
                        help='Path to config file',
                        required=False,
                        type=str)
    parser.add_argument('--clear',
                        help='Clear all performance data and reset the application',
                        required=False,
                        action='store_true')

    return parser.parse_args()


if __name__ == "__main__":
    main()
