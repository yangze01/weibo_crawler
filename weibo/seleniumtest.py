from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.by import By
import time
import urllib
import urllib2
import cookielib
import httplib

#get opener with cookie
def getOpener(head):
    cj = cookielib.CookieJar()
    pro = urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(pro)
    header = []
    for key,value in head.items():
        elem = (key,value)
        header.append(elem)
    opener.addheaders=header
    return opener





# Create a new instance of the Chrome driver
driver = webdriver.Chrome()
# go to the weibo login page
driver.get("http://login.weibo.cn/login/")
# find the element
inputUsername = driver.find_element_by_name("mobile")
inputUsername.send_keys("18330274826")
inputPassword = driver.find_element_by_xpath("//input[@type='password']")
inputPassword.send_keys("523581600")
inputSubmit = driver.find_element_by_name("submit")
inputSubmit.click()






cur_url=driver.current_url
print cur_url
ck=[item["name"]+"="+item["value"] for item in driver.get_cookies()]
ckstr=";".join(item for item in ck)
print ckstr

head={
    'Connection':'keep-alive',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36',
    'Accept-Encoding':'gzip, deflate, sdch'
}
head.setdefault('Cookie',ckstr)
opener = getOpener(head)
op = opener.open()
#crawl page
req = urllib2.Request(init_url,headers=header)
try:
    urllib2.urlopen(req)
except urllib2.URLError,e:
    if hasattr(e,"code"):
        print e.code
    if hasattr(e,"reason"):
        print e.reason
    else:
        print "the url is OK"
