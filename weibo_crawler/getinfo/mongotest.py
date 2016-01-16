#-*- coding: UTF-8 -*-
from get_data import *
from login import *
from user_unit import *
from collections import deque
from user_unit import *
from optOnMongo import *
import time
if __name__=="__main__":
    driver = getLoginDriver(18330274826)
    time.sleep(3)
    headers = getHeaders(driver)
    db_uri = "mongodb://yangze01:123@localhost:27017/?authSource=admin"
    db_name = "admin"
    try:
        old_user_unit = userUnit()
        old_user_unit.user_unit[user_ID]="123"
        #connect2Mongo
        opt = optOnMongo()
        print opt.connect2Mongo(db_uri,db_name)
        print opt.insertUser2Mongo(opt.db,old_user_unit.user_unit)

        while queue:

            catch_id = queue.pop()#取出待爬取的id
            visited |= {catch_id}  # 标记为已访问
            print visited
            tmp_userUnit = userUnit()
            tmp_userUnit.user_unit["user_ID"]=catch_id
            tmp_userUnit.user_unit["userinfo"] = get_userinfo(catch_id,headers)
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
