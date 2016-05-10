__author__ = 'Lin'

Rules = {"CHANGE":{},"DELETE":[]}
RuleUrl = "rule.config"

#load rules into memory
def loadRules(url=RuleUrl):
    with open(url,"r",encoding="gbk") as fo:
        lst = fo.read().rstrip().split("\n")
        while '' in lst:
            lst.remove('')
        for line in lst:
            ins = line.split(" ")
            typ = ins[0]
            if(typ!="CHANGE"):
                Rules[typ].append(ins[1])
            elif(typ=="CHANGE"):
                Rules["CHANGE"][ins[1]]=ins[3]

