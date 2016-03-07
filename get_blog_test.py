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


from get_blogcont.analysisBlogPage import *
usernamePoolDir = '/home/warrior/Coding/usernamePool.txt'
userIDList = ['1929644930', '1497035431', '1991303247']
analisysInstace = analisysBlogPage()
analisysInstace.startBlogAnalysisWork(userIDList, usernamePoolDir)
print analisysInstace.normalizeTimeFrom('今天 11:11')
