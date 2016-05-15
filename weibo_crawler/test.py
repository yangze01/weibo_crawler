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
    ifp=open(f_name,'rb')
    return eval(ifp.read())
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
    for state in states:
        if obs[0] in prob_emit[state]:
            v[0][state]= math.exp(prob_start[state]*prob_emit[state][obs[0]])
            
