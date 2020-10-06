#!/usr/bin/env python3


from flask import abort
from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

import forms
import models


app = Flask(__name__)
app.config['SECRET_KEY'] = 'placeholder required to use flask_wtf'


@app.route("/")
def index():
    """homepage with all entries"""
    entries = models.Entry.select().limit(1000)
    return render_template('index.html', entries=entries)


@app.route("/entries")
def listing():
    """homepage with all entries, alternate route"""
    entries = models.Entry.select().limit(1000)
    return render_template('index.html', entries=entries)


@app.route("/entries/<int:entry_id>")
def detail(entry_id):
    """view entry detail"""
    entry = models.Entry.select().where(models.Entry.entry_id == entry_id)
    if entry.count() == 0:
        abort(404)
    return render_template('detail.html', entry=entry)


@app.route("/entries/new", methods=('GET', 'POST'))
def add():
    """add entry form"""
    form = forms.EntryForm()
    if form.validate_on_submit():
        data = request.form.to_dict()
        entry_list = models.convert_form_data(data)
        models.add_entries(entry_list)
        return redirect(url_for('index'))
    return render_template('new.html', form=form)


@app.route("/entries/<int:entry_id>/edit", methods=('GET', 'POST'))
def edit(entry_id):
    """edit entry form"""
    entry = models.Entry.select().where(models.Entry.entry_id == entry_id)
    if entry.count() == 0:
        abort(404)
    entry_dict = models.Entry.select().where(models.Entry.entry_id == entry_id).dicts().get()
    form = forms.UpdateForm(data=entry_dict)
    if form.validate_on_submit():
        data = request.form.to_dict()
        entry_list = models.convert_form_data(data)
        entry = entry_list[0]
        models.Entry.update(entry_title=entry['entry_title'],
                            entry_date=entry['entry_date'],
                            time_spent=entry['time_spent'],
                            what_you_learned=entry['what_you_learned'],
                            resources_to_remember=entry['resources_to_remember']).where(
                            models.Entry.entry_id == entry_id).execute()
        return redirect(url_for('index'))
    return render_template('edit.html', entry=entry, form=form)


@app.route("/entries/<int:entry_id>/delete")
def delete(entry_id):
    """delete entry"""
    entry = models.Entry.select().where(models.Entry.entry_id == entry_id)
    if entry.count() == 0:
        abort(404)
    entry.delete_instance()
    return redirect(url_for('index'))


if __name__ == "__main__":
    models.initialize()
    app.run(debug=True, port=8000, host='0.0.0.0')
