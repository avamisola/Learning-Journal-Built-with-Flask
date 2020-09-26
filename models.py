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
    entry_date = DateTimeField(default=datetime.now)
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
        read_csv()


def read_csv():
    """read csv and clean data, add to database"""
    with open('entry.csv', newline='') as csvfile:
        entry_reader = csv.DictReader(csvfile, delimiter=',')
        rows = list(entry_reader)
        entry_list = []
        for row in rows:
            converted_date = datetime.strptime(row['entry_date'], '%m/%d/%Y')
            row['entry_date'] = datetime.combine(converted_date, datetime.min.time())
            entry_list.append(row)
        add_entries(entry_list)


def add_entries(entry_list):
    """add new products to database, update existing products"""
    for entry in entry_list:
        try:
            Entry.create(title=entry['title'],
                        entry_date=entry['entry_date'],
                        time_spent=entry['time_spent'],
                        what_you_learned=entry['what_you_learned'],
                        resources_to_remember=entry['resources_to_remember'])
        except IntegrityError:
            entry_record = Entry.get(product_name=product['title'])
            entry_record.entry_date = product['entry_date']
            entry_record.time_spent = product['time_spent']
            entry_record.what_you_learned = product['what_you_learned']
            entry_record.resources_to_remember = product['resources_to_remember']
            entry_record.save()


if __name__ == "__main__":
    initialize()
