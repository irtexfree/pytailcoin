from sqlobject import *

sqlhub.processConnection = connectionForURI('sqlite:/:memory:')
