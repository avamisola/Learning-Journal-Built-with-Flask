#!/usr/bin/env python3

import csv
import os
import sys

from datetime import date
from datetime import datetime

from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/entries")
def entries():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True, port=8000, host='0.0.0.0')
