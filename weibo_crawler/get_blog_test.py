#!/usr/bin/python
#-*- coding: UTF-8 -*-

#filename: get_blog_test.py
#description: the test manage on getting blog content in python
#author: warrior  ,mail: oowarrioroo@163.com
#data: 2016-1-2
#log:

"""
    the test manage on getting blog content in python
"""
from get_blogcont.getlastdata import *

from get_blogcont.analysisBlogPage import *
usernamePoolDir = '/home/john/userpool1.txt'
userIDList = list(get_visited("/home/john/visited1.txt"))
analisysInstace = analisysBlogPage()
analisysInstace.startBlogAnalysisWork(userIDList, usernamePoolDir)
print analisysInstace.normalizeTimeFrom('今天 11:11')
