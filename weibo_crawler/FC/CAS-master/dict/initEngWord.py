#!/usr/bin/evn python
# -*- coding:utf-8 -*-
__author__ = 'Qhw'

#该程序用来初始化生成英文词表
import os
import sys  
reload(sys)  
sys.setdefaultencoding('utf-8')

ENGFILE = 'EngWord.txt'
total = 0
Englist = [u'\uff41',u'\uff42',u'\uff43',u'\uff44',u'\uff45',u'\uff46',u'\uff47',u'\uff48',u'\uff49',u'\uff47',u'\uff4b',u'\uff4c',u'\uff4d',u'\uff4e',u'\uff4f',u'\uff50',u'\uff51',u'\uff52',u'\uff53',u'\uff54',u'\uff55',u'\uff56',u'\uff57',u'\uff58',u'\uff59',u'\uff5a',u'\uff21',u'\uff22',u'\uff23',u'\uff24',u'\uff25',u'\uff26',u'\uff27',u'\uff28',u'\uff29',u'\uff2a',u'\uff2b',u'\uff2c',u'\uff2d',u'\uff2e',u'\uff2f',u'\uff30',u'\uff31',u'\uff32',u'\uff33',u'\uff35',u'\uff36',u'\uff37',u'\uff38',u'\uff39',u'\uff3a']

if os.path.isfile(ENGFILE):
	os.remove(ENGFILE)
print 'Creating EngWord...'	

f = open(ENGFILE, 'a')
for item in range(len(Englist)) :
	s = Englist[item] + '\n'
	f.write(s)
	total += 1
f.close()
print 'EngWord created successly, Total:%d' % total