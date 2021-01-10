#!/usr/bin/env python3
# -*- coding: future_fstrings -*-

import os
from lighthouse_garden.utility import output, system
from lighthouse_garden.export import render


def get_data_dir(absolute_path=True):
    """
    Return the data directory path and handle missing slashes
    :param absolute_path: Boolean
    :return:
    """
    _data_dir_path = ''
    if absolute_path:
        _data_dir_path += get_export_dir()
    _data_dir_path += f'/{system.config["data_dir"]}'
    if _data_dir_path[-1] != '/':
        _data_dir_path += '/'
    return _data_dir_path.replace('//', '/')


def get_export_dir():
    """
    Return the export directory path and handle missing slashes
    :return:
    """
    _export_dir_path = f'{system.config["export_path"]}'
    if _export_dir_path[-1] != '/':
        _export_dir_path += '/'
    return _export_dir_path


def remove_file(file_name):
    """
    Remove a local file
    :param file_name:
    :return:
    """
    if os.path.exists(file_name):
        os.remove(file_name)


def extend_html_report_with_info(result, file_name):
    """
    Extend the existing lighthouse html report with an additional info box
    :param result: Dict
    :param file_name: String
    :return:
    """
    if os.path.isfile(file_name):
        with open(file_name, "r") as read_file:
            _html = read_file.readlines()
            _info = render.render_template('partials/info.html.j2',
                                           title=result['title'],
                                           url=result['url'],
                                           date=result['date'],
                                           logo=render.render_logo()
                                           )
            _html[-2] = f'{_info}\n</body>\n</html>'
            del(_html[-1])

        with open(file_name, 'w') as file:
            output.println(f'{output.Subject.INFO} Extend html report with info box', verbose_only=True)
            file.writelines(_html)
