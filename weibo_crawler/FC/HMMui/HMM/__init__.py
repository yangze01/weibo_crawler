__author__ = 'Lin'
import HMM.prob_emit,HMM.prob_trans,HMM.prob_start
import string
MIN_FLOAT = -3.14e100
#states
States = ('B','M','E','S')
#every possible previous of each state
PrevStatus = {
    'B':('E','S'),
    'M':('M','B'),
    'S':('S','E'),
    'E':('B','M')
}

start_P, trans_P, emit_P = {},{},{}
#initiallize Possibliities
def init_P():
    global start_P,trans_P,emit_P
    start_P = HMM.prob_start.P
    trans_P = HMM.prob_trans.P
    emit_P = HMM.prob_emit.P

#vitebi algorithm ~
#obs is the sentence we want to segment
def viterbi(obs):
    V = [{}]
    path={}
    #possess the first char
    for s in States:
        #this state's possibility is the start * emit
        V[0][s] = start_P[s] + emit_P[s].get(obs[0],MIN_FLOAT)
        #record this path
        path[s] = [s]
    #poseess the other chars
    for i in range(1,len(obs)):
        char = obs[i]
        V.append({})
        newPath = {}
        #check every state it can be
        for s in States:
            #assume that in this case and calculate what the possibility is
            emit =  emit_P[s].get(char, MIN_FLOAT) #emit it
            prob_max = MIN_FLOAT
            state_max = PrevStatus[s][0]
            for preState in PrevStatus[s]:
                #calculate the previous state
                prob = V[i-1][preState] + trans_P[preState][s] + emit
                if(prob>prob_max):
                    prob_max = prob
                    state_max = preState
            V[i][s] = prob_max
            newPath[s] = path[state_max] + [s]
        path = newPath

    finalProb = MIN_FLOAT
    finalState = ""
    for fs in ('E','S'):
        p = V[len(obs)-1][fs]
        if(p>finalProb):
            finalProb = p
            finalState = fs
    return (finalProb,path[finalState])
#judge if the char is a digit or a english char or a punctuation
def isDigitOrEng(char):
    return char in string.ascii_letters or char in string.digits or char in string.punctuation
#this is to find the indexes of non-Chinese chars of this sentence
def findEngAndDigits(sentence):
    ind_start = []
    ind_end = []
    for i in range(len(sentence)):
        if(i==0 and isDigitOrEng(sentence[i])):
            ind_start.append(i)
            if(not isDigitOrEng(sentence[i+1])):
                ind_end.append(i)
        elif(i==len(sentence)-1 and isDigitOrEng(sentence[i])):
            ind_end.append(i)
            if(not isDigitOrEng(sentence[i-1])):
                ind_start.append(i)
        else:
            if(isDigitOrEng(sentence[i]) and (not isDigitOrEng(sentence[i-1]))):
                ind_start.append(i)
            if(isDigitOrEng(sentence[i]) and (not isDigitOrEng(sentence[i+1]))):
                ind_end.append(i)
    return ind_start,ind_end
#the sentence must be then entirely Chinese sentence
def cutWithHMM(sentence):
    #possess the english and digits
    #find their indexes
    init_P()
    words = []
    prob,path = viterbi(sentence)
    buf = "" # temporary variable
    for i in range(len(sentence)):
        flag = path[i]
        if(flag=='S'):
            buf = sentence[i]
            words.append(buf)
            buf=""
        elif(flag=='B'):
            buf = sentence[i]
        elif(flag=='M'):
            buf = buf + sentence[i]
        elif(flag=='E'):
            buf = buf+sentence[i]
            words.append(buf)
            buf=""
    return words

#cut the unrecognized sentence . This sentence can be fixed up with eng and chs
def cutUnrecognized(sentence):
    #first we need to find all indexes of abnormal char
    eng_dgt_start,eng_dgt_end = findEngAndDigits(sentence)
    cur = 0
    N = len(eng_dgt_start)
    L = len(sentence)
    words = []
    #And then we need to ues them as the flag to segment the sentence
    if(N!=0):
        for t in range(N):
            begin = eng_dgt_start[t]
            end = eng_dgt_end[t]
            if(t==0 and begin!=0):
                buf = sentence[0:begin]
                words += cutWithHMM(buf)

            if(t!=N-1):
                next_start = eng_dgt_start[t+1]
                buf = sentence[begin:end+1]
                words.append(buf)
                buf = sentence[end+1:next_start]
                words += cutWithHMM(buf)
            else:
                buf = sentence[begin:end+1]
                words.append(buf)
                if(end!=L-1):
                    buf = sentence[end+1:L]
                    words += cutWithHMM(buf)
    else:
        words += cutWithHMM(sentence)
    return words


#print(cutUnrecognized(""))

