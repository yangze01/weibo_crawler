#!/usr/bin/python
#-*- coding: UTF-8 -*-

#filename: blogUnit.py
#description: unit form of blog
#author: warrior  ,mail: oowarrioroo@163.com
#data: 2015-12-30
#log:
#--- 2016-1-1 : add {"blog_device": ""} into blog_unit, record a blog be sended from what device
#               add {"repost_device": ""}, {"repost_time": ""}, {"repost_attitude": ""},
#               add {"comment_device": ""}, {"comment_time": ""}, {"comment_attitude": ""}, 

"""
    set unit form of blog
"""


#********************-----------------********************#

#********************-----------------********************#
class blogUnit(object):
    '''
        the form of blog , include:
        [blog_id, blog_address, blog_time, blog_device, blog_content],
        blog_attitude,
        [repost_id, repost_content, repost_device, repost_time, repost_attitude],
        [comment_id, comment_content, comment_device, comment_time, comment_attitude]
    '''
    def __init__(self):
        self.blog_unit = {
            "user_ID": "",
            "blog": {
            "blog_id": "",
            "blog_address": "",
            "blog_time": "",
            "blog_device": "",
            "blog_content": ""
            },
            "repost": {
            "repost_id": "",
            "repost_content": "",
            "repost_device": "",
            "repost_time": "",
            "repost_attitude": ""
            },
            "comment": {
            "comment_id": "",
            "comment_content": "",
            "comment_device": "",
            "comment_time": "",
            "comment_attitude": ""
            },
            "blog_attitude": ""
        }
