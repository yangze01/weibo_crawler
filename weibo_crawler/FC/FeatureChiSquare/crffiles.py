import os
import shutil
import codecs
import sys

def crffiles(srcpath,dstpath):
  for fp in os.listdir(srcpath):
    input_data = codecs.open(os.path.join(srcpath,fp),'r','GB18030')
    output_data= codecs.open(os.path.join(dstpath,fp),'w','utf-8') 
    try:
      for line in input_data.readlines():
        words=line.strip()
        if len(words) != 0:
          for word in words:
            output_data.write(word + "\tS\n")
    except UnicodeDecodeError,e:
      print os.remove(os.path.join(dstpath,fp))

    input_data.close()
    output_data.close()  
         

if __name__ == '__main__':
  srcpath = sys.argv[1]
  dstpath = sys.argv[2]
  crffiles(srcpath,dstpath)

