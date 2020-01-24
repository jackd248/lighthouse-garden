#!/usr/bin/python

import utility, datetime

def export_html (path = "./"):
    now = datetime.datetime.now()
    file = path + "index.html"

    html = open(file,"w")
    results = utility.add_average_data_and_sort(utility.get_results())

    entries = ''
    for result in results:
        entry = render_template('template/partials/item.template.html',
            title = result['title'],
            url = result['url'],
            identifier = utility.get_target_by_attribute(result['title'],'title')['identifier'],
            graph_values = ', '.join(map(str, utility.get_history_by_attribute(utility.get_target_by_attribute(result['title'],'title'), 'performance'))),
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
            circle_accessibility = render_percentage_circle(
                result['report'],
                'accessibility',
                result['accessibility']
            ),
            circle_best_practices = render_percentage_circle(
                result['report'],
                'best-practices',
                result['best-practices']
            ),
            circle_seo = render_percentage_circle(
                result['report'],
                'seo',
                result['seo']
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