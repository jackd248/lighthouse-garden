#!/usr/bin/env python3
# -*- coding: future_fstrings -*-

import datetime
import json
import os
import sys

from lighthouse_garden.utility import output, system
from lighthouse_garden.lighthouse import utility


def get_result_by_report_file(target, file_name):
    """

    :param target: Dict
    :param file_name: String
    :return:
    """
    output.println(f'{output.Subject.INFO} Processing result of report', verbose_only=True)
    _report_path = f'{utility.get_data_dir()}{file_name}.report.json'
    _report = None

    if os.path.isfile(_report_path):
        with open(_report_path, 'r') as read_file:
            _report = json.load(read_file)
    else:
        sys.exit(f'{output.Subject.ERROR} Report file not found: {_report_path}')

    if not isinstance(_report, dict):
        sys.exit(f'{output.Subject.ERROR} Report not readable')

    if _report['categories']['performance']['score']:
        _performance = int(round(_report['categories']['performance']['score'] * 100))
    else:
        return None

    _result = {
        'title': target['title'],
        'url': target['url'],
        'performance': _performance,
        'report': f'{utility.get_data_dir(absolute_path=False)}{file_name}.report.html',
        'date': '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
    }

    if 'accessibility' in _report['categories']:
        _result['accessibility'] = int(round(_report['categories']['accessibility']['score'] * 100))

    if 'best-practices' in _report['categories']:
        _result['best-practices'] = int(round(_report['categories']['best-practices']['score'] * 100))

    if 'seo' in _report['categories']:
        _result['seo'] = int(round(_report['categories']['seo']['score'] * 100))

    return _result


def get_data(target):
    data_file = f'{utility.get_data_dir()}_{target["identifier"]}.json'
    if os.path.isfile(data_file):
        with open(data_file, 'r') as read_file:
            return json.load(read_file)
    else:
        return []


def set_data(target, data):
    data_file = f'{utility.get_data_dir()}_{target["identifier"]}.json'
    with open(data_file, 'w') as write_file:
        json.dump(data, write_file)


def add_value_to_history(target, result):
    _data = get_data(target)
    while len(_data) > system.config['keep_history']:
        utility.remove_file(f'{utility.get_export_dir()}{_data[0]["report"]}')
        del _data[0]
    _data.append(result)
    set_data(target, _data)


def get_average_by_attribute(target, attribute):
    history_data = get_history_by_attribute(target, attribute)
    return sum(history_data) / float(len(history_data))


def get_history_by_attribute(target,attribute):
    history_data = []
    for history in get_data(target):
        history_data.append(history[attribute])
    return history_data


def get_target_by_attribute(value,attribute):
    for target in system.config['targets']:
        if target[attribute] == value:
            return target
    return None


def get_last_results():
    results = []
    for target in system.config['targets']:
        _result = get_data(target)
        if _result:
            results.append(_result[-1])

    # sort by performance
    results.sort(key=lambda x: x['performance'], reverse=True)

    return results


def add_average_data_and_sort(results):
    for result in results:
        result['average'] = get_average_by_attribute(get_target_by_attribute(result['title'], 'title'), 'performance')

    # sort by average
    results.sort(key=lambda x: x['average'], reverse=True)
    return results
