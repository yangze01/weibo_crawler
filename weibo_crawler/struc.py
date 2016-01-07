from collections import deque

class all_url:
    def __init__(self):
        self.userid = 3199208303
        self.home_page = "http://weibo.cn/"
        self.weibourl = self.home_page+str(self.userid)+"/profile?page="
        self.followurl = self.home_page+str(self.userid)+"/follow?page="
        self.fansurl = self.home_page+str(self.userid)+"/fans?page="

class per_deque:
    def __init__(self):
        self.id_queue=deque()
        self.name_queue=deque()

class per_struct:
    def __init__(self):
        self.fans_set = set()
        self.follow_set = set()
        self.friends_set = set()
        self.all_set = set()
class userinfo(object):
    def __init__(self):
        self.relation={
            "fans": "",
            "follow": "",
            "union": "",
            "intersection": ""
        }
