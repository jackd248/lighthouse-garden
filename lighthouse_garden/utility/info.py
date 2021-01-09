#!/usr/bin/env python3
# -*- coding: future_fstrings -*-

from lighthouse_garden import info
from lighthouse_garden.utility import output, system


def print_header():
    """
    Printing console header
    :return:
    """
    print(f'{output.CliFormat.BLACK}#################################################{output.CliFormat.ENDC}')
    print(f'{output.CliFormat.BLACK}#                                               #{output.CliFormat.ENDC}')
    print(f'{output.CliFormat.BLACK}#{output.CliFormat.ENDC}               LIGHTHOUSE GARDEN               {output.CliFormat.BLACK}#{output.CliFormat.ENDC}')
    print(f'{output.CliFormat.BLACK}#                    v{info.__version__}                     #{output.CliFormat.ENDC}')
    print(f'{output.CliFormat.BLACK}# {info.__homepage__} #{output.CliFormat.ENDC}')
    print(f'{output.CliFormat.BLACK}#                                               #{output.CliFormat.ENDC}')
    print(f'{output.CliFormat.BLACK}#################################################{output.CliFormat.ENDC}')


def print_footer():
    """
    Printing console footer
    :return:
    """
    if 'errors' in system.config:
        output.println(f'{output.Subject.WARNING} Errors occurred during execution, see console output for more information')
    else:
        output.println(f'{output.Subject.OK} Successfully fetched lighthouse data')


def get_target_name(target):
    """

    :param target: Dict
    :return:
    """
    _name = target['url']
    if 'title' in target:
        _name = f'{target["title"]} ({_name})'
    return _name
