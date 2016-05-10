#!/usr/bin/python
# -*-coding:utf-8-*-

import sys
import time
import jieba

jieba.load_userdict(r'/home/heqi/TagClassification/userdict/userdict.txt')
#jieba.enable_parallel()


def usage():
    print "Usage: python file_cut.py <input> <output>"
    sys.exit(1)


def main():
    if len(sys.argv) == 3:
        f = sys.argv[1]
        o = sys.argv[2]

    else:
        usage()

    fd = open(f, "rb")
    fo = open(o, "wb")

    print "Start cut word."
    start = time.time()

    progress = 0
    for line in fd.xreadlines():

        progress += 1
        sys.stdout.write("Process line %d.\r" % progress)

        tokens = jieba.cut(line)
        res = " ".join(tokens).encode("utf-8")
        fo.write(res)

    end = time.time()
    time_cost = end - start
    print "\n"
    print "Cost time %s." % time_cost
    print "Process file completely."

if __name__ == "__main__":
    main()