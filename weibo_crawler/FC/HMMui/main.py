__author__ = 'Lin'
import HMM
from math import log
import Lexicon
import Rule
import string
Dictionary_URL = Lexicon.url #the default url
PrefixDict = None #It will be initialized later
Possibility = {} #this dict will be initialized later too
total = 0.0 #it will be updated after initializing the dict
isInitialized = False
min_Possibility = 0.0
#return a file_object to read the dict.txt


#cut every word in Dict into several pieces to be prefix
def generatePrefixDict():
    global Possibility,PrefixDict,total,Dictionary_URL
    fo = Lexicon.loadDict(Dictionary_URL)
    PrefixDict = set()
    FREQ = {}
    for line in fo.read().rstrip().split("\n"):
        word,freq = line.split(' ')[:2]
        FREQ[word] = float(freq)
        total += float(freq) #calculate the total number of words
        for idx in range(len(word)): #generate the prefix dictionary
            prefix = word[0:idx+1]
            PrefixDict.add(prefix)
    fo.close()
    #Transform the freq into possibilities
    Possibility = dict((key,log(value/total)) for key,value in FREQ.items())
#get the DAG of a sentence
def getDAG(sentence:str):
    global PrefixDict,Possibility
    DAG = {}
    N = len(sentence)
    for i in range(N):
        lst_pos = []
        #this list is to save the indexes of those chars who can make up a word with i-th char.
        j = i
        word = sentence[i]
        #if this char is not in dict, we must let it be a single word
        lst_pos.append(i)
        while(j<N and word in PrefixDict):
            if(word in Possibility):
                if(lst_pos[0]!=j):
                    lst_pos.append(j)
            j+=1
            word = sentence[i:j+1]
        #put this list of i-th into DAG[i]
        DAG[i]=lst_pos
    return  DAG
#Dynamic Planning.
#calculate the most possible route of every beginning-char.
def calculateRoute(DAG:dict,route:dict,sentence:str):
    #from right to left
    global Possibility , min_Possibility

    N = len(sentence)
    route[N]=(0.0,'')
    #In fact, it is a recurse procedure.
    for i in range(N-1,-1,-1):
        max_psblty = None
        max_cur = i
        for j in DAG[i]:
            #to consider every possible word
            word = sentence[i:j+1]
            posb1 = Possibility.get(word,min_Possibility)
            posb2 = route[j+1][0]
            posb = posb1 + posb2
            if max_psblty is None:
                max_psblty = posb
            if(posb>=max_psblty):
                max_psblty = posb
                max_cur = j
        route[i] = (max_psblty,max_cur)
#to delete the Translating Meaning word like'\n' '\r' '\t'...
def deleteTMword(oriSentence,char):
    i = oriSentence.find(char)
    while(i!=-1):
        s1 = oriSentence[0:i]
        s2 = oriSentence[i+1:]
        oriSentence = s1+s2
        i = oriSentence.find(char)
    return oriSentence

#to process the sentence with rules before segmentation
def preprocess(oriSentence):
    oriSentence = deleteTMword(oriSentence,'\r')
    oriSentence = deleteTMword(oriSentence,'\n')
    oriSentence = deleteTMword(oriSentence,'\t')
    #load the rules
    deletes = Rule.Rules["DELETE"]
    updates = Rule.Rules["CHANGE"].keys()
    #we must delete the whitespaces.
    deletes.append(' ')
    deletes.append('　')
    sentence = ''
    for char in oriSentence:
        if(char in deletes):
            sentence += ''
        elif(char in updates):
            sentence += Rule.Rules["CHANGE"][char]
        else:
            sentence += char
    return sentence
#segment the sentence
def segmentWord(oriSentence,useRules=True):
    sentence = preprocess(oriSentence)

    #this judgement is very necessary.
    #if we have initialized the dictionary, we don't have to do it again.
    if(not isInitialized):
        initialize()
    DAG = getDAG(sentence)
    route = {}
    calculateRoute(DAG,route,sentence)
    words = []
    cur = 0
    buf = ""
    N = len(sentence)
    #cur is the current curse of state
    while(cur<N):
        next_cur = route[cur][1]
        word = sentence[cur:next_cur+1]
        #if the word is just a single char, then it might be un-login word
        #buf is the temporary part.
        if(len(word)==1):
            buf+=word
        else:
            #until we have next word which is not single.
            if(len(buf)!=0):
                #we have buf
                #if this word is in dictionary, usually not
                #or if it is a single word
                if(buf in Possibility or len(buf)==1):
                    words.append(buf)
                else:
                #if not , it is an un-login word.
                #we must use HMM to cut them
                    words += HMM.cutUnrecognized(buf)
                #clear the buf
                buf=""
            words.append(word)
        cur = next_cur+1
    if(buf):
        words += HMM.cutUnrecognized(buf)
    return words

#to cut a paragraph into several simplest sentences
def segmentSentence(text,isForSegmentWord=False):
    lst = [',','!','?','…','，','。','！','？','"','“','”','\'','‘','’',':','：',';','；','—','(',')','（','）']
    if(isForSegmentWord):
        #these punctuations shouldn't cut the sentence.
        lst += ['、','《','》','<','>']
    assert isinstance(text, str)
    text_seg = ""
    for char in text:
        text_seg += char in lst and '|' or char
    sentence_lst = text_seg.split('|')
    while('' in sentence_lst):
        sentence_lst.remove('')

    return sentence_lst

#initialize the program
def initialize():
    #initial the program with several sections

    global isInitialized,PrefixDict,Possibility,total,min_Possibility
    generatePrefixDict()
    min_Possibility = min(Possibility.values())
    Rule.loadRules()
    isInitialized = True