#!/usr/bin/evn python
# -*- coding:utf-8 -*-

from Ngram import Ngram
from Dictionary import Dictionary

DICTFILE1	= 'dict/dict1.txt'
DICTFILE2	= 'dict/dict2.txt'
TESTFILE	= 'evaluate/test.txt'
OUTFILE		= 'evaluate/result.txt'
SEP			= ' '

dict = Dictionary(DICTFILE1, DICTFILE2)
ngram = Ngram(dict)

f = open(TESTFILE)
wf = open(OUTFILE,'w')

total_row = 0	#总行数


while True:
	inStr = f.readline().strip().decode('utf-8')
	if len(inStr) == 0:
		break
	lineList = ngram.senSegment(inStr)
	outStr = SEP.join(lineList) + '\n'
	wf.write(outStr.encode('utf-8'))
	total_row += 1
	print outStr

print '测试文本：',TESTFILE
print '结果文本：', OUTFILE
print '总行数：', total_row
f.close()
wf.close()

