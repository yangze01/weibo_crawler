import urllib
import urllib2
import cookielib
def get_data(this_url,headers):
    req = urllib2.Request(this_url,headers=headers)
    response = urllib2.urlopen(req)
    data = response.read()
    return data

def get_pageNum(data):
    re_pagenum = '<input name="mp" type="hidden" value=.*?>'
    pattern = re.compile(re_pagenum,re.S)
    items = re.findall(pattern,data)
    item=items[0]
    return int(item[38:-4])

def get_fansfollow(catch_url,headers):
    idnset=set()
    home_page = catch_url+'1'
    data1 = get_data(home_page,headers)
    page=get_pageNum(data1)

    re_id = '<a href="http://weibo.cn/u/\d{0,11}">[^<].*?[^>]</a>'
    pattern = re.compile(re_id,re.S)
    for i in range(1,page):
        this_url = catch_url+str(i)
        data = get_data(this_url,headers)
        items = re.findall(pattern,data)
        for item in items:
            idnset.add(item[27:37]+item[39:-4])
    return idnset

def get_friends(fansset,followset):
    return fansset&followset
