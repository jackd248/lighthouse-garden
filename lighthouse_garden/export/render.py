#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import jinja2
import os
import sys

from lighthouse_garden import info
from lighthouse_garden.utility import output, system
from lighthouse_garden.lighthouse import database, utility

ASSETS_CSS = 'lighthouse_garden/templates/assets/css'
ASSETS_JS = 'lighthouse_garden/templates/assets/js'

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
    results = database.add_average_data_and_sort(
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
                                    target=_target,
                                    description=f'<strong>Average</strong><br/>'
                                                f'Calculates all available performance values to an average value.<br/><br/>'
                                                f'Click here to get the average badge.',
                                    attribute='average',
                                    value=result['average']
                                ),
                                circle_performance=render_percentage_circle(
                                    target=_target,
                                    description=f'<strong>Performance</strong><br/>'
                                                f'The performance score is calculated directly from various metrics. '
                                                f'See the lighthouse report for further information.<br/><br/>'
                                                f'Click here to get the performance badge.',
                                    attribute='performance',
                                    value=result['performance']
                                ),
                                circle_accessibility=render_percentage_circle(
                                    target=_target,
                                    description=f'<strong>Accessibility</strong><br/>'
                                                f'These checks highlight opportunities to improve the accessibility of '
                                                f'your web app.<br/><br/>'
                                                f'Click here to get the accessibility badge.',
                                    attribute='accessibility',
                                    value=result['accessibility'],
                                    additional_class='small'
                                ),
                                circle_best_practices=render_percentage_circle(
                                    target=_target,
                                    description=f'<strong>Best practices</strong><br/>'
                                                f'Further information about best practices.'
                                                f'See the lighthouse report for further information.<br/><br/>'
                                                f'Click here to get the best practices badge.',
                                    attribute='best-practices',
                                    value=result['best-practices'],
                                    additional_class='small'
                                ),
                                circle_seo=render_percentage_circle(
                                    target=_target,
                                    description=f'<strong>SEO</strong><br/>'
                                                f'These checks ensure that your page is optimized for search engine '
                                                f'results ranking.<br/><br/>'
                                                f'Click here to get the seo badge.',
                                    attribute='seo',
                                    value=result['seo'],
                                    additional_class='small'
                                )
                                )
        _items += _item
    return _items


def render_percentage_circle(target, description, attribute, value, additional_class=None):
    return render_template('partials/circle.html.j2',
                           url=f'{utility.get_data_dir(absolute_path=False)}_{target["identifier"]}.{attribute}.svg',
                           value=str(int(round(value))),
                           description=description,
                           color=get_percentage_classification(int(round(value))),
                           small=additional_class
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
    for file in os.listdir(path):
        with open(path + '/' + file, 'r') as read_file:
            _html += f'<!-- {file} -->\n<{tag}>\n{read_file.read()}\n</{tag}>\n'
    return _html


def render_logo():
    """

    :return:
    """
    with open('./lighthouse_garden/templates/assets/tower.svg', 'r') as read_file:
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
