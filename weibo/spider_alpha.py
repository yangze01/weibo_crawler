from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.by import By
from collections import deque
import urllib
import urllib2
import cookielib
import sys
import time
import re
reload(sys)
sys.setdefaultencoding('utf-8')
# Create a new instance of the Chrome driver

def getLoginDriver(username,password):
    driver = webdriver.Chrome()

    # go to the weibo login page
    driver.get("http://login.weibo.cn/login/")
    # find the element
    inputUsername = driver.find_element_by_name("mobile")
    inputUsername.send_keys(username)
    inputPassword = driver.find_element_by_xpath("//input[@type='password']")
    inputPassword.send_keys(password)
    inputSubmit = driver.find_element_by_name("submit")
    inputSubmit.click()
    return driver

#get headers with cookie
def getHeaders(driver):
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



class all_url:
    def __init__(self):
        self.userid = 3199208303
        self.home_page = "http://weibo.cn/"
        self.weibourl = self.home_page+str(self.userid)+"/profile?page="
        self.followurl = self.home_page+str(self.userid)+"/follow?page="
        self.fansurl = self.home_page+str(self.userid)+"/fans?page="

class per_deque:
    def __init__(self):
        self.id_queue=deque()
        self.name_queue=deque()

class per_struct:
    def __init__(self):
        self.fans_set = set()
        self.follow_set = set()
        self.friends_set = set()
        self.all_set = set()

def get_data(this_url,headers):
    req = urllib2.Request(this_url,headers=headers)
    response = urllib2.urlopen(req)
    data = response.read()
    return data

def get_pageNum(data):
    re_pagenum = '<input name="mp" type="hidden" value=.*?>'
    pattern = re.compile(re_pagenum,re.S)
    items = re.findall(pattern,data)
    item=items[0]
    return int(item[38:-4])

def get_fansfollow(catch_url,headers):
"""

hello

"""
    idnset=set()
    home_page = catch_url+'1'
    data1 = get_data(home_page,headers)
    page=get_pageNum(data1)

    re_id = '<a href="http://weibo.cn/u/\d{0,11}">[^<].*?[^>]</a>'
    pattern = re.compile(re_id,re.S)
    for i in range(1,page):
        this_url = catch_url+str(i)
        data = get_data(this_url,headers)
        items = re.findall(pattern,data)
        for item in items:
            idnset.add(item[27:37]+item[39:-4])
    return idnset

def get_friends(fansset,followset):
    return fansset&followset

if __name__=="__main__":
    driver = getLoginDriver(18330274826,523581600)
    time.sleep(3)
    headers = getHeaders(driver)

    use_url = all_url()
    this_url = use_url.fansurl+str(2)

    req = urllib2.Request(this_url,headers=headers)
    try:
        response = urllib2.urlopen(req)
        data = response.read()

        # file = open("test1.html","w")
        # file.write(data)
        # file.close()

        print data

    except urllib2.URLError,e:
        if hasattr(e,"code"):
            print e.code
        if hasattr(e,"reason"):
            print e.reason
    else:
        print "OK"
