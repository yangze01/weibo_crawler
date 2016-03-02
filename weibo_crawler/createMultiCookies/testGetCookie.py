#!/usr/bin/python
#-*- coding: UTF-8 -*-

#filename: getRandomCookie.py
#description: get one rangdom cookie for crawler
#author: warrior  ,mail: oowarrioroo@163.com
#data: 2016-1-16
#log:


"""
    get one rangdom cookie for crawler

"""

from getRandomCookie import *
import re
from login import *
import random
import random
import urllib2
import cookielib


usernamePoolDir = '/home/warrior/Coding/usernamePool.txt'
userTempID = '1877161011'
test = getRandomCookie()
test.get5PagesOnce(userTempID,usernamePoolDir)
