#!/usr/bin/python
#-*- coding: UTF-8 -*-

#filename: optOnMongo.py
#description: set interface for operations on blog data to pymongo
#author: warrior  ,mail: oowarrioroo@163.com
#data: 2015-12-31
#log:

"""
    set interface for operations on blog data to pymongo
"""

import pymongo
from pymongo import MongoClient
import time
from blogUnit import *
import pdb



#********************-----------------********************#

#********************-----------------********************#
class optOnMongo(object):
    '''
        operations on mongodb in python,
        like connect, insert, find, updata, delete
    '''
    def __init__(self):
        self.db_uri= ''
        self.db_name= ''
        self.xlient = ''
        self.db = ''
        self.db_opt_blog_unit = ''


    #-----------------********************-----------------#
    def connect2Mongo(self, db_uri, db_name):
        '''
            description:
                connect to the mongodb in python by db's uri
            input:
                db_name: name of mongodb to be connected
                db_uri: the uri of specified mongodb,
                        like "mongodb://[username:password@]host1[:port1][,host2[:port2],...[,hostN[:portN]]][/[database][?options]]"
            output:
                return statue number: 0:fail; 1:success
        '''
        self.db_uri = db_uri
        self.db_name = db_name
        #try connect to the specified mongodb
        try:
            self.xlient = MongoClient(self.db_uri)
            self.db = self.xlient[self.db_name]
            self.testResult = self.db.test123.find()
            for self.doc in self.testResult:
                print(self.doc)

            #self.address = self.xlient.client.address
            print("connect %s success!!" % self.db_name)
            return 1
        except :
            print("connect %s failure!!" % self.db_name)
            return 0


    #-----------------********************-----------------#
    def insertBlog2Mongo(self, dbInstance, blog_unit):
        '''
            description:
                insert a blog_unit to mongodb

            input:
                dbInstance: instance of mongodb to insert
                blog_unit: blog unit to be inserted

            output:
                return statue number: 0:fail; 1:success
        '''

        self.db = dbInstance
        self.db_opt_blog_unit = blog_unit
        self.db_opt_old_blog_unit = self.db.blog.find_one({"_id":self.db_opt_blog_unit['_id']})
        if self.db_opt_old_blog_unit:
            print('blog is exist!! update now!!')
            self.updataBlog2Mongo(self.db, self.db_opt_old_blog_unit, self.db_opt_blog_unit)
        else:
            try:
                #del self.db_opt_blog_unit['_id']
                self.result = self.db.blog.insert_one(self.db_opt_blog_unit)
                print(self.result.inserted_id)
                self.db.blog.find(self.db_opt_blog_unit)
                print("insert success!!")
                return 1
            except :
                print("insert failure!!")
                return 0



    #-----------------********************-----------------#
    def insertBlogs2Mongo(self, dbInstance, blog_unit_list):
        '''
            description:
                insert a blog_unit to mongodb

            input:
                dbInstance: instance of mongodb to insert
                blog_unit_list: blog units to be inserted

            output:
                return statue number: 0:fail; 1:success
        '''

        self.db = dbInstance
        self.db_opt_blog_unit_list = blog_unit_list
        for self.db_opt_blog_unit in self.db_opt_blog_unit_list:
            self.insertBlog2Mongo(self.db, self.db_opt_blog_unit)


    #-----------------********************-----------------#
    def updataBlog2Mongo(self, dbInstance, old_blog_unit, new_blog_unit):
        '''
            description:
                updata the old_blog_unit to new_blog_unit on mongodb

            input:
                dbInstance: instance of mongodb to updata
                old_blog_unit: old blog unit content
                new_blog_unit: new bolg unit content to updata into mongodb

            output:
                return statue number: 0:fail; 1:success
        '''

        self.db = dbInstance

        self.old_blog_unit = old_blog_unit
        self.new_blog_unit = new_blog_unit

        try:

            self.result = self.db.blog.replace_one(
                self.old_blog_unit,
                self.new_blog_unit
            )
            #self.db.blog.find(self.new_blog_unit)
            print("updata success!!")
            print("matched count: %d" % self.result.matched_count)
            print("modified count: %d" % self.result.modified_count)
            return 1
        except :
            print("update failure!!")
            return 0


    #-----------------********************-----------------#
    def deleteBlog2Mongo(self, dbInstance, delete_blog_condition):
        '''
            description:
                delete blogs specified delete_blog_condition in dbInstance

            input:
                dbInstance: db instance of mongodb to delete
                delete_blog_condition: the matched blog

            output:
                return statue number: 0:fail; 1:success
        '''

        self.db = dbInstance
        self.delete_blog_condition = delete_blog_condition

        try:
            self.result = self.db.blog.delete_one(self.delete_blog_condition)
            #print "delete matced count: %" % self.result.matched_count
            print ("delete count: %d" % self.result.deleted_count)
            print ("delete success!!")
            return 1
        except :
            print ("delete failure!!")
            return 0

    #-----------------********************-----------------#
    def getBlog2Mongo(self, dbInstance, get_blog_condition, get_blog_unit):
        '''
            description:
                get blogs specified get_blog_condition in dbInstance

            input:
                dbInstance: db instance of mongodb to get
                get_blog_condition: the matched blog condition
                get_blog_unit: storage the blogs matched condition

            output:
                return statue number: 0:fail; 1:success
        '''

        self.db = dbInstance
        self.get_blog_condition = get_blog_condition
        self.get_blog_unit = []
        self.blog_number = 0
        try:
            self.result = self.db.blog.find(self.get_blog_condition)
            for self.db_opt_blog_unit in self.result :
                self.blog_number += 1
                self.get_blog_unit.append(self.db_opt_blog_unit)

            ##get_blog_unit = self.get_blog_unit
            print ("get blog count: %d" % self.blog_number)
            ##print self.get_blog_unit
            print("get blog success!!")
            return self.get_blog_unit
        except :
            print("get blog failure!!")
            return 0
