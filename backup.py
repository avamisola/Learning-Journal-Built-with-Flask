#!/usr/bin/env python3

import csv
import os
import sys

from datetime import date
from datetime import datetime

from peewee import *
from playhouse.shortcuts import model_to_dict

db = SqliteDatabase('inventory.db')


class Product(Model):
    product_id = AutoField()
    product_name = CharField(max_length=255, unique=True)
    product_quantity = IntegerField(default=0)
    product_price = IntegerField(default=0)
    date_updated = DateTimeField(default=datetime.now)

    class Meta:
        database = db


def initialize():
    """connect db, create db and table if don't exist"""
    db.connect()
    db.create_tables([Product], safe=True)


def convert_price(price):
    """convert dollar price to cents"""
    return int(round(float(price.replace('$','')) * 100))


def read_csv():
    """read csv and clean data, add to database"""
    with open('inventory.csv', newline='') as csvfile:
        product_reader = csv.DictReader(csvfile, delimiter=',')
        rows = list(product_reader)
        product_list = []
        for row in rows:
            row['product_price'] = convert_price(row['product_price'])
            converted_date = datetime.strptime(row['date_updated'], '%m/%d/%Y')
            row['date_updated'] = datetime.combine(converted_date, datetime.min.time())
            product_list.append(row)
        add_products(product_list)


def add_products(product_list):
    """add new products to database, update existing products"""
    for product in product_list:
        try:
            Product.create(product_name=product['product_name'],
                            product_price=product['product_price'],
                            product_quantity=product['product_quantity'],
                            date_updated=product['date_updated'])
        except IntegrityError:
            product_record = Product.get(product_name=product['product_name'])
            product_record.product_price = product['product_price']
            product_record.product_quantity = product['product_quantity']
            product_record.date_updated = product['date_updated']
            product_record.save()


def menu_loop():
    """show the menu"""
    clear()
    choice_main = None

    print("""\n
======================================================
--Welcome to the Store Inventory Database--\n
Select an option by entering the corresponding letter\n
v) View entry in database
a) Add entry to database
b) Backup the database to csv
q) Quit the app
======================================================
    """)

    choice_main = input("Enter letter to select option: ").lower().strip()

    if choice_main == 'v':
        view_entry()
    elif choice_main == 'a':
        add_entry()
    elif choice_main == 'b':
        backup_database()
    elif choice_main == 'q':
        quit_app()
    else:
        error_handler()
        

def view_entry():
    """view entry in database by product id"""
    id_input = None
    id_input = input("Enter product_id to view entry: ").lower().strip()

    try:
        query_result = Product.get(Product.product_id == id_input)
    except DoesNotExist:
        print("\n\nThat product_id does not exist in database")
        error_handler()

    dollar_price = '${:,.2f}'.format(query_result.product_price / 100)

    print(f"""\n
    product_id: {query_result.product_id}
    product_name: {query_result.product_name}
    product_price: {dollar_price}
    product_quantity: {query_result.product_quantity}
    date_updated: {query_result.date_updated}
    """)
    continue_prompt()


def add_entry():
    """add entry to database"""
    entry_dict = {}
    current_datetime = datetime.now().replace(microsecond=0)

    try:
        name_input = str(input("Enter product name: "))
        price_input = convert_price(input("Enter product price: "))
        quantity_input = int(input("Enter product quantity: "))
    except ValueError:
        error_handler()

    entry_dict["product_name"] = name_input
    entry_dict["product_price"] = price_input
    entry_dict["product_quantity"] = quantity_input
    entry_dict["date_updated"] = current_datetime

    product_list = [entry_dict]
    add_products(product_list)
    
    print("\n\nProduct has been added to database")
    continue_prompt()


def backup_database():
    """backup the database to csv"""
    db_data = [model_to_dict(item) for item in Product.select().order_by(Product.product_id)]

    with open('backup.csv', 'w', newline='') as csvfile:
        fieldnames = ['product_id',
                    'product_name',
                    'product_price',
                    'product_quantity',
                    'date_updated']
        productwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        productwriter.writeheader()
        productwriter.writerows(db_data)

    print("\n\nDatabase table has been backed up to backup.csv")
    continue_prompt()


def quit_app():
    """quit the application"""
    print("\n\nThank you for using this app. Goodbye!")
    print("\n\n----END----\n\n")
    sys.exit()


def error_handler():
    """generic error message and reroute to main menu choice"""
    print("\n\nThat is not a valid input, please try again.")
    continue_prompt()


def continue_prompt():
    """prompt to press enter to continue back to main menu"""
    input("\nPress ENTER to continue...")
    menu_loop()


def clear():
    """clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == "__main__":
    initialize()
    read_csv()
    menu_loop()
