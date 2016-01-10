#!/usr/bin/python
#-*- coding: UTF-8 -*-

#filename: py2mongoTest.py
#description: the test manage on mongodb in python
#author: warrior  ,mail: oowarrioroo@163.com
#data: 2015-12-30
#log:

"""
    test the operates on mongodb in python
"""
from con2mongo.blogUnit import *
from con2mongo.optOnMongo import *
import time

#********************-----------------********************#

#********************-----------------********************#
db_uri = "mongodb://labUser:aaaaaa@localhost:27017/?authSource=lab"
db_name = "lab"

old_blogdata = blogUnit()
old_blogdata.blog_unit = {'blog': {'blog_id': 'M_D9Cx6tkCn', 'content': {'url_name': ['http://t.cn/R4UWtbd'], 'topic_name': [], 'mention_name': [], 'text_content': '\xe3\x80\x90\xe4\xb8\xad\xe5\x9b\xbd\xe2\x80\x9c\xe5\xbd\xa9\xe8\x99\xb9\xe2\x80\x9d\xe6\x97\xa0\xe4\xba\xba\xe6\x9c\xba\xe5\x8a\xa9\xe4\xbc\x8a\xe6\x8b\x89\xe5\x85\x8b\xe6\x91\xa7\xe6\xaf\x81IS\xe6\x8d\xae\xe7\x82\xb9(\xe5\x9b\xbe)_\xe6\x89\x8b\xe6\x9c\xba\xe6\x96\xb0\xe6\xb5\xaa\xe7\xbd\x91\xe3\x80\x91\xe6\x88\x91\xe5\x88\x9a\xe5\x88\x9a[good]\xe4\xba\x86\xe8\xbf\x99\xe7\xaf\x87\xe6\x96\x87\xe7\xab\xa0\xef\xbc\x8c\xe5\xb0\x8f\xe4\xbc\x99\xe4\xbc\xb4\xe4\xbd\xa0\xe4\xbb\xac\xe6\x80\x8e\xe4\xb9\x88\xe7\x9c\x8b\xef\xbc\x9f  http://t.cn/R4UWtbd', 'topic_content': [], 'url_content': ['http://weibo.cn/sinaurl?f=w&amp;u=http%3A%2F%2Ft.cn%2FR4UWtbd&amp;ep=D9Cx6tkCn%2C2631208437%2CD9Cx6tkCn%2C2631208437'], 'mention_content': []}, 'blog_address': 'no address', 'time': '2015-12-22 19:17:22', 'device': '\xe6\x89\x8b\xe6\x9c\xba\xe6\x96\xb0\xe6\xb5\xaa\xe7\xbd\x91', 'blog_attitude': '0'}, 'comment': [],  'user_ID': '2631208437', 'repost': []}
blog_unit_list = []
new_blogdata = blogUnit()
new_blogdata.blog_unit['attitude'] = 'good'

null_blogdata = blogUnit()
get_blog_unit = []
opt = optOnMongo()
print opt.connect2Mongo(db_uri, db_name)
#print opt.insertBlog2Mongo(opt.db, old_blogdata.blog_unit)
old_blogdata.blog_unit['blog']['blog_id'] = '1'
blog_unit_list.append(old_blogdata.blog_unit)
##print opt.insertBlog2Mongo(opt.db, old_blogdata.blog_unit)
old_blogdata.blog_unit['blog']['blog_id'] = '2'
blog_unit_list.append(old_blogdata.blog_unit)
#print opt.insertBlog2Mongo(opt.db, old_blogdata.blog_unit)
old_blogdata.blog_unit['blog']['blog_id'] = '3'
blog_unit_list.append(old_blogdata.blog_unit)
#print opt.insertBlog2Mongo(opt.db, old_blogdata.blog_unit)
old_blogdata.blog_unit['blog']['blog_id'] = '4'
blog_unit_list.append(old_blogdata.blog_unit)
#print opt.insertBlog2Mongo(opt.db, old_blogdata.blog_unit)
old_blogdata.blog_unit['blog']['blog_id'] = '5'
blog_unit_list.append(old_blogdata.blog_unit)
#print opt.insertBlog2Mongo(opt.db, old_blogdata.blog_unit)
old_blogdata.blog_unit['blog']['blog_id'] = '6'
blog_unit_list.append(old_blogdata.blog_unit)
#print opt.insertBlog2Mongo(opt.db, old_blogdata.blog_unit)
old_blogdata.blog_unit['blog']['blog_id'] = '7'
new_blogdata.blog_unit = old_blogdata.blog_unit
blog_unit_list.append(old_blogdata.blog_unit)
#print opt.insertBlog2Mongo(opt.db, old_blogdata.blog_unit)
##print opt.insertBlog2Mongo(opt.db, old_blogdata.blog_unit)
time.sleep(2)
#print opt.insertBlogs2Mongo(opt.db, blog_unit_list)
#print opt.db.blog.insert_one({'blog': {'blog_id': 'M_D9Cx6tkCn', 'content': {'url_name': ['http://t.cn/R4UWtbd'], 'topic_name': [], 'mention_name': [], 'text_content': '\xe3\x80\x90\xe4\xb8\xad\xe5\x9b\xbd\xe2\x80\x9c\xe5\xbd\xa9\xe8\x99\xb9\xe2\x80\x9d\xe6\x97\xa0\xe4\xba\xba\xe6\x9c\xba\xe5\x8a\xa9\xe4\xbc\x8a\xe6\x8b\x89\xe5\x85\x8b\xe6\x91\xa7\xe6\xaf\x81IS\xe6\x8d\xae\xe7\x82\xb9(\xe5\x9b\xbe)_\xe6\x89\x8b\xe6\x9c\xba\xe6\x96\xb0\xe6\xb5\xaa\xe7\xbd\x91\xe3\x80\x91\xe6\x88\x91\xe5\x88\x9a\xe5\x88\x9a[good]\xe4\xba\x86\xe8\xbf\x99\xe7\xaf\x87\xe6\x96\x87\xe7\xab\xa0\xef\xbc\x8c\xe5\xb0\x8f\xe4\xbc\x99\xe4\xbc\xb4\xe4\xbd\xa0\xe4\xbb\xac\xe6\x80\x8e\xe4\xb9\x88\xe7\x9c\x8b\xef\xbc\x9f  http://t.cn/R4UWtbd', 'topic_content': [], 'url_content': ['http://weibo.cn/sinaurl?f=w&amp;u=http%3A%2F%2Ft.cn%2FR4UWtbd&amp;ep=D9Cx6tkCn%2C2631208437%2CD9Cx6tkCn%2C2631208437'], 'mention_content': []}, 'blog_address': 'no address', 'time': '2015-12-22 19:17:22', 'device': '\xe6\x89\x8b\xe6\x9c\xba\xe6\x96\xb0\xe6\xb5\xaa\xe7\xbd\x91', 'blog_attitude': '0'}, 'comment': [],  'user_ID': '2631208437', 'repost': []})
old_blogdata.blog_unit['blog']['blog_id'] = '6'
print opt.insertBlog2Mongo(opt.db, old_blogdata.blog_unit)
print old_blogdata.blog_unit
del old_blogdata.blog_unit['_id']
print opt.insertBlog2Mongo(opt.db, old_blogdata.blog_unit)
print old_blogdata.blog_unit
del old_blogdata.blog_unit['_id']
#print opt.db.blog.insert_one({'blog': {'blog_id': 'M_D9Cx6tkCn', 'content': {'url_name': ['http://t.cn/R4UWtbd'], 'topic_name': [], 'mention_name': [], 'text_content': '\xe3\x80\x90\xe4\xb8\xad\xe5\x9b\xbd\xe2\x80\x9c\xe5\xbd\xa9\xe8\x99\xb9\xe2\x80\x9d\xe6\x97\xa0\xe4\xba\xba\xe6\x9c\xba\xe5\x8a\xa9\xe4\xbc\x8a\xe6\x8b\x89\xe5\x85\x8b\xe6\x91\xa7\xe6\xaf\x81IS\xe6\x8d\xae\xe7\x82\xb9(\xe5\x9b\xbe)_\xe6\x89\x8b\xe6\x9c\xba\xe6\x96\xb0\xe6\xb5\xaa\xe7\xbd\x91\xe3\x80\x91\xe6\x88\x91\xe5\x88\x9a\xe5\x88\x9a[good]\xe4\xba\x86\xe8\xbf\x99\xe7\xaf\x87\xe6\x96\x87\xe7\xab\xa0\xef\xbc\x8c\xe5\xb0\x8f\xe4\xbc\x99\xe4\xbc\xb4\xe4\xbd\xa0\xe4\xbb\xac\xe6\x80\x8e\xe4\xb9\x88\xe7\x9c\x8b\xef\xbc\x9f  http://t.cn/R4UWtbd', 'topic_content': [], 'url_content': ['http://weibo.cn/sinaurl?f=w&amp;u=http%3A%2F%2Ft.cn%2FR4UWtbd&amp;ep=D9Cx6tkCn%2C2631208437%2CD9Cx6tkCn%2C2631208437'], 'mention_content': []}, 'blog_address': 'no address', 'time': '2015-12-22 19:17:22', 'device': '\xe6\x89\x8b\xe6\x9c\xba\xe6\x96\xb0\xe6\xb5\xaa\xe7\xbd\x91', 'blog_attitude': '0'}, 'comment': [],  'user_ID': '2631208437', 'repost': []})
#print opt.updataBlog2Mongo(opt.db, old_blogdata.blog_unit, new_blogdata.blog_unit)
print opt.getBlog2Mongo(opt.db, old_blogdata.blog_unit, get_blog_unit)
#print opt.deleteBlog2Mongo(opt.db, new_blogdata.blog_unit)
