#!/usr/bin/env python3
# -*- coding: future_fstrings -*-

import json
import os
import shutil
import subprocess
import sys

from lighthouse_garden.utility import output
from lighthouse_garden.lighthouse import utility

config = {
    'verbose': False,
    'mute': False,
    'run': 1,
    'export': False,
    'export_path': None,
    'config_file_path': None,
    'data_dir': 'd/',
    'keep_history': 0,
    'title': 'Lighthouse Garden',
    'description': 'Monitoring performance data by Google Lighthouse',
    'lighthouse': {
        'chrome_flags': '--no-sandbox --headless --disable-gpu --ignore-certificate-errors --disable-dev-shm-usage',
        'options': '--quiet --no-enable-error-reporting --preset=desktop --disable-storage-reset'
    }
}


def check_args(config_file=None,
               verbose=False):
    """

    :param config_file:
    :param verbose:
    :return:
    """
    global config

    config['verbose'] = verbose

    if not config_file is None:
        config['config_file_path'] = config_file


def check_config(additional_config={}):
    """
    Checking configuration information by file or dictionary
    :param additional_config: Dictionary
    :return:
    """
    global config

    if config['config_file_path'] is None and additional_config == {}:
        sys.exit(f'{output.Subject.ERROR} Configuration is missing')

    if additional_config:
        config.update(additional_config)

    _config_file_path = config['config_file_path']
    if not _config_file_path is None:
        if os.path.isfile(_config_file_path):
            with open(_config_file_path, 'r') as read_file:
                config.update(json.load(read_file))
                output.println(
                    f'{output.Subject.INFO} Loading host configuration {output.CliFormat.BLACK}{_config_file_path}{output.CliFormat.ENDC}', verbose_only=True)
        else:
            sys.exit(f'{output.Subject.ERROR} Local configuration not found: {config["config_file_path"]}')


def run_command(command, return_output=False, allow_fail=False):
    """
    Run local command
    :param command: String Shell command
    :param return_output: Boolean Return shell command output
    :param allow_fail: Boolean
    :return:
    """
    output.println(
        f'{output.Subject.DEBUG}{output.Subject.CMD} {output.CliFormat.BLACK}{command}{output.CliFormat.ENDC}', verbose_only=True)

    res = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    out, err = res.communicate()

    if res.wait() != 0 and err.decode() != '':
        _error_message = f'{output.Subject.ERROR} {err.decode()}'
        if allow_fail:
            output.println(_error_message)
            return False
        else:
            sys.exit(_error_message)

    if return_output:
        return out.decode()

    return True


def check_lighthouse_version():
    """
    Check sshpass version
    :return:
    """
    _version = run_command('lighthouse --version', return_output=True)

    if _version:
        output.println(
            f'{output.Subject.INFO} lighthouse version {_version}',
            verbose_only=True
        )
        config['lighthouse']['version'] = _version


def check_path(path):
    """
    Create a path on the system if not exists
    :param path: String Directory path
    :return:
    """
    run_command(
        f'[ ! -d "{path}" ] && mkdir -p "{path}"'
    )


def clear_data():
    """
    Clear the performance data and the lighthouse garden dashboard
    :return:
    """
    output.println(f'{output.Subject.INFO} Clear data')
    _file_path = f'{config["export_path"]}index.html'
    _dir_path = utility.get_data_dir()

    if os.path.isfile(_file_path):
        os.remove(_file_path)

    shutil.rmtree(_dir_path)
