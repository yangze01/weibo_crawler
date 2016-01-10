#-*- coding: UTF-8 -*-
from login import *
from getinfo import *
import urllib
import urllib2
import cookielib

driver = getLoginDriver(18330274826,523581600)
time.sleep(3)
headers = getHeaders(driver)
this_url = "http://weibo.cn/5187664653/info"
try:
    data = get_data(this_url,headers)
    item = get_userinfo(data)[0]


    re_vip = "(?<=会员等级：).*?(?=&nbsp)"
    re_username="(?<=昵称:).*?(?=<br/>)"
    re_certificate="(?<=认证:).*?(?=<br/>)"
    re_sex="(?<=性别:).*?(?=<br/>)"
    re_district="(?<=地区:).*?(?=<br/>)"
    re_birthday="(?<=生日:).*?(?=<br/>)"
    re_certimes="(?<=认证信息：).*?(?=<br/>)"

    pat_vip = re.compile(re_vip,re.S)
    pat_username = re.compile(re_username,re.S)
    pat_certificate = re.compile(re_certificate,re.S)
    pat_sex = re.compile(re_sex,re.S)
    pat_district = re.compile(re_district,re.S)
    pat_birthday = re.compile(re_birthday,re.S)
    pat_certimes = re.compile(re_certimes,re.S)

    vip = re.findall(pat_vip,item)[0]
    username = re.findall(pat_username,item)[0]
    certificate = re.findall(pat_certificate,item)[0]
    sex = re.findall(pat_sex,item)[0]
    district = re.findall(pat_district,item)[0]
     = re.findall(pat_birthday,item)[0]
    vip = re.findall(pat_certimes,item)[0]




except urllib2.URLError,e:
    if hasattr(e,"code"):
        print e.code
    if hasattr(e,"reason"):
        print e.reason
else:
    print "OK"
