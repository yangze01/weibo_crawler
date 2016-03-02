#-*- coding: UTF-8 -*-
from get_data import *
from login import *
from user_Unit import *
from collections import deque
from multi import *
import time
if __name__=="__main__":

    userlistdir = '/home/john/userpool.txt'
    optHeaderlist = getRandomheaderlist()
    optHeaderlist.headerlist=optHeaderlist.get_headerlist(userlistdir)#返回headers池

    queue = list()
    visited = set()
    queue.append("2890733820")
    #print queue
    try:
        while queue:
            catch_id = queue.pop()#取出待爬取的id
            print "the id will be read:"+str(catch_id)
            if catch_id not in visited:
                visited |= {catch_id}  # 标记为已访问

                tmp_userUnit = userUnit()
                tmp_userUnit.user_unit["user_ID"]=catch_id
                tmp_userUnit.user_unit["userinfo"] = get_userinfo(catch_id,optHeaderlist)
                print tmp_userUnit.user_unit["userinfo"]
                tmp_userUnit.user_unit["relation"] = get_relation(catch_id,optHeaderlist)
                queue = tmp_userUnit.user_unit["relation"]["intersection"]+queue
                print queue

            print "the id has beed read:"
            print visited

    except urllib2.URLError,e:
        if hasattr(e,"code"):
            print e.code
        if hasattr(e,"reason"):
            print e.reason
    else:
        print "OK"
