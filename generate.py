#!/usr/bin/python

import os, json, sys, time, subprocess, datetime, sys, export
from tabulate import tabulate

def main ():
    global config
    global data_dir
    global results

    # read config
    with open("config.json", "r") as read_file:
        config = json.load(read_file)

    print(config['title'])
    print('======================')

    data_dir = config['data_dir']
    # create target dir
    if not os.path.exists('./var/' + data_dir):
        os.makedirs('./var/' + data_dir)

    # processing targets
    results = []
    print('Checking the following site(s)')
    for target in config['targets']:
        sys.stdout.write('> ' + target['title'] + ' (' + target['url'] + ') ... ')
        sys.stdout.flush()
        #print('> ' + target['title'] + ' (' + target['url'] + ') ...')

        # create target dir
        if not os.path.exists('./var/' + data_dir + target['identifier']):
            os.makedirs('./var/' + data_dir + target['identifier'])

        lighthouse(target)
        
        result = get_result(target)
        results.append(result)

        history = export.get_history(target)
        history.append(result)
        export.set_history(target,history)
        print(result['performance'])

    # export
    #print_stdout()
    export.export_html()

# functions
def get_config ():
    # read config
    with open("config.json", "r") as read_file:
        config = json.load(read_file)
    return config

def get_data_dir ():
    return get_config()['data_dir']

def get_result(target):
    with open('./var/' + get_data_dir() + target['identifier'] + '/index.report.json', 'r') as read_file:
            report = json.load(read_file)

    result = {
        'title': target['title'],
        'url': target['url'],
        'performance': int(round(report['categories']['performance']['score'] * 100)),
        'accessibility': int(round(report['categories']['accessibility']['score'] * 100)),
        'best-practices': int(round(report['categories']['best-practices']['score'] * 100)),
        'seo': int(round(report['categories']['seo']['score'] * 100)),
        'report': '/var/' + get_data_dir() + target['identifier'] + '/index.report.html',
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

def lighthouse (target):
    os.system('lighthouse ' + target['url'] + ' --quiet --chrome-flags="--no-sandbox --headless --disable-gpu" --output json --output html --output-path ./var/' + data_dir + target['identifier'] + '/index ')

def label (float):
    if float >= 0.9:
        return '<span class="label label-success">'
    elif float >= 0.5:
        return '<span class="label label-warning">'
    else: 
        return '<span class="label label-danger">'

def print_stdout ():
    headers = ['Title', 'URL', 'Performance', 'Accessibility', 'Best practices', 'SEO', 'Details', 'Date']
    table = tabulate(results, headers, tablefmt="github", floatfmt=".2f")
    print('Result(s):')
    print(table)

if __name__ == "__main__":
    main()