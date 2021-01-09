#!/usr/bin/env python3
# -*- coding: future_fstrings -*-

import datetime
import json
import os
import sys
from collections import defaultdict

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

    _result = defaultdict(dict)
    _result = {
        'title': target['title'],
        'url': target['url'],
        'performance': {
            'value': _performance
        },
        'report': f'{utility.get_data_dir(absolute_path=False)}{file_name}.report.html',
        'date': '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
    }

    # audits
    if _report['audits']['first-contentful-paint']:
        _result['performance']['first-contentful-paint'] = _report['audits']['first-contentful-paint']['displayValue']

    if _report['audits']['largest-contentful-paint']:
        _result['performance']['largest-contentful-paint'] = _report['audits']['largest-contentful-paint']['displayValue']

    if _report['audits']['speed-index']:
        _result['performance']['speed-index'] = _report['audits']['speed-index']['displayValue']

    if _report['audits']['total-blocking-time']:
        _result['performance']['total-blocking-time'] = _report['audits']['total-blocking-time']['displayValue']

    if _report['audits']['interactive']:
        _result['performance']['interactive'] = _report['audits']['interactive']['displayValue']

    if _report['audits']['cumulative-layout-shift']:
        _result['performance']['cumulative-layout-shift'] = _report['audits']['cumulative-layout-shift']['displayValue']

    # average
    _result['average'] = {
        'value': get_average_by_attribute(target, 'performance', _performance),
        'min': get_average_peak(target, 'performance', _performance, True),
        'max': get_average_peak(target, 'performance', _performance, False)
    }

    # additional metrics
    if 'accessibility' in _report['categories'] and _report['categories']['accessibility']['score']:
        _result['accessibility']['value'] = int(round(_report['categories']['accessibility']['score'] * 100))

    if 'best-practices' in _report['categories'] and _report['categories']['best-practices']['score']:
        _result['best-practices']['value'] = int(round(_report['categories']['best-practices']['score'] * 100))

    if 'seo' in _report['categories'] and _report['categories']['seo']['score']:
        _result['seo']['value'] = int(round(_report['categories']['seo']['score'] * 100))

    return _result


def get_data(target, file_suffix=''):
    """

    :param target:
    :param file_suffix:
    :return:
    """
    data_file = f'{utility.get_data_dir()}_{target["identifier"]}{file_suffix}.json'
    if os.path.isfile(data_file):
        with open(data_file, 'r') as read_file:
            return json.load(read_file)
    else:
        return []


def set_data(target, data, file_suffix=''):
    """

    :param target:
    :param data:
    :param file_suffix:
    :return:
    """
    data_file = f'{utility.get_data_dir()}_{target["identifier"]}{file_suffix}.json'
    with open(data_file, 'w') as write_file:
        json.dump(data, write_file)


def add_value_to_history(target, result):
    """

    :param target:
    :param result:
    :return:
    """
    _data = get_data(target, '.history')
    while len(_data) > system.config['keep_history']:
        utility.remove_file(f'{utility.get_export_dir()}{_data[0]["report"]}')
        del _data[0]
    _data.append(result)
    set_data(target, _data, '.history')


def get_average_by_attribute(target, attribute):
    """

    :param target:
    :param attribute:
    :return:
    """
    history_data = get_history_by_attribute(target, attribute)
    return sum(history_data) / float(len(history_data))


def get_average_peak(target, attribute, min_max=True):
    """

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

    :param target:
    :param attribute:
    :return:
    """
    history_data = []
    for history in get_data(target, '.history'):
        history_data.append(history[attribute])
    return history_data


def get_target_by_attribute(value, attribute):
    for target in system.config['targets']:
        if target[attribute] == value:
            return target
    return None


def get_last_results():
    results = []
    for target in system.config['targets']:
        _result = get_data(target)
        if _result:
            results.append(_result)

    # sort by performance
    results.sort(key=lambda x: x['performance'], reverse=True)

    return results


def get_last_value(target, attribute):
    _result = get_data(target, '.history')
    return _result[-1][attribute]


def sort_by_average(results):
    # sort by average
    results.sort(key=lambda x: x['average']['value'], reverse=True)
    return results
