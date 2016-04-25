
from collections import deque
import urllib
#import urllib2
#import cookielib
import urllib.request
import re
import random
from con2mongo.user_Unit import *


def get_data(this_url,headers):
    '''
        description:
            get data from webpage
        input:
            this_url:the page to be crawler
            headers:the headers of a sina_weibo cookie
        output:
            the page data
    '''
    req = urllib.request.Request(this_url,headers=headers)
    response = urllib.request.urlopen(req)
    data = response.read()
    return data
def get_pageNum(data):
    '''
    description:
        get the weibo,fans,follow page number
    input:
        data:the page data
    output:
        return the page number
    '''
    re_pagenum = '<input name="mp" type="hidden" value=.*?>'
    pattern = re.compile(re_pagenum,re.S)
    items = re.findall(pattern,data)
    print(items)
    if items:
        item=items[0]
        return int(item[38:-4])
    else:
        return 1

def getUserWithCondition(optHeaderlist,keyword=u"华北电力大学（保定）",gender="all",age="0",searchtype="all",isv = "all"):
    # keyword = "华北电力大学（保定）"
    # gender ="all"#all,f,m
    # age = "0" #18 22 29 39 40
    # searchtype = "scho"#nike tags scho comp all
    advancedfilter = "1"
    # isv = "all" # all 1 0
    # page = "49"
    headers = optHeaderlist.getOneRandomCookie()
    catch_url = "http://weibo.cn/search/user/?keyword="+keyword+"&gender="+gender+"&age="+age+"&type="+searchtype+"&advancedfilter="+advancedfilter+"&isv="+isv+"&page="
    idnset = set()
    home_page = catch_url+'1'
    data1 = get_data(home_page,headers)
    page = 400
    # re_id = '<a href="http://weibo.cn/u/\d{0,11}">[^<].*?[^>]</a>'
    # <a href="/u/2365961811?f=search_16&amp;vt=4">皓伦王明川</a>
    re_id = '<a href="/u/\d{0,11}.*?"[^<].*?[^>]</a>'
    pattern = re.compile(re_id,re.S)
    countpageNum = 0
    for i in range(1,page):
        if countpageNum%5 == 0:
            headers = optHeaderlist.getOneRandomCookie()
        this_url = catch_url+str(i)
        data = get_data(this_url,headers)
        items = re.findall(pattern,data)
        if items:
            for item in items:
                #print item
                #print item[12:22]
                idnset.add(item[12:22])
    return list(idnset)

def get_fans(userid,optHeaderlist):
    '''
    description:
        get user's fans list
    input:
        userid:the user's id
        headers:the headers of a sina_weibo cookie
    '''
    headers = optHeaderlist.getOneRandomCookie()
    catch_url = "http://weibo.cn/"+userid+"/fans?page="
    idnset = set()
    home_page = catch_url+'1'
    data1 = get_data(home_page,headers)
    page = get_pageNum(data1)
    print(page)
    re_id = '<a href="http://weibo.cn/u/\d{0,11}">[^<].*?[^>]</a>'
    pattern = re.compile(re_id,re.S)
    countpageNum = 0

    for i in range(1,page):
        if countpageNum%5 == 0:
            headers = optHeaderlist.getOneRandomCookie()
        this_url = catch_url+str(i)
        data = get_data(this_url,headers)
        items = re.findall(pattern,data)
        for item in items:
            #idnset.add(item[27:37]+item[39:-4])
            idnset.add(item[27:37])
    return idnset

def get_follow(userid,optHeaderlist):
    '''
    description:
        get user's follow set
    input:
        userid:the user's id
        headers:the headers of a sina_weibo cookie
    '''
    headers = optHeaderlist.getOneRandomCookie()
    catch_url = "http://weibo.cn/"+userid+"/follow?page="
    idnset=set()
    home_page = catch_url+'1'
    data1 = get_data(home_page,headers)
    page=get_pageNum(data1)
    print(page)
    re_id = '<a href="http://weibo.cn/u/\d{0,11}">[^<].*?[^>]</a>'
    pattern = re.compile(re_id,re.S)
    countpageNum = 0
    for i in range(1,page):
        if countpageNum%5 == 0:
            headers = optHeaderlist.getOneRandomCookie()
        this_url = catch_url+str(i)
        data = get_data(this_url,headers)
        items = re.findall(pattern,data)
        for item in items:
            #idnset.add(item[27:37]+item[39:-4])
            idnset.add(item[27:37])
    return idnset


def get_friends(fansset,followset):
    '''
    description:
        get the union set of fansset and followset
    input:
        fansset:the user's fans set
        followset:the user's follow set
    output:
        return the union of fansset and followset
    '''
    return fansset&followset
def get_all(fansset,followset):
    '''
    description:
        get the intersection of fansset and followset
    input:
        fansset:the user's fans set
        followset:the user's follow set
    output:
        return the intersection of fansset and followset
    '''
    return fansset|followset

def get_relation(userid,optHeaderlist):
    '''
    description:
        get the user's relation
    input:
        userid:the user's id
        headers:the headers of a sina_weibo cookie
    output:
        return a dict of relation
    '''
    relation = dict()
    fans_set = get_fans(userid,optHeaderlist)
    follow_set = get_follow(userid,optHeaderlist)

    all_set = get_friends(fans_set,follow_set)
    friends_set = get_all(fans_set,follow_set)

    relation["fans"]=list(fans_set)
    relation["follow"]=list(follow_set)
    relation["union"]=list(all_set)
    relation["intersection"]=list(friends_set)
    return relation

def get_userinfo(userid,optHeaderlist):
    '''
    description:
        get the user's relation
    input:
        userid:the user's id
        headers:the headers of a sina_weibo cookie
    output:
        return a dict of userinfo
    '''
    headers = optHeaderlist.getOneRandomCookie()
    userinfo=dict()
    this_url = "http://weibo.cn/"+userid+"/info"
    data = get_data(this_url,headers)

    re_allinfo='<div class="c">.*?<br/></div>'
    pattern = re.compile(re_allinfo,re.S)
    if(re.findall(pattern,data)):
        item = re.findall(pattern,data)[0]
    else:
        return userinfo
    re_vip = "(?<=会员等级：).*?(?=&nbsp)"
    re_username="(?<=昵称:).*?(?=<br/>)"
    re_certificate="(?<=认证:).*?(?=<br/>)"
    re_sex="(?<=性别:).*?(?=<br/>)"
    re_district="(?<=地区:).*?(?=<br/>)"
    re_birthday="(?<=生日:).*?(?=<br/>)"
    re_certimes="(?<=认证信息：).*?(?=<br/>)"
    re_summary="(?<=简介:).*?(?=<br/>)"
    re_tags = "(?<=标签:).*?(?=</div>)"
    re_studyinfo='学习经历</div><div class="c">.*?<br/></div>'
    re_schoolORwork = "((?<=·).*?(?=&nbsp;)|(?<=·).*?(?=<br/>))"
    re_studytimeORworktime = "(?<=&nbsp;)\S+?(?=<br/>)"
    re_workinfo='工作经历</div><div class="c">.*?<br/></div>'

    pat_vip = re.compile(re_vip,re.S)
    pat_username = re.compile(re_username,re.S)
    pat_certificate = re.compile(re_certificate,re.S)
    pat_sex = re.compile(re_sex,re.S)
    pat_district = re.compile(re_district,re.S)
    pat_birthday = re.compile(re_birthday,re.S)
    pat_certimes = re.compile(re_certimes,re.S)
    pat_summary = re.compile(re_summary,re.S)
    pat_tags = re.compile(re_tags,re.S)
    pat_study = re.compile(re_studyinfo,re.S)
    pat_schoolORwork = re.compile(re_schoolORwork,re.S)
    pat_studtimeORworktime = re.compile(re_studytimeORworktime,re.S)
    pat_work = re.compile(re_workinfo,re.S)

    #if re.match(pat_vip,item):
    #    print re.findall(pat_vip,item)[0]

    if re.findall(pat_vip,item):
        userinfo["vip"] = re.findall(pat_vip,item)[0]
    if re.findall(pat_username,item):
        userinfo["username"] = re.findall(pat_username,item)[0]
    if re.findall(pat_certificate,item):
        userinfo["certificate"] = re.findall(pat_certificate,item)[0]
    if re.findall(pat_sex,item):
        userinfo["sex"] = re.findall(pat_sex,item)[0]
    if re.findall(pat_district,item):
        userinfo["district"] = re.findall(pat_district,item)[0]
    if re.findall(pat_birthday,item):
        userinfo["birthday"] = re.findall(pat_birthday,item)[0]
    if re.findall(pat_certimes,item):
        userinfo["certimes"] = re.findall(pat_certimes,item)[0]
    if re.findall(pat_summary,item):
        userinfo["summary"] = re.findall(pat_summary,item)[0]
    if re.findall(pat_tags,item):
        tags =  re.findall(pat_tags,item)[0]
        re_tag = "(?<=\">).*?(?=</a>&nbsp;)"
        pat_tag = re.compile(re_tag,re.S)
        if re.findall(pat_tag,tags):
            userinfo["tags"]=re.findall(pat_tag,tags)
    if re.findall(pat_study,data):
        print("studyplace____________________________________________________________________________________________________________")
        studyitem = re.findall(pat_study,data)[0]
        print(studyitem)
        if re.findall(pat_schoolORwork,studyitem):
            userinfo["studyin"]=re.findall(pat_schoolORwork,studyitem)
            for i in re.findall(pat_schoolORwork,studyitem):
                print(i)
        if re.findall(pat_studtimeORworktime,studyitem):
            userinfo["studytime"]=re.findall(pat_studtimeORworktime,studyitem)
            for i in re.findall(pat_studtimeORworktime,studyitem):
                print(i)
            # print len(re.findall(pat_study,item))
            print(type(re.findall(pat_schoolORwork,studyitem)))
    if re.findall(pat_work,data):
        print ("workplace____________________________________________________________________________________________________________")
        studyitem = re.findall(pat_work,data)[0]
        print(studyitem)
        if re.findall(pat_schoolORwork,studyitem):
            userinfo["workin"]=re.findall(pat_schoolORwork,studyitem)
            for i in re.findall(pat_schoolORwork,studyitem):
                print(i)
        if re.findall(pat_studtimeORworktime,studyitem):
            userinfo["worktime"]=re.findall(pat_studtimeORworktime,studyitem)
            for i in re.findall(pat_studtimeORworktime,studyitem):
                print(i)
    #print userinfo
    return userinfo
