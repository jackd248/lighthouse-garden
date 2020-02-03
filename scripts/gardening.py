#!/usr/bin/python

import os, sys, json, utility
# from tabulate import tabulate
from urlparse import urlparse

CHROME_FLAGS = '--no-sandbox --headless --disable-gpu'
LIGHTHOUSE_OPTIONS=' --quiet --emulated-form-factor=none --no-enable-error-reporting'
PERFORMANCE_ONLY_OPTION = ' --only-categories=performance'

def fetch_data (save = True, url = None, performanceOnly = False):
    global data_dir
    global results
    data_dir = utility.get_config()['data_dir']
    # create target dir
    if not os.path.exists('./' + data_dir):
        os.makedirs('./' + data_dir)

    # processing targets
    results = []
    print('Checking the following site(s)')
    if url is None:
        for target in utility.get_config()['targets']:
            process_target(target, save, performanceOnly)
    else:
        process_target({
            'title': urlparse(url).netloc,
            'url': url,
            'identifier': urlparse(url).netloc
        }, False)
        

    # export
    #print_stdout()

def process_target(target, save, performanceOnly = False):
    sys.stdout.write('> ' + target['title'] + ' (' + target['url'] + ') ... ')
    sys.stdout.flush()

    lighthouse(target, performanceOnly)

    result = utility.get_result(target)

    results.append(result)

    if save is True:
        utility.add_result_to_history(target, result)

    print(result['performance'])

def lighthouse (target, performanceOnly = False):
    _options = LIGHTHOUSE_OPTIONS
    _options += ' --chrome-flags="' + CHROME_FLAGS + '"'
    _options += ' --output json --output html --output-path ./' + data_dir + target['identifier']
    if performanceOnly:
        _options += PERFORMANCE_ONLY_OPTION
    return os.system('lighthouse ' + target['url'] + _options)

def print_stdout ():
    headers = ['Title', 'URL', 'Performance', 'Accessibility', 'Best practices', 'SEO', 'Details', 'Date']
    table = tabulate(utility.get_results(), headers, tablefmt="github", floatfmt=".2f")
    print('Result(s):')
    print(table)
