#-*- coding: UTF-8 -*-
#from login import *
from createMultiCookies.multi import *
from collections import deque
from getinfo.get_data import *
from con2mongo.user_Unit import *
from con2mongo.UserOnMongo import *
from getinfo.getlastdata import *
from createMultiCookies.login import *
import time


if __name__=="__main__":

    userlistdir = '/home/john/userpool/userpool2.txt'
    optHeaderlist = getRandomheaderlist()
    optHeaderlist.headerlist=optHeaderlist.get_headerlist(userlistdir)#返回headers池
    db_uri = "mongodb://labUser:aaaaaa@localhost:27017/?authSource=university"
    db_name = "university"
    #db_uri = "mongodb://labUser:aaaaaa@localhost:27017/?authSource=lab"
    #db_name = "lab"
    opt = UseroptOnMongo()
    print(opt.connect2Mongo(db_uri,db_name))
    visited = set()
    queue = list()
    # queue = get_queue("/home/john/queue.txt")#tmpqueue:爬取
    visited = get_visited("/home/john//visited/visitedwithuniversity.txt")
    # queue = getUserWithCondition(optHeaderlist,keyword="复旦大学",searchtype="scho")+get_queue("/home/john/queue/queuewithuniversity.txt")
    queue = get_queue("/home/john/queue/queuewithuniversity.txt")
    # queue.append('1182391231')


    flag1 = True
    i=2000
    print(len(queue))
    try:
        while queue:
            # i=i-1
            catch_id = queue.pop()#取出待爬取的id
            print("the id will be read:"+str(catch_id))
            if catch_id not in visited:
                visited |= {catch_id}  # 标记为已访问

                tmp_userUnit = userUnit()
                tmp_userUnit.user_unit["_id"]=catch_id
                tmp_userUnit.user_unit["userinfo"] = get_userinfo(catch_id,optHeaderlist)

                if(len(queue)>=12000):
                    queue=list(set(queue))
                #    queue=queue[3000:]
                    flag1 = False
                if(flag1):
                    tmp_userUnit.user_unit["relation"] = get_relation(catch_id,optHeaderlist)
                    queue = tmp_userUnit.user_unit["relation"]["fans"]+queue
                opt.insertUser2Mongo(opt.db,tmp_userUnit.user_unit)
                print("the queue len is: "+str(len(queue)))
            print("the visited len is: "+str(len(visited)))
        f1 = open("/home/john/visited/visitedwithuniversity.txt","w")
        f1.write(str(visited))
        f1.close()
        f2 = open("/home/john/queue/queuewithuniversity.txt","w")
        f2.write(str(queue))
        f2.close()
    except:
        #退出保存
        f1 = open("/home/john/visited/visitedwithuniversity.txt","w")
        f1.write(str(visited))
        f1.close()
        f2 = open("/home/john/queue/queuewithuniversity.txt","w")
        f2.write(str(queue))
        f2.close()
    else:
        print("OK")
