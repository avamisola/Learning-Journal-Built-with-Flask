#!/usr/bin/env python3

from flask_wtf import Form
from wtforms import DateField
from wtforms import IntegerField
from wtforms import StringField
from wtforms import TextAreaField
from wtforms.validators import DataRequired
from wtforms.validators import ValidationError

from models import Entry


def entry_title_exists(form, field):
    if Entry.select().where(Entry.entry_title == field.data).exists():
        raise ValidationError("Entry title already exists.")


class EntryForm(Form):
    entry_title = StringField(
        "Title", validators=[
            DataRequired(),
            entry_title_exists
        ])
    entry_date = DateField(
        "Date (mm/dd/yyyy)",
        format='%m/%d/%Y',
        validators=[
            DataRequired()
        ])
    time_spent = IntegerField(
        "Time Spent (hours)",
        validators=[
            DataRequired()
        ])
    what_you_learned = TextAreaField(
        "What I Learned",
        validators=[
            DataRequired()
        ])
    resources_to_remember = TextAreaField(
        "Resources to Remember",
        validators=[
            DataRequired()
        ])
