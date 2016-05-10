#!/usr/bin/evn python
# -*- coding:utf-8 -*-

RESULTFILE	= 'evaluate/result.txt'
TRAINFILE	= 'evaluate/gold.txt'
SEP			= ' '

total_correct	= 0	#正确分词结果总数
total_result	= 0	#结果集分词总数
total_train		= 0	#训练集分词总数
total_row		= 0	#总行数

rf = open(RESULTFILE)
tf = open(TRAINFILE)

while True:
	rLineStr = rf.readline().strip()
	tLineStr = tf.readline().strip()
	if len(rLineStr) == 0 or len(tLineStr) == 0:
		break
	
	rList = []
	tList = []
	
	pos = 0
	for i in range(1,len(rLineStr)):
		if rLineStr[i] == SEP:
			node = (pos, i)
			rList.append(node)
			pos = i
	lastNode = (pos, len(rLineStr))	
	rList.append(lastNode)
	
	pos = 0
	for i in range(1,len(tLineStr)):
		if tLineStr[i] == SEP:
			node = (pos, i)
			tList.append(node)
			pos = i
	lastNode = (pos, len(tLineStr))
	tList.append(lastNode)
	
	CountR = len(rList)
	CountT = len(tList)
	CountC = 0
	for item in rList:
		if item in tList:
			CountC += 1
	
	total_correct += CountC
	total_result += CountR
	total_train += CountT
	
	total_row += 1
	#lineP = float(CountC) / CountR
	#lineR = float(CountC) / CountT
	#lineF = 2 * lineP * lineR / (lineP + lineR)

P = float(total_correct) / total_result
R = float(total_correct) / total_train
if P + R != 0:
	F = 2 * P * R / (P + R)	
else:
	F = 0

print '\n答案文本：', TRAINFILE
print '结果文本：', RESULTFILE
print '\n测试总行数：', total_row
print '答案分词总数：', total_train
print '程序分词总数：', total_result
print '正确总数：', total_correct
print '正确率:', P
print '召回率:', R
print 'F值:', F
	
	
	
	
	
	
	
	
	
	
	