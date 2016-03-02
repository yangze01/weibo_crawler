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
from blogUnit import *
from optOnMongo import *
#********************-----------------********************#

#********************-----------------********************#
db_uri = "mongodb://labUser:aaaaaa@localhost:27017/?authSource=lab"
db_name = "lab"

old_blogdata = blogUnit()
old_blogdata.blog_unit['blog']['blog_id'] = '5'

new_blogdata = blogUnit()
new_blogdata.blog_unit['attitude'] = 'good'

null_blogdata = blogUnit()
get_blog_unit = []
opt = optOnMongo()
print opt.connect2Mongo(db_uri, db_name)
print opt.insertBlog2Mongo(opt.db, old_blogdata.blog_unit)
print opt.updataBlog2Mongo(opt.db, old_blogdata.blog_unit, new_blogdata.blog_unit)
print opt.getBlog2Mongo(opt.db, new_blogdata.blog_unit, get_blog_unit)
print opt.deleteBlog2Mongo(opt.db, new_blogdata.blog_unit)
