#!/usr/bin/python
#-*- coding: UTF-8 -*-

#filename: analysisBlogPage.py
#description: analisys blog page , and get blog attributes and others in blogUnit.blog_unit
#author: warrior  ,mail: oowarrioroo@163.com
#data: 2016-1-1
#log:


from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.by import By
import urllib
import urllib2
import cookielib
import sys
import os
import time
import re
from createMultiCookies.login import *
from analysisAttributesPage import *
from con2mongo.blogUnit import *
from con2mongo.optOnMongo import *
from createMultiCookies.getRandomCookie import *
#import pdb
#sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

#********************-----------------********************#

#********************-----------------********************#
class analisysBlogPage(analisysAttributePage, blogUnit, getRandomCookie):
    '''
        set functions for analisys blog page , and get blog attributes and others in blogUnit.blog_unit
        like :
    '''
    #-----------------********************-----------------#
    def __init__(self):
        analisysAttributePage.__init__(self)
        blogUnit.__init__(self)
        getRandomCookie.__init__(self)
        ##optOnMongo.__init__(self)
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
        self.repost_url = {"repost_url": ""}
        self.comment_url = {"comment_url": ""}
        self.countNum = ''
        self.optOnMongoInstance = optOnMongo()
        self.getBlogsCount = 0
        self.visitPageCount = 0
        self.userIDList = list()
        #startBlogAnalysisWork(self, user_id_list)
        self.user_id_list = ''
        self.sinaNetHeader = ''
        self.user_id = ''
        #visitIntoUserBlog(self, sinaNetHeader, user_id)
        self.blogCurrentPageUrl = ''
        self.req = ''
        self.response = ''
        self.blogPage = ''
        self.blogPageFD = ''
        self.blogPageNumber = ''
        #getOnePageBlogs(self, sinaNetHeader, blogPageUrl)
        self.blogText = ''
        self.blogIDListPattern = ''
        self.blogIDList = ''
        self.oneBlogAllContentPattern = ''
        self.oneBlogAllContent = ''
        #getOneBlog(self, oneBlogAllContent)
        self.blogIDPattern = ''
        self.blogTextContentPattern = ''
        self.patternContTamp = ''
        self.patternMentionTamp = ''
        self.blogAddressPattern = ''
        self.blogTimeDevicePattern = ''
        self.blogTimePattern = ''
        self.blogDevicePattern = ''
        self.blogAttitudePattern = ''
        self.blogRepostUrlPattern = ''
        self.blogCommentUrlPattern = ''



    #-----------------********************-----------------#
    def startBlogAnalysisWork(self, user_id_list, usernamePoolDir):
        '''
            description:
                start analisys work
            input:
                user_id_list: a list of user_id for who to be visited
            output:
                none
        '''

        self.user_id_list = user_id_list
        #self.sinaNetHeader = getHeaders(getLoginDriver('usename', 'password'))
        #create header pool
        self.sinaHeaderList = getRandomCookie.createCookiePool(self, \
                                usernamePoolDir \
                                )
        self.sinaNetHeader = getRandomCookie.getOneRandomCookie(self,  self.sinaHeaderList)

        self.db_uri = "mongodb://labUser:aaaaaa@localhost:27017/?authSource=lab"
        self.db_name = "lab"
        self.optOnMongoInstance.connect2Mongo(self.db_uri, self.db_name)
        print self.optOnMongoInstance.db
        for self.user_id in self.user_id_list:
            self.visitIntoUserBlog(self.sinaNetHeader, \
                                    self.user_id, \
                                    self.optOnMongoInstance)
        print 'get blog number: %d' % self.getBlogsCount
        print 'visited page number: %d' % self.visitPageCount


    #-----------------********************-----------------#
    def visitIntoUserBlog(self, sinaNetHeader, user_id, optOnMongoInstance):
        '''
            description:
                visit into main blog page  ,and get all content that is related to blog
            input:
                sinaNetHeader:
                    header for using to skip verification when visiting sina web server
                user_id:
                    user_id for who to be visited
                optOnMongoInstance:
                    mongodb db instance
            output:
                none
        '''
        self.optOnMongoInstance = optOnMongoInstance
        self.blogInitPageUrl = "http://weibo.cn/" + user_id + "/profile"
        self.sinaNetHeader = sinaNetHeader
        #print self.sinaNetHeader
        ##print self.blogInitPageUrl
        self.countNum = 0
        self.req = urllib2.Request(self.blogInitPageUrl,headers=self.sinaNetHeader)
        self.response = urllib2.urlopen(self.req)
        self.blogPage = self.response.read() #get_data(self.blogCurrentPageUrl, self.sinaNetHeader)

        self.blogPageNumber = self.getPageNumber(self.blogPage)
        ##print "blog page number: %d" % self.blogPageNumber
        ##self.getOnePageBlogs('./get_blogcont/currentBlogPage.html')
        if self.blogPageNumber > 0:
            for self.countNum in range(self.blogPageNumber): #range(2):#
                self.countNum = self.countNum+1
                self.blogCurrentPageUrl = self.blogInitPageUrl + "?page=" + "%d" % self.countNum
                print self.blogCurrentPageUrl
                self.req = urllib2.Request(self.blogCurrentPageUrl,headers=self.sinaNetHeader)
                self.response = urllib2.urlopen(self.req)
                self.blogPage = self.response.read() #get_data(self.blogCurrentPageUrl, self.sinaNetHeader)
                self.getOnePageBlogs(self.blogPage, self.optOnMongoInstance)
        else:
            self.blogCurrentPageUrl = self.blogInitPageUrl
            self.req = urllib2.Request(self.blogCurrentPageUrl,headers=self.sinaNetHeader)
            self.response = urllib2.urlopen(self.req)
            self.blogPage = self.response.read() #get_data(self.blogCurrentPageUrl, self.sinaNetHeader)
            self.getOnePageBlogs(self.blogPage, self.optOnMongoInstance)



    #-----------------********************-----------------#
    def getOnePageBlogs(self, blogPage, optOnMongoInstance):
        '''
            description:
                visit into blog page  ,and get blog all attributes
            input:
                blogPage:
                    blog web page
                optOnMongoInstance:
                    mongodb db instance
            output:
                none
        '''
        self.optOnMongoInstance = optOnMongoInstance
        self.blogText = blogPage
        self.visitPageCount += 1
        #selecte a random header every 4 pages
        if self.visitPageCount%4 == 0:
            self.sinaNetHeader = getRandomCookie.getOneRandomCookie(self, self.sinaHeaderList)
            time.sleep(random.randint(2,10))
        ##self.db_uri = "mongodb://labUser:aaaaaa@localhost:27017/?authSource=lab"
        ##self.db_name = "lab"
        ##self.optOnMongoInstance.connect2Mongo(self.db_uri, self.db_name)
        ##get all blog
        ##get repost blog
        ##get user post blog
        self.oneBlogAllContentPattern = re.compile("""(?<=<div class="c" id=)"M_\w+"><div><span class="ctt">.*?(?=</div></div>)""")
        if self.oneBlogAllContentPattern.findall(self.blogText):
            for self.oneBlogAllContent in self.oneBlogAllContentPattern.findall(self.blogText):
                self.blog_unit = self.getOneBlog(self.oneBlogAllContent, self.optOnMongoInstance)
                ##self.optOnMongoInstance.insertBlog2Mongo(self.optOnMongoInstance.db, self.getOneBlog(self.oneBlogAllContent))
                ##print self.blog_unit
                self.optOnMongoInstance.insertBlog2Mongo(self.optOnMongoInstance.db, self.blog_unit)
                self.getBlogsCount = self.getBlogsCount + 1
        else:
            print "no blog"
        ##self.blogPageFD.close()
        ##get all blogID
        ##self.blogIDListPattern = re.compile("""(?<=<div class="c" id=")M_\w+(?="><div>)""")
        ##get repost blogID
        ##self.blogIDListPattern = re.compile("""(?<=<div class="c" id=")M_\w+(?="><div><span class="cmt">)""")
        ##get user post blogID
        ##self.blogIDListPattern = re.compile("""(?<=<div class="c" id=")M_\w+(?="><div><span class="ctt">)""")
        ##self.blogIDList = self.blogIDListPattern.findall(self.blogText)
        ##print self.blogIDList


    #-----------------********************-----------------#
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
        self.patternContTamp = self.blogAttitudePattern.findall(self.oneBlogAllContent)[0]
                    #print self.patternContTamp
        self.blogAttitudePattern = re.compile("""(?<=赞\[).*""")
        self.oneBlogAllContentDict['blog_attitude'] = self.blogAttitudePattern.findall(self.patternContTamp)[0]
        ##print "blog_attitude :%s" % self.oneBlogAllContentDict['blog_attitude']
        #get repost url
        self.blogRepostUrlPattern = re.compile("""<a href="http://weibo.cn/repost.*?转发\[[0-9]+(?=\]</a>)""")
        self.patternContTamp = self.blogRepostUrlPattern.findall(self.oneBlogAllContent)[0]
        self.blogRepostUrlPattern = re.compile("""(?<=<a href=").*?(?=;|&|"|\?^u)""")
        self.repost_url['repost_url'] = self.blogRepostUrlPattern.findall(self.patternContTamp)[0]
        ##print "repost_url :%s" % self.oneBlogAllContentDict['repost_url']
        #get comment url
        self.blogCommentUrlPattern = re.compile("""<a href="http://weibo.cn/comment.*?评论\[[0-9]+(?=\]</a>)""")
        self.patternContTamp = self.blogCommentUrlPattern.findall(self.oneBlogAllContent)[0]
        self.blogCommentUrlPattern = re.compile("""(?<=<a href=").*?(?=;|&|"|\?^u)""")
        self.comment_url['comment_url'] = self.blogCommentUrlPattern.findall(self.patternContTamp)[0]
        ##print "comment_url :%s" % self.oneBlogAllContentDict['comment_url']
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
