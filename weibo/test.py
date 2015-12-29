#-*- coding: UTF-8 -*-
import re
from collections import deque
import json
import sys
import json
import pymongo
reload(sys)
sys.setdefaultencoding('utf-8')

class per_struct:
    def __init__(self):
        self.fans_set=set()
        self.follow_set=set()
        self.friends_set=set()
        self.all_set=set()

#test_dump = json.dumps(testA, sort_keys = True, indent = 4,ensure_ascii=False)

per_set = per_struct()

file = open("test1.html")
re_id = '<a href="http://weibo.cn/u/\d{0,11}">[^<].*?[^>]</a>'
re_test = '\d{10}'
re_pageNum = '<input name="mp" type="hidden" value=.*?>'
pattern = re.compile(re_id,re.S)
test={}
try:
    data=file.read()
    items = re.findall(pattern,data)
    # item = items[0]
    # print item[38:-4]
    for item in items:
        print item
        per_set.fans_set.add(item[27:37]+item[39:-4])
    test['fans']=list(per_set.fans_set)
    a = json.dumps(test)
    conn = pymongo.Connection()
    db = conn.test
    users = db.users
    db.users.insert(test)
    b=db['users']

finally:
    file.close()
