#!/usr/bin/env python3

import csv
import os
import sys

from datetime import date
from datetime import datetime

from peewee import *
from playhouse.shortcuts import model_to_dict

db = SqliteDatabase('journal.db')


class Entry(Model):
    entry_id = AutoField()
    title = CharField(max_length=255, unique=True)
    date = DateTimeField(default=datetime.now)
    time_spent = IntegerField(default=0)
    what_you_learned = TextField()
    resources_to_remember = TextField()

    class Meta:
        database = db


def initialize():
    """connect db, create db and table if don't exist"""
    db.connect()
    db.create_tables([Entry], safe=True)
    if Entry.select().count() == 0:
        print("hey")


if __name__ == "__main__":
    initialize()
