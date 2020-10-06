#!/usr/bin/env python3

import csv

from datetime import datetime

from peewee import *


db = SqliteDatabase('journal.db')


class Entry(Model):
    entry_id = AutoField()
    entry_title = CharField(max_length=255, unique=True)
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


def convert_date(date):
    """convert date for db insert"""
    converted_date = datetime.strptime(date, '%m/%d/%Y')
    return datetime.combine(converted_date, datetime.min.time())


def read_csv():
    """read csv and clean data, add to database"""
    with open('entry.csv', newline='') as csvfile:
        entry_reader = csv.DictReader(csvfile, delimiter=',')
        rows = list(entry_reader)
        entry_list = []
        for row in rows:
            row['entry_date'] = convert_date(row['entry_date'])
            entry_list.append(row)
        add_entries(entry_list)


def add_entries(entry_list):
    """add new entries to database, update existing entries"""
    for entry in entry_list:
        try:
            Entry.create(entry_title=entry['entry_title'],
                        entry_date=entry['entry_date'],
                        time_spent=entry['time_spent'],
                        what_you_learned=entry['what_you_learned'],
                        resources_to_remember=entry['resources_to_remember'])
        except IntegrityError:
            entry_record = Entry.get(entry_title=entry['entry_title'])
            entry_record.entry_date = entry['entry_date']
            entry_record.time_spent = entry['time_spent']
            entry_record.what_you_learned = entry['what_you_learned']
            entry_record.resources_to_remember = entry['resources_to_remember']
            entry_record.save()


def convert_form_data(data):
    """convert form data into dictionary inside list, format required by add_entries"""
    entry_dict = {}
    entry_dict["entry_title"] = data["entry_title"].strip()
    entry_dict["entry_date"] = convert_date(data["entry_date"])
    entry_dict["time_spent"] = data["time_spent"].strip()
    entry_dict["what_you_learned"] = data["what_you_learned"].strip()
    entry_dict["resources_to_remember"] = data["resources_to_remember"].strip()
    entry_list = [entry_dict]
    return entry_list


if __name__ == "__main__":
    initialize()
