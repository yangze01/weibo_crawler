#-*- coding: UTF-8 -*-
from getinfo.get_data import *
from createMultiCookies.login import *
from con2mongo.user_Unit import *
import random
import re
import time
class getRandomheaderlist():
    def __init__(self):
        self.headerlist=list()

    def get_headerstr(self,u,p,logindriver):
        '''
            description:use the get Login to get headers with Cookie
            input:
                k:the username of sina_user
                v:the password of sina_user
            output:
                return the headers of a sina_user
        '''
        ckstr = get_ckstr(u,p,logindriver)
        time.sleep(3)
        headers = getHeaders(ckstr)
        return headers

    def get_headerlist(self,userdictdir,logindriver):
        '''
            description:get a list of Hearders
            input:
                userdictdir:userlistdir of sina_weibo
            output:
                return a list of headers
        '''
        self.usernameRE = re.compile('(?<=\').*?(?=\',)')
        self.pwdRE = re.compile('(?<=,\').*?(?=\')')
        try:
            self.userdiropen = open(userdictdir,'r')
        except:
            print 'open %s error' % userdictdir

        self.userline = self.userdiropen.readline()
        while self.userline:
            print self.userline

            if self.usernameRE.findall(self.userline):
                self.usernametmp = self.usernameRE.findall(self.userline)
            else:
                print 'the username error'
            if self.pwdRE.findall(self.userline):
                self.pswtmp = self.pwdRE.findall(self.userline)
            else:
                print 'the psw error'
            print self.usernametmp[0],self.pswtmp[0]
            self.userline = self.userdiropen.readline()
            self.tmpheader_str = self.get_headerstr(self.usernametmp[0],self.pswtmp[0],logindriver)
            # time.sleep(3)
            while len(self.tmpheader_str['Cookie'])<100:
                self.tmpheader_str = self.get_headerstr(self.usernametmp[0],self.pswtmp[0],logindriver)
                # time.sleep(3)
            self.headerlist.append(self.tmpheader_str)
            print len(self.headerlist)
        return self.headerlist

    def getOneRandomCookie(self):
        '''
            description:
                get one random cookie for crawler
            input:
                usernamePoolDir: username pool
            output:
                0:error
                a random cookie
        '''
        #self.headerList = headerList##createCookiePool(usernamePoolDir)
        self.listIndex = random.randint(0,len(self.headerlist)-1)
        self.currentHeader = self.headerlist[self.listIndex]
        return self.currentHeader

#if __name__=="__main__":
#    userdict = {
#        '15933533880':'',
#        '18610356434':'',
#        '13473601525':'',
#        '17816861780':'',
#        '18330274826':'',
#        '15230239181':''
#    }

#    while True:
#        randomheader = optHeaderlist.getOneRandomCookie()
#        print randomheader
