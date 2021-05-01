from sqlobject import *

sqlhub.processConnection = connectionForURI('database.db')

class Person(SQLObject):
    name = StringCol()
    password = StringCol()

try:
    Person.createTable()
except:
    pass