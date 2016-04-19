#-*- coding: UTF-8 -*-
import time
from createMultiCookies.multi import *
from createMultiCookies.login import *
from collections import deque
from getinfo.get_data import *
from con2mongo.user_Unit import *
if __name__=="__main__":
    driver = getLoginDriver()
    header = getHeaders(driver)
    userid1 = "1765519035"
    userid2 = "3277737114"
    userid3 = "1445975867"
    userid4 = "2890733820"
