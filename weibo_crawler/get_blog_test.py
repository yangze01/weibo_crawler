#!/usr/bin/python
#-*- coding: UTF-8 -*-
from get_blogcont.getlastdata import *
from get_blogcont.analysisBlogPage import *
from createMultiCookies.login import *
from createMultiCookies.multi import *
from collections import deque
from con2mongo.blogUnit import *
from getinfo.getlastdata import *
import time

# usernamePoolDir = '/home/john/userpool1.txt'
# userIDList = list(get_visited("/home/john/visited1.txt"))
# analisysInstace = analisysBlogPage()
# analisysInstace.startBlogAnalysisWork(userIDList, usernamePoolDir)
# print analisysInstace.normalizeTimeFrom('今天 11:11')
if __name__=="__main__":
    userlistdir = '/home/john/userpool2.txt'
    optHeaderlist = getRandomheaderlist()
    optHeaderlist.headerlist=optHeaderlist.get_headerlist(userlistdir)#返回headers池
    db_uri = "mongodb://labUser:aaaaaa@localhost:27017/?authSource=university"
    db_name = "university"
    opt = UseroptOnMongo()
    print(opt.connect2Mongo(db_uri,db_name))
    visited = set()
    queue = list()
    queue = get_queue("/home/john/.txt")#tmpqueue:爬取
    visited = get_visited("/home/john/.txt")
    print("the queue length is"+len(queue))
    try:
        while queue:
            catch_id = queue.pop()#取待爬id
            print("the id will be read:"+str(catch_id))
