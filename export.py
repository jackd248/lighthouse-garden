#!/usr/bin/python

import os, json, sys, time, subprocess, datetime, sys, generate

def generate_percentage_circle (value):
    if value >= 90:
        return '<div class="c100 p' + str(value) + ' green"><span>' + str(value) + '</span><div class="slice"><div class="bar"></div><div class="fill"></div></div></div>'
    elif value >= 50:
        return '<div class="c100 p' + str(value) + ' orange"><span>' + str(value) + '</span><div class="slice"><div class="bar"></div><div class="fill"></div></div></div>'
    else:
        return '<div class="c100 p' + str(value) + ' red"><span>' + str(value) + '</span><div class="slice"><div class="bar"></div><div class="fill"></div></div></div>'

def export_html ():
    now = datetime.datetime.now()
    html = open("index.html","w")
    html.write('<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, minimum-scale=1"><link rel="icon" href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAEhklEQVR4AWJxL/BhIAesev1U5tcflpncgNrKIsqNIwzC9feMpDUzs70kOczMzMzJJcxwCTMzncPMnOwtzBwzMzPb0vRfeZPp0VhPS5I39V5fdiXV1/VD+9QC7OVn9BsyH1XIoEI1PfmJvLFowVV564+34DFUHudbmfDh4kVXh//7XwE+WjS/YfXZe3yr4j2rqj1AIhSB7hZ8ZtPZu/zw8cK523U4wE1/rvPfWrz4zs0m9ZdC9yUJAlASdBAgocRegfF/f3/h/PuaFsxMdwjAR0vm1+06eMMfIrhLqTWqdH4EumU2SPfMhigJAlRQbZrgrRsl9U+Y2DYDFCz3ILC9kiAiqSrMwbWT0nceEnR+9Kggc2zjOJCASDENkg0a5HfZZgDP81CM3CrQs2Z1+o7DJ6ePr8sK0AOCHv5Jjdt3evyYSaZ351VIStIxPRAUtrBYbxC6w+BZ0ivVSBKkIhJhemSyZpfB00EiPO2VjzYkxhcqXQqCWCShGplvi3y0QxqbuBurMjyJeWnkHZuAEgIQGsUBqwrfjZ+IlBgKyRJzVVYF8O6qFWdh86YzQzMrZigYmxAyfvHgLZQ/LC1CbeniW2Hkqr/PH16SgvGuf2/uzNMBwJA/njxizGPtSyAf7EziJCMGRDRdhoAC4PL1A/SrKQMAAQkEfpJAcRQdrBJ7gNwjSpJsdwK+CANBkqa1LgQB4IicV9nYUct7gaxuDJUErQIiEAiMxLVOFlKzIktPpT0ggpdpC/8YAHnxbgkUY4tAAFSR7AAXNyAAWHJrA/kHGjzg5nleuwFO7Nd/IoDw4Pm58+4jNLmYG0wRA5bErc2Mr3Y+dXTDW1VvwqbJkzMCHQ4S1GTCBOIgUHJrGdEwqzR+jAp/o2qAZelUDoQnruEEdDclJI6576AlNVfc+22XN/+Y1vnJD0Yind6UpEEvn/Hqq15EYjCW7jZCJEpnNvDgkyelDjs106kuux2AAXCSobULOWP8mLhYlpoDMK4qAFXJGk+grtH8YXVz5KJblqaG1+VUdTc0I290bmUQAriGITRbdQnom0aoFj8kx1+wMD2ifncAXUQE4SkDqN1hE0jEophs1SUwZAOhUAiMCLwRtamtTZtbbmZErSAUHbSysaoEmnrsakiMiUAURi283gN6wans9oX8rOCrj7/JP35DFD+iQ7Au/K2KE1jzx6ujjUnXFH9KjEq6ZlhsTBICrNLJf47Pv/pkHzvup1w4dmUbEei0+bcXRqJuh5kVARQ8byyYxOwNGr7A87xh1tp8sGT+uMInrwi++Xj7TQz2d27NvwEkrOflAFQGIDA5khASBCGdO2/Z/MnLPwYfv5TFhjW7QhVKAB6afwe2LpFlFsCnlQEosgQgDsdOG1/LKeNqJS4JCSPJ/i+TakwEARor7gER1Iva5JmPOJK0RUqmoPnnlzFCtmIAhAAQEIQRgDaiYPIauNXcnDlRIrWNFY3hm7PG9YRqr7IV7HrCgAC17befjEvRq2nGhAHtBqDpOuI/I1diUUAMYIxEdyejBJqLnNoszGZtfiX/CztGv2mq+sdaAAAAAElFTkSuQmCC"><title>' + generate.get_config()['title'] + '</title><link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css"><link rel="stylesheet" href="assets/percentage.css"><script src="https://cdn.plot.ly/plotly-latest.min.js"></script><script src="assets/graph.js"></script></head><body>')
    html.write('<div class="jumbotron"><div class="container"><h1>' + generate.get_config()['title'] + '</h1><p>' + generate.get_config()['description'] + '</p></div></div><div class="container"><p class="text-right"><small>Last checked <span class="label label-default">' + now.strftime("%d/%m/%Y %H:%M") + '</span></small></p><table class="table"><thead><tr><th>Title</th><th>Average</th><th>Performance Graph</th><th>Performance</th><th>Accessibility</th><th>Best practices</th><th>SEO</th></tr><tbody>')
    for result in generate.get_results():
        html.write('<tr>')
        html.write('<td><strong>' + result['title'] + '</strong><br/><a href="' + result['url'] + '" target="_blank">' + result['url'] + '</a></td>')
        html.write('<td><a href="' + result['report'] + '" target="_blank">' + generate_percentage_circle(int(round(get_average_by_attribute(generate.get_target_by_attribute(result['title'],'title'),'performance')))) + '</a></td>')
        html.write('<td><div id="graph-' + generate.get_target_by_attribute(result['title'],'title')['identifier'] + '" class="graph" data-values="' + ', '.join(map(str, get_history_by_attribute(generate.get_target_by_attribute(result['title'],'title'), 'performance'))) +'"></div></td>')
        
        html.write('<td><a href="' + result['report'] + '#performance" target="_blank">' + generate_percentage_circle(int(round(result['performance']))) + '</a></td>')
        html.write('<td><a href="' + result['report'] + '#accessibility" target="_blank">' + generate_percentage_circle(int(round(result['accessibility']))) + '</a></td>')
        html.write('<td><a href="' + result['report'] + '#best-practices" target="_blank">' + generate_percentage_circle(int(round(result['best-practices']))) + '</a></td>')
        html.write('<td><a href="' + result['report'] + '#seo" target="_blank">' + generate_percentage_circle(int(round(result['seo']))) + '</a></td>')
        html.write('</tr>')
        # ', '.join(map(str, get_history_by_attribute(generate.get_target_by_attribute(result['title'],'title'), 'performance')))
    html.write('</tbody></table></div></body></html>')
    html.close()

def get_average_by_attribute(target,attribute):
    history_data = get_history_by_attribute(target,attribute)
    return sum(history_data) / float(len(history_data))

def get_history_by_attribute(target,attribute):
    history_data = []
    for history in get_history(target):
        history_data.append(history[attribute])
    return history_data

def get_history(target):
    history_file = './var/' + generate.get_data_dir() + target['identifier'] + '/history.json'
    if os.path.isfile(history_file):
        with open(history_file, "r") as read_file:
            return json.load(read_file)
    else:
        open(history_file, 'w').close()
        return []

def set_history(target, history):
    history_file = './var/' + generate.get_data_dir() + target['identifier'] + '/history.json'
    with open(history_file, "w") as write_file:
        json.dump(history, write_file)