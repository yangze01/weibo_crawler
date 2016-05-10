import codecs
import sys
import os

features={}
df={}

global path 
global output 
global foutput

def write(filename,kv):
  output_data = codecs.open(filename, 'w', 'utf-8')
  #sort kv by value
  tkv = sorted(kv.items(), key=lambda d:d[1], reverse=True) 
  for t in tkv:
    output_data.write(t[0] + "\t" + str(t[1])+'\n')
  output_data.close()

def writedf(kv):
  output_data = codecs.open(os.path.join(foutput,"features.txt"), 'w', 'utf-8')
  	
  #sort kv by value
  tkv = sorted(kv.items(), key=lambda d:len(d[1]), reverse=True)
  for t in tkv:
    output_data.write(t[0] + "\t" + str(len(t[1]))+'\n')
  output_data.close()


def insert(key,kv):
  if kv.has_key(key) == True:
    kv[key]+=1
  else:
    kv[key]=1

def insertdf(key,value,dfkv):
  if dfkv.has_key(key):
    tmpdict = dfkv[key]
    tmpdict[value] = 1;
  else:
    dfkv[key]={value:1}

def number():
  dirlist=os.listdir(path)
  for f in dirlist:
    input_data = codecs.open(os.path.join(path,f), 'r', 'utf-8')
    bj = 0
    tmpword = ''  
    for line in input_data.readlines():
      if len(line.strip()) == 0:
        break
      words= line.strip().split('\t')
     # print words[0]
     # print len(words)
      if len(words) < 3:
        words.insert(0,'X')
      if bj==1 and words[2]=='E':
        bj = 0
        tmpword+=words[0]
        insert(tmpword,features)
        insertdf(tmpword,f,df)
        tmpword=''
      if words[2] == 'S':
        insert(words[0],features)
        insertdf(tmpword,f,df)
      elif words[2] == 'B':
        bj = 1
        tmpword+=words[0]
      elif words[2] == 'M':
        tmpword+=words[0]
    write(os.path.join(output,f),features)
    features.clear()
  writedf(df)

if __name__ == '__main__':
  path=sys.argv[1]
  output=sys.argv[2]
  foutput = sys.argv[3]
  number()
