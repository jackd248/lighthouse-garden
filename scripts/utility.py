#!/usr/bin/python
import json, datetime, os, sys
from urlparse import urlparse
sys.path.append('../')
import illuminate

config = None

def get_config ():
    if not config is None:
        return config
    else:
        if os.path.isfile('config.json'):
            set_config('config.json')
        else:
            # Default config
            return {
                'title': 'Lighthouse garden',
                'description': 'Aggregate performance data',
                'data_dir': 'data/'
            }
        return config

def set_config (config_file):
    global config
    with open(config_file, 'r') as read_file:
        config =  json.load(read_file)
    

def get_data_dir ():
    return get_config()['data_dir']

def get_result(target, file_name = None):

    if file_name is None:
        file_name = target['identifier'] + '.report.json'

    with open('./' + get_data_dir() + file_name, 'r') as read_file:
            report = json.load(read_file)

    result = {
        'title': target['title'],
        'url': target['url'],
        'performance': int(round(report['categories']['performance']['score'] * 100)),
        'accessibility': int(round(report['categories']['accessibility']['score'] * 100)),
        'best-practices': int(round(report['categories']['best-practices']['score'] * 100)),
        'seo': int(round(report['categories']['seo']['score'] * 100)),
        'report': '/' + get_data_dir() + '/' + target['identifier'] + '.report.html',
        'date': '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
    }

    return result

def get_results():
    results = []
    for target in get_config()['targets']:
        results.append(get_result(target))

    # sort by performance
    results.sort(key=lambda x: x['performance'], reverse=True)

    return results


def get_target_by_attribute(value,attribute):
    for target in get_config()['targets']:
        if target[attribute] == value:
            return target
    return None


def add_average_data_and_sort(results):
    for result in results:
        result['average'] = get_average_by_attribute(get_target_by_attribute(result['title'],'title'),'performance')

    # sort by average
    results.sort(key=lambda x: x['average'], reverse=True)
    return results

def get_average_by_attribute(target,attribute):
    history_data = get_history_by_attribute(target,attribute)
    return sum(history_data) / float(len(history_data))

def get_history_by_attribute(target,attribute):
    history_data = []
    for history in get_history(target):
        history_data.append(history[attribute])
    return history_data

def get_history(target):
    history_file = './' + get_data_dir() + target['identifier'] + '.history.json'
    if os.path.isfile(history_file):
        with open(history_file, "r") as read_file:
            return json.load(read_file)
    else:
        open(history_file, 'w').close()
        return []

def set_history(target, history):
    history_file = './' + get_data_dir() + target['identifier'] + '.history.json'
    with open(history_file, "w") as write_file:
        json.dump(history, write_file)