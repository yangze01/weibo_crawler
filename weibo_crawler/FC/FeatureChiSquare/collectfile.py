import os
import shutil

def collectfile(srcpath,dstpath):
  for fp in os.listdir(srcpath):
    path=os.path.join(srcpath,fp)
    if os.path.isdir(path):
      for fn in os.listdir(path):
        tmp=os.path.splitext(fn)
        shutil.copy(os.path.join(path,fn),dstpath+tmp[0]+'-'+fp[-2:]+tmp[1])
 
if __name__ == '__main__':
  collectfile(srcpath,dstpath)
