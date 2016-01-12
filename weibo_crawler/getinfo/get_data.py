#-*- coding: UTF-8 -*-
from collections import deque
import urllib
import urllib2
import cookielib
import re
from struc import *
def get_data(this_url,headers):
    req = urllib2.Request(this_url,headers=headers)
    response = urllib2.urlopen(req)
    data = response.read()
    return data
def get_pageNum(data):
    re_pagenum = '<input name="mp" type="hidden" value=.*?>'
    pattern = re.compile(re_pagenum,re.S)
    items = re.findall(pattern,data)
    print items
    item=items[0]
    return int(item[38:-4])

def get_fans(userid,headers):
    catch_url = "http://weibo.cn/"+userid+"/fans?page="
    idnset = set()
    home_page = catch_url+'1'
    data1 = get_data(home_page,headers)
    page = get_pageNum(data1)
    print page
    re_id = '<a href="http://weibo.cn/u/\d{0,11}">[^<].*?[^>]</a>'
    pattern = re.compile(re_id,re.S)
    for i in range(1,page):
        this_url = catch_url+str(i)
        data = get_data(this_url,headers)
        items = re.findall(pattern,data)
        for item in items:
            #idnset.add(item[27:37]+item[39:-4])
            idnset.add(item[27:37])
    return idnset

def get_follow(userid,headers):
    catch_url = "http://weibo.cn/"+userid+"/follow?page="
    idnset=set()
    home_page = catch_url+'1'
    data1 = get_data(home_page,headers)
    page=get_pageNum(data1)
    print page
    re_id = '<a href="http://weibo.cn/u/\d{0,11}">[^<].*?[^>]</a>'
    pattern = re.compile(re_id,re.S)
    for i in range(1,page):
        this_url = catch_url+str(i)
        data = get_data(this_url,headers)
        items = re.findall(pattern,data)
        for item in items:
            #idnset.add(item[27:37]+item[39:-4])
            idnset.add(item[27:37])
    return idnset


def get_friends(fansset,followset):
    return fansset&followset
def get_all(fansset,followset):
    return fansset|followset

def get_relation(userid,headers):
    tmp_userinfo = userinfo()
    fans_set = get_fans(userid,headers)
    follow_set = get_follow(userid,headers)

    all_set = get_friends(fans_set,follow_set)
    friends_set = get_all(fans_set,follow_set)

    tmp_userinfo.relation["fans"]=list(fans_set)
    tmp_userinfo.relation["follow"]=list(follow_set)
    tmp_userinfo.relation["union"]=list(all_set)
    tmp_userinfo.relation["intersection"]=list(friends_set)
    return tmp_userinfo.relation

def get_userinfo(userid,headers):
    this_url = "http://weibo.cn/"+userid+"/info"
    userdata = userinfo()
    data = get_data(this_url,headers)

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
