from peewee import *

db = SqliteDatabase('database.db')

class Person(Model):
    login = CharField()
    password = CharField()

    class Meta:
        database = db


db.connect()
db.create_tables([Person])