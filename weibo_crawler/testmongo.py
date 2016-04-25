#-*- coding: UTF-8 -*-
#from login import *
#from createMultiCookies.multi import *
from collections import deque
#from getinfo.get_data import *
#from con2mongo.user_Unit import *
#from con2mongo.UserOnMongo import *
from getinfo.getlastdata import *
#from createMultiCookies.login import *
from pymongo import MongoClient
import pymongo
import time
import json
import time
import pdb
#********************-----------------********************#
class MongoProcess(object):
    def __init__(self,db_uri,db_name):
        self.db_uri = "mongodb://labUser:aaaaaa@localhost:27017/?authSource=university"
        self.db_name = "universisy"
        try:
            self.client = MongoClient(self.db_uri)
            self.db = client[self.client]
            print ("connect %s mongodb success" % self.db)
        except:
            print ("connect %s mongodb fail" % self.db)
#********************-----------------********************#

def chinese_zodiac(year):
    d = [u'猴',u'鸡',u'狗',u'猪',u'鼠',u'牛',u'虎',u'兔',u'龙',u'蛇',u'马',u'羊']
    return u'猴鸡狗猪鼠牛虎兔龙蛇马羊'[year%12]
    #  return d[year%12]
    # return year%12

def zodiac(month, day):
    n = [u'摩羯座',u'水瓶座',u'双鱼座',u'白羊座',u'金牛座',u'双子座',u'巨蟹座',u'狮子座',u'处女座',u'天秤座',u'天蝎座',u'射手座']
    d = ((1,20),(2,19),(3,21),(4,21),(5,21),(6,22),(7,23),(8,23),(9,23),(10,23),(11,23),(12,23))
    #return n[len(filter(lambda y:y<=(month,day), d))%12]
    # return len(filter(lambda y:y<=(month,day), d))%12
    return n[len(list(filter(lambda y:y<=(month,day), d)))%12]

def get_decades(year):
    d=(1930,1940,1950,1960,1970,1980,1990,2000,2010)
    return len(list(filter(lambda y:y<=(year),d)))%9-1

def get_birthabout(db):
    i = 0
#    zodiac_count = [0]*12
#    chinese_zodiac_count = [0]*12
    decades_count = [0]*9
    chinese_zodiac_count = {u'猴':0,u'鸡':0,u'狗':0,u'猪':0,u'鼠':0,u'牛':0,\
                            u'虎':0,u'兔':0,u'龙':0,u'蛇':0,u'马':0,u'羊':0}
    zodiac_count = {u'摩羯座':0,u'水瓶座':0,u'双鱼座':0,u'白羊座':0,u'金牛座':0,u'双子座':0,\
                    u'巨蟹座':0,u'狮子座':0,u'处女座':0,u'天秤座':0,u'天蝎座':0,u'射手座':0}

    birthdayiter = db.user.find({"userinfo.birthday":{"$exists":1}},{"userinfo.birthday":1})
    length = birthdayiter.count()
    while(i<length):
        print(i)

        birthday = birthdayiter[i]["userinfo"]["birthday"]
        if len(birthday)==10 and birthday[0:4]!=u'0000' and birthday[5:7]!=u'00' and birthday[8:10]!=u'00' and birthday[0:4]<u'2013' and birthday[0:4]>u'1930':
            print(birthday)
            tmptime=time.strptime(birthday,"%Y-%m-%d")
            chinese_zodiac_count[chinese_zodiac(tmptime[0])]=chinese_zodiac_count[chinese_zodiac(tmptime[0])]+1
            zodiac_count[zodiac(tmptime[1],tmptime[2])]=zodiac_count[zodiac(tmptime[1],tmptime[2])]+1
            decades_count[get_decades(tmptime[0])]=decades_count[get_decades(tmptime[0])]+1

            print ("the chinese_zodiac_count",chinese_zodiac_count)
            print ("the zadiac_count",zodiac_count)
            print ("the decades_count",decades_count)
        if len(birthday)==3:
            zodiac_count[birthday]=zodiac_count[birthday]+1
        i=i+1
    return "OK!"
def get_tags(db):
    i=0
    # tagset=get_visited("/home/john/tagvisitedwithuniversity.txt")
    tagset =set()
    myiter = db.user.find({"userinfo.tags":{"$exists":1}},{"userinfo":1})
    print(myiter.count())
    length=myiter.count()
    while(i<length):
        print(i)
        for item in myiter[i]["userinfo"]["tags"]:
            print(i)
            print(item)
            tagset.add(item)
        i=i+1
    print("the length of tagset is:",len(tagset))
    print(tagset)
    f1 = open("/home/john/tagsetwithuniversity.txt","w")
    f1.write(str(tagset))
    f1.close()
def get_district(db):
    i = 0
    flag = 0
    a=set()
    prov_count ={}
    districtiter = db.user.find({"userinfo.district":{"$exists":1}},{"userinfo.district":1})
    length = districtiter.count()
    while(i<length):
    #while(i<1500):
        print(i)

        # print(districtiter[i]["userinfo"]["district"])
        tmp_prov_city = districtiter[i]["userinfo"]["district"].split(' ')
        #print(tmp_prov_city[0])
        if len(prov_count)==36:
            flag=1
        if flag==1:
            prov_count[tmp_prov_city[0]]=prov_count[tmp_prov_city[0]]+1
        if flag==0:
            if tmp_prov_city[0] in prov_count:
                prov_count[tmp_prov_city[0]]=prov_count[tmp_prov_city[0]]+1
            else:
                prov_count[tmp_prov_city[0]]=1
        print(prov_count)
        i=i+1
    return(prov_count)

def get_sex(db):
    m_count = db.user.count({"userinfo.sex":"男"})
    f_count = db.user.count({"userinfo.sex":"女"})
    return [m_count,f_count]

if __name__=="__main__":
    db_uri = "mongodb://labUser:aaaaaa@localhost:27017/?authSource=university"
    db_name = "university"
    the_chinese_zodiac_count = {'猪': 2389, '鸡': 2303, '马': 2291, '兔': 1723, '虎': 1695, '牛': 1918, \
                                '猴': 2403, '龙': 2095, '蛇': 1812, '羊': 1997, '鼠': 2153, '狗': 3062}
    the_zadiac_count = {'双子座': 2197, '双鱼座': 2348, '摩羯座': 3278, '天秤座': 2569, '射手座': 2126,\
                        '天蝎座': 2592, '水瓶座': 2257, '处女座': 2490, '金牛座': 2087, '白羊座': 2159,\
                        '狮子座': 2407, '巨蟹座': 2136}
    the_decades_count = [16, 47, 109, 488, 2171, 6626, 14848, 1294, 242]
    print(the_chinese_zodiac_count)
    print(the_zadiac_count)
    print(the_decades_count)
    xlient = MongoClient(db_uri)
    db = xlient[db_name]
    print(db)
    # myiter = db.user.find({"userinfo.tags":{"$exists":1}},{"userinfo":1})
    # for item in myiter[5]["userinfo"]["tags"]:
    #     print(item)
    # get_tags(db)
    # print("the_sex_count = ",get_sex(db))
    # district = get_district(db)
#    get_district(db)
    # print(get_birthabout(db))
############将字典转化为json    ##    a = json.dumps(aa)##################################################
############将json转换回字典    ##    aa = json.loads(a)##################################################
# the_chinese_zodiac_count = {'猪': 2389, '鸡': 2303, '马': 2291, '兔': 1723, '虎': 1695, '牛': 1918,\
#                             '猴': 2403, '龙': 2095, '蛇': 1812, '羊': 1997, '鼠': 2153, '狗': 3062}
# the_zadiac_count = {'双子座': 2197, '双鱼座': 2348, '摩羯座': 3278,\
#                     '天秤座': 2569, '射手座': 2126, '天蝎座': 2592,\
#                     '水瓶座': 2257, '处女座': 2490, '金牛座': 2087,\
#                     '白羊座': 2159, '狮子座': 2407, '巨蟹座': 2136}
# the_decades_count = [16, 47, 109, 488, 2171, 6626, 14848, 1294, 242]
# the_district_count = {'上海': 3020, '台湾': 310, '北京': 7251, '贵州': 441, '河南': 1641, '海外': 2807, \
#                       '河北': 2560, '江西': 768, '黑龙江': 794, '西藏': 161, '宁夏': 244, '吉林': 671, \
#                       '山西': 889, '香港': 518, '广西': 726, '澳门': 160, '其他': 6186, '重庆': 881,\
#                       '湖北': 1288, '云南': 780, '江苏': 3580, '新疆': 438, '陕西': 1026, '山东': 1993,\
#                       '内蒙古': 576, '海南': 339, '四川': 1545, '湖南': 1034, '青海': 218, '天津': 750, \
#                       '辽宁': 1191, '浙江': 3289, '甘肃': 559, '福建': 1492, '广东': 4965, '安徽': 990}
# the_sex_count =  [31309, 35083]
# print(the_district_count)
# print(the_chinese_zodiac_count)
# print(the_zadiac_count)
# print(the_decades_count)
# print(the_sex_count)
