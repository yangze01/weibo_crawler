#!/usr/bin/evn python
# -*- coding:utf-8 -*-

#该程序用来初始化生成字典

import os

TRAINSET_FILE 	= 'TrainData.txt'	#训练集数据文件名
DICT1_FILE		= 'dict1.txt'			#需要生成的1元字典文件名
DICT2_FILE		= 'dict2.txt'			#需要生成的2元字典文件名
SEP				= ' '				#分隔符

def creatDict_1(trainsfile, dictfile) :
#通过训练集生成1元频数字典
#参数：
#		trainsfile 	训练集文件
#		dictfile 		生成字典文件
#字典格式：
#		keyword frequency
#		起始符：<s>
#		结束符：</s>

	if os.path.isfile(dictfile):
		os.remove(dictfile)
	print 'Creating dict1...'	
	
	dicMap = {}	#字典Map
	types = 0		#记录Types数目
	tokens = 0	#记录Tokens数目
	
	f = open(trainsfile)
	wf = open(dictfile, 'a')
	
	#遍历训练集生成dicMap
	for line in f :
		lineList = line.strip().decode('utf-8').split(SEP)
		if len(lineList) > 0 :
			#处理起始符
			if not dicMap.has_key('<s>') :
				dicMap['<s>'] = 1
				types += 1
			else:
				dicMap['<s>'] += 1
			
			#处理中间词
			for item in lineList :
				if item != '':					
					if not dicMap.has_key(item) :
						dicMap[item] = 1
						types += 1
					else:
						dicMap[item] += 1
					tokens += 1
			
			#处理结束符
			if not dicMap.has_key('</s>') :
				dicMap['</s>'] = 1
				types += 1
			else:
				dicMap['</s>'] += 1
				
			tokens += 2	#起始符和结束符的tokens
			
	dicList = sorted(dicMap.items(), key=lambda d:d[0])	#按key排序
	
	#将dicList写入文件
	for item in dicList :
		wStr = item[0].encode('utf-8') + ' ' + str(item[1]) + '\n' 
		wf.write(wStr)
	f.close()
	wf.close()
	print 'Dict1 created successly, Types:%d, Tokens:%d' % (types, tokens)	

def creatDict_2(trainsfile, dictfile) :
#通过训练集生成2元频数字典
#参数：
#		trainsfile 	训练集文件
#		dictfile 		生成字典文件
#字典格式：
#		keyword1 keyword2 frequency
#		起始符：<s>
#		结束符：</s>

	if os.path.isfile(dictfile):
		os.remove(dictfile)
	print 'Creating dict2...'	
	
	f = open(trainsfile)
	wf = open(dictfile, 'a')
	
	dicMap = {}	#字典Map，结构{'word1':{'postword1': value1, 'postword2': value2, ...}, ...}
	dicMap['<s>'] = {}
	types = 0		#记录Types数目
	tokens = 0	#记录Tokens数目
	
	#遍历训练集生成dicMap
	for line in f :
		lineList = line.strip().decode('utf-8').split(SEP)
		
		#对起始符处理
		if lineList[0] != '' :
			tokens += 1
			if not dicMap['<s>'].has_key(lineList[0]) :
				types += 1
				dicMap['<s>'][lineList[0]] = 1
			else:
				dicMap['<s>'][lineList[0]] += 1
		
		#对中间单词处理
		for i in range(len(lineList) - 1) :
			if lineList[i] != '' and (not dicMap.has_key(lineList[i])) :
				dicMap[lineList[i]] = {}
			if lineList[i] != '' :
				if not dicMap[lineList[i]].has_key(lineList[i+1]) :
					types += 1
					dicMap[lineList[i]][lineList[i+1]] = 1
				else:
					dicMap[lineList[i]][lineList[i+1]] += 1
				tokens += 1
				
		#对结束符处理
		if lineList[-1] != '' and (not dicMap.has_key(lineList[-1])) :
			dicMap[lineList[-1]] = {}
		if lineList[-1] != '' :
			tokens += 1
			if not dicMap[lineList[-1]].has_key('</s>') :
				types += 1
				dicMap[lineList[-1]]['</s>'] = 1
			else:
				dicMap[lineList[-1]]['</s>'] += 1
	dicList = sorted(dicMap.items(), key=lambda d:d[0])	#按key排序
	#将dicList写入文件
	for item in dicList :
		subList = sorted(item[1].items(), key = lambda d:d[0])
		for subitem in subList :
			wStr = item[0].encode('utf-8') + ' ' + subitem[0].encode('utf-8') + ' ' + str(subitem[1]) + '\n'
			wf.write(wStr)
	f.close()
	wf.close()
	print 'Dict2 created successly, Types:%d, Tokens:%d' % (types, tokens)			
	
if __name__ == '__main__' :
	if not os.path.isfile(TRAINSET_FILE):	
		print '训练集"%s"不存在 ！' % TRAINSET_FILE
	else:
		creatDict_1(TRAINSET_FILE, DICT1_FILE)
		creatDict_2(TRAINSET_FILE, DICT2_FILE)
	