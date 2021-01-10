#!/usr/bin/env python3
# -*- coding: future_fstrings -*-

import json
import os

from lighthouse_garden.utility import output, system
from lighthouse_garden.lighthouse import utility


def get_data(target, file_suffix=''):
    """
    Get json data file by target
    :param target: Dict
    :param file_suffix: String Additional suffix
    :return: Dict
    """
    data_file = f'{utility.get_data_dir()}_{target["identifier"]}{file_suffix}.json'
    if os.path.isfile(data_file):
        with open(data_file, 'r') as read_file:
            return json.load(read_file)
    else:
        return []


def set_data(target, data, file_suffix=''):
    """
    Write json data by target
    :param target: Dict
    :param data: Dict
    :param file_suffix: String Additional suffix
    :return:
    """
    data_file = f'{utility.get_data_dir()}_{target["identifier"]}{file_suffix}.json'
    with open(data_file, 'w') as write_file:
        json.dump(data, write_file)


def add_value_to_history(target, result):
    """
    Adding a new result value to the history data of a specific target
    :param target: Dict
    :param result: Dict
    :return:
    """
    _data = get_data(target, '.history')
    while len(_data) > system.config['keep_history']:
        output.println(f'{output.Subject.INFO} Cleaning history value', verbose_only=True)
        utility.remove_file(f'{utility.get_export_dir()}{_data[0]["report"]}')
        del _data[0]
    _data.append(result)
    set_data(target, _data, '.history')


def get_average_by_attribute(target, attribute):
    """
    Calculates the average value from a specific attribute by all available history values
    :param target: Dict
    :param attribute: String
    :return: Float
    """
    history_data = get_history_by_attribute(target, attribute)
    return sum(history_data) / float(len(history_data))


def get_average_peak(target, attribute, min_max=True):
    """
    Get the min or max value of a specific attribute by all available history values
    :param target:
    :param attribute:
    :param min_max:
    :return:
    """
    history_data = get_history_by_attribute(target, attribute)

    if min_max:
        return min(history_data)
    else:
        return max(history_data)


def get_history_by_attribute(target, attribute):
    """
    Fetch all history values of a specific attribute
    :param target: Dict
    :param attribute: String
    :return:
    """
    history_data = []
    for history in get_data(target, '.history'):
        history_data.append(history[attribute])
    return history_data


def get_target_by_attribute(value, attribute):
    """
    Return a target by a specific attribute
    :param value: String
    :param attribute: String
    :return:
    """
    for target in system.config['targets']:
        if target[attribute] == value:
            return target
    return None


def get_last_results():
    """
    Get last results of all targets
    :return: Dict
    """
    results = []
    for target in system.config['targets']:
        _result = get_data(target)
        if _result:
            results.append(_result)

    # sort by performance
    results.sort(key=lambda x: x['performance'], reverse=True)

    return results


def get_last_value(target, attribute):
    """
    Get the last value of a specific attribute
    :param target: Dict
    :param attribute: String
    :return:
    """
    _result = get_data(target, '.history')
    return _result[-1][attribute]


def sort_by_average(results):
    """
    Sort the dict by the average value
    :param results: Dict
    :return: Dict
    """
    # sort by average
    results.sort(key=lambda x: x['average']['value'], reverse=True)
    return results
