#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lighthouse_garden.utility import system


class CliFormat:
    """
    Provides text colors for command line.
    """

    def __init__(self):
        pass

    BEIGE = '\033[96m'
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLACK = '\033[90m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Subject:
    """
    Provides subjects for output in command line.
    """

    def __init__(self):
        pass

    TEST = f'{CliFormat.BEIGE}[TEST]{CliFormat.ENDC}'
    INFO = f'{CliFormat.BLUE}[INFO]{CliFormat.ENDC}'
    CI = f'{CliFormat.BEIGE}[CI]{CliFormat.ENDC}'
    OK = f'{CliFormat.GREEN}[OK]{CliFormat.ENDC}'
    WARNING = f'{CliFormat.YELLOW}[WARNING]{CliFormat.ENDC}'
    ERROR = f'{CliFormat.RED}[ERROR]{CliFormat.ENDC}'
    DEBUG = f'{CliFormat.BLACK}[DEBUG]{CliFormat.ENDC}'
    LOCAL = f'{CliFormat.BLACK}[LOCAL]{CliFormat.ENDC}'
    REMOTE = f'{CliFormat.BLACK}[REMOTE]{CliFormat.ENDC}'
    CMD = f'{CliFormat.BLACK}[CMD]{CliFormat.ENDC}'


def println(message, verbose_only=False):
    """
    Print a message to the console
    :param message: String
    :param verbose_only: Boolean
    :return:
    """
    if verbose_only and not system.config['verbose']:
        return
    print(message)
