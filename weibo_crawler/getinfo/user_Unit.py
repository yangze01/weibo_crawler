#-*- coding: UTF-8 -*-
from collections import deque

class userUnit(object):
    '''
        the class in define a dict of userinfo,include:

    '''
    # def __init__(self):
    #     self.relation={
    #         "fans": "",
    #         "follow": "",
    #         "union": "",
    #         "intersection": ""
    #     }
    #     self.info={
    #         "vip":"",
    #         "username":"",
    #         "certificate":"",
    #         "sex":"",
    #         "district":"",
    #         "birthday":"",
    #         "certimes":""
    #     }


    # def __init__(self):
    #     self.user_unit = {
    #         "user_ID":"",
    #         "userinfo":{
    #             "vip":"",
    #             "username":"",
    #             "certificate":"",
    #             "sex":"",
    #             "district":"",
    #             "birthday":"",
    #             "certimes":""
    #         },
    #         "relation":{
    #             "fans": "",
    #             "follow": "",
    #             "union": "",
    #             "intersection": ""
    #         }
    #     }
    def __init__(self):
        self.user_unit={
            #"user_ID":"",
            "_id":"",
            "userinfo":{},
            "relation":{}
        }
