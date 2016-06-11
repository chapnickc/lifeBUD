from LifeBud import *


services = lb.dev.discoverServices()

lb = LifeBud()
lb.scan(timeout = 5)
lb.show_services()
lb.enable_notifications()
lb.listen()












