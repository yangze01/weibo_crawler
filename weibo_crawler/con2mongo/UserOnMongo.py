#!/usr/bin/python
#-*- coding: UTF-8 -*-

#filename: optOnMongo.py
#description: set interface for operations on user data to pymongo
#author: warrior  ,mail: oowarrioroo@163.com
#data: 2015-12-31
#log:

"""
    set interface for operations on user data to pymongo
"""

import pymongo
from pymongo import MongoClient
import time
from user_Unit import *
import pdb



#********************-----------------********************#

#********************-----------------********************#
class UseroptOnMongo(object):
    '''
        operations on mongodb in python,
        like connect, insert, find, updata, delete
    '''
    def __init__(self):
        self.db_uri= ''
        self.db_name= ''
        self.xlient = ''
        self.db = ''
        self.db_opt_user_unit = ''


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
                print self.doc

            #self.address = self.xlient.client.address
            print "connect %s success!!" % self.db_name
            return 1
        except :
            print "connect %s failure!!" % self.db_name
            return 0


    #-----------------********************-----------------#
    def insertUser2Mongo(self, dbInstance, user_unit):
        '''
            description:
                insert a user_unit to mongodb

            input:
                dbInstance: instance of mongodb to insert
                user_unit: user unit to be inserted

            output:
                return statue number: 0:fail; 1:success
        '''

        self.db = dbInstance
        self.db_opt_user_unit = user_unit
        self.db_opt_old_user_unit = self.db.user.find_one({"_id":self.db_opt_user_unit['_id']})
        if self.db_opt_old_user_unit:
            print 'user is exist!! update now!!'
            self.updataUser2Mongo(self.db, self.db_opt_old_user_unit, self.db_opt_user_unit)
        else:

            try:
                #del self.db_opt_user_unit['_id']
                self.result = self.db.user.insert_one(self.db_opt_user_unit)
                print self.result.inserted_id
                self.db.user.find(self.db_opt_user_unit)
                print "insert success!!"
                return 1
            except :
                print "insert failure!!"
                return 0



    #-----------------********************-----------------#
    def insertUsers2Mongo(self, dbInstance, user_unit_list):
        '''
            description:
                insert a user_unit to mongodb

            input:
                dbInstance: instance of mongodb to insert
                user_unit_list: user units to be inserted

            output:
                return statue number: 0:fail; 1:success
        '''

        self.db = dbInstance
        self.db_opt_user_unit_list = user_unit_list
        for self.db_opt_user_unit in self.db_opt_user_unit_list:
            self.insertUser2Mongo(self.db, self.db_opt_user_unit)


    #-----------------********************-----------------#
    def updataUser2Mongo(self, dbInstance, old_user_unit, new_user_unit):
        '''
            description:
                updata the old_user_unit to new_user_unit on mongodb

            input:
                dbInstance: instance of mongodb to updata
                old_user_unit: old user unit content
                new_user_unit: new user unit content to updata into mongodb

            output:
                return statue number: 0:fail; 1:success
        '''

        self.db = dbInstance

        self.old_user_unit = old_user_unit
        self.new_user_unit = new_user_unit

        try:

            self.result = self.db.user.replace_one(
                self.old_user_unit,
                self.new_user_unit
            )
            #self.db.user.find(self.new_user_unit)
            print "updata success!!"
            print "matched count: %d" % self.result.matched_count
            print "modified count: %d" % self.result.modified_count
            return 1
        except :
            print "update failure!!"
            return 0


    #-----------------********************-----------------#
    def deleteUser2Mongo(self, dbInstance, delete_user_condition):
        '''
            description:
                delete users specified delete_user_condition in dbInstance

            input:
                dbInstance: db instance of mongodb to delete
                delete_user_condition: the matched user

            output:
                return statue number: 0:fail; 1:success
        '''

        self.db = dbInstance
        self.delete_user_condition = delete_user_condition

        try:
            self.result = self.db.user.delete_one(self.delete_user_condition)
            #print "delete matced count: %" % self.result.matched_count
            print "delete count: %d" % self.result.deleted_count
            print "delete success!!"
            return 1
        except :
            print "delete failure!!"
            return 0

    #-----------------********************-----------------#
    def getUser2Mongo(self, dbInstance, get_user_condition, get_user_unit):
        '''
            description:
                get users specified get_user_condition in dbInstance

            input:
                dbInstance: db instance of mongodb to get
                get_user_condition: the matched user condition
                get_user_unit: storage the users matched condition

            output:
                return statue number: 0:fail; 1:success
        '''

        self.db = dbInstance
        self.get_user_condition = get_user_condition
        self.get_user_unit = []
        self.user_number = 0
        try:
            self.result = self.db.user.find(self.get_user_condition)
            for self.db_opt_user_unit in self.result :
                self.user_number += 1
                self.get_user_unit.append(self.db_opt_user_unit)

            ##get_user_unit = self.get_user_unit
            print "get user count: %d" % self.user_number
            ##print self.get_user_unit
            print "get user success!!"
            return self.get_user_unit
        except :
            print "get user failure!!"
            return 0
