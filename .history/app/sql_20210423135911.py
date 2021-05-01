from peewee import *

db = SqliteDatabase('people.db')

class Person(Model):
    name = CharField()
    password = CharField()

    class Meta:
        database = db # This model uses the "people.db" database.