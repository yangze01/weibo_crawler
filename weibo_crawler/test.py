# #!/usr/bin/python
# #-*-coding:utf-8
# import os
# import sys
# import pdb
# import re
# import math
# from pymongo import MongoClient
# import pymongo
# import time
# import json
# import time
# import pdb
# #123123123
from getinfo.getlastdata import *
queue = get_queue("/home/john/queue/blogqueue.txt")[:0]#[:800]
print(len(queue))
a=get_queue("/home/john/queue/blogqueue.txt")#[800:]
# print(len(a))
visited = get_visited("/home/john/visited/blogvisited.txt")|set(a)
print(len(visited))
# #
# f1 = open("/home/john/visited/blogvisited.txt","w")
# f1.write(str(visited))
# f1.close()
# f2 = open("/home/john/queue/blogqueue.txt","w")
# f2.write(str(queue))
# f2.close()


# def load_model(f_name):
#     ifp=open(f_name,'rb')
#     return eval(ifp.read())
# def viterbi(obs,states,prob_start,prob_trans,prob_emit):
#     v=[{}]
#     path={}
#     for state in states:
#         if obs[0] in prob_emit[state]:
#             v[0][state] = math.exp(prob_start[state]*prob_emit[state][obs[0]])
#         else:
#             v[0][state]=0
#         path[state]=[state]
#     for i in range(1,len(obs)):
#         v.append({})
#         newpath = {}
#         for state in states:
#             est_list = []
#             for pstate in [s for s in states if v[i-1][s]>0]:
#                 if obs[i] in prob_emit[state]:
#                     est_list.append((v[i-1][pstate]*math.exp(prob_trans[pstate][state]*prob_emit[state][obs[i]]),pstate))
#                 else:
#                     est_list.append((v[i-1][pstate],pstate))
#             if len(est_list)!=0:
#                 print(len(est_list))
#                 p,ps = max([(p,ps) for (p,ps) in est_list])
#                 v[i][state] = p
#                 newpath[state]=path[ps]+[state]
#             path=newpath
#         (prob,state) = max([(v[len(obs)-1][state],state) for state in states])
#         try:
#             if prob_emit['M'][obs[-1]]>prob_emit['S'][obs[-1]]:
#                 (prob,state) = max([(v[len(obs)-1][state],state)for state in ('S','E')])
#         except:
#             pass
#         raw=""
#         if path:
#             for i,char in enumerate(obs):
#                 if path[state][i]=="E":
#                     raw+=char+" "
#                 elif path[state][i]=="S":
#                     raw+=char+" "
#                 else:
#                     raw+=char
#             return (raw,"",join(path[state]))
#         else:
#             return ("","")
# def cut(sentence):
#     # prob, pos_list =  viterbi(sentence,('B','M','E','S'), prob_start, prob_trans, prob_emit)
#     prob,pos_list = viterbi(sentence,('B','M','E','S'),prob_start,prob_trans,prob_emit)
#     return (prob,pos_list)
# if __name__=="__main__":
#     prob_start = load_model("/home/john/pythonspace/sina_crawler/weibo_crawler/FC/HMM/prob_start.py")
#     prob_trans = load_model("/home/john/pythonspace/sina_crawler/weibo_crawler/FC/HMM/prob_trans.py")
#     prob_emit = load_model("/home/john/pythonspace/sina_crawler/weibo_crawler/FC/HMM/prob_emit.py")
#     db_uri = "mongodb://labUser:aaaaaa@localhost:27017/?authSource=blog"
#     db_name = "blog"
#     xlient = MongoClient(db_uri)
#     db = xlient[db_name]
#     myiter = db.blog.find({"blog.content.text_content":{"$exists":1}},{"blog.content.text_content":1})
#     print(db)
#     print("##")
#     print(myiter[7]['blog']['content']['text_content'])
#     test_str = "wat Chongkae，龙婆碰 佛历2513年[good][good]@泰国佛牌咖 <br/>龙婆碰是现今泰国最受追捧的师傅之一，督造的金属自身系列更是年年升值，其招财及人缘口碑是非常好的。高僧在Wat Chongkae担任主持60余年，圆寂后高僧的遗体被安放入玻璃棺木内放在寺庙里供人祭拜，而大师的遗体至今都没有腐化，而且头发与指 <a href='/comment/DrEoyaIxH'>全文</a>"
#
#     prob,pos_list = cut(test_str)
#     print(prob,pos_list)
