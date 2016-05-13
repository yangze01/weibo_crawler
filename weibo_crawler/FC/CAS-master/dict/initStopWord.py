#!/usr/bin/evn python
# -*- coding:utf-8 -*-
__author__ = 'Qhw'

#该程序用来初始化生成停顿词表
import os
import sys  
reload(sys)  
sys.setdefaultencoding('utf-8')

STWFILE = 'StopWord.txt'
total = 0
StopWordtmp = [' ', u'\u3000',u'\u3001', u'\u300a', u'\u300b', u'\uff1b', u'\uff02', u'\u30fb', u'\u25ce',  u'\x30fb', u'\u3002', u'\uff0c', u'\uff01', u'\uff1f', u'\uff1a', u'\u201c', u'\u201d', u'\u2018', u'\u2019', u'\uff08', u'\uff09', u'\u3010', u'\u3011', u'\uff5b', u'\uff5d', u'-', u'\uff0d', u'\uff5e', u'\uff3b', u'\uff3d', u'\u3014', u'\u3015', u'\uff0e', u'\uff20', u'\uffe5', u'\u2022', u'.']

if os.path.isfile(STWFILE):
	os.remove(STWFILE)
print 'Creating stopword...'	

f = open(STWFILE, 'a')
for item in range(len(StopWordtmp)) :
	s = StopWordtmp[item] + '\n'
	f.write(s)
	total += 1
f.close()
print 'StopWord created successly, Total:%d' % total