
import re,math
from pymongo import MongoClient
import pymongo
import time
import json
import time
import pdb
wordbag={}
def load_model(f_name):
    ifp = open(f_name, 'rb')
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
		#ß	print(est_list)
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
		#("".join(path[state]))
			#p,s=max([(value,key) for key,value in ])
		# 	print(s,p,obs[i],prob)
		# 	v[i][state]=p
		# 	newpath[state]=path[s]+[state]
		# path=newpath
def raw_seg(chunk,wordbag):
	i,j =0,0
	while j<len(chunk)-1:
		#print("chunk[j:j+2]",chunk[j:j+2])
		if not (chunk[j:j+2] in wordbag):
			yield chunk[i:j+1]
			i=j+1
		j+=1
	yield chunk[i:j+1]

def train():
	d={}
	prob_emit={}
	states=['B','M','E','S']
	count={}
	for state in states:
		d[state]={}
		count[state]=0
	raw=""
	for line in open("/home/john/pythonspace/sina_crawler/weibo_crawler/FC/HMM/RenMinData.txt_utf8"):
		for word in line.rstrip("\n").split():
			if word in wordbag:
				wordbag[word]+=1
			else:
				wordbag[word]=1
			chars=[char for char in word]
			if len(chars)==1:
				if chars[0] in d["S"]:
					d["S"][chars[0]]+=1
					count["S"]+=1
				else:
					d["S"][chars[0]]=1
					count["S"]+=1
				s="S"
			else:
				if chars[0] in d["B"]:
					d["B"][chars[0]]+=1
					count["B"]+=1
				else:
					d["B"][chars[0]]=1
					count["B"]+=1
				start="B"
				if chars[-1] in d["E"]:
					d["E"][chars[-1]]+=1
					count["E"]+=1
				else:
					d["E"][chars[-1]]=1
					count["E"]+=1
				end="E"
				for char in chars[1:-1]:
					if chars[-1] in d["M"]:
						d["M"][chars[-1]]+=1
						count['M']+=1
					else:
						d["M"][chars[-1]]=1
						count["M"]+=1
				mid="M"*len(chars[1:-1])
				s=start+mid+end
			raw+=s

	total=count['M']+count['E']+count["B"]+count['S']
	prob_start={'B': float(count["B"]/total), 'E': float(count["E"]/total), 'M': float(count['M']/total), 'S': float(count['S']/total)}
	prob_trans={}
	d_trans={}
	#print(raw)
	for s1 in states:
		d_trans[s1]={}
		prob_trans[s1]={}
		for s2 in states:
			d_trans[s1][s2]=0
	for i in range(len(raw)-1):
		s1,s2=raw[i:i+2]
		d_trans[s1][s2]+=1
	for s1 in states:
		total_s1=0
		for key,value in d_trans[s1].items():
			total_s1+=value
		#print(prob_trans[s1])
		for s2 in states:
			prob_trans[s1][s2]= float(d_trans[s1][s2]/total_s1)
	for state,mapps in d.items():
		prob_emit[state]={}
		for k,v in mapps.items():
			prob_emit[state][k]=float(d[state][k]/count[state])
	return prob_trans,prob_start,prob_emit,wordbag

def cut(sentence,allow_oov=False):
	re_han=re.compile(r"([\u4E00-\u9FA5]+)")
	if allow_oov:
		pass
	else:
		for chunk in re_han.split(sentence):
			if chunk:
				yield chunk
# if __name__== "__main__":
#	states=['B','M','E','S']
#	prob_trans,prob_start,prob_emit,wordbag=train()
	# ref=[line for line in open("/home/john/pythonspace/sina_crawler/weibo_crawler/FC/HMM/RenMinData.txt_utf8").readlines()[:10]]
	# for i,line in enumerate(open("/home/john/pythonspace/sina_crawler/weibo_crawler/FC/HMM/RenMinData.txt_utf8").readlines()[:10]):
	# 	print("#"*60)
	# 	obs=[char for char in line.rstrip("\n")]
	# 	print("Ref segment:",ref[i].rstrip("\n"))
	# 	raw_seg_with_dict=[seg for chunk in cut(line.rstrip("\n")) for seg in raw_seg(chunk,wordbag) ]
	# 	print("Raw segment:","  ".join(raw_seg_with_dict))
	# 	output,SQ=viterbi(obs,states,prob_start,prob_trans,prob_emit)
	# 	print("HMM segment:",output)
if __name__ == "__main__":
    # for char in test_str:
    #     print(char)
    #prob_trans,prob_start,prob_emit,wordbag=train()
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
    test_str = myiter[7]['blog']['content']['text_content'].strip().strip('#')
	#test_str    = "新华网东京电记者吴谷丰据日本共同社28日报道，日本行政改革担当大臣稻田朋美当天参拜了供奉有二战甲级战犯牌位的靖国神社。她成为第四个参拜靖国神社的安倍内阁成员。靖国神社位于东京千代田区，供奉有包括东条英机在内的14名第二次世界大战甲级战犯的牌位。长期以来，日本部分政客参拜靖国神社，导致日本与中国、韩国等亚洲国家关系"
    obs=[char for char in test_str]#.rstrip("\n")]
    prob,pos_list=viterbi(obs,('B','M','E','S'),prob_start,prob_trans,prob_emit)
    print("HMM segment:",prob)




	# print("#Prob_start:",prob_start)
	# print("#Prob_trans:",prob_trans)
	# ref=[line for line in open("icwb2data/gold/pku_test_gold.utf8").readlines()]
	# for i,line in enumerate(open("icwb2data/testing/pku_test.utf8").readlines()):
	# 	obs=[char for char in line.rstrip("\n")]
	# 	output,SQ=viterbi(obs,states,prob_start,prob_trans,prob_emit)
	# 	print("Ref:",ref[i].rstrip("\n"))
	# 	print("Test:",output)
	# 	print("Seq:",SQ+"\n")

# re_han, re_skip = re.compile(ur"([\u4E00-\u9FA5]+)"), re.compile(ur"[^a-zA-Z0-9+#\n]")
# blocks = re_han.split(sentence)
