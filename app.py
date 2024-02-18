from datetime import date

import numpy as np
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    try:
        start = date.fromisoformat(request.args["from"])
        end = date.fromisoformat(request.args["to"])
        assert start < end
    except:
        end = date.today()
        start = end.replace(year=end.year - 1)

    np.random.seed(0)
    table = np.random.random((7, 40))

    return render_template("index.html", table=table, dates=(start, end))


if __name__ == "__main__":
    app.run(debug=True)
