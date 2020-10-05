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
app.config['SECRET_KEY'] = 'required to use flask_wtf'


@app.route("/")
def index():
    """homepage with all entries"""
    entries = models.Entry.select().limit(10)
    return render_template('index.html', entries=entries)

@app.route("/entries")
def listing():
    """homepage with all entries, alternate route"""
    entries = models.Entry.select().limit(10)
    return render_template('index.html', entries=entries)

@app.route("/entries/<int:entry_id>", methods=('GET', 'POST'))
def detail(entry_id):
    """view entry detail"""
    entry = models.Entry.select().where(models.Entry.entry_id == entry_id)
    print(entry)
    return render_template('detail.html', entry=entry)

@app.route("/entries/new", methods=('GET', 'POST'))
def add():
    """add entry form"""
    form = forms.Entry()
    if form.validate_on_submit():
        print(form)
        return redirect(url_for('index'))
    return render_template('new.html', form=form)

@app.route("/entries/<int:entry_id>/edit", methods=('GET', 'POST'))
def edit(entry_id):
    """edit entry form"""
    return render_template('edit.html')

@app.route("/entries/<int:entry_id>/delete", methods=('GET', 'POST'))
def delete(entry_id):
    """delete entry"""
    entry = models.Entry.select().where(models.Entry.entry_id == entry_id)
    if entry.count() == 0:
        abort(404)
    entry.delete_instance()
    flash("Entry has been deleted!", "success")
    return redirect(url_for('index'))


if __name__ == "__main__":
    models.initialize()
    app.run(debug=True, port=8000, host='0.0.0.0')
