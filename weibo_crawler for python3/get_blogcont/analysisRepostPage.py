#!/usr/bin/python
#-*- coding: UTF-8 -*-

#filename: analysisRepostPage.py
#description: analisys repost page , and get repost attributes and store in oneRepostContentDict
#author: warrior  ,mail: oowarrioroo@163.com
#data: 2016-1-3
#log:

from selenium import webdriver
import urllib
import urllib2
import cookielib
import sys
import os
import time
import re
from login import *



#********************-----------------********************#

#********************-----------------********************#
class analisysRepostPage(object):
    '''
        set functions for analisys repost page , and get repost attributes and store in oneRepostContentDict
        like :
    '''

    #-----------------********************-----------------#
    def __init__(self):
        self.oneRepostContentDict = {
            "repost_id": "",
            "repost_user_id": "",
            "repost_content": "",
            "repost_device": "",
            "repost_time": "",
            "repost_attitude": ""
        }
        self.countNum = ''
        #getBlogReposts(self, sinaNetHeader, blogRepostUrl)
        self.sinaNetHeader = ''
        self.blogRepostUrl = ''
        self.req = ''
        self.response = ''
        self.blogRepostPage = ''
        self.blogRepostPageFD = ''
        self.repostPageNumber = ''
        self.currentBlogRepostPageUrl = ''
        #getOnePageReposts(self, repostDir)
        self.repostDir = ''
        self.repostPageText = ''
        self.oneRepostAllContentPattern = ''
        self.oneRepostAllContent = ''
        



    #-----------------********************-----------------#
    def getBlogReposts(self, sinaNetHeader, blogRepostUrl):
        '''
            description:
                get all reposts of one blog
            input:
                none
            output:
                none
        '''
        self.sinaNetHeader = sinaNetHeader
        self.blogRepostUrl = blogRepostUrl

        self.req = urllib2.Request(self.blogRepostUrl,headers=self.sinaNetHeader)
        self.response = urllib2.urlopen(self.req)
        self.blogRepostPage = self.response.read() #get_data(self.blogCurrentPageUrl, self.sinaNetHeader)
        self.blogRepostPageFD = open('./get_blogcont/currentBlogRepostPage.html', 'w')
        self.blogRepostPageFD.write(self.blogRepostPage)
        self.blogRepostPageFD.close()

        self.repostPageNumber = self.getPageNumber('./get_blogcont/currentBlogRepostPage.html')
        print "repost page number: %d" % self.repostPageNumber

        if self.repostPageNumber > 0 :
            for self.countNum in range(self.repostPageNumber):
                self.countNum = self.countNum+1
                #print "#########################################################%d" % self.countNum
                self.currentBlogRepostPageUrl = self.blogRepostUrl + "&page=%d" % self.countNum
                #print self.currentBlogRepostPageUrl
                self.req = urllib2.Request(self.currentBlogRepostPageUrl,headers=self.sinaNetHeader)
                self.response = urllib2.urlopen(self.req)
                self.blogRepostPage = self.response.read() #get_data(self.blogCurrentPageUrl, self.sinaNetHeader)
                self.blogRepostPageFD = open('./get_blogcont/currentBlogRepostPage.html', 'w')
                self.blogRepostPageFD.write(self.blogRepostPage)
                self.blogRepostPageFD.close()
                self.getOnePageReposts('./get_blogcont/currentBlogRepostPage.html')
        else:
            self.getOnePageReposts('./get_blogcont/currentBlogRepostPage.html')


    #-----------------********************-----------------#
    def getOnePageReposts(self, repostDir):
        '''
            description:
                get all reposts from the loaded repost page repostDir:"./get_blogcont/currentBlogRepostPage.html"
            input:
                repostDir:
                    repost page file dir
            output:
                none
        '''
        self.repostDir = repostDir
        self.blogRepostPageFD = open(self.repostDir, 'r')
        self.repostPageText = self.blogRepostPageFD.read()
        self.oneRepostAllContentPattern = re.compile("""(?<=<div class="c">)<a href="/u/.*?(?=</span></div>)""")
        if self.oneRepostAllContentPattern.findall(self.repostPageText) :
            for self.oneRepostAllContent in self.oneRepostAllContentPattern.findall(self.repostPageText):
                self.getOneRepost(self.oneRepostAllContent)
                ##print self.oneRepostAllContent
        else:
            print "no repost!!"
        self.blogRepostPageFD.close()
