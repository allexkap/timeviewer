from datetime import date

import numpy as np
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['get', 'post'])
def index():
    try:
        start = date.fromisoformat(request.form['from'])
        end = date.fromisoformat(request.form['to'])
        assert start < end
    except:
        end = date.today()
        start = end.replace(year=end.year - 1)

    apps = (('app0', 'app1', 'app2'), request.form.get('app', ''))

    np.random.seed(0)
    table = np.random.random((7, 40))

    return render_template('index.html', table=table, apps=apps, dates=(start, end))


if __name__ == '__main__':
    app.run(debug=True)
