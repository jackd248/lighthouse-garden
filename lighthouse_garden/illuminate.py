#!/usr/bin/env python3
# -*- coding: future_fstrings -*-

import argparse
import os
import sys

from lighthouse_garden.utility import info, system
from lighthouse_garden.lighthouse import process
from lighthouse_garden.export import render


class Lighthouse:
    """
    Fetch lighthouse performance data.
    """
    def __init__(self,
                 config_file=None,
                 verbose=False,
                 config={}
                 ):
        """
        Initialization
        :param config_file:
        :param verbose:
        :param config:
        """
        info.print_header()
        system.check_args(config_file=config_file,
                          verbose=verbose)
        system.check_config(config)
        system.check_lighthouse_version()
        process.fetch_data()
        render.generate_dashboard()
        info.print_footer()
