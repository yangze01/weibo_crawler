#-*- coding: UTF-8 -*-
from login import *
from getinfo import *
from struc import *
import urllib
import urllib2
import cookielib
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

driver = getLoginDriver(183302748)
time.sleep(3)
headers = getHeaders(driver)

try:
    userid = "2890733820"
    a = get_userinfo(userid,headers)
    print a



except urllib2.URLError,e:
    if hasattr(e,"code"):
        print e.code
    if hasattr(e,"reason"):
        print e.reason
else:
    print "OK"
