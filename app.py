import numpy as np
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    np.random.seed(0)
    data = np.random.random((7, 40))
    return render_template("index.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)
