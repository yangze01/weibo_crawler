#-*- coding: UTF-8 -*-
from collections import deque

class per_deque:
    def __init__(self):
        self.id_queue=deque()
        self.name_queue=deque()


class userinfo(object):
    def __init__(self):
        self.relation={
            "fans": "",
            "follow": "",
            "union": "",
            "intersection": ""
        }
        self.info={
            "vip":"",
            "username":"",
            "certificate":"",
            "sex":"",
            "district":"",
            "birthday":"",
            "certimes":""
        }
