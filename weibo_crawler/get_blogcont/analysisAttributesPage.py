#!/usr/bin/python
#-*- coding: UTF-8 -*-

#filename: analysisCommentPage.py
#description: analisys comment page , and get comment attributes and store in oneCommentContentDict
#author: warrior  ,mail: oowarrioroo@163.com
#data: 2016-1-3
#log:
import re
import os
import sys
import time
import urllib
import urllib2
import datetime
import cookielib
from selenium import webdriver
from createMultiCookies.login import *



#********************-----------------********************#

#********************-----------------********************#
class analisysAttributePage(object):
    '''
        set functions for analisys comment page , and get comment attributes and store in oneCommentContentDict
        like :
    '''

    #-----------------********************-----------------#
    def __init__(self):
        self.oneCommentContentDict = {
            "comment_id": "",
            "comment_user_id": "",
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
            "device": "",
            "time": "",
            "comment_attitude": ""
        }
        self.oneRepostContentDict = {
            "repost_id": "",
            "repost_user_id": "",
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
            "device": "",
            "time": "",
            "repost_attitude": ""
        }
        self.repostsMainDict = []
        self.commentsMainDict = []
        self.repostsSubDict = []
        self.commentsSubDict = []
        self.RepostsContentDict = []
        self.CommentsContentDict = []
        self.subDict = []
        self.mainDict = []
        self.countNum = ''
        self.ISOTIMEFORMAT= '%Y-%m-%d %X'
        #getPageNumber(self, fileDir)
        self.fileDir = ''
        self.PageFD = ''
        self.PageText = ''
        self.getPageNumber_RE = ''
        self.getPageNumberPattern = ''
        self.PageNumber = ''
        #getBlogComments(self, sinaNetHeader, blogCommentUrl)
        self.sinaNetHeader = ''
        self.blogCommentUrl = ''
        self.req = ''
        self.response = ''
        self.blogCommentPage = ''
        self.blogCommentPageFD = ''
        self.commentPageNumber = ''
        self.currentBlogCommentPageUrl = ''
        #getOnePageComments(self, commentDir)
        self.commentDir = ''
        self.commentPageText = ''
        self.oneCommentAllContentPattern = ''
        self.oneCommentAllContent = ''
        #getOneComment(self, oneCommentAllContent)
        self.commentIDPattern = ''
        self.commentContentPattern = ''
        self.patternContTamp = ''
        self.patternMentionTamp = ''
        self.countNum = ''
        self.commentUserIDPattern = ''
        self.commentAttitudePattern = ''
        self.commentTimeDevicePattern = ''
        self.commentDevicePattern = ''
        self.commentTimePattern = ''
        #getOneRepost(self, oneRepostAllContent)
        self.repostUserIDPattern = ''
        self.repostContentPattern = ''
        self.patternContTamp = ''
        self.patternMentionTamp = ''
        self.countNum = ''
        self.repostAttitudePattern = ''
        self.repostTimeDevicePattern = ''
        self.repostDevicePattern = ''
        self.repostTimePattern = ''


    #-----------------********************-----------------#
    def getPageNumber(self, webPage):
        '''
            description:
                 get web page number
            input:
                webPage:
                    content of webPage
            output:
                none
        '''

        #***********get page number***********#
        self.PageText = webPage
        self.getPageNumber_RE = r"""<input +name="mp" +type="hidden" +value="[0-9]+" +/>"""
        self.getPageNumberPattern = re.compile(self.getPageNumber_RE)
        if self.getPageNumberPattern.findall(self.PageText):
            self.PageNumber = int(re.findall('[0-9]+',self.getPageNumberPattern.findall(self.PageText)[0])[0])
            return self.PageNumber
        else:
            return 1

    #-----------------********************-----------------#
    def getBlogAttributes(self, sinaNetHeader, blogAttributeUrl, statueFlag=0):
        '''
            description:
                get all attributes of one blog
            input:
                sinaNetHeader:
                    header for using to skip verification when visiting sina web server
                blogAttributeUrl:
                    url to be interview comment_url or repost_url
                statueFlag:
                    1 : for comment
                    2 : for repost
                    others : error
            output:
                self.commentsMainDict/self.repostsMainDict/None
        '''
        self.sinaNetHeader = sinaNetHeader
        self.blogAttributeUrl = blogAttributeUrl
        self.statueFlag = statueFlag
        self.commentsMainDict = []
        self.repostsMainDict = []

        self.req = urllib2.Request(self.blogAttributeUrl,headers=self.sinaNetHeader)
        self.response = urllib2.urlopen(self.req)
        self.blogAttributePage = self.response.read() #get_data(self.blogCurrentPageUrl, self.sinaNetHeader)

        self.attributePageNumber = self.getPageNumber(self.blogAttributePage)
        if self.statueFlag==1:

            print "comment page number: %d" % self.attributePageNumber
        elif self.statueFlag==2:

            print "repost page number: %d" % self.attributePageNumber
        else :
            print "please set statueFlag at correct value '1:comment' and '2:repost'"
            return None
        if self.attributePageNumber > 1 :
            if self.attributePageNumber > 10:
                self.attributePageNumber = 10
            for self.countNum in range(self.attributePageNumber): #range(2):#
                self.countNum = self.countNum + 1
                self.currentBlogAttributePageUrl = self.blogAttributeUrl + "&page=%d" % self.countNum
                self.req = urllib2.Request(self.currentBlogAttributePageUrl,headers=self.sinaNetHeader)
                self.response = urllib2.urlopen(self.req)
                self.blogAttributePage = self.response.read()
                #get_data(self.blogCurrentPageUrl, self.sinaNetHeader)
                if self.statueFlag==1: #for comment
                    self.oneAttributeAllContentPattern = re.compile("""(?<=<div class="c" id=)"C_\w+">.*?(?=</span></div>)""")
                    self.commentsSubDict = self.getOnePageAttributes(self.blogAttributePage, \
                                            self.oneAttributeAllContentPattern, \
                                            1)
                    self.getSubDict2MainDict(self.commentsSubDict, self.commentsMainDict)
                elif self.statueFlag==2: #for repost
                    ##print self.currentBlogAttributePageUrl
                    self.oneAttributeAllContentPattern = re.compile("""(?<=<div class="c">)<a href="/u/.*?(?=</span></div>)""")
                    self.repostsSubDict = self.getOnePageAttributes(self.blogAttributePage, \
                                            self.oneAttributeAllContentPattern, \
                                            2)

                    self.repostsMainDict = self.getSubDict2MainDict(self.repostsSubDict, self.repostsMainDict)
                else:
                    print "please input statueFlag 1:for commont 2:for repost"
                    return None
        else:
            if self.statueFlag==1: #for comment
                self.oneAttributeAllContentPattern = re.compile("""(?<=<div class="c" id=)"C_\w+">.*?(?=</span></div>)""")
                self.commentsSubDict = self.getOnePageAttributes(self.blogAttributePage, \
                                        self.oneAttributeAllContentPattern, \
                                        1)
                ##self.commentsMainDict = self.commentsMainDict
                self.getSubDict2MainDict(self.commentsSubDict, self.commentsMainDict)
            elif self.statueFlag==2: #for repost
                ##print self.blogAttributeUrl
                self.oneAttributeAllContentPattern = re.compile("""(?<=<div class="c">)<a href="/u/.*?(?=</span></div>)""")
                self.repostsSubDict = self.getOnePageAttributes(self.blogAttributePage, \
                                        self.oneAttributeAllContentPattern, \
                                        2)
                ##self.repostsMainDict = self.repostsSubDict
                self.repostsMainDict = self.getSubDict2MainDict(self.repostsSubDict, self.repostsMainDict)
            else:
                print "please input statueFlag 1:for commont 2:for repost"
                return None
        if self.statueFlag==1:
            ##self.CommentsContentDict = self.commentsMainDict
            return self.commentsMainDict
        elif self.statueFlag==2:
            ##print self.repostsMainDict
            ##print "这里还有呢！！"
            ##self.RepostsContentDict = self.repostsMainDict
            return self.repostsMainDict
        else:
            print "please input statueFlag 1:for commont 2:for repost"
            return None

    #-----------------********************-----------------#
    def getSubDict2MainDict(self, subDict, mainDict):
        '''
            description:
                assemble sub dictionary list into main dictionary list
            input:
                subDict:
                    sub dictionary list
                mainDict:
                    main dictionary list
            output:
                self.mainDict
        '''
        self.subDict = subDict
        self.mainDict = mainDict
        self.oneItem = {}
        if self.subDict:
            for self.oneItem in self.subDict:
                oneDictTamp = {}
                for keyTamp,valueTamp in self.oneItem.items():
                    if keyTamp == "content":
                        oneDictTamp["content"] = {}
                        for keyTamp2,valueTamp2 in valueTamp.items():
                            oneDictTamp["content"][keyTamp2] = valueTamp2
                    else:
                        oneDictTamp[keyTamp] = valueTamp
                self.mainDict.append(oneDictTamp)
        return self.mainDict

    #-----------------********************-----------------#
    def getOnePageAttributes(self, blogAttributePage, oneAttributeAllContentPattern, statueFlag=0):
        '''
            description:
                get all attributes from the loaded attribute page attributeDir:"./get_blogcont/currentBlogAttributePage.html"
            input:
                blogAttributePage:
                    attribute web page
                oneAttributeAllContentPattern:
                    re pattern for attribute of blog comment/repost
                statueFlag:
                    1:for comment
                    2:for repost
            output:
                self.repostsSubDic/self.commentsSubDict/None
        '''

        ##self.attributeDir = attributeDir
        self.oneAttributeAllContentPattern = oneAttributeAllContentPattern

        self.attributePageText = blogAttributePage
        if self.oneAttributeAllContentPattern.findall(self.attributePageText) :
            if self.statueFlag==1: #for comment
                self.commentsSubDict = []
                for self.oneAttributeAllContent in self.oneAttributeAllContentPattern.findall(self.attributePageText):
                    oneDictTamp = {}
                    for keyTamp,valueTamp in self.getOneComment(self.oneAttributeAllContent).items():
                        if keyTamp == "content":
                            oneDictTamp["content"] = {}
                            for keyTamp2,valueTamp2 in valueTamp.items():
                                oneDictTamp["content"][keyTamp2] = valueTamp2
                        else:
                            oneDictTamp[keyTamp] = valueTamp
                    ##print oneDictTamp
                    ##print '########################################################'
                    self.commentsSubDict.append(oneDictTamp)
                ##print self.commentsSubDict
                ##print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
                return self.commentsSubDict
            elif self.statueFlag==2: #for repost
                self.repostsSubDict = []
                for self.oneAttributeAllContent in self.oneAttributeAllContentPattern.findall(self.attributePageText):
                    oneDictTamp = {}
                    for keyTamp,valueTamp in self.getOneRepost(self.oneAttributeAllContent).items():
                        if keyTamp == "content":
                            oneDictTamp["content"] = {}
                            for keyTamp2,valueTamp2 in valueTamp.items():
                                oneDictTamp["content"][keyTamp2] = valueTamp2
                        else:
                            oneDictTamp[keyTamp] = valueTamp
                    self.repostsSubDict.append(oneDictTamp)
                return self.repostsSubDict
            else:
                print "please input statueFlag 1:for commont 2:for repost"
                return None
        else :
            if self.statueFlag==1:
                print "no comment !!"
                self.commentsSubDict = []
                return self.commentsSubDict
            elif self.statueFlag==2 :
                print "no repost lala!!"
                self.repostsSubDict = []
                return self.repostsSubDict
            else:
                print "please input statueFlag 1:for commont 2:for repost"
                return None

    #-----------------********************-----------------#
    def getOneComment(self, oneCommentAllContent):
        '''
            description:
                get one comment from the oneCommentAllContent
            input:
                oneCommentAllContent:
                    a string of comments content
            output:
                none
        '''
        self.oneCommentAllContent = oneCommentAllContent
        #get comment id
        self.commentIDPattern = re.compile("""(?<=")C_\w+?(?=">)""")
        self.oneCommentContentDict['comment_id'] = self.commentIDPattern.findall(self.oneCommentAllContent)[0]
        ##print "comment_id :%s" % self.oneCommentContentDict['comment_id']
        #get comment content
        self.commentContentPattern = re.compile("""(?<=<span class="ctt">).*?(?=</span>)""")
        if self.commentContentPattern.findall(self.oneCommentAllContent):
            self.textContentTamp = self.commentContentPattern.findall(self.oneCommentAllContent)[0]
        else:
            print "no comment content!!"
        self.getTextContent(self.oneCommentContentDict, self.textContentTamp)
        ##print "comment_content :%s" % self.oneCommentContentDict['content']['text_content'].encode('utf-8')
        #get comment user id
        self.commentUserIDPattern = re.compile("""(?<=&amp;fuid=)\d*?(?=&|;)""")
        self.oneCommentContentDict['comment_user_id'] = self.commentUserIDPattern.findall(self.oneCommentAllContent)[0]
        ##print "comment_user_id :%s" % self.oneCommentContentDict['comment_user_id']
        #get comment attitude
        self.commentAttitudePattern = re.compile("""(?<=>赞\[)\d*?(?=\]</a>)""")
        self.oneCommentContentDict['comment_attitude'] = self.commentAttitudePattern.findall(self.oneCommentAllContent)[0]
        ##print "comment_attitude :%s" % self.oneCommentContentDict['comment_attitude']
        #get comment device and time
        self.commentTimeDevicePattern = re.compile("""(?<=<span class="ct">).*""")
        self.oneCommentContentDict['time'], self.oneCommentContentDict['device'] = self.getTimeDevice(self.oneCommentContentDict, self.oneCommentAllContent, self.commentTimeDevicePattern)
        ##print "comment_time :%s" % self.oneCommentContentDict['time']
        ##print "comment_device :%s" % self.oneCommentContentDict['device']
        return self.oneCommentContentDict

    #-----------------********************-----------------#
    def getOneRepost(self, oneRepostAllContent):
        '''
            description:
                get one repost from the oneRepostAllContent
            input:
                oneRepostAllContent:
                    a string of reposts content
            output:
                none
        '''
        self.oneRepostAllContent = oneRepostAllContent
        ##get repost id
        ##self.repostIDPattern = re.compile("""(?<=")C_\w+?(?=">)""")
        ##self.oneRepostContentDict['repost_id'] = self.repostIDPattern.findall(self.oneRepostAllContent)[0]
        ##print "repost_id :%s" % self.oneRepostContentDict['repost_id']
        ##print self.oneRepostAllContent
        #get repost user id


        self.repostUserIDPattern = re.compile("""<a href="/.*?">""")
        if self.repostUserIDPattern.findall(self.oneRepostAllContent):

            self.textContentTamp = self.repostUserIDPattern.findall(self.oneRepostAllContent)[0]
            self.repostUserIDPattern = re.compile("""(?<=<a href="/u/).*?(?=">)""")
            if self.repostUserIDPattern.findall(self.textContentTamp):#example: <a href="/u/3107989303">阿呀龙</a>
                self.oneRepostContentDict['repost_user_id'] = self.repostUserIDPattern.findall(self.textContentTamp)[0]
            else:
                self.repostUserIDPattern = re.compile("""(?<=<a href="/).*?(?=">)""")
                self.oneRepostContentDict['repost_user_id'] = self.repostUserIDPattern.findall(self.textContentTamp)[0]
        else:
            print "error repost_user_id"
        ##print "repost_user_id :%s" % self.oneRepostContentDict['repost_user_id']
        #get repost content
        self.repostContentPattern = re.compile("""<a href="/.*"/>""") #<a href="/u/1704419855">我就是旺旺</a><img src="http://u1.sinaimg.cn/upload/2011/08/16/5547.gif" alt="达人"/><img src="http://u1.sinaimg.cn/upload/h5/img/hyzs/donate_btn_s.png" alt="M"/>:一记巴掌&nbsp;<span
        if self.repostContentPattern.findall(self.oneRepostAllContent):
            ##print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
            ##print self.repostContentPattern.findall(self.oneRepostAllContent)[0].encode('utf-8')
            self.repostContentPattern = re.compile("""(?<="/>):.*?(?=<span)""") #"/><img src="http://u1.sinaimg.cn/upload/h5/img/hyzs/donate_btn_s.png" alt="M"/>:一记巴掌&nbsp;<span
            if self.repostContentPattern.findall(self.oneRepostAllContent):
                self.textContentTamp = self.repostContentPattern.findall(self.oneRepostAllContent)[0]
            else:
                print "error repost_content2"
        else:
            self.repostContentPattern = re.compile("""(?<=</a>).*?(?=<span)""")
            if self.repostContentPattern.findall(self.oneRepostAllContent):
                self.textContentTamp = self.repostContentPattern.findall(self.oneRepostAllContent)[0]
            else:
                print "error repost_content2"
        self.getTextContent(self.oneRepostContentDict, self.textContentTamp)
        ##print "repost_content :%s" % self.oneRepostContentDict['content']['text_content'].encode('utf-8')
        #get repost attitude
        self.repostAttitudePattern = re.compile("""(?<=>赞\[)\d*?(?=\]</a>)""")
        self.oneRepostContentDict['repost_attitude'] = self.repostAttitudePattern.findall(self.oneRepostAllContent)[0]
        ##print "repost_attitude :%s" % self.oneRepostContentDict['repost_attitude']
        #get repost device and time
        self.repostTimeDevicePattern = re.compile("""(?<=<span class="ct">&nbsp;).*""")
        self.oneRepostContentDict['time'], self.oneRepostContentDict['device'] = self.getTimeDevice(self.oneRepostContentDict, self.oneRepostAllContent, self.repostTimeDevicePattern)
        ##print "repost_time :%s" % self.oneRepostContentDict['time']
        ##print "repost_device :%s" % self.oneRepostContentDict['device']
        return self.oneRepostContentDict



    #-----------------********************-----------------#
    def getTimeDevice(self, oneContentDict, oneAllContent, oneTimeDevicePattern):
        '''
            description:
                get one time and device from the oneTimeDeviceContent
            input:
                oneContentDict:
                    a dictionary data form for blog/comment/repost
                oneAllContent:
                    all content of blog/comment/repost
                oneTimeDevicePattern:
                    re pattern for blog/comment/repost time and device
            output:
                self.oneContentDict['time'], self.oneContentDict['device']
        '''
        self.oneTimeDevicePattern = oneTimeDevicePattern
        self.oneAllContent = oneAllContent
        self.oneContentDict = oneContentDict
        if self.oneTimeDevicePattern.findall(self.oneAllContent):
            self.patternContTamp = self.oneTimeDevicePattern.findall(self.oneAllContent)[0]
        ##print self.patternContTamp
        self.oneTimePattern = re.compile(""".*?(?=&nbsp;)""")
        if self.oneTimePattern.findall(self.patternContTamp):
            self.oneContentDict['time'] = self.oneTimePattern.findall(self.patternContTamp)[0]
            self.oneContentDict['time'] = self.normalizeTimeFrom(self.oneContentDict['time'])

        ##print self.oneContentDict['time']

#        self.oneContentDict['time'] = self.normalizeTimeFrom(self.oneContentDict['time'])
        ##print self.oneContentDict['time']
        ##print "time :%s" % oneContentDict['time'].encode('utf-8')
        self.oneDevicePattern = re.compile("""(?<=&nbsp;来自).*""")
        if self.oneDevicePattern.findall(self.patternContTamp): #whether have device
            self.oneDevicePattern = re.compile("""(?<=&nbsp;来自<a href=").*""")
            if self.oneDevicePattern.findall(self.patternContTamp) : #whether use xxx客户端,,这个因解析内容比较特殊
                self.oneDevicePattern = re.compile("""(?<=">).*?(?=</a>)""")
                self.oneContentDict['device'] = self.oneDevicePattern.findall(self.patternContTamp)[0]
            else :
                self.oneDevicePattern = re.compile("""(?<=&nbsp;来自).*""")
                self.oneContentDict['device'] = self.oneDevicePattern.findall(self.patternContTamp)[0]
        else:
            self.oneContentDict['device'] = 'no device'

        return self.oneContentDict['time'], self.oneContentDict['device']
        ##print "device :%s" % oneContentDict['device'].encode('utf-8')


    #-----------------********************-----------------#
    def normalizeTimeFrom(self, initTimeForm):
        '''
            description:
                normalize other kinds of time into xxxx.xx.xx xx.xx.xx
            input:
                initTimeForm:
                    any other kinds of time, like : 刚刚，1-59分钟前，1-23小时前，昨天xx.xx
            output:
                normalizeTime: xxxx.xx.xx xx.xx.xx
                0 : error
        '''
        #self.TimeFormFlag = TimeFormFlag
        self.initTimeForm = initTimeForm
        self.oneTimePattern = re.compile("""刚刚""")
        if self.oneTimePattern.findall(self.initTimeForm):
            self.TimeFormFlag = 1
        self.oneTimePattern = re.compile(""".*?(?=分钟前)""")
        if self.oneTimePattern.findall(self.initTimeForm):
            self.TimeFormFlag = 2
            self.initTimeForm = self.oneTimePattern.findall(self.initTimeForm)[0]
        self.oneTimePattern = re.compile(""".*?(?=小时前)""")
        if self.oneTimePattern.findall(self.initTimeForm):
            self.TimeFormFlag = 3
            self.initTimeForm = self.oneTimePattern.findall(self.initTimeForm)[0]
        self.oneTimePattern = re.compile("""(?<=今天).*""")
        if self.oneTimePattern.findall(self.initTimeForm):
            self.TimeFormFlag = 6
            self.initTimeForm = self.oneTimePattern.findall(self.initTimeForm)[0]
        self.oneTimePattern = re.compile("""(?<=昨天).*""")
        if self.oneTimePattern.findall(self.initTimeForm):
            self.TimeFormFlag = 4
            self.oneday = datetime.timedelta(days=1)
            self.initTimeForm = self.oneTimePattern.findall(self.initTimeForm)[0]
        self.oneTimePattern = re.compile(""".*日.*""")
        if self.oneTimePattern.findall(self.initTimeForm):
            self.TimeFormFlag = 5
            self.oneday = datetime.timedelta(days=1)
            self.yearsString = time.strftime( '%Y', time.localtime( time.time() ))
            self.oneTimePattern = re.compile(""".*(?=月)""")
            self.monthsString = self.oneTimePattern.findall(self.initTimeForm)[0]
            self.oneTimePattern = re.compile("""(?<=月).*(?=日)""")
            self.daysString = self.oneTimePattern.findall(self.initTimeForm)[0]
            self.oneTimePattern = re.compile("""(?<=日).*""")
            self.timeString = self.oneTimePattern.findall(self.initTimeForm)[0]
            self.initTimeForm = self.yearsString+'-'+self.monthsString+'-'+self.daysString+' '+self.timeString+':01'
        self.oneTimePattern = re.compile(""".*-.*-.*""")
        if self.oneTimePattern.findall(self.initTimeForm):
            self.TimeFormFlag = 5

        self.normalizeTimeDict = {
            1 : lambda initTimeForm: time.strftime( self.ISOTIMEFORMAT, time.localtime() ),
            2 : lambda minuts: time.strftime( self.ISOTIMEFORMAT, time.localtime( time.time() - int(minuts)*60) ),
            3 : lambda hours: time.strftime( self.ISOTIMEFORMAT, time.localtime( time.time() - int(hours)*60*60) ),
            6 : lambda initTimeForm: '%s' % datetime.date.today() +  initTimeForm + ':01',
            4 : lambda initTimeForm: '%s ' % (datetime.date.today() - self.oneday) +  initTimeForm + ':01',
            5 : lambda initTimeForm: initTimeForm
        }
        return self.normalizeTimeDict.get(self.TimeFormFlag)(self.initTimeForm)



    #-----------------********************-----------------#
    def getTextContent(self, oneAllConttentDict, textContentTamp):
        '''
            description:
                get text content  from the unstructure data textContentTamp
            input:
                oneAllConttentDict:
                    store text content in sturcture data
                textContentTamp:
                    the text content unstructure data
            output:
                none
        '''
        oneAllConttentDict = oneAllConttentDict
        self.textContentTamp = textContentTamp
        oneAllConttentDict['content']['mention_name'] = []
        oneAllConttentDict['content']['mention_content'] = []
        oneAllConttentDict['content']['topic_name'] = []
        oneAllConttentDict['content']['topic_content'] = []
        oneAllConttentDict['content']['url_name'] = []
        oneAllConttentDict['content']['url_content'] = []
        oneAllConttentDict['content']['text_content'] = ''
        #whether have topic/url/mention
        self.TextContentPattern = re.compile("""(?<=<a href=).*?</a>.*""")
        if self.TextContentPattern.findall(self.textContentTamp) :#含有特殊文本情况
            #self.TextContentPattern = re.compile("""^(<a href=)""")
            #if self.TextContentPattern.findall(self.patternContTamp) :#
            while self.textContentTamp: #直到文本内容解析完成
                ##print self.textContentTamp
                self.TextContentPattern = re.compile("""^(<a href=).*?</a>""")
                if self.TextContentPattern.findall(self.textContentTamp): #是否以特殊内容开始
                    self.TextContentPattern = re.compile("""^(<a href=.*?</a>)""")
                    self.patternContTamp = self.TextContentPattern.findall(self.textContentTamp)[0]
                    ##print "patternContTamp:"
                    ##print self.patternContTamp
                    self.TextContentPattern = re.compile("""(?<=">)@.*?(?=</a>)""")
                    if self.TextContentPattern.findall(self.patternContTamp): #是否@某人
                        self.patternMentionTamp= self.TextContentPattern.findall(self.patternContTamp)[0]
                        oneAllConttentDict['content']['mention_name'].append(self.patternMentionTamp)
                        #组装内容部分
                        oneAllConttentDict['content']['text_content'] = \
                                                oneAllConttentDict['content']['text_content'] + \
                                                self.patternMentionTamp
                        self.TextContentPattern = re.compile("""(?<=<a href=").*?(?=">)""")
                        self.patternMentionTamp= self.TextContentPattern.findall(self.patternContTamp)[0]
                        oneAllConttentDict['content']['mention_content'].append(self.patternMentionTamp)
                    self.TextContentPattern = re.compile("""(?<=">)#.*?(?=</a>)""")
                    if self.TextContentPattern.findall(self.patternContTamp): #是否是话题
                        self.patternMentionTamp= self.TextContentPattern.findall(self.patternContTamp)[0]
                        oneAllConttentDict['content']['topic_name'].append(self.patternMentionTamp)
                        #组装内容部分
                        oneAllConttentDict['content']['text_content'] = \
                                                oneAllConttentDict['content']['text_content'] + \
                                                self.patternMentionTamp
                        self.TextContentPattern = re.compile("""(?<=<a href=").*?(?=">)""")
                        self.patternMentionTamp= self.TextContentPattern.findall(self.patternContTamp)[0]
                        oneAllConttentDict['content']['topic_content'].append(self.patternMentionTamp)
                    self.TextContentPattern = re.compile("""(?<=">)http://.*?(?=</a>)""")
                    if self.TextContentPattern.findall(self.patternContTamp): #是否是url
                        self.patternMentionTamp= self.TextContentPattern.findall(self.patternContTamp)[0]
                        oneAllConttentDict['content']['url_name'].append(self.patternMentionTamp)
                        #组装内容部分
                        oneAllConttentDict['content']['text_content'] = \
                                                oneAllConttentDict['content']['text_content'] + \
                                                self.patternMentionTamp
                        self.TextContentPattern = re.compile("""(?<=<a href=").*?(?=">)""")
                        self.patternMentionTamp= self.TextContentPattern.findall(self.patternContTamp)[0]
                        oneAllConttentDict['content']['url_content'].append(self.patternMentionTamp)

                    #self.TextContentPatternRE = """%s""" % self.patternContTamp
                    self.stringLength = len(self.patternContTamp)
                    self.textContentTamp = self.textContentTamp[self.stringLength:]
                    #self.TextContentPattern = re.compile("""%s""" % self.patternContTamp)
                    #self.textContentTamp = re.sub(self.TextContentPattern,'',self.textContentTamp)
                else : #以文本开始
                    self.TextContentPattern = re.compile(""".*?(?=<a href=")""")
                    if self.TextContentPattern.findall(self.textContentTamp):
                        self.patternContTamp = self.TextContentPattern.findall(self.textContentTamp)[0]
                        oneAllConttentDict['content']['text_content'] = \
                                            oneAllConttentDict['content']['text_content'] + \
                                            self.patternContTamp
                    else :
                        self.TextContentPattern = re.compile(""".*""")
                        if self.TextContentPattern.findall(self.textContentTamp):
                            self.patternContTamp = self.TextContentPattern.findall(self.textContentTamp)[0]
                            oneAllConttentDict['content']['text_content'] = \
                                                oneAllConttentDict['content']['text_content'] + \
                                                self.patternContTamp
                    self.stringLength = len(self.patternContTamp)
                    self.textContentTamp = self.textContentTamp[self.stringLength:]
                    #self.TextContentPattern = re.compile("""%s""" % self.patternContTamp)
                    #self.textContentTamp = re.sub(self.TextContentPattern,'',self.textContentTamp)
        else:#不含有特殊文本情况
            self.TextContentPattern = re.compile(""".*""")
            if self.TextContentPattern.findall(self.textContentTamp):
                oneAllConttentDict['content']['text_content'] = self.TextContentPattern.findall(self.textContentTamp)[0]
        oneAllConttentDict['content']['text_content'] = re.sub(r'&[a-z]*?;', " ", oneAllConttentDict['content']['text_content'])
