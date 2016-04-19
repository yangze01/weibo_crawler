#-*- coding: UTF-8 -*-
import time
from createMultiCookies.multi import *
#from createMultiCookies.login import *
from collections import deque
from getinfo.get_data import *
from con2mongo.user_Unit import *
from getinfo.getlastdata import *
import random
import re
def getLoginDriver(username,password):
    driver = webdriver.Firefox()
    #driver = webdriver.Chrome()
    driver.get("http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.5)")
    inputUsername = driver.find_element_by_name("username")
    inputUsername.send_keys(username)
    time.sleep(1)
    inputPassword = driver.find_element_by_xpath("//input[@type='password']")
    inputPassword.send_keys(password)
    inputSubmit = driver.find_element_by_xpath("//input[@type='submit']")
    time.sleep(1)
    inputSubmit.click()
    time.sleep(3)
    #driver.get("http://weibo.cn/")
    #time.sleep(1)
    return driver
def getdriverlist(userdictdir):
    driverlist=list()
    usernameRE = re.compile('(?<=\').*?(?=\',)')
    pwdRE = re.compile('(?<=,\').*?(?=\')')
    try:
        userdiropen = open(userdictdir,'r')
    except:
        print 'open %s error' % userdictdir

    userline = userdiropen.readline()
    while userline:
        print userline

        if usernameRE.findall(userline):
            usernametmp = usernameRE.findall(userline)
        else:
            print 'the username error'
        if pwdRE.findall(userline):
            pswtmp = pwdRE.findall(userline)
        else:
            print 'the psw error'
        print usernametmp[0],pswtmp[0]
        userline = userdiropen.readline()
        driverlist.append(getLoginDriver(usernametmp,pswtmp))
    return driverlist

if __name__=="__main__":
    userlistdir = '/home/john/userpool.txt'
    queue= get_queue("/home/john/pythonspace/sina_crawler/weibo_crawler/salequeue.txt")
    visited = get_visited("/home/john/pythonspace/sina_crawler/weibo_crawler/salevisited.txt")
    driverlist = getdriverlist(userlistdir)
#    driver=driverlist[0]
    print driverlist
#    print driver
    try:
        while queue:
            userid = queue.pop()#取出待爬取的id
            print "the id will be read:"+str(userid)
            print 1
            if userid not in visited:
                print 2
                time.sleep(2)
                visited |= {userid}  # 标记为已访问
                catch_url = "http://weibo.com/u/"+userid+"?is_all=1"
                driverlist[len(queue)%len(driverlist)].get(catch_url)
                print 3
                time.sleep(10)
                # sixin = driver.find_element_by_xpath("//*[@id='Pl_Official_Headerv6__1']/div/div/div[2]/div[4]/div/div[2]/a")
                # sixin.click()
                time.sleep(10)
                print 4
        print "ok"
        f1 = open("/home/john/pythonspace/sina_crawler/weibo_crawler/salevisited.txt","w")
        f1.write(str(visited))
        f1.close()
        f2 = open("/home/john/pythonspace/sina_crawler/weibo_crawler/salequeue.txt","w")
        f2.write(str(queue))
        f2.close()
    except:
        print "error"
        #退出保存
        f1 = open("/home/john/pythonspace/sina_crawler/weibo_crawler/salevisited.txt","w")
        f1.write(str(visited))
        f1.close()
        f2 = open("/home/john/pythonspace/sina_crawler/weibo_crawler/salequeue.txt","w")
        f2.write(str(queue))
        f2.close()
