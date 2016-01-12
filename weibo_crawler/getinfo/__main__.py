#-*- coding: UTF-8 -*-
from get_data import *
from login import *
from struc import *
from collections import deque

if __name__=="__main__":
    driver = getLoginDriver(183302748)
    time.sleep(3)
    headers = getHeaders(driver)
    #123456
#   init two struct:queue and set
    queue = deque()
    testqueue = deque()
    visited = set()
    queue.append("2890733820")
    #print queue
    try:
        while queue:
            catch_id = queue.popleft()#取出待爬取的id
            visited |= {catch_id}  # 标记为已访问
            print catch_id
            tmp_userinfo = userinfo()
            tmp_userinfo.info = get_userinfo(catch_id,headers)
            tmp_userinfo.relation = get_relation(catch_id,headers)
            print tmp_userinfo.info
            print tmp_userinfo.relation["fans"]
            for item in tmp_userinfo.relation["fans"]:
                print item
    except urllib2.URLError,e:
        if hasattr(e,"code"):
            print e.code
        if hasattr(e,"reason"):
            print e.reason
    else:
        print "OK"
