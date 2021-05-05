import threading

from service.lbapi import loop

threading.Thread(target=loop).start()