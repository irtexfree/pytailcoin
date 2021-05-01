from sqlobject import *

sqlhub.processConnection = connectionForURI('sqlite:/:memory:')

class Person(SQLObject):
    name = StringCol()
    login = StringCol()
    password = StringCol()

Person.createTable()