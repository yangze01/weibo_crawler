#!/usr/bin/evn python
# -*- coding:utf-8 -*-

#字典类，同时载入1元字典和2元字典
SEP = ' '	#字典分隔符

class Dictionary:
	def __init__(self, dict1, dict2):
		self.dict1Map = {}
		self.dict2Map = {}
		self.N1 = 0
		self.N2 = 0
		self.V1 = 0
		self.V2 = 0
		
		#载入1元字典
		f = open(dict1)
		print '\nloading unigram dict ...'
		for line in f :
			line = line.strip().decode('utf-8')
			if line != '' :
				strlist = line.split(SEP)
				self.dict1Map[strlist[0]] = int(strlist[1])
				self.N1 += int(strlist[1])
				self.V1 += 1
		f.close()
		print 'unigram dict load successly!'
		print 'tokens:', self.N1
		print 'types:', self.V1
		
		#载入2元字典
		f = open(dict2)
		print '\nloading bigram dict ...'
		for line in f :
			line = line.strip().decode('utf-8')
			if line != '' :
				strlist = line.split(SEP)
				if not self.dict2Map.has_key(strlist[0]) :
					self.dict2Map[strlist[0]] = {}
				self.dict2Map[strlist[0]][strlist[1]] = int(strlist[2])
				self.N2 += int(strlist[2])
				self.V2 += 1
		f.close()
		print 'bigram dict load successly!'
		print 'tokens:', self.N2
		print 'types:', self.V2
		
	def getCount(self, wordtuple):
	#获取单词在字典中的频数，返回C(w)或C(w1,w2)
		if not isinstance(wordtuple, tuple):
			if self.dict1Map.has_key(wordtuple):
				return self.dict1Map[wordtuple]
			else:
				return 0
		else:
			if self.dict2Map.has_key(wordtuple[0]):
				if self.dict2Map[wordtuple[0]].has_key(wordtuple[1]):
					return self.dict2Map[wordtuple[0]][wordtuple[1]]
			return 0
	
	def getP(self, wordtuple):
	#获取单词在字典中的频率，返回P(w)
	#若为二元组，(w1, w2)，返回P(w2|w1)
	#不进行平滑处理
		if not isinstance(wordtuple, tuple):
			c = self.getCount(wordtuple)
			return float(c) / self.N1
		else:
			cw1 = self.getCount(wordtuple[0])
			cw1w2 = self.getCount(wordtuple)
			if cw1 != 0 :
				return float(cw1w2) / cw1
			else:
				return 0
	
	def isWord(self, word) :
	#判断是否是一个单词
		return self.dict1Map.has_key(word)
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		