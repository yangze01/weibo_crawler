#!/usr/bin/python
# -*- coding:utf-8 -*-


import random
import json


def getid(raw):
    ll = json.loads(raw)
    return ll['_id']

def filterid(raw, ids):
    ll = json.loads(raw)
    if ll['_id'] not in ids:
        return True
    else:
        return False

def randomsampling(dataMat,number):
  try:
     slice = random.sample(dataMat, number)     
     return slice
  except:
     print 'sample larger than population'



def main():
    f = "../data/weibo.filtered"
    fd = open(f, 'rb')

    _ids = map(getid, fd.xreadlines())


    slices = []
    for i in range(5):
        _slice = randomsampling(_ids, 1000)
        slices.append(_slice)

    fd.seek(0)

    samples = [[],[],[],[],[]]
    for line in fd.xreadlines():

        for i in range(5):

            if not filterid(line, slices[i]):
                samples[i].append(line)
            else:
                pass

    fd.close()

    for i in range(1, 6):
        fout = open("../data/sample" + str(i), 'wb')

        for raw in samples[i - 1]:
            fout.write(raw)

        fout.close()


if __name__ == "__main__":
    main()

    




    

