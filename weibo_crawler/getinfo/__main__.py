#-*- coding: UTF-8 -*-
from get_data import *
from login import *
from user_unit import *
from collections import deque

if __name__=="__main__":
    driver = getLoginDriver("18330274826","523581600")
    time.sleep(3)
    headers = getHeaders(driver)
#   init two struct:queue and set
    queue = list()
    visited = set()

    queue.append("2890733820")
    #print queue
    try:
        while queue:
            catch_id = queue.pop()#取出待爬取的id
            print catch_id
            print type(catch_id)
            visited |= {catch_id}  # 标记为已访问
            print visited
            tmp_userUnit = userUnit()
            tmp_userUnit.user_unit["user_ID"]=catch_id
            tmp_userUnit.user_unit["userinfo"] = get_userinfo(catch_id,headers)
            print tmp_userUnit.user_unit["userinfo"]
            tmp_userUnit.user_unit["relation"] = get_relation(catch_id,headers)
            queue = tmp_userUnit.user_unit["relation"]["intersection"]+queue
            print queue
    except urllib2.URLError,e:
        if hasattr(e,"code"):
            print e.code
        if hasattr(e,"reason"):
            print e.reason
    else:
        print "OK"
