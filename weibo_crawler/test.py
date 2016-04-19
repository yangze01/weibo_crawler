# -*- coding: UTF-8 -*-
# from login import *
from getinfo.getlastdata import *
# visited = get_visited("/home/john/pythonspace/sina_crawler/weibo_crawler/salevisited.txt")
# print "the visited len is:"+str(len(visited))
queue = get_queue("/home/john/queue.txt")
print("the queue len is:"+str(len(queue)))





# n = ['摩羯座','水瓶座','双鱼座','白羊座','金牛座','双子座','巨蟹座','狮子座','处女座','天秤座','天蝎座','射手座']
# shuxiang = '猴鸡狗猪鼠牛虎兔龙蛇马羊'
# print type(n[0])
# listVal = [0]*12
# listVal[0]=listVal[0]+2
# print listVal
#
# def get_decades(year):
#     d=(1930,1940,1950,1960,1970,1980,1990,2000,2010)
#     return len(filter(lambda y:y<=(year),d))%9-1
# def get_province(prov):
#     d=[u'贵州',u'河南',u'山东',u'四川',u'江苏',u'青海',u'新疆',u'福建',u'浙江',\
#        u'湖北',u'天津',u'江西',u'海南',u'重庆',u'云南',u'黑龙',u'北京',u'台湾',\
#        u'海外',u'澳门',u'其他',u'广西',u'陕西',u'甘肃',u'河北',u'宁夏',u'广东',\
#        u'内蒙',u'吉林',u'湖南',u'安徽',u'香港',u'上海',u'山西',u'西藏',u'辽宁']
#     return d.index(prov)
#
# d=[u'贵州',u'河南',u'山东',u'四川',u'江苏',u'青海',u'新疆',u'福建',u'浙江',\
#    u'湖北',u'天津',u'江西',u'海南',u'重庆',u'云南',u'黑龙',u'北京',u'台湾',\
#    u'海外',u'澳门',u'其他',u'广西',u'陕西',u'甘肃',u'河北',u'宁夏',u'广东',\
#    u'内蒙',u'吉林',u'湖南',u'安徽',u'香港',u'上海',u'山西',u'西藏',u'辽宁']
# #print d
# print '##################################################################'
# print get_province(u'陕西')
# #print tagset
a=dict()
a["湖南"]=1
print(a)
a["湖南"]=a["湖南"]+2
print(a)
