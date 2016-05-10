import codecs
import sys
import os
import math
import string

path='/home/lfr/svmfeature/datatrans' 

df={}

def writefile():
  for k,v in df.items():
    output_data = codecs.open(os.path.join("/home/lfr/svmfeature/weight/",k), 'w', 'utf-8')
    for k1,v1 in v.items():
      output_data.write(k1+ "\t" + str(v1)+'\n')

def guigehua():
  for k,v in df.items():
    val = 0
    for k1,v1 in v.items():
      val += v1*v1
      val = math.sqrt(val)
    for k2,v2 in v.items():
      tv = df[k]
      tv[k2] = v2/val

def insertdata(key1,key2,value):
 if df.has_key(key1) == True:
   v = df[key1]
   v[key2] = value
 else:
   df[key1]={key2:value}
     

def features():
  allfeatures={}
  t = os.listdir(path)
  TOTALNUM = len(t)
  input_data = codecs.open("/home/lfr/svmfeature/features.txt", 'r', 'utf-8')
  for line in input_data.readlines():
    words= line.strip().split('\t')
    allfeatures[words[0]]=words[1]
  dirlist=os.listdir(path)
  for f in dirlist:
    input_data1 = codecs.open(os.path.join(path,f), 'r', 'utf-8')
    for l in input_data1.readlines():
      words1=l.strip().split('\t')
#      print words1[0]
      if allfeatures.has_key(words1[0]) == True:
#        print words1[0]
        val = string.atof(words1[1]) * math.log(TOTALNUM/string.atof(allfeatures[words1[0]])+0.01,2)
        insertdata(f,words1[0],val)
  guigehua()
  writefile()
  
if __name__ == '__main__':
  features()

