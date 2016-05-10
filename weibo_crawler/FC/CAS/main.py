#!/usr/bin/evn python
# -*- coding:utf-8 -*-

from Ngram import Ngram
from Dictionary import Dictionary


dict = Dictionary('dict/dict1.txt', 'dict/dict2.txt')
ngram = Ngram(dict)

while True :
	sentence = raw_input('\nInput a Chinese Sentence: ').decode('utf-8')
	senList = ngram.senSegment(sentence)
	print '/'.join(senList)
	
