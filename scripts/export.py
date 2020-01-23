#!/usr/bin/python

import utility, datetime

def export_html (path = "./"):
    now = datetime.datetime.now()
    file = path + "index.html"

    html = open(file,"w")
    results = utility.add_average_data_and_sort(utility.get_results())

    entries = ''
    for result in results:
        entry = render_template('template/item.template.html',
            title = result['title'],
            url = result['url'],
            identifier = utility.get_target_by_attribute(result['title'],'title')['identifier'],
            graph_values = ', '.join(map(str, utility.get_history_by_attribute(utility.get_target_by_attribute(result['title'],'title'), 'performance'))),
            circle_average = render_template('template/circle.template.html',
                url = result['report'],
                attribute = '',
                value = str(int(round(result['average']))),
                color = get_percentage_classification(int(round(result['average'])))
            ),
            circle_performance = render_template('template/circle.template.html',
                url = result['report'],
                attribute = 'performance',
                value = str(int(round(result['performance']))),
                color = get_percentage_classification(int(round(result['performance'])))
            ),
            circle_accessibility = render_template('template/circle.template.html',
                url = result['report'],
                attribute = 'accessibility',
                value = str(int(round(result['accessibility']))),
                color = get_percentage_classification(int(round(result['accessibility'])))
            ),
            circle_best_practices = render_template('template/circle.template.html',
                url = result['report'],
                attribute = 'best-practices',
                value = str(int(round(result['best-practices']))),
                color = get_percentage_classification(int(round(result['best-practices'])))
            ),
            circle_seo = render_template('template/circle.template.html',
                url = result['report'],
                attribute = 'seo',
                value = str(int(round(result['seo']))),
                color = get_percentage_classification(int(round(result['seo'])))
            )
        )
        entries += entry

    rendered_html = render_template('template/index.template.html',
        title = utility.get_config()['title'],
        description = utility.get_config()['description'],
        date = now.strftime("%d/%m/%Y %H:%M"),
        list = entries
    )
    html.write(rendered_html)
    html.close()

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