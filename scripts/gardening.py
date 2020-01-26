#!/usr/bin/python

import os, sys, json, utility
from tabulate import tabulate
from urlparse import urlparse

CHROME_FLAGS = '--no-sandbox --headless --disable-gpu'

def fetch_data (save = True, url = None):
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
            process_target(target, save)
    else:
        process_target({
            'title': urlparse(url).netloc,
            'url': url,
            'identifier': urlparse(url).netloc
        }, False)
        

    # export
    #print_stdout()

def process_target(target, save):
    sys.stdout.write('> ' + target['title'] + ' (' + target['url'] + ') ... ')
    sys.stdout.flush()

    output = '--output json --output-path ./' + data_dir + target['identifier'] + ' '
    if save is True:
        output += ' --output html'

    lighthouse(target, output)
    
    #if save is True:
    #    file_name = 'index.report.json'
    #else:
    #    file_name = 'index'

    result = utility.get_result(target)

    results.append(result)

    if save is True:
        history = utility.get_history(target)
        history.append(result)
        utility.set_history(target,history)

    print(result['performance'])

def lighthouse (target, output):
    return os.system('lighthouse ' + target['url'] + ' --quiet --chrome-flags="' + CHROME_FLAGS + '" ' + output)

def print_stdout ():
    headers = ['Title', 'URL', 'Performance', 'Accessibility', 'Best practices', 'SEO', 'Details', 'Date']
    table = tabulate(utility.get_results(), headers, tablefmt="github", floatfmt=".2f")
    print('Result(s):')
    print(table)