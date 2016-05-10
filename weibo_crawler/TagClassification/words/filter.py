#!/usr/bin/python
# -*-coding:utf-8-*-


"""
微博用户数据是由json行构成的文本文件. 此脚本用于过滤记录.
在main函数中, filters是二元组列表, 每一个二元组表示一个tag和
一个value, 如果tag的值是value, 就要过滤.
"""

import json


def filter_record(j1, filters):
    """ @param: j1 一个记录, 由json转的字典.
    @param: filters 二元组的列表, 每个二元组 (tag, value), 表示tag值为value时要过滤.
    @return: True 要过滤, False 不用.
    """

    for tag, value in filters:
        if tag not in j1:
            return True

        if j1[tag] == value:
            return True

    return False


def main():
    filters = [('tg', '-1'), ('tg', "")]
    f = "../data/weibo.txt"
    output = "../data/weibo.filtered"
    fd = open(f, "rb")
    fo = open(output, "wb")

    for line in fd.xreadlines():
        j1 = json.loads(line)
        if filter_record(j1, filters):
            pass
        else:
            fo.write(line)
    fd.close()
    fo.close()

if __name__ == "__main__":
    main()

