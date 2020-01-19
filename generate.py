#!/usr/bin/python

import os, json, sys, time, subprocess, datetime, sys
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
        with open('./var/' + data_dir + target['identifier'] + '/index.report.json', 'r') as read_file:
            report = json.load(read_file)

        result = [
            target['title'],
            target['url'],
            report['categories']['performance']['score'],
            report['categories']['accessibility']['score'],
            report['categories']['best-practices']['score'],
            report['categories']['seo']['score'],
            '/var/' + data_dir + target['identifier'] + '/index.report.html',
            '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        ]

        results.append(result)

        history = get_history(target)
        history.append(result)
        set_history(target,history)
        print('✓ (' + report['categories']['performance']['score'] + ')')


    # sort by performance
    results.sort(key=lambda x: x[2], reverse=True)

    # export
    print_stdout()
    export_html()

# functions
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

def export_html ():
    now = datetime.datetime.now()
    html = open("index.html","w")
    html.write('<html><head><title>' + config['title'] + '</title><link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css"></head><body>')
    html.write('<div class="jumbotron"><div class="container"><h1>' + config['title'] + '</h1><p>' + config['description'] + '</p></div></div><div class="container"><p class="text-right"><small>Last checked <span class="label label-default">' + now.strftime("%d/%m/%Y %H:%M") + '</span></small></p><table class="table"><thead><tr><th>Title</th><th>URL</th><th>Performance</th><th>Accessibility</th><th>Best practices</th><th>SEO</th><th>Details</th></tr><tbody>')
    for result in results:
        html.write('<tr>')
        for item in result:
            if item != result[-1]:
                if item != result[6] and item != result[1]:
                    if (isinstance(item, float) or isinstance(item, int)):
                        item = label(item) + str('{:10.2f}'.format(item)) + '</span>'
                    html.write('<td>' + str(item)+ '</td>')
                else: 
                    html.write('<td><a href="' + item + '" target="_blank">' + item + '</a></td>')
        html.write('</tr>')
    # html.write(tabulate(results, headers, tablefmt="html", floatfmt=".2f"))
    html.write('</tbody></table></div></body></html>')
    html.close()

def get_history(target):
    history_file = './var/' + data_dir + target['identifier'] + '/history.json'
    if os.path.isfile(history_file):
        with open(history_file, "r") as read_file:
            return json.load(read_file)
    else:
        open(history_file, 'w').close()
        return []

def set_history(target, history):
    history_file = './var/' + data_dir + target['identifier'] + '/history.json'
    with open(history_file, "w") as write_file:
        json.dump(history, write_file)

if __name__ == "__main__":
    main()