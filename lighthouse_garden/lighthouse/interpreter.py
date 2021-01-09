#!/usr/bin/env python3
# -*- coding: future_fstrings -*-

import datetime
import json
import os
import sys
from collections import defaultdict

from lighthouse_garden.utility import output, system
from lighthouse_garden.lighthouse import utility, database


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

    _result = defaultdict(lambda: defaultdict(dict))
    _result = {
        'title': target['title'],
        'url': target['url'],
        'performance': _performance,
        'report': f'{utility.get_data_dir(absolute_path=False)}{file_name}.report.html',
        'link': f'#{target["identifier"]}',
        'date': '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
    }

    # additional metrics
    if 'accessibility' in _report['categories'] and _report['categories']['accessibility']['score']:
        _result['accessibility'] = int(round(_report['categories']['accessibility']['score'] * 100))

    if 'best-practices' in _report['categories'] and _report['categories']['best-practices']['score']:
        _result['best-practices'] = int(round(_report['categories']['best-practices']['score'] * 100))

    if 'seo' in _report['categories'] and _report['categories']['seo']['score']:
        _result['seo'] = int(round(_report['categories']['seo']['score'] * 100))

    database.add_value_to_history(target, _result)

    # audits
    _result['audits'] = {}
    if _report['audits']['first-contentful-paint']:
        _result['audits']['first-contentful-paint'] = _report['audits']['first-contentful-paint']['displayValue']

    if _report['audits']['largest-contentful-paint']:
        _result['audits']['largest-contentful-paint'] = _report['audits']['largest-contentful-paint'][
            'displayValue']

    if _report['audits']['speed-index']:
        _result['audits']['speed-index'] = _report['audits']['speed-index']['displayValue']

    if _report['audits']['total-blocking-time']:
        _result['audits']['total-blocking-time'] = _report['audits']['total-blocking-time']['displayValue']

    if _report['audits']['interactive']:
        _result['audits']['interactive'] = _report['audits']['interactive']['displayValue']

    if _report['audits']['cumulative-layout-shift']:
        _result['audits']['cumulative-layout-shift'] = _report['audits']['cumulative-layout-shift']['displayValue']

    # average
    _result['average'] = {
        'value': database.get_average_by_attribute(target, 'performance'),
        'min': database.get_average_peak(target, 'performance', True),
        'max': database.get_average_peak(target, 'performance', False),
        'trend': get_trend(target, 'performance')
    }

    return _result


def get_trend(target, attribute):
    """

    :param target:
    :param attribute:
    :return:
    """
    _average = database.get_average_by_attribute(target, attribute)
    _value = database.get_last_value(target, attribute)

    _indicator = (10.0 * _average) / 100.0

    if (_average - _indicator) > _value:
        return -1

    if (_average + _indicator) < _value:
        return 1

    return 0

