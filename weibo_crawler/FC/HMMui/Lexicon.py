__author__ = 'Lin'


#The url of dictionary
url = "dict.txt"

#load the dict.txt to memory
#return a file operation obj
def loadDict(fileurl:str = url):
    try:
        #gbk
        fo = open(fileurl,"r",encoding="gbk")
        return fo
    except:
        print("Loading Dict Failed.")
#read the fo
#return a list of lines every line has two parts
def readDict(fo):
    #for line in fo.read().rstrip().split("\n"):
    #    word,freq = line.split(' ')[:2]
    line_lst = fo.read().rstrip().split("\n")
    fo.close()
    return  line_lst
#save the changes into the file
def updateDict(newDict:str):
    try:
        with open(url,'w') as fo:
            fo.write(newDict)
    except:
        print("Error!")
#get the new word
def addNewWord(oriD,word,freq):
    newD = oriD + str(word)+' '+freq+'\n'
    return newD
