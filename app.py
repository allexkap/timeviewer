import os
from datetime import date, timedelta

import numpy as np
from flask import Flask, render_template, request

from screen_logs import ScreenLogs
from viewer import gen_day_view, get_log_handler

app = Flask(__name__)

logs = ScreenLogs(
    os.environ['SCREENLOGS_DB_PATH'],
    os.environ['SCREENLOGS_RAW_PATH'],
    os.environ['SCREENLOGS_BAK_PATH'],
)


def normalize(arr):
    return arr.astype(dtype=float) / arr.max()


def zip2d(*args):
    for axes in zip(*args):
        yield zip(*axes)


def gen_details(table, start, get_detail_func):
    start -= timedelta(days=start.weekday())
    return (
        (
            f'{(start + timedelta(days=7*j+i)).strftime("%d.%m.%Y")} - '
            f'{get_detail_func(value)}'
            for j, value in enumerate(line)
        )
        for i, line in enumerate(table)
    )


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

    titles = tuple(title for title, _ in logs[:].most_common())

    selected_title = request.form.get('title')
    if selected_title is None:
        selected_title = titles[0]

    handler = get_log_handler(titles=(selected_title,))
    table = gen_day_view(logs, handler, start, stop + timedelta(days=1), hour_shift=8)
    values = normalize(table)
    details = gen_details(table, start, logs.get_detail)

    info = (
        f'Max per day: {logs.get_detail(table.max())}',
        f'On record: {logs.get_detail(table.sum())}',
    )

    return render_template(
        'index.html',
        titles=titles,
        selected_title=selected_title,
        dates=(start, stop),
        data=zip2d(values, details),
        info=info,
    )


if __name__ == '__main__':
    app.run(debug=True)
