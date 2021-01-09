#!/usr/bin/env python3
# -*- coding: future_fstrings -*-

import datetime
import anybadge
from lighthouse_garden.utility import info, output, system
from lighthouse_garden.lighthouse import database, utility, interpreter


def fetch_data():
    """

    :return:
    """
    output.println(f'{output.Subject.INFO} Checking export path', verbose_only=True)
    system.check_path(f'{system.config["export_path"]}/{system.config["data_dir"]}')
    output.println(f'{output.Subject.INFO} Starting to process targets')
    for target in system.config['targets']:
        _output_name = lighthouse(target)
        _result = interpreter.get_result_by_report_file(target, _output_name)
        if _result:
            database.set_data(target, _result)
            output.println(f'{output.Subject.OK} > {info.get_target_name(target)} ... {_result["performance"]}')
            utility.extend_html_report_with_info(_result, f'{utility.get_data_dir()}{_output_name}.report.html')
            generate_badges(target)
        else:
            utility.remove_file(f'{utility.get_data_dir()}{_output_name}.report.html')
        utility.remove_file(f'{utility.get_data_dir()}{_output_name}.report.json')


def lighthouse(target):
    """

    :param target:
    :return:
    """
    output.println(f'{output.Subject.INFO} Fetching performance data for {info.get_target_name(target)}', verbose_only=True)

    _output_name = generate_output_name(target)
    _result = system.run_command(
        f'lighthouse {target["url"]} {build_options(_output_name)}', allow_fail=True
    )

    if not _result:
        output.println(f'{output.Subject.ERROR} > {info.get_target_name(target)} ...')
        system.config['errors'] = True

    return _output_name


def build_options(output_name):
    """

    :param output_name:
    :return:
    """
    _options = system.config['lighthouse']['options']
    _options += f' --chrome-flags="{system.config["lighthouse"]["chrome_flags"]}"'
    _options += f' --output json --output html --output-path {system.config["export_path"]}/{system.config["data_dir"]}' \
                f'{output_name}'
    return _options


def generate_output_name(target):
    """
    Generate a temporary output name, e.g. _google_28-12-2020_15-59
    :return:
    """
    return f'_{target["identifier"]}_{datetime.datetime.now().strftime("%d-%m-%Y_%H-%M")}'


def generate_badges(target):
    """

    :param target:
    :return:
    """
    output.println(f'{output.Subject.INFO} Generating badges', verbose_only=True)
    badges = {
        'performance': {
            'label': 'performance',
            'value': database.get_data(target)['performance'],
         },
        'accessibility': {
            'label': 'accessibility',
            'value': database.get_data(target)['accessibility'],
        },
        'best-practices': {
            'label': 'best-practices',
            'value': database.get_data(target)['best-practices'],
        },
        'seo': {
            'label': 'seo',
            'value': database.get_data(target)['seo'],
        },
        'average': {
            'label': 'performance',
            'value': database.get_data(target)['average']['value']
        }
    }

    for key, value in badges.items():
        generate_badge(
            target=target,
            layout=value,
            attribute=key
        )


def generate_badge(target, layout, attribute):
    """

    :param target:
    :param layout:
    :param attribute:
    :return:
    """
    thresholds = {50: 'red',
                  90: 'yellow',
                  100: 'green'}
    badge = anybadge.Badge(layout['label'], round(layout['value']), thresholds=thresholds)

    badge.write_badge(f'{utility.get_data_dir()}_{target["identifier"]}.{attribute}.svg', overwrite=True)
