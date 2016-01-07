#-*- coding: UTF-8 -*-
from get_data import *
from login import *
from struc import *
from collections import deque

if __name__=="__main__":
    driver = getLoginDriver(183302746,)
    time.sleep(3)
    headers = getHeaders(driver)
    #123456
#   init two struct:queue and set
    queue = deque()
    testqueue = deque()
    visited = set()
    queue.append(3199208303)
    #print queue
    use_url = all_url()
#    req = urllib2.Request(this_url,headers=headers)
    try:
        while deque:
            tmp_userinfo = userinfo()
            a=per_struct()
            catch_id = queue.popleft()#pop the left var
            print catch_id
            use_url.userid = catch_id
            a.fans_set = get_fansfollow(use_url.fansurl,headers)
            a.follow_set = get_fansfollow(use_url.followurl,headers)
            a.all_set = get_friends(a.fans_set,a.follow_set)
            a.friends_set = get_all(a.fans_set,a.follow_set)
            tmp_userinfo.relation["fans"]=list(a.fans_set)
            tmp_userinfo.relation["follow"]=list(a.follow_set)
            tmp_userinfo.relation["union"]=list(a.all_set)
            tmp_userinfo.relation["intersection"]=list(a.friends_set)

            print tmp_userinfo.relation

    except urllib2.URLError,e:
        if hasattr(e,"code"):
            print e.code
        if hasattr(e,"reason"):
            print e.reason
    else:
        print "OK"
