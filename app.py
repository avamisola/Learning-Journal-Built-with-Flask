#!/usr/bin/env python3

import csv
import os
import sys

from datetime import date
from datetime import datetime

from flask import abort
from flask import flash
from flask import Flask
from flask import redirect
from flask import render_template
from flask import url_for

import forms
import models


app = Flask(__name__)


@app.route("/")
def index():
    """homepage with all entries"""
    return render_template('index.html')

@app.route("/entries")
@app.route("/entries/index.html")
def listing():
    """homepage with all entries, alternate route"""
    return render_template('index.html')

@app.route("/entries/<int:id>")
def detail(id):
    """view entry detail"""
    return render_template('detail.html')

@app.route("/entries/new")
def add():
    """add entry form"""
    return render_template('new.html')

@app.route("/entries/<int:id>/edit")
def edit(id):
    """edit entry form"""
    return render_template('edit.html')

@app.route("/entries/<int:id>/delete")
def delete():
    """delete entry"""
    entry = models.Entry.select().where(models.Entry.id == id)
    if entry.count() == 0:
        abort(404)
    entry.delete_instance()
    flash("Entry has been deleted!", "success")
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True, port=8000, host='0.0.0.0')
