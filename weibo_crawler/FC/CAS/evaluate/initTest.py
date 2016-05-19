#!/usr/bin/evn python
# -*- coding:utf-8 -*-

#该程序用于生成测试文本和答案文本

import re

TRAINFILE	= '../dict/TrainData.txt'	#训练集文件名
TESTFILE	= 'Test.txt'				#生成的测试集文件名
GOLDFILE	= 'gold.txt'				#生成的正确答案文件名
SEP			= ' '						#训练集的分词符
MAXROW		= 120						#总行数


regular = u'(' + SEP + u')'
p = re.compile(regular) 

f = open(TRAINFILE)
wf = open(TESTFILE, 'w')
gf = open(GOLDFILE, 'w')

for i in range(MAXROW):
	lineStr = f.readline()
	if len(lineStr) == 0:
		break
	gf.write(lineStr)
	lineStr = p.sub('',lineStr)
	wf.write(lineStr)

f.close()
wf.close()
gf.close()