#!/usr/bin/python
# -*-coding:utf-8-*-

"""
此脚本的作用是从json构成的文本串中, 抽取指定的字段.
"""
import re
import sys
import json


def extract_fields(j1, filters):
    """
    @param: j1 一个记录, 由json转的字典.
    @param: filters 需要抽取的字段列表.
    @return: 结果.
    """

    res = {}
    for tag in filters:
        if tag not in j1:
            return {}
        else:
            res[tag] = j1[tag]

    return res


def preperform(s):
    """
    标签词的预处理, 将由逗号, 分号, 空格分隔的标签词分开成一行一词.
    :param s: 一个用户的所有标签.
    :return: 一个标签词的列表.
    """
    delimiters = "[;,；，]"
    fields = re.split(delimiters, s)
    return fields


def prefilter(s):
    """
    对标签词进行粗过滤, 除掉太长的词, 只保留4字内的词.
    :param s: 标签词
    :return: 是否过滤, True表示要滤掉, False要保留.
    """
    # 常量
    cnfixedlength = 4
    enfixedlength = 4

    # 判断标签词类型
    fields = s.strip().split(" ")
    stype = "cn"
    for field in fields:
        if field.encode("utf-8").isalnum():
            stype = "en"
        else:
            stype = "cn"

    # print s.encode("utf-8"), stype, len(s)
    if stype == "cn" and len(s) <= cnfixedlength:
        return False
    elif stype == "en" and len(fields) <= enfixedlength:
        return False
    else: 
        return True


def extractword(s):
    """
    抽取可以用于构建词库的标签词．
    :param s: 用户的所有标签词
    :return:　可以作为词库词的标签词, 是一个集合类型.
    """
    res = set()
    words = preperform(s)

    for word in words:
        if not prefilter(word):
            res.add(word)

    return res


def buildciku():
    """
    构建词库的主函数．
    :return: 无返回值.
    """
    if len(sys.argv) >= 4:
        inputf = sys.argv[1]
        output = sys.argv[2]
        filters = sys.argv[3:]
    else:
        filters = ['tg']
        inputf = "../data/tag.j1"
        output = "../data/output.j1"
    fd = open(inputf, "rb")
    fo = open(output, "wb")

    for line in fd.xreadlines():
        j1 = json.loads(line)
        res = extract_fields(j1, filters)
        if not res:
            pass
        else:
            if len(res.keys()) == 1:
                value = res.values()[0]
                #print value.encode("utf-8")
                words = extractword(value)

                for word in words:
                    # print len(word), word.encode("utf-8")
                    fo.write(word.encode("utf-8") + "\n")
            else:
                pass
    fd.close()
    fo.close()

    return


def main():
    if len(sys.argv) >= 4:
        inputf = sys.argv[1]
        output = sys.argv[2]
        filters = sys.argv[3:]
    else:
        filters = ['tg']
        inputf = "../data/tag.j1"
        output = "../data/output.j1"
    fd = open(inputf, "rb")
    fo = open(output, "wb")

    for line in fd.xreadlines():
        j1 = json.loads(line)
        res = extract_fields(j1, filters)
        if not res:
            pass
        else:
            if len(res.keys()) == 1:
                value = res.values()[0]
                # print value
                fo.write(value.encode("utf-8") + "\n")
            else:
                pass
    fd.close()
    fo.close()

if __name__ == "__main__":
    buildciku()
