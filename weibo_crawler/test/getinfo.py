#-*- coding: UTF-8 -*-
import re
import urllib
import urllib2
def get_userinfo(data):
    re_allinfo='<div class="c">.*?<br/></div>'
    #re_allinfo="(?<=会员等级：).*?(?=&nbsp)"
    pattern = re.compile(re_allinfo,re.S)
    items = re.findall(pattern,data)
    return items
def get_data(this_url,headers):
    req = urllib2.Request(this_url,headers=headers)
    response = urllib2.urlopen(req)
    data = response.read()
    return data
