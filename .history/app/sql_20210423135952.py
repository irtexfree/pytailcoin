from peewee import *

db = SqliteDatabase('database.db')

class Person(Model):
    name = CharField()
    password = CharField()

    class Meta:
        database = db


db.connect()
