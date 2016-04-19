#!/usr/bin/python
#-*- coding: UTF-8 -*-

#filename: getRandomCookie.py
#description: get one rangdom cookie for crawler
#author: warrior  ,mail: oowarrioroo@163.com
#data: 2016-1-16
#log:


"""
    get one rangdom cookie for crawler
"""


import re
from login import *
import random
import urllib2
import cookielib


#********************-----------------********************#

#********************-----------------********************#
class getRandomCookie():
    """
        get one rangdom cookie for crawler

    """
    def __init__(self):
        self.driverList = []
        self.headerList = []
        self.countNum = 0


    #-----------------********************-----------------#
    def createCookiePool(self, usernamePoolDir):
        '''
            description:
                create one cookie pool
            input:
                usernamePoolDir: username pool
            output:
                0:error
                a cookie pool
        '''
        #line example: 'username','password'
        self.usernameRE = re.compile('(?<=\').*?(?=\',)')
        self.passwordRE = re.compile('(?<=,\').*?(?=\')')
        try:
            self.usernamePoolFD = open(usernamePoolDir, 'r')
        except:
            print 'open %s error' % usernamePoolDir

        self.oneLineData = self.usernamePoolFD.readline()
        self.countNum = 0
        
        while self.oneLineData:
            print self.oneLineData
            if self.usernameRE.findall(self.oneLineData):
                self.username = self.usernameRE.findall(self.oneLineData)[0]
            else:
                print 'username error at %d line' % self.countNum
                return 0
            if self.passwordRE.findall(self.oneLineData):
                self.password = self.passwordRE.findall(self.oneLineData)[0]
            else:
                print 'password error at %d line' % self.countNum
                return 0
            self.driverList.append(getLoginDriver(self.username,self.password))
            self.headerList.append(getHeaders(self.driverList[self.countNum]))
            self.countNum += 1
            self.oneLineData = self.usernamePoolFD.readline()
        ##print '########################################################################'
        ##print self.driverList
        ##print '########################################################################'
        ##print self.headerList
        return self.headerList

    #-----------------********************-----------------#
    def getOneRandomCookie(self,  headerList):
        '''
            description:
                get one random cookie for crawler
            input:
                usernamePoolDir: username pool
            output:
                0:error
                a random cookie
        '''
        self.headerList = headerList##createCookiePool(usernamePoolDir)
        self.listIndex = random.randint(0,len(self.headerList)-1)
        self.currentHeader = self.headerList[self.listIndex]
        return self.currentHeader



    #-----------------********************-----------------#
    def get4PagesOnce(self, userTempID, usernamePoolDir):
        '''
            description:
                get 5 pages at once test
            input:
                userTempID: a temple user id
            output:
                0:error
        '''

        self.headerList = self.getOneCookie(usernamePoolDir)
        self.blogInitPageUrl = "http://weibo.cn/" + userTempID + "/profile"
        self.allPageNumber = 0
        self.countNum = 0
        self.currentHeader = self.getOneRandomCookie(self.headerList)
        self.running = True

        while self.running :
            ##print self.allPageNumber
            if self.countNum > 3:
                self.countNum = 0
                self.currentHeader = self.getOneRandomCookie(self.headerList)
            ##print self.currentHeader
            self.req = urllib2.Request(self.blogInitPageUrl,headers=self.currentHeader)
            self.response = urllib2.urlopen(self.req)
            self.blogPage = self.response.read()
            self.countNum += 1
            self.allPageNumber = self.allPageNumber + 1
            print self.allPageNumber*4
            if self.allPageNumber > 1000 :
                self.running = False
        else:
            print 'get blog over!!'
