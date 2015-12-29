#-*- coding: UTF-8 -*-
from get_data import *
from login import *
from struc import *

if __name__=="__main__":
    driver = getLoginDriver(18330274826,523581600)
    time.sleep(3)
    headers = getHeaders(driver)

    use_url = all_url()
    this_url = use_url.fansurl+str(2)

    req = urllib2.Request(this_url,headers=headers)
    try:
        response = urllib2.urlopen(req)
        data = response.read()

        # file = open("test1.html","w")
        # file.write(data)
        # file.close()

        print data

    except urllib2.URLError,e:
        if hasattr(e,"code"):
            print e.code
        if hasattr(e,"reason"):
            print e.reason
    else:
        print "OK"
