#-*- coding: UTF-8 -*-
import re
import urllib
import urllib2
import sys
from struc import *
reload(sys)
sys.setdefaultencoding('utf-8')
def get_data(this_url,headers):
    req = urllib2.Request(this_url,headers=headers)
    response = urllib2.urlopen(req)
    data = response.read()
    return data

def get_userinfo(userid,headers):
    this_url = "http://weibo.cn/"+userid+"/info"
    userdata = userinfo()
    data = get_data(this_url,headers)
    #print data

    re_allinfo='<div class="c">.*?<br/></div>'
    pattern = re.compile(re_allinfo,re.S)
    item = re.findall(pattern,data)[0]

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
    #if re.match(pat_vip,item):
    #    print re.findall(pat_vip,item)[0]
    if re.findall(pat_vip,item):
        userdata.info["vip"] = re.findall(pat_vip,item)[0]
    if re.findall(pat_username,item):
        userdata.info["username"] = re.findall(pat_username,item)[0]
    if re.findall(pat_certificate,item):
        userdata.info["certificate"] = re.findall(pat_certificate,item)[0]
    if re.findall(pat_sex,item):
        userdata.info["sex"] = re.findall(pat_sex,item)[0]
    if re.findall(pat_district,item):
        userdata.info["district"] = re.findall(pat_district,item)[0]
    if re.findall(pat_birthday,item):
        userdata.info["birthday"] = re.findall(pat_birthday,item)[0]
    if re.findall(pat_certimes,item):
        userdata.info["certimes"] = re.findall(pat_certimes,item)[0]
    return userdata.info
