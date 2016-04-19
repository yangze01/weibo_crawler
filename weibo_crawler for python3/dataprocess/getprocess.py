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
