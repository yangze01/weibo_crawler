#!/usr/bin/evn python
# -*- coding:utf-8 -*-
__author__ = 'Qhw'

#该程序用来初始化生成数量词表
import os
import sys  
reload(sys)  
sys.setdefaultencoding('utf-8')

NMWFILE = 'NumWord.txt'
total = 0
NumWord = [u'\uff11',u'\uff12',u'\uff13',u'\uff14',u'\uff15',u'\uff16',u'\uff17',u'\uff18',u'\uff19',u'\uff10',u'\u4e00',u'\u4e8c',u'\u4e09',u'\u56db',u'\u4e94',u'\u516d',u'\u4e03',u'\u516b',u'\u4e5d',u'\u96f6',u'\u5341',u'\u767e',u'\u5343',u'\u4e07',u'\u4ebf',u'\u5146',u'\uff2f']

if os.path.isfile(NMWFILE):
	os.remove(NMWFILE)
print 'Creating NumWord...'	

f = open(NMWFILE, 'a')
for item in range(len(NumWord)) :
	s = NumWord[item] + '\n'
	f.write(s)
	total += 1
f.close()
print 'NumWord created successly, Total:%d' % total