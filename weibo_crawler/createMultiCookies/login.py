#-*- coding: UTF-8 -*-
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.by import By
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# Create a new instance of the Chrome driver
# the test push

def getLoginDriver(username,password):
    '''
        description:use the selenium to get the driver of a user's driver
        input:
            username:the username of a sina_user
            password:the password of a sina_user
        output:
            return the driver with a user's Cookie
    '''
    driver = webdriver.Firefox()
    #driver = webdriver.Chrome()
    # go to the weibo login page
    #driver.get("http://login.weibo.cn/login/")
    driver.get("http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.5)")
    # find the element
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
    time.sleep(2)
    driver.get("http://weibo.cn/")
    #time.sleep(1)
    return driver

#get headers with cookie
def getHeaders(driver):
    '''
        description:get the headers with a user's Cookie
        input:
            driver:the chrome driver of the return value of getLoginDriver
        output:
            return the headers with a user's Cookie
    '''
    ck=[item["name"]+"="+item["value"] for item in driver.get_cookies()]
    ckstr=";".join(item for item in ck)
    print ckstr
    head={
        'Connection':'keep-alive',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36',
        'Cookie':ckstr
    }
    return head
