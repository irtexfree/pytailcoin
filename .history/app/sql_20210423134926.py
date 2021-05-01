from sqlobject import *

sqlhub.processConnection = connectionForURI('sqlite:/:memory:')

class Person(SQLObject):
    name = StringCol()
    login = StringCol()
    paswword = StringCol()