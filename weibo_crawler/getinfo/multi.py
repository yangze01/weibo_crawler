from get_data import *
from login import *
from user_unit import *

def get_headerstr(k,v):
    '''
        description:use the get Login to get headers with Cookie
        input:
            k:the username of sina_user
            v:the password of sima_user
        output:
            return the headers of a sina_user
    '''
    driver = getLoginDriver(k,v)
    time.sleep(3)
    headers = getHeaders(driver)
    return headers
def get_headerlist(userdict):
    '''
        description:get a list of Hearders
        input:
            userdict:userlist of sina_weibo
        output:
            return a list of headers
    '''
    a=list()
    for (k,v) in userdict.items():
        a.append(get_headerstr(k,v))
    return a
   
if __name__=="__main__":

    headerlist=get_headerlist(a)#返回headers池
    sizeofheaderslist = headerlist.__len__()
