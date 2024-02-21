from datetime import date

import numpy as np
from flask import Flask, render_template, request

from dummy_logs import DummyLogs
from viewer import gen_day_view, get_log_handler

app = Flask(__name__)

dummy_logs = DummyLogs()


@app.route('/', methods=['get', 'post'])
def index():
    try:
        start = date.fromisoformat(request.form['from'])
        stop = date.fromisoformat(request.form['to'])
        assert start < stop
    except:
        stop = date.today()
        start = stop.replace(year=stop.year - 1)

    apps = (('app0', 'app1', 'app2'), request.form.get('app', ''))

    dummy_logs.random.seed(0)
    handler = get_log_handler()
    table = gen_day_view(dummy_logs, handler, start, stop) / 255

    return render_template('index.html', table=table, apps=apps, dates=(start, stop))


if __name__ == '__main__':
    app.run(debug=True)
