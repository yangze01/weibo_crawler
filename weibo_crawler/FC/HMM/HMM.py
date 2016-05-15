#!/usr/bin/python
#-*-coding:utf-8
import os
import sys
import pdb
import re
import math
from pymongo import MongoClient
import pymongo
import time
import json
import time
import pdb
def load_model(f_name):
    ifp = open(f_name, 'rb')
    return eval(ifp.read())
# def viterbi(obs, states, start_p, trans_p, emit_p):
#     V = [{}] #tabular
#     path = {}
#     for y in states: #init
#         V[0][y] = start_p[y] * emit_p[y].get(obs[0],0)
#         path[y] = [y]
#     for t in range(1,len(obs)):
#         V.append({})
#         newpath = {}
#         for y in states:
#             (prob,state ) = max([(V[t-1][y0] * trans_p[y0].get(y,0) * emit_p[y].get(obs[t],0) ,y0) for y0 in states if V[t-1][y0]>0])
#             V[t][y] =prob
#             newpath[y] = path[state] + [y]
#         path = newpath
#     (prob, state) = max([(V[len(obs) - 1][y], y) for y in states])
#     return (prob, path[state])

def viterbi(obs,states,prob_start,prob_trans,prob_emit):
	"""
	obs=observed values
	states=['B','M','E','S'] (Begin, Middle, End, Single word)
	prob_start=probability of start
	prob_trans=state-transition matrix
	Status(i)＝f({Status(i-1), Status(i-2), Status(i-3), ... Status(i - n)})
	prob_emit＝emission probability EmitProbMatrix
	P(Observed[i], Status[j]) = P(Status[j]) * P(Observed[i]|Status[j])
	"""
	v=[{}]
	path={}
	#init the start node
	for state in states:
		if obs[0] in prob_emit[state]:
			v[0][state]=math.exp(prob_start[state]*prob_emit[state][obs[0]])
		else:
			v[0][state]=0
		path[state]=[state]
	#print(path)
	# for all
	for i in range(1,len(obs)):
		v.append({})
		newpath={}
		for state in states:
			est_list=[]
			for pstate in [s for s in states if v[i-1][s]>0]:
				if obs[i] in prob_emit[state]:
					est_list.append((v[i-1][pstate]*math.exp(prob_trans[pstate][state]*prob_emit[state][obs[i]]),pstate))
				else:
					est_list.append((v[i-1][pstate],pstate))
			p,ps=max([(p,ps) for (p,ps) in est_list])
			v[i][state]=p
			newpath[state]= path[ps] + [state]
		path=newpath
	(prob, state) = max([(v[len(obs) - 1][state], state) for state in states])
	try:
		if prob_emit['M'][obs[-1]]> prob_emit['S'][obs[-1]]:
			(prob, state) = max([(v[len(obs) - 1][state], state) for state in ('S','E')])
	except:
	 	pass
	raw=""
	if path:
		for i,char in enumerate(obs):
			#Sprint(path)
			if path[state][i]=="E":
				raw+=char+"  "
			elif path[state][i]=="S":
				raw+=char+"  "
			else:
				raw+=char

		return (raw,"".join(path[state]))
	else:
		return ("","")
def cut(sentence):
    #pdb.set_trace()
    prob, pos_list =  viterbi(sentence,('B','M','E','S'), prob_start, prob_trans, prob_emit)
    return (prob,pos_list)

if __name__ == "__main__":
    prob_start = load_model("/home/john/pythonspace/sina_crawler/weibo_crawler/FC/HMM/prob_start.py")
    prob_trans = load_model("/home/john/pythonspace/sina_crawler/weibo_crawler/FC/HMM/prob_trans.py")
    prob_emit = load_model("/home/john/pythonspace/sina_crawler/weibo_crawler/FC/HMM/prob_emit.py")

    db_uri = "mongodb://labUser:aaaaaa@localhost:27017/?authSource=blog"
    db_name = "blog"
    xlient = MongoClient(db_uri)
    db = xlient[db_name]
    print(db)
    myiter = db.blog.find({"blog.content.text_content":{"$exists":1}},{"blog.content.text_content":1})
    length = 1000
    print("##")
    print(myiter[7]['blog']['content']['text_content'])
    i=0
    while i<length:
        print(i)
        test_str = myiter[i]['blog']['content']['text_content'].strip().strip('#')
        # print(test_str)
        prob,pos_list = cut(test_str)
        print(prob)
        # print(pos_list)
        i=i+1

    # test_str = "微卖 快来围观我的“微卖”小店，我又进了不少新货 http://t.cn/R4U3Dp1"
    # test_str = myiter[1000]['blog']['content']['text_content']
    # print(test_str)
    prob,pos_list = cut(test_str)
    print(prob)
    print(pos_list)
    # while i:
    #     i=i-1
    #     test_str = myiter[1000]['blog']['content']['text_content'].strip()
    #     # test_str    = "新华网东京电记者吴谷丰据日本共同社28日报道，日本行政改革担当大臣稻田朋美当天参拜了供奉有二战甲级战犯牌位的靖国神社。她成为第四个参拜靖国神社的安倍内阁成员。靖国神社位于东京千代田区，供奉有包括东条英机在内的14名第二次世界大战甲级战犯的牌位。长期以来，日本部分政客参拜靖国神社，导致日本与中国、韩国等亚洲国家关系"
    #     prob,pos_list = cut(test_str)
    #     print("HMM segment:",prob)
    # print(pos_list)
    #print(type(prob))
