#-*- coding: UTF-8 -*-
from get_data import *
from login import *
from user_Unit import *
from collections import deque
from multi import *
import time

if __name__=="__main__":
    userinfo=dict()
    a=list()
    a.append(1)
    a.append(2)
    a.append(3)
    a.append(4)
    f = open("/home/john/visited.txt","w")
    f.write(str(a))
    f.close()
    f = open("/home/john/pythonspace/sina_crawler/weibo_crawler/getinfo/info.txt","r")
    data = f.read()
    print data
    print "======================================"
    re_allinfo='<div class="c">.*?<br/></div>'
    pattern = re.compile(re_allinfo,re.S)
    item = re.findall(pattern,data)[0]
    print item
    print "======================================"
    re_tags = "(?<=标签:).*?(?=</div>)"
    pat_tags = re.compile(re_tags,re.S)
    if re.findall(pat_tags,item):
        tags =  re.findall(pat_tags,item)[0]
        re_tag = "(?<=\">).*?(?=</a>&nbsp;)"
        pat_tag = re.compile(re_tag,re.S)
        if re.findall(pat_tag,tags):
            userinfo["tags"]=re.findall(pat_tag,tags)

    re_vip = "(?<=会员等级：).*?(?=&nbsp)"
    pat_vip = re.compile(re_vip,re.S)
    if re.findall(pat_vip,item):
        userinfo["vip"] = re.findall(pat_vip,item)[0]
    print userinfo
