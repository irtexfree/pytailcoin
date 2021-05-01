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
    chat_id = CharField()
    wantHelp = CharField()

    class Meta:
        database = db


db.connect()
db.create_tables([Person, Dialog, Customer])