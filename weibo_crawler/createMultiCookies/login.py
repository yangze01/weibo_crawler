#-*- coding: UTF-8 -*-
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.by import By
import time
import sys
import random
from random import choice
reload(sys)
sys.setdefaultencoding('utf-8')
# Create a new instance of the Chrome driver
# the test push

def get_ckstr(username,password):
    '''
        description:use the selenium to get the driver of a user's driver
        input:
            username:the username of a sina_user
            password:the password of a sina_user
        output:
            return the driver with a user's Cookie
    '''
    # driver = webdriver.Firefox()
    driver = webdriver.Chrome()
    # go to the weibo login page
    #driver.get("http://login.weibo.cn/login/")
    driver.get("http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.5)")
    # find the element
    time.sleep(1)
    #inputUsername = driver.find_element_by_name("mobile")
    inputUsername = driver.find_element_by_name("username")
    inputUsername.send_keys(username)
    time.sleep(1)
    inputPassword = driver.find_element_by_xpath("//input[@type='password']")
    inputPassword.send_keys(password)
    time.sleep(1)
    #inputCode = driver.find_element_by_xpath("//input[@type='text' and @name='code']").get_attribute("value")
    #inputCode = driver.find_element_by_xpath("//input[@type='text' and @name='code']").get_attribute("value")
#    a = raw_input("please input the code:")
#    inputCode =a
    # print len(inputCode)
    # while len(inputCode)<3:
    #     print len(inputCode)
    #     inputCode = driver.find_element_by_xpath("//input[@type='text' and @name='code']").get_attribute("value")
    inputSubmit = driver.find_element_by_xpath("//input[@type='submit']")
    time.sleep(2)
    inputSubmit.click()
    time.sleep(1)
    driver.get("http://weibo.cn/")
    time.sleep(2)
    ck=[item["name"]+"="+item["value"] for item in driver.get_cookies()]
    ckstr=";".join(item for item in ck)
    while(len(ckstr)<=100):
        driver.get("http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.5)")
        time.sleep(1)
        driver.get("http://weibo.cn/")
        time.sleep(2)
        ck=[item["name"]+"="+item["value"] for item in driver.get_cookies()]
        ckstr=";".join(item for item in ck)
        if(len(ckstr)>100):
            return ckstr
        driver.get("http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.5)")
        # find the element
        time.sleep(1)
        #inputUsername = driver.find_element_by_name("mobile")
        inputUsername = driver.find_element_by_name("username")
        inputUsername.send_keys(username)
        time.sleep(1)
        inputPassword = driver.find_element_by_xpath("//input[@type='password']")
        inputPassword.send_keys(password)
        time.sleep(1)
        #inputCode = driver.find_element_by_xpath("//input[@type='text' and @name='code']").get_attribute("value")
        #inputCode = driver.find_element_by_xpath("//input[@type='text' and @name='code']").get_attribute("value")
    #    a = raw_input("please input the code:")
    #    inputCode =a
        # print len(inputCode)
        # while len(inputCode)<3:
        #     print len(inputCode)
        #     inputCode = driver.find_element_by_xpath("//input[@type='text' and @name='code']").get_attribute("value")
        inputSubmit = driver.find_element_by_xpath("//input[@type='submit']")
        time.sleep(2)
        inputSubmit.click()
        time.sleep(1)

        time.sleep(2)
        driver.get("http://weibo.cn/")
        time.sleep(2)
        ck=[item["name"]+"="+item["value"] for item in driver.get_cookies()]
        ckstr=";".join(item for item in ck)

        #time.sleep(1)
    return ckstr

#get headers with cookie
def getHeaders(ckstr):
    '''
        description:get the headers with a user's Cookie
        input:
            driver:the chrome driver of the return value of getLoginDriver
        output:
            return the headers with a user's Cookie
    '''
    # ck=[item["name"]+"="+item["value"] for item in driver.get_cookies()]
    # ckstr=";".join(item for item in ck)
    print ckstr
    user_agent_list = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1",
    "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0",
    "Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20130401 Firefox/31.0",
    "Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16",
    "Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14",
    "Opera/12.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.02",
    "Opera/9.80 (Windows NT 6.1; U; es-ES) Presto/2.9.181 Version/12.00",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 7.0; InfoPath.3; .NET CLR 3.1.40767; Trident/6.0; en-IN)",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36"]
    ua = random.choice(user_agent_list)
    print "the length of ckstr:"+str(len(ckstr))
    head={
        'Connection':'keep-alive',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'User-Agent':ua,
        'Cookie':ckstr
    }
    return head
