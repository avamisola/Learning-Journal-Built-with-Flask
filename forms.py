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
        raise ValidationError("Entry entry_title already exists.")


class EntryForm(Form):
    entry_title = StringField("entry_title", validators=[
        DataRequired(), entry_title_exists])
    created = DateField("Data", validators=[
        DataRequired()])
    time_spent = IntegerField("Time Spent", validators=[
        DataRequired()])
    learned = TextAreaField("What you learned", validators=[
        DataRequired()])
    to_remember = TextAreaField("Resources to remember",
                                validators=[DataRequired()])