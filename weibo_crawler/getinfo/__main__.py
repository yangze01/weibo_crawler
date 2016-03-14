#-*- coding: UTF-8 -*-
from get_data import *
from login import *
from user_Unit import *
from collections import deque
from multi import *
from UserOnMongo import *
import time
from getlastdata import *
if __name__=="__main__":

    userlistdir = '/home/john/userpool.txt'
    optHeaderlist = getRandomheaderlist()
    optHeaderlist.headerlist=optHeaderlist.get_headerlist(userlistdir)#返回headers池
    #测试数据库访问
    old_userdata = userUnit()
    old_userdata.user_unit["userinfo"]["vip"]='2'
    db_uri = "mongodb://labUser:aaaaaa@localhost:27017/?authSource=lab"
    db_name = "lab"
    opt = UseroptOnMongo()
    print opt.connect2Mongo(db_uri,db_name)
    #print opt.insertUser2Mongo(opt.db,old_userdata.user_unit)
    #print opt.deleteUser2Mongo(opt.db,old_userdata.user_unit)
    #visited = set()
    queue = get_queue("/home/john/queue.txt")
    visited = get_visited("/home/john/visited.txt")
    visited.add("5857668803")
    visited.add("5258924632")
    visited.add("5872642166")
    visited.add("5817256045")
    visited.add("5788759176")
    visited.add("5818864566")
    visited.add("5797065069")
    visited.add("5878919480")
    #queue.append("3331417710")
    flag1 = True

    print queue
    try:
        while queue:
            catch_id = queue.pop()#取出待爬取的id
            print "the id will be read:"+str(catch_id)
            if catch_id not in visited:
                visited |= {catch_id}  # 标记为已访问

                tmp_userUnit = userUnit()
                tmp_userUnit.user_unit["_id"]=catch_id
                tmp_userUnit.user_unit["userinfo"] = get_userinfo(catch_id,optHeaderlist)
                #print tmp_userUnit.user_unit["userinfo"]
                #tmp_userUnit.user_unit["relation"]["intersection"]=s
                if(len(list(set(queue)))>=5000):
                    a=list(set(queue))
                    flag1 = False
                if(flag1):
                    tmp_userUnit.user_unit["relation"] = get_relation(catch_id,optHeaderlist)
                    queue = tmp_userUnit.user_unit["relation"]["intersection"]+queue
                opt.insertUser2Mongo(opt.db,tmp_userUnit.user_unit)
                print queue
            print "the id has beed read:"
            print visited
    # except urllib2.URLError,e:
    #     if hasattr(e,"code"):
    #         print e.code
    #     if hasattr(e,"reason"):
    #         print e.reason
    except:
        #退出保存
        f1 = open("/home/john/visited.txt","w")
        f1.write(str(visited))
        f1.close()
        f2 = open("/home/john/queue.txt","w")
        f2.write(str(queue))
        f2.close()
    else:
        print "OK"
