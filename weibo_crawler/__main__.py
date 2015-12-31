#-*- coding: UTF-8 -*-
from get_data import *
from login import *
from struc import *
from collections import deque

if __name__=="__main__":
    driver = getLoginDriver("","")
    time.sleep(3)
    headers = getHeaders(driver)
#   init two struct:queue and set
    queue = deque()
    visited = set()
    queue.append(3199208303)
    use_url = all_url()
    this_url = use_url.fansurl+str(2)

    req = urllib2.Request(this_url,headers=headers)
    try:
        while deque:
            catch_id = queue.popleft()#pop the left var


    except urllib2.URLError,e:
        if hasattr(e,"code"):
            print e.code
        if hasattr(e,"reason"):
            print e.reason
    else:
        print "OK"
