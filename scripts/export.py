#!/usr/bin/python

import utility, datetime, os

ASSETS_CSS = 'assets/css'
ASSETS_JS ='assets/js'

TAG_CSS = 'style'
TAG_JS ='script'

def export_html (path = "./"):
    now = datetime.datetime.now()
    file = path + "index.html"

    html = open(file,"w")
    results = utility.add_average_data_and_sort(utility.get_results())

    entries = ''
    for result in results:
        if 'accessibility' in result:
            circle_accessibility = render_percentage_circle(
                result['report'],
                'accessibility',
                result['accessibility']
            )
        else:
            circle_accessibility = ''

        if 'best-practices' in result:
            circle_best_practices = render_percentage_circle(
                result['report'],
                'best-practices',
                result['best-practices']
            )
        else:
            circle_best_practices = ''

        if 'seo' in result:
            circle_seo = render_percentage_circle(
                result['report'],
                'seo',
                result['seo']
            )
        else:
            circle_seo = ''

        entry = render_template('template/partials/item.template.html',
            title = result['title'],
            url = result['url'],
            identifier = utility.get_target_by_attribute(result['title'],'title')['identifier'],
            graph_values_y = ', '.join(map(str, utility.get_history_by_attribute(utility.get_target_by_attribute(result['title'],'title'), 'performance'))),
            graph_values_x = ', '.join(map(str, utility.get_history_by_attribute(utility.get_target_by_attribute(result['title'],'title'), 'date'))),
            circle_average = render_percentage_circle(
                result['report'],
                '',
                result['average']
            ),
            circle_performance = render_percentage_circle(
                result['report'],
                'performance',
                result['performance']
            ),
            circle_accessibility = circle_accessibility,
            circle_best_practices = circle_best_practices,
            circle_seo = circle_seo
        )
        entries += entry

    rendered_html = render_template('template/index.template.html',
        logo = render_logo(),
        date = now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        list = entries,
        assets_css = render_assets(ASSETS_CSS, TAG_CSS),
        assets_js = render_assets(ASSETS_JS, TAG_JS)
    )
    html.write(rendered_html)
    html.close()

def render_percentage_circle (url, attribute, value):
    return render_template('template/partials/circle.template.html',
       url = url,
       attribute = attribute,
       value = str(int(round(value))),
       color = get_percentage_classification(int(round(value)))
   )

def get_percentage_classification (value):
    if value >= 90:
        return 'green'
    elif value >= 50:
        return 'orange'
    else:
        return 'red'

# http://www.pythonmania.de/article/templateengine.html
def render_template(template, **params):
    f_in = open(template, "r")
    html = f_in.read()
    f_in.close
    for arg in params:
        replaceString = "<% " + arg + " %>"
        html = html.replace(replaceString, params[arg])
    return html

def render_assets (dir, tag):
    html = ''
    for file in os.listdir(dir):
        with open(dir + '/' + file, 'r') as read_file:
            html += '<!-- ' + file + ' -->\n<' + tag + '>\n' + read_file.read() + '\n</' + tag + '>\n'
    return html

def render_logo():
    with open('assets/tower.svg', 'r') as read_file:
        return read_file.read()
    