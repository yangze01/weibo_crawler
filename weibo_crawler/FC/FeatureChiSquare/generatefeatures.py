import sys,os,codecs,string,numpy,threading

features_mat={}
features_chisquare={}

global narr
global items

global fepath
global inputpath
global fematpath

def writefeatures():
  out_data = codecs.open(fepath,'w','utf-8')
  for k,v in features_chisquare.items():
    out_data.write(str(k)+'\t')

#sort
    tmp = sorted(v,key=lambda value: value[1])
    for a,b in tmp:
      out_data.write(a+':'+str(b)+',')
    out_data.write('\n')

def thread1(start,end):
  for i in range(start,end):
    for j in range(len(features_mat)):
      calcFeatures(i,j)
#      print j
#  print 'class is :',i


def calcFeatures(i,j):  #i(int)=class j(int)=word
  if i not in features_chisquare:
    features_chisquare[i]=[]
  tmp = features_chisquare[i]
  A = narr[j,i]
  B=numpy.sum(narr[j,0:i])+numpy.sum(narr[j,i+1:])
  C=numpy.sum(narr[0:j,i])+numpy.sum(narr[j+1:,i])
  D=numpy.sum(narr) - numpy.sum(narr[j])-numpy.sum(narr[0:j,i]) - numpy.sum(narr[j+1:,i])

  tmp.append((items[j][0],chisquare(A,B,C,D)))
#  print A," ",B," ",C," ",D

def chisquare(A,B,C,D):
  tmp = (A*D-B*C)*(A*D-B*C)
  tmp1 = (A+B)*(C+D)
  return tmp/tmp1

def insert(word,cls):
  if word not in features_mat:
    features_mat[word] = [0,0,0,0,0,0,0,0,0]
  tmp = features_mat[word]
  tmp[string.atoi(cls)-1]+=1

def writefile():
  out_data = codecs.open(fematpath,'w','utf-8')
  for k,v in features_mat.items():
    out_data.write(k+'\t')
    for a in v:
      out_data.write(str(a)+',')
    out_data.write('\n')

for f in os.listdir(inputpath):
  input_data=codecs.open(os.path.join(inputpath,f),'r','utf-8')
  for line in input_data.readlines():
    words = line.split()
    cls = f.split('-')
    insert(words[0],cls[1])

items = features_mat.items()

writefile()
fl=[]
for k,v in features_mat.items():
  fl.append(v)
narr = numpy.array(fl)

#print numpy.sum(narr[1:,0])
#print numpy.sum(narr)
#for i in range(0,9):
#  for j in range(len(features_mat)):
#    calcFeatures(i,j)
#    print j
#  print 'class is :',i

threads=[]
t = threading.Thread(target=thread1,args=(0,1))
threads.append(t)

t = threading.Thread(target=thread1,args=(1,2))
threads.append(t)
t = threading.Thread(target=thread1,args=(2,3))
threads.append(t)
t = threading.Thread(target=thread1,args=(3,4))
threads.append(t)

t = threading.Thread(target=thread1,args=(4,5))
threads.append(t)

t = threading.Thread(target=thread1,args=(5,6))
threads.append(t)

t = threading.Thread(target=thread1,args=(6,7))
threads.append(t)

t = threading.Thread(target=thread1,args=(7,9))
threads.append(t)

for t in threads:
  t.start()

for t in threads:
  t.join()

writefeatures()
