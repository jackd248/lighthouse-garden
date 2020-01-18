import os, json, sys, time, subprocess, datetime
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
        print('> ' + target['title'] + ' (' + target['url'] + ') ...')

        # create target dir
        if not os.path.exists('./var/' + data_dir + target['identifier']):
            os.makedirs('./var/' + data_dir + target['identifier'])

        lighthouse(target)
        with open('./var/' + data_dir + target['identifier'] + '/index.report.json', 'r') as read_file:
            report = json.load(read_file)

        results.append([
            target['title'],
            target['url'],
            report['categories']['performance']['score'],
            report['categories']['accessibility']['score'],
            report['categories']['best-practices']['score'],
            report['categories']['seo']['score'],
            '/' + target['identifier'] + '/index.report.html'
        ])

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
    headers = ['Title', 'URL', 'Performance', 'Accessibility', 'Best practices', 'SEO', 'Details']
    table = tabulate(results, headers, tablefmt="github", floatfmt=".2f")
    print('Result(s):')
    print(table)

def export_html ():
    now = datetime.datetime.now()
    html= open("index.html","w")
    html.write('<html><head><title>' + config['title'] + '</title><link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css"></head><body>')
    html.write('<div class="container"><h1>' + config['title'] + '</h1><p class="text-muted">' + config['description'] + '</p><p>Last checked <span class="label label-default">' + now.strftime("%d/%m/%Y %H:%M") + '</span></p><table class="table"><thead><tr><th>Title</th><th>URL</th><th>Performance</th><th>Accessibility</th><th>Best practices</th><th>SEO</th><th>Details</th></tr><tbody>')
    for result in results:
        html.write('<tr>')
        for item in result:
            if item != result[-1] and item != result[1]:
                if (isinstance(item, float) or isinstance(item, int)):
                    item = label(item) + str('{:10.2f}'.format(item)) + '</span>'
                html.write('<td>' + str(item)+ '</td>')
            else: 
                html.write('<td><a href="' + item + '" target="_blank">' + item + '</a></td>')
        html.write('</tr>')
    # html.write(tabulate(results, headers, tablefmt="html", floatfmt=".2f"))
    html.write('</tbody></table></div></body></html>')
    html.close()

if __name__ == "__main__":
    main()