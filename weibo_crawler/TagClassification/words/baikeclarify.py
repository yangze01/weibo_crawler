#!/usr/bin/python
# -*-coding:utf-8-*-

__author__ = 'hadoop'


import re
import sys


delimiters = re.compile("[:,.;：，．；]")


def prefilter(s):
    """
    对词进行粗过滤, 除掉有标点的词.
    :param s: 词条
    :return: 是否过滤, True表示要滤掉, False要保留.
    """

    if delimiters.search(s):
        return True
    else:
        False


def usage():
    print "Usage: python baikeclarify.py <input> <output> <otheroutput>"
    sys.exit(1)


def baikeclarify():
    """
    构建词库的主函数．
    :return: 无返回值.
    """
    if len(sys.argv) == 4:
        inputf = sys.argv[1]
        output = sys.argv[2]
        tmpput = sys.argv[3]
    else:
        usage()

    fd = open(inputf, "rb")
    fo = open(output, "wb")
    ft = open(tmpput, "wb")

    progress = 0
    for line in fd.xreadlines():
        progress += 1
        sys.stdout.write(str(progress) + "\r")

        res = prefilter(line)
        if not res:
            fo.write(line)
        else:
            ft.write(line)

    fd.close()
    fo.close()
    ft.close()

    return


if __name__ == "__main__":
    baikeclarify()
