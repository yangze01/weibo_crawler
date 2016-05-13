#!/usr/bin/python
#-*- coding: UTF-8 -*-

# from get_blogcont.analysisBlogPage import *

from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from createMultiCookies.getRandomCookie import *
from selenium.webdriver.common.by import By
from createMultiCookies.login import *
from createMultiCookies.multi import *
from get_blogcont.analysisAttributesPage import *
from con2mongo.optOnMongo import *
from getinfo.getlastdata import *
from con2mongo.blogUnit import *
from getinfo.getlastdata import *
from selenium import webdriver
import threading
import time
import random
import urllib
import urllib2
import cookielib
import sys
import os
import time
import re
class analisysBlogPage(threading.Thread,analisysAttributePage, blogUnit, getRandomheaderlist):
    def __init__(self,userpooldir,threadname,logintype):
        threading.Thread.__init__(self)
        analisysAttributePage.__init__(self)
        blogUnit.__init__(self)
        getRandomheaderlist.__init__(self)
        self.userpooldir = userpooldir
        self.threadname = threadname
        self.logintype = logintype
        self.oneBlogAllContentDict = {
            "blog_id": "",
            "blog_address": "",
            "time": "",
            "device": "",
            "content":
            {
                "topic_name": [],
                "topic_content": [],
                "mention_name": [],
                "mention_content": [],
                "url_name": [],
                "url_content": [],
                "text_content": ""
            },
            "blog_attitude": ""
        }
        self.repost_url = {"repost_url":""}
        self.comment_url = {"comment_url": ""}
        # self.countNum = ''
        self.optOnMongoInstance = optOnMongo()
        self.getBlogsCount = 0
        self.visitPageCount = 0
        # self.userIDList = list()
        # self.user_id_list = ''
        # self.sinaNetHeader = ''
        self.user_id = ''
        # self.blogCurrentPageUrl = ''
        # self.req = ''
        # self.response = ''
        # self.blogPage = ''
        # self.blogPageFD = ''
        # self.blogPageNumber = ''
        # self.blogText = ''
        # self.blogIDListPattern = ''
        # self.blogIDList = ''
        # self.oneBlogAllContentPattern = ''
        # self.oneBlogAllContent = ''
        # self.blogIDPattern = ''
        # self.blogTextContentPattern = ''
        # self.patternContTamp = ''
        # self.patternMentionTamp = ''
        # self.blogAddressPattern = ''
        # self.blogTimeDevicePattern = ''
        # self.blogTimePattern = ''
        # self.blogDevicePattern = ''
        # self.blogAttitudePattern = ''
        # self.blogRepostUrlPattern = ''
        # self.blogCommentUrlPattern = ''
    def run(self):
        print self.userpooldir
        global queue
        global visited
        getRandomheaderlist.headerlist = getRandomheaderlist.get_headerlist(self,self.userpooldir,self.logintype)
        self.sinaNetHeader = getRandomheaderlist.getOneRandomCookie(self)
        self.db_uri = "mongodb://labUser:aaaaaa@localhost:27017/?authSource=blog"
        self.db_name = "blog"
        self.optOnMongoInstance.connect2Mongo(self.db_uri, self.db_name)
        print self.optOnMongoInstance.db
        i=10000
        try:
            while i:
                if queue:
                    print i
                    CONDITION.acquire()
                    catch_id = queue.pop()
                    CONDITION.release()
                    print self.threadname+"   the id will be read:"+str(catch_id)
                    if catch_id not in visited:
                        self.user_id = catch_id
                        visited |= {catch_id}  # 标记为已访问
                        self.visitIntoUserBlog(self.sinaNetHeader,catch_id,self.optOnMongoInstance)
                        print("the queue len is: "+str(len(queue)))
                    i=i-1
                    print("the visited len is: "+str(len(visited)))

            f1 = open("/home/john/visited/blogvisited.txt","w")
            f1.write(str(visited))
            f1.close()
            f2 = open("/home/john/queue/blogqueue.txt","w")
            f2.write(str(queue))
            f2.close()
        except:
            #退出保存
            print "except"
            f1 = open("/home/john/visited/blogvisited.txt","w")
            f1.write(str(visited))
            f1.close()
            f2 = open("/home/john/queue/blogqueue.txt","w")
            f2.write(str(queue))
            f2.close()
        else:
            print("OK")



    def visitIntoUserBlog(self,sinaNetHeader,user_id,optOnMongoInstance):
        self.optOnMongoInstance = optOnMongoInstance
        self.blogInitPageUrl = "http://weibo.cn/" + user_id + "/profile"
        self.sinaNetHeader = getRandomheaderlist.getOneRandomCookie(self)

        self.countNum = 0
        self.req = urllib2.Request(self.blogInitPageUrl,headers = self.sinaNetHeader)
        self.response = urllib2.urlopen(self.req)
        self.blogPage = self.response.read()

        self.blogPageNumber = self.getPageNumber(self.blogPage)
        print "blog page number: %d" % self.blogPageNumber
        if self.blogPageNumber > 0:
            # for self.countNum in range(self.blogPageNumber):
            # self.countNum = self.countNum+1
            self.countNum = 1
            self.blogCurrentPageUrl = self.blogInitPageUrl + "?page=" + "%d" % self.countNum
            print self.blogCurrentPageUrl
            self.req = urllib2.Request(self.blogCurrentPageUrl,headers = self.sinaNetHeader)
            self.response = urllib2.urlopen(self.req)
            self.blogPage = self.response.read()
            # print self.blogPage
            self.getOnePageBlogs(self.blogPage, self.optOnMongoInstance)
        else:
            self.blogCurrentPageUrl = self.blogInitPageUrl
            self.req = urllib2.Request(self.blogCurrentPageUrl,headers=self.sinaNetHeader)
            self.response = urllib2.urlopen(self.req)
            self.blogPage = self.response.read()
            # get_data(self.blogCurrentPageUrl, self.sinaNetHeader)
            self.getOnePageBlogs(self.blogPage, self.optOnMongoInstance)

    def getOnePageBlogs(self,blogPage,optOnMongoInstance):

        self.optOnMongoInstance = optOnMongoInstance
        self.blogText = blogPage
        self.visitPageCount += 1
        if self.visitPageCount%4 == 0:
            self.sinaNetHeader = getRandomheaderlist.getOneRandomCookie(self)
            time.sleep(random.randint(2,10))
        self.oneBlogAllContentPattern = re.compile("""(?<=<div class="c" id=)"M_\w+"><div><span class="ctt">.*?(?=</div></div>)""")
        if self.oneBlogAllContentPattern.findall(self.blogText):

            print "weibo numbers :"len(self.oneBlogAllContentPattern.findall(self.blogText))

            self.oneBlogAllContent = self.oneBlogAllContentPattern.findall(self.blogText)[0]
            self.blog_unit = self.getOneBlog(self.oneBlogAllContent, self.optOnMongoInstance)
            self.optOnMongoInstance.insertBlog2Mongo(self.optOnMongoInstance.db, self.blog_unit)
            self.getBlogsCount = self.getBlogsCount + 1

            # for self.oneBlogAllContent in self.oneBlogAllContentPattern.findall(self.blogText):
            #     self.blog_unit = self.getOneBlog(self.oneBlogAllContent, self.optOnMongoInstance)
            #     ##self.optOnMongoInstance.insertBlog2Mongo(self.optOnMongoInstance.db, self.getOneBlog(self.oneBlogAllContent))
            #     ##print self.blog_unit
            #     self.optOnMongoInstance.insertBlog2Mongo(self.optOnMongoInstance.db, self.blog_unit)
            #     self.getBlogsCount = self.getBlogsCount + 1
        else:
            print "no blog"

    def getOneBlog(self, oneBlogAllContent, optOnMongoInstance):
        '''
            description:
                get one blog from the loaded blog page "./get_blogcont/currentBlogPage.html"
            input:
                oneBlogAllContent:
                    all content of one blog: blog contnet , comment content , repost content
                optOnMongoInstance:
                    mongodb db instance
            output:
                none
        '''
        self.optOnMongoInstance = optOnMongoInstance
        self.oneBlogAllContent = oneBlogAllContent
        ##print self.oneBlogAllContent
        ##self.oneBlogAllContentDict = self.oneNewBlogAllContentDict
        #get blog ID
        self.blogIDPattern = re.compile("""(?<=")M_\w+(?="><div><span class="ctt">)""")
        self.oneBlogAllContentDict['blog_id'] = self.blogIDPattern.findall(self.oneBlogAllContent)[0]
        ##print "blog_id :%s" % self.oneBlogAllContentDict['blog_id']
        #get blog text content
        self.blogTextContentPattern = re.compile("""(?<=<div><span class="ctt">).*?(?=</span>|\[位置\])""")
        if self.blogTextContentPattern.findall(self.oneBlogAllContent):
            self.textContentTamp = self.blogTextContentPattern.findall(self.oneBlogAllContent)[0]
        else:
            print "get blog error!!"
            return None

        ##print "textContentTamp: %s" % self.textContentTamp.encode('utf-8')
        super(analisysBlogPage, self).getTextContent(self.oneBlogAllContentDict, self.textContentTamp)
        ##print "blog_content :%s" % self.oneBlogAllContentDict['content']['text_content'].encode('utf-8')
        #get blog address
        self.blogAddressPattern = re.compile("""(?<=\[位置\]<a href=).*?(?=</a>)""")
        if self.blogAddressPattern.findall(self.oneBlogAllContent):
            self.patternContTamp = self.blogAddressPattern.findall(self.oneBlogAllContent)[0]
            self.blogAddressPattern = re.compile("""(?<=">).*""")
            if self.blogAddressPattern.findall(self.patternContTamp):
                self.oneBlogAllContentDict['blog_address'] = self.blogAddressPattern.findall(self.patternContTamp)[0]
            self.blogAddressPattern = re.compile("""(?<=<a href=).*?(?=>显示地图</a>)""")
            if self.blogAddressPattern.findall(self.oneBlogAllContent):
                self.patternContTamp = self.blogAddressPattern.findall(self.oneBlogAllContent)[0]
                self.blogAddressPattern = re.compile("""(?<=center=).*?(?=&amp)""")
                if self.blogAddressPattern.findall(self.patternContTamp):
                    self.patternContTamp = self.blogAddressPattern.findall(self.patternContTamp)[0]
                    self.oneBlogAllContentDict['blog_address'] = self.oneBlogAllContentDict['blog_address'] + self.patternContTamp
            ##print "blog_address :%s" % self.oneBlogAllContentDict['blog_address']
        else:
            self.oneBlogAllContentDict['blog_address'] = 'no address'
            ##print 'no address'
        #get blog time and device

        self.blogTimeDevicePattern = re.compile("""(?<=<span class="ct">).*?(?=</span>)""")

        self.oneBlogAllContentDict['time'] ,self.oneBlogAllContentDict['device'] = super(analisysBlogPage, self).getTimeDevice(self.oneBlogAllContentDict, self.oneBlogAllContent, self.blogTimeDevicePattern)
        ##print "blog_device :%s" % self.oneBlogAllContentDict['device'].encode('utf-8')
        ##print "blog_time :%s" % self.oneBlogAllContentDict['time'].encode('utf-8')
        #get blog attitude
        self.blogAttitudePattern = re.compile("""<a href="http://weibo.cn/attitude.*?赞\[[0-9]+(?=\]</a>)""")
        if self.blogAttitudePattern.findall(self.oneBlogAllContent):
            self.patternContTamp = self.blogAttitudePattern.findall(self.oneBlogAllContent)[0]
                    #print self.patternContTamp
        self.blogAttitudePattern = re.compile("""(?<=赞\[).*""")
        if self.blogAttitudePattern.findall(self.patternContTamp):
            self.oneBlogAllContentDict['blog_attitude'] = self.blogAttitudePattern.findall(self.patternContTamp)[0]
        ##print "blog_attitude :%s" % self.oneBlogAllContentDict['blog_attitude']
        #get repost url
        self.blogRepostUrlPattern = re.compile("""<a href="http://weibo.cn/repost.*?转发\[[0-9]+(?=\]</a>)""")
        if self.blogRepostUrlPattern.findall(self.oneBlogAllContent):
            self.patternContTamp = self.blogRepostUrlPattern.findall(self.oneBlogAllContent)[0]
        self.blogRepostUrlPattern = re.compile("""(?<=<a href=").*?(?=;|&|"|\?^u)""")
        if self.blogRepostUrlPattern.findall(self.patternContTamp):
            self.repost_url['repost_url'] = self.blogRepostUrlPattern.findall(self.patternContTamp)[0]
        ##print "repost_url :%s" % self.oneBlogAllContentDict['repost_url']
        #get comment url

        self.blogCommentUrlPattern = re.compile("""<a href="http://weibo.cn/comment.*?评论\[[0-9]+(?=\]</a>)""")
        if self.blogCommentUrlPattern.findall(self.oneBlogAllContent):
            self.patternContTamp = self.blogCommentUrlPattern.findall(self.oneBlogAllContent)[0]
        self.blogCommentUrlPattern = re.compile("""(?<=<a href=").*?(?=;|&|"|\?^u)""")
        self.comment_url['comment_url'] = self.blogCommentUrlPattern.findall(self.patternContTamp)[0]
        # print "comment_url :%s" % self.comment_url['comment_url']
        #get comment
        self.CommentsContentDict = []
        self.CommentsContentDict = analisysAttributePage.getBlogAttributes(self, self.sinaNetHeader, self.comment_url['comment_url'], 1)
        #get repost
        self.RepostsContentDict = [1]
        self.RepostsContentDict = analisysAttributePage.getBlogAttributes(self, self.sinaNetHeader, self.repost_url['repost_url'], 2)
        ##print self.RepostsContentDict
        self.blog_unit['blog'] = self.oneBlogAllContentDict
        self.blog_unit['_id'] = self.blog_unit['blog']['blog_id']
        self.blog_unit['repost'] = self.RepostsContentDict
        self.blog_unit['comment'] = self.CommentsContentDict
        self.blog_unit['user_ID'] = self.user_id
        ##print self.RepostsContentDict
        ##print self.CommentsContentDict

        ##del self.blog_unit['_id']
        return self.blog_unit

if __name__=="__main__":
    CONDITION = threading.Condition()
    visited = get_visited("/home/john/visited/blogvisited.txt")
    queue = get_queue("/home/john/queue/blogqueue.txt")
    userlistdir1 = '/home/john/userpool/userpool1.txt'
    userlistdir2 = '/home/john/userpool/userpool2.txt'
    userlistdir3 = '/home/john/userpool/userpool3.txt'

    thread1 = analisysBlogPage(userlistdir1,"thread1",1)
    thread2 = analisysBlogPage(userlistdir2,"thread2",2)
    thread3 = analisysBlogPage(userlistdir3,"thread3",3)
    thread1.start()
    thread2.start()
    # thread3.start()
