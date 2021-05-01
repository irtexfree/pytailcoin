from peewee import *

db = SqliteDatabase('database.db')

class Person(Model):
    login = CharField()
    password = CharField()

    class Meta:
        database = db

class Dialog(Model):
    chat_id = CharField()
    text = CharField()
    time = CharField()
    first_name= CharField()
    sender = CharField()

    class Meta:
        database = db


class Customer(Model):
    chat_id = CharField(primary_key=True)
    want_help = CharField()
    first_name= CharField()
    link = CharField()

    class Meta:
        database = db


class Ticket(Model):
    chat_id = CharField(primary_key=True)
    first_name= CharField()
    from_currency = CharField()
    to_currency = CharField()
    count_currency = CharField()
    price_currency = CharField()

    class Meta:
        database = db


class Adventure(Model):
    id = CharField(primary_key=True)
    price = CharField()
    amount = CharField()
    provider = CharField()
    city = CharField()
    url = CharField()

    class Meta:
        database = db


db.connect()
db.create_tables([Person, Dialog, Customer, Adventure])