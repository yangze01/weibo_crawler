#-*- coding: UTF-8 -*-
import pymongo

conn = pymongo.Connection()
db = conn.test
users = db.users

users.save()
