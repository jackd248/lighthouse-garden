#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import jinja2
import os
import sys

import lighthouse_garden
from lighthouse_garden import info
from lighthouse_garden.utility import output, system
from lighthouse_garden.lighthouse import database, utility

ASSETS_CSS = '/templates/assets/css'
ASSETS_JS = '/templates/assets/js'

TAG_CSS = 'style'
TAG_JS = 'script'


def generate_dashboard():
    _now = datetime.datetime.now()
    _file = f'{system.config["export_path"]}index.html'
    output.println(f'{output.Subject.INFO} Generating dashboard {output.CliFormat.BLACK}{_file}{output.CliFormat.ENDC}')

    html = open(_file, "w")

    _rendered_html = render_template('index.html.j2',
                                     logo=render_logo(),
                                     date=_now.strftime("%Y-%m-%dT%H:%M:%SZ"),
                                     assets_css=render_assets(ASSETS_CSS, TAG_CSS),
                                     assets_js=render_assets(ASSETS_JS, TAG_JS),
                                     items=render_items(),
                                     title=system.config['title'],
                                     description=system.config['description'],
                                     version=info.__version__,
                                     homepage=info.__homepage__,
                                     lighthouse_version=system.config['lighthouse']['version']
                                     )
    html.write(_rendered_html)
    html.close()


def render_items():
    _items = ''
    results = database.sort_by_average(
        database.get_last_results()
    )

    for result in results:
        _target = database.get_target_by_attribute(result['title'], 'title')
        _item = render_template('partials/item.html.j2',
                                title=result['title'],
                                url=result['url'],
                                last_report=result['report'],
                                identifier=_target['identifier'],
                                graph_values_y=','.join(map(str, database.get_history_by_attribute(
                                    _target, 'performance'))),
                                graph_values_x=','.join(map(str, database.get_history_by_attribute(
                                    _target, 'date'))),
                                graph_values_text=','.join(map(str, database.get_history_by_attribute(
                                    _target, 'report'))),
                                circle_average=render_percentage_circle(
                                    description=f'<strong>Average</strong><br/>'
                                                f'Calculates all available performance values to an average value.<br/><br/>'
                                                f'Maximum value: {int(result["average"]["max"])}<br/>'
                                                f'Minimum value: {int(result["average"]["min"])}<br/>',
                                    value=result['average']['value']
                                ),
                                circle_performance=render_percentage_circle(
                                    trend=render_trend(result),
                                    description=f'<strong>Performance</strong><br/>'
                                                f'The performance score is calculated directly from various metrics.<br/><br/>'
                                                f'Click here to get more information from the last report.',
                                    url=f'{result["report"]}#performance',
                                    value=result['performance']
                                ),
                                circle_accessibility=render_percentage_circle(
                                    description=f'<strong>Accessibility</strong><br/>'
                                                f'These checks highlight opportunities to improve the accessibility of '
                                                f'your web app.<br/><br/>'
                                                f'Click here to get more information from the last report.',
                                    value=result['accessibility'],
                                    url=f'{result["report"]}#accessibility',
                                    additional_class='small'
                                ),
                                circle_best_practices=render_percentage_circle(
                                    description=f'<strong>Best practices</strong><br/>'
                                                f'Further information about best practices.'
                                                f'See the lighthouse report for further information.<br/><br/>'
                                                f'Click here to get more information from the last report.',
                                    value=result['best-practices'],
                                    url=f'{result["report"]}#best-practices',
                                    additional_class='small'
                                ),
                                circle_seo=render_percentage_circle(
                                    description=f'<strong>SEO</strong><br/>'
                                                f'These checks ensure that your page is optimized for search engine '
                                                f'results ranking.<br/><br/>'
                                                f'Click here to get more information from the last report.',
                                    value=result['seo'],
                                    url=f'{result["report"]}#seo',
                                    additional_class='small'
                                ),
                                api_json=f'{utility.get_data_dir(absolute_path=False)}_{_target["identifier"]}.json',
                                badge_average=f'{utility.get_data_dir(absolute_path=False)}_{_target["identifier"]}.average.svg',
                                badge_performance=f'{utility.get_data_dir(absolute_path=False)}_{_target["identifier"]}.performance.svg',
                                badge_accessibility=f'{utility.get_data_dir(absolute_path=False)}_{_target["identifier"]}.accessibility.svg',
                                badge_best_practices=f'{utility.get_data_dir(absolute_path=False)}_{_target["identifier"]}.best-practices.svg',
                                badge_seo=f'{utility.get_data_dir(absolute_path=False)}_{_target["identifier"]}.seo.svg',
                                )
        _items += _item
    return _items


def render_percentage_circle(description, value, trend='', url='', additional_class=None):
    return render_template('partials/circle.html.j2',
                           url=url,
                           value=str(int(round(value))),
                           description=description,
                           color=get_percentage_classification(int(round(value))),
                           small=additional_class,
                           trend=trend
                           )


def render_trend(result):
    """

    :param result:
    :return:
    """
    _description = ''
    _class = ''
    if result['average']['trend'] == 1:
        _description = f'<strong>Performance trend</strong><br/>' \
                       f'Ascending trend in dependence of the last performance measurement to the average value.'
        _class = 'asc'
    elif result['average']['trend'] == -1:
        _description = f'<strong>Performance trend</strong><br/>' \
                       f'Descending trend in dependence of the last performance measurement to the average value.'
        _class = 'desc'

    if result['average']['trend'] == 0:
        return ''
    else:
        return render_template('partials/trend.html.j2',
                           description=_description,
                           trend=_class
                           )


def get_percentage_classification(value):
    if value >= 90:
        return 'green'
    elif value >= 50:
        return 'orange'
    else:
        return 'red'


def render_assets(path, tag):
    """

    :param path: String
    :param tag: String
    :return: String
    """
    _html = ''
    for file in os.listdir(os.path.dirname(lighthouse_garden.__file__) + path):
        with open(os.path.dirname(lighthouse_garden.__file__) + path + '/' + file, 'r') as read_file:
            _html += f'<!-- {file} -->\n<{tag}>\n{read_file.read()}\n</{tag}>\n'
    return _html


def render_logo():
    """

    :return:
    """
    with open(os.path.dirname(lighthouse_garden.__file__) + '/templates/assets/tower.svg', 'r') as read_file:
        return read_file.read()


def render_template(template, **args):
    """
    Render a template with jinja2
    :param template: String Template file
    :param args: Dictionary Template arguments
    :return: String Rendered Template
    """
    _template_loader = jinja2.FileSystemLoader(searchpath="./lighthouse_garden/templates/")
    _template_environment = jinja2.Environment(loader=_template_loader)
    _template = _template_environment.get_template(template)
    return _template.render(args)
