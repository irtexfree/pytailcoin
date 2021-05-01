from sqlobject import *

sqlhub.processConnection = connectionForURI('sqlite:/:memory:')

class Person(SQLObject):
    name = StringCol()
    password = StringCol()

Person.createTable()