from sqlobject import *

sqlhub.processConnection = connectionForURI('database.db')

class Person(SQLObject):
    name = StringCol()
    password = StringCol()

Person.createTable()