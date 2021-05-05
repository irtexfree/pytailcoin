from peewee import *

db = SqliteDatabase('database.db')

class Person(Model):
    # Password data
    PASSPORT_SECRET = CharField()
    PASSPORT_ID= CharField()
    
    # Account data
    login = CharField()
    first_name = CharField()
    last_name = CharField()
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
    first_name= CharField()
    link = CharField()

    class Meta:
        database = db


class Wallet(Model):
    id= CharField(primary_key=True)
    currency = CharField()
    value= CharField()
    address = CharField()
    name= CharField()
    
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
    hash = CharField()

    class Meta:
        database = db


class ConfirmAdventure(Model):
    id = CharField(primary_key=True)
    contact_id = CharField()
    created_at = CharField()
    amount = CharField()
    currency = CharField()
    status = CharField()
    hash = CharField()

    class Meta:
        database = db


db.connect()
db.create_tables([Person, Dialog, Customer, Adventure,  Wallet,  Ticket, ConfirmAdventure])
