#-*- coding: UTF-8 -*-
#from login import *
from createMultiCookies.multi import *
from collections import deque
from getinfo.get_data import *
from con2mongo.user_Unit import *
from con2mongo.UserOnMongo import *
from getinfo.getlastdata import *
from createMultiCookies.login import *
from pymongo import MongoClient
import pymongo
import time
import json
import time
import pdb
#********************-----------------********************#
class MongoProcess(object):
    def __init__(self,db_uri,db_name):
        self.db_uri = "mongodb://labUser:aaaaaa@localhost:27017/?authSource=lab"
        self.db_name = "lab"
        try:
            self.client = MongoClient(self.db_uri)
            self.db = client[self.client]
            print "connect %s mongodb success" % self.db
        except:
            print "connect %s mongodb fail" % self.db
#********************-----------------********************#

def chinese_zodiac(year):
    d = [u'猴',u'鸡',u'狗',u'猪',u'鼠',u'牛',u'虎',u'兔',u'龙',u'蛇',u'马',u'羊']
    #  return u'猴鸡狗猪鼠牛虎兔龙蛇马羊'[year%12]
    #  return d[year%12]
    return year%12

def zodiac(month, day):
    n = [u'摩羯座',u'水瓶座',u'双鱼座',u'白羊座',u'金牛座',u'双子座',u'巨蟹座',u'狮子座',u'处女座',u'天秤座',u'天蝎座',u'射手座']
    d = ((1,20),(2,19),(3,21),(4,21),(5,21),(6,22),(7,23),(8,23),(9,23),(10,23),(11,23),(12,23))
    # return n[len(filter(lambda y:y<=(month,day), d))%12]
    return len(filter(lambda y:y<=(month,day), d))%12

def get_decades(year):
    d=(1930,1940,1950,1960,1970,1980,1990,2000,2010)
    return len(filter(lambda y:y<=(year),d))%9-1

def get_province(prov):
    d=[u'贵州',u'河南',u'山东',u'四川',u'江苏',u'青海',u'新疆',u'福建',u'浙江',\
       u'湖北',u'天津',u'江西',u'海南',u'重庆',u'云南',u'黑龙',u'北京',u'台湾',\
       u'海外',u'澳门',u'其他',u'广西',u'陕西',u'甘肃',u'河北',u'宁夏',u'广东',\
       u'内蒙',u'吉林',u'湖南',u'安徽',u'香港',u'上海',u'山西',u'西藏',u'辽宁']
    return d.index(prov)

def get_birthabout(db):
    i = 0
    zodiac_count = [0]*12
    chinese_zodiac_count = [0]*12
    decades_count = [0]*9

    n = [u'摩羯座',u'水瓶座',u'双鱼座',u'白羊座',u'金牛座',u'双子座',u'巨蟹座',u'狮子座',u'处女座',u'天秤座',u'天蝎座',u'射手座']

    birthdayiter = db.user.find({"userinfo.birthday":{"$exists":1}},{"userinfo.birthday":1})
    while(i<birthdayiter.count()):
        print i
        i=i+1
        birthday = birthdayiter[i]["userinfo"]["birthday"]
        if len(birthday)==10 and birthday[0:4]!=u'0000' and birthday[5:7]!=u'00' and birthday[8:10]!=u'00' and birthday[0:4]<u'2013' and birthday[0:4]>u'1930':
            print birthday
            tmptime=time.strptime(birthday,"%Y-%m-%d")
            chinese_zodiac_count[chinese_zodiac(tmptime[0])]=chinese_zodiac_count[chinese_zodiac(tmptime[0])]+1
            zodiac_count[zodiac(tmptime[1],tmptime[2])]=zodiac_count[zodiac(tmptime[1],tmptime[2])]+1
            decades_count[get_decades(tmptime[0])]=decades_count[get_decades(tmptime[0])]+1

            print "the chinese_zodiac_count",chinese_zodiac_count
            print "the zadiac_count",zodiac_count
            print "the decades_count",decades_count
        if len(birthday)==3:
            zodiac_count[n.index(birthday)]=zodiac_count[n.index(birthday)]+1

def get_tags(db):
    tagset=get_visited("/home/john/tagset.txt")

    myiter = db.user.find({"userinfo.tags":{"$exists":1}},{"userinfo":1})
    print myiter.count()
    i=myiter.count()
    while(i):
        i=i-1
        for item in myiter[i]["userinfo"]["tags"]:
            print i
            print item
            tagset.add(item)
    print len(tagset)
    print tagset
    f1 = open("/home/john/tagset.txt","w")
    f1.write(str(tagset))
    f1.close()
def get_district(db):
    i = 0
    a=set()
    prov_count = [0]*36
    districtiter = db.user.find({"userinfo.district":{"$exists":1}},{"userinfo.district":1})
    length = districtiter.count()
    while(i<length):
    #while(i<1500):
        print i
        i=i+1
        print districtiter[i]["userinfo"]["district"][0:2]
        prov_count[get_province(districtiter[i]["userinfo"]["district"][0:2])] = prov_count[get_province(districtiter[i]["userinfo"]["district"][0:2])]+1
        print prov_count
def get_sex(db):
    m_count = db.user.count({"userinfo.sex":"男"})
    f_count = db.user.count({"userinfo.sex":"女"})
    return [m_count,f_count]

if __name__=="__main__":
    db_uri = "mongodb://labUser:aaaaaa@localhost:27017/?authSource=lab"
    db_name = "lab"
    xlient = MongoClient(db_uri)
    db = xlient[db_name]
    print db
#    get_district(db)
    print get_sex(db)
        #a.add(districtiter[i]["userinfo"]["district"][0:2])
        #print a
#    for i in a:
#        print i
#    print len(a)
    #get_tags(db)
    # get_birthabout(db)

#####################################################################################################
#####################################################################################################
#####################################################################################################
    # userset={}
    # #userset[str(1)]="asd"
    # userset[str(myiter[0]["_id"])]={"tags":myiter[0]["userinfo"]["tags"],"district":myiter[0]["userinfo"]["district"]}
    # print "=================================="
    # print userset[str(myiter[0]["_id"])]
    # print userset
    # print userset[str(myiter[0]["_id"])]["tags"]
    # print userset[str(myiter[0]["_id"])]["district"]
    #########################################################
    # myiter = db.user.find({"userinfo":{"$exists":1}},{"userinfo":1})
    # print myiter.count()
    # i=myiter.count()
    # visited = set()
    # # # # userset={}
    # while(i):
    #     i=i-1
    #     visited.add(str(myiter[i]["_id"]))
    #     # userset[str(myiter[i]["_id"])]={"tags":myiter[i]["userinfo"]["tags"],"district":myiter[i]["userinfo"]["district"]}
    #     print i
    # f1 = open("/home/john/visited1.txt","w")
    # f1.write(str(visited))
    # f1.close()
    #
    # f2 = open("/home/john/userset.txt","w")
    # usersetjson=json.dumps(userset)
    # f2.write(usersetjson)
    # f2.close()
    ########################################################################################
    # visited = get_visited("/home/john/visited_with_tags.txt")
    #print len(visited)
    # a=get_visited("/home/john/visitedfirst50000.txt")|get_visited("/home/john/visited.txt")
    # print len(a)
    # f2 = open("/home/john/visted1.txt","w")
    # #usersetjson=json.dumps(userset)
    # f2.write(a)
    # f2.close()
############将字典转化为json    ##    a = json.dumps(aa)##################################################
############将json转换回字典    ##    aa = json.loads(a)##################################################
    # print myiter[0]["_id"],myiter[0]["userinfo"]["district"]
    # print type(myiter[0]["userinfo"]["tags"])
    # #a["_id"]=int(myiter[0]["_id"])
    # a["tags"]=myiter[0]["userinfo"]["tags"]
    # a["district"]=myiter[0]["userinfo"]["district"]
    # print a["tags"]
    # a["tags"]=myiter[1]["userinfo"]["tags"]
    # a["district"]=myiter[1]["userinfo"]["district"]
    # print a["tags"]
    # b[int(myiter[0]["_id"])]=a
    # print b[2890733820]["tags"]
    #opt = UseroptOnMongo()
    #print opt.connect2Mongo(db_uri,db_name)
    ##print opt.getBlog2Mongo(opt.db, new_blogdata.blog_unit, get_blog_unit)
    ##print opt.getBlog2Mongo(opt.db, new_blogdata.blog_unit, get_blog_unit)
    #mycursor = opt.getUser2Mongo({"userinfo.tags":{$exitsts:true}},{"userinfo.tags":1})
    #printjson(mycursor)
