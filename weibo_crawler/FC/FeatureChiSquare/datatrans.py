import codecs
import sys
import os

stopword={}

global path 
global outpath
global stoppath

def removefiles(filename):
  input_data=codecs.open(os.path.join(outpath,filename),'r','utf-8')
  lines = input_data.readlines()
  if len(lines) < 50:
    os.remove(os.path.join(outpath,filename))
  input_data.close()

def dataop(filename):
  input_data=codecs.open(os.path.join(path,filename),'r','utf-8')
  output_data=codecs.open(os.path.join(outpath,filename),'w','utf-8')
  for line in input_data.readlines():
    words = line.split('\t')
    t = 0
    for word in words[0]:
      if word >= u'\u4e00' and word <= u'\u9fa5':
        t = 0
      else:
	t = 1
        break;
    if t == 0:
    #stop word test
      if words[0] not in stopword:
        output_data.write(words[0]+'\t'+words[1])
  input_data.close()
  output_data.close()


def datatrans():
  #initialize stopword dict
  input_data=codecs.open(stoppath,'r','utf-8')
  for line in input_data.readlines():
    stopword[line[:-1]] = 0  

  for l in os.listdir(path):
    dataop(l)
  for ll in os.listdir(outpath):
    removefiles(ll)


if __name__ == '__main__':
  path = sys.argv[1]
  outpath = sys.argv[2]
  stoppath = sys.argv[3]
  datatrans()
               
