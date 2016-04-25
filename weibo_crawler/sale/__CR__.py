#-*- coding: UTF-8 -*-
import time
from createMultiCookies.multi import *
from createMultiCookies.login import *
from collections import deque
from getinfo.get_data import *
from con2mongo.user_Unit import *
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
    print items
    if items:
        item=items[0]
        return int(item[38:-4])
    else:
        return 1


def getUserWithCondition(optHeaderlist,keyword="销售",gender="all",age="0",searchtype="tags",isv = "all"):
    # keyword = "华北电力大学（保定）"
    # gender ="all"#all,f,m
    # age = "0" #18 22 29 39 40
    # searchtype = "scho"#nike tags scho comp
    advancedfilter = "1"
    # isv = "all" # all 1 0
    # page = "49"
    headers = optHeaderlist.getOneRandomCookie()
    catch_url = "http://weibo.cn/search/user/?keyword="+keyword+"&gender="+gender+"&age="+age+"&type="+searchtype+"&advancedfilter="+advancedfilter+"&isv="+isv+"&page="
    idnset = set()
    home_page = catch_url+'1'
    data1 = get_data(home_page,headers)
    page = get_pageNum(data1)
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
if __name__=="__main__":
    userlistdir = '/home/john/userpool.txt'
    optHeaderlist = getRandomheaderlist()
    optHeaderlist.headerlist=optHeaderlist.get_headerlist(userlistdir)#返回headers池
    ###############################################################################
    isvlist=["0","1"]
    searchtypelist=["tags","comp","nick"]
    agelist = ["18","22","29","39","40"]
    salequeue=list()
    salevisited=set()
    try:
        for i in isvlist:
            for j in searchtypelist:
                for k in agelist:
                    tmp = getUserWithCondition(optHeaderlist,isv=i,searchtype=j,age=k)
                    salequeue=salequeue+tmp
                    print len(salequeue)
        salequeue = list(set(salequeue))
        f1 = open("/home/john/pythonspace/sina_crawler/weibo_crawler/salevisited.txt","w")
        f1.write(str(salevisited))
        f1.close()
        f2 = open("/home/john/pythonspace/sina_crawler/weibo_crawler/salequeue.txt","w")
        f2.write(str(salequeue))
        f2.close()
    except:
        #退出保存
        f1 = open("/home/john/pythonspace/sina_crawler/weibo_crawler/salevisited.txt","w")
        f1.write(str(salevisited))
        f1.close()
        f2 = open("/home/john/pythonspace/sina_crawler/weibo_crawler/salequeue.txt","w")
        f2.write(str(salequeue))
        f2.close()
