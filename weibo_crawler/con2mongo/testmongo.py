#!/usr/bin/python
#-*- coding: UTF-8 -*-
from UserOnMongo import *
from user_unit import *


db_uri = "mongodb://labUser:aaaaaa@localhost:27017/?authSource=lab"
db_name = "lab"

old_userdata = userUnit()
old_userdata.user_unit["userinfo"]["vip"]='2'

new_userdata = userUnit()
new_userdata.user_unit["_id"]="123"
opt = UseroptOnMongo()
print opt.connect2Mongo(db_uri,db_name)
print opt.insertUser2Mongo(opt.db,old_userdata.user_unit)
print opt.deleteUser2Mongo(opt.db,old_userdata.user_unit)
