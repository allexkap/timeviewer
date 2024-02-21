from datetime import date

import numpy as np
from flask import Flask, render_template, request

from dummy_logs import DummyLogs
from viewer import gen_day_view, get_log_handler

app = Flask(__name__)

logs = DummyLogs()


def normalize(arr):
    return arr.astype(dtype=float) / arr.max()


def zip2d(*args):
    for axes in zip(*args):
        yield zip(*axes)


@app.route('/', methods=['get', 'post'])
def index():
    try:
        start = date.fromisoformat(request.form['from'])
        stop = date.fromisoformat(request.form['to'])
        assert start < stop
    except:
        stop = date.today()
        offset = 0
        while True:
            try:
                start = stop.replace(year=stop.year - 1, day=stop.day - offset)
            except ValueError:
                offset += 1
            else:
                break

    logs.random.seed(0)

    titles = ('test0', 'test1', 'test2')  # gen titles from logs

    selected_title = request.form.get('title')
    if selected_title is None:
        selected_title = titles[0]

    handler = get_log_handler()
    table = gen_day_view(logs, handler, start, stop)
    values = normalize(table)
    details = table  # get repr from logs

    return render_template(
        'index.html',
        titles=titles,
        selected_title=selected_title,
        dates=(start, stop),
        data=zip2d(values, details),
    )


if __name__ == '__main__':
    app.run(debug=True)
