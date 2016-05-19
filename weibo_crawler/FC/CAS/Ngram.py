#!/usr/bin/evn python
# -*- coding:utf-8 -*-

#Ngram模块

SPAN = 16	#最大词长

class Ngram :
	def __init__(self, dict) :
		self.dict	= dict						#初始化字典
		self.fnP	= self.plusDelta				#平滑算法（unSmooth，plusDelta，constantSet）
	
	def getBestWord(self, sentence, pos, best_word_list):
	#获得以pos位置为尾的最佳词，返回该词的起始位置和累积概率，best_word_list为最佳词列表
		
		max_word_length = min(pos, SPAN)	#最大词长
		tmp_list = []						#存储临时词list
		
		#以不同长度遍历所有可能的词
		for word_len in range(1, max_word_length+1):
			word_pos = pos - word_len		#该词的起始位置
			word = sentence[word_pos:pos]	#该词的片段
			
			#计算从该词的前驱词指向该词的转移概率
			if word_pos == 0:
			#若该词为句首词，以<s>为前驱计算
				transP = self.fnP(('<s>', word))
			else:
			#否则，通过该词的最佳前驱词计算
				pre_pos = best_word_list[word_pos]['pre_pos']
				pre_word = sentence[pre_pos:word_pos]
				transP = self.fnP((pre_word, word))
			
			#获取该词最佳前驱词的累积概率
			pre_P = best_word_list[word_pos]['P']
			
			#获取当前词的概率
			#cur_P = self.fnP(word)
			
			#计算当前词的累积概率
			#公式P(wi) = P(wi-1) * P(wi|wi-1)
			P = pre_P * transP
			
			#将该词加入临时词list
			tmp_list.append((word_pos, P))
		
		#从临时前驱词list中找到累积概率最大的词返回
		(best_word, best_P) = max(tmp_list, key = lambda d:d[1])
		
		return (best_word, best_P)
		
	def senSegment(self, sen):
		sen = sen.strip()
		slen = len(sen)
		
		#初始化最佳词list，best_word_list[i]表示以第i个位置结尾的最佳词信息，i=0时表示句首
		best_word_list = []
		ini_node = {}
		ini_node['pre_pos'] = -1
		ini_node['P'] = 1
		best_word_list.append(ini_node)
	
		#从前往后寻找每个位置的最佳词，写入best_word_list
		for pos in range(1, slen+1):
			(best_word, best_P) = self.getBestWord(sen, pos, best_word_list)
			
			#加入最佳词list
			cur_node = {}
			cur_node['pre_pos'] = best_word
			cur_node['P'] = best_P
			best_word_list.append(cur_node)
		
		#从最后位置回溯，得到最优路径
		best_path = []
		pos = slen
		best_path.append(pos)
		while True:
			pre_pos = best_word_list[pos]['pre_pos']
			if pre_pos == -1:
				break
			best_path.insert(0, pre_pos)
			pos = pre_pos
		
		#构建分词list
		senList = []
		for i in range(len(best_path)-1):
			word_left = best_path[i]
			word_right = best_path[i+1]
			word = sen[word_left:word_right]
			senList.append(word)
		
		return senList
			
	def plusDelta(self, wordtuple, Delta = 1):
	#返回加1平滑后的概率P(w)或P(w2|w1)
		if not isinstance(wordtuple, tuple):
			#原始数目
			c = self.dict.getCount(wordtuple)
			#平滑过后的概率
			p = float(c + Delta) / (self.dict.N1 + self.dict.V1 * Delta)
		else:
			#原始数目
			cw1w2 = self.dict.getCount(wordtuple)
			cw1 = self.dict.getCount(wordtuple[0])
			#平滑过后的概率
			p = float(cw1w2 + Delta) / (cw1 + self.dict.V2 * Delta)
		return p			
			
	def unSmooth(self, wordtuple):
	#返回不经平滑的概率P(w)或P(w2|w1)
		return self.dict.getP(wordtuple)
			
	def constantSet(self, wordtuple, Delta = 0.5):
	#对数目为0的恒置为0.5
		if not isinstance(wordtuple, tuple):
			#原始数目
			c = self.dict.getCount(wordtuple)
			if c == 0:
				c = Delta
			p = float(c) / self.dict.N1
		else:
			#原始数目
			cw1w2 = self.dict.getCount(wordtuple)
			cw1 = self.dict.getCount(wordtuple[0])
			#平滑过后的概率
			if cw1 == 0:
				cw1w2 = 0.5
				cw1 = 0.5 / self.dict.N1
			elif cw1w2 == 0:
				cw1w2 = 0.5
			p = float(cw1w2) / cw1
		return p
		