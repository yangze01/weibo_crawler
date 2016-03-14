# import re
# userlistdir = '/home/john/userpool.txt'
# userdiropen = open(userlistdir,'r')
# usernameRE = re.compile('(?<=\').*?(?=\',)')
# pwdRE = re.compile('(?<=,\').*?(?=\')')
# userline = userdiropen.readline()
# while userline:
#     print userline
#     usernametmp = usernameRE.findall(userline)
#     pswtmp = pwdRE.findall(userline)
#     print usernametmp[0],pswtmp[0]
#     userline = userdiropen.readline()
#f = open("/home/john/pythonspace/sina_crawler/weibo_crawler/getinfo/info.txt","r")
#data = f.read()
#print data
import re
def get_visited(userdir):
    f = open(userdir,'r')
    idRE = re.compile('(?<=\')\d+?(?=\',)')
    userread = f.read()
    a = idRE.findall(userread)
    f.close()
    print(len(a))
    return set(a)
def get_queue(userdir):
    f = open(userdir,'r')
    idRE = re.compile('(?<=\')\d+?(?=\',)')
    userread = f.read()
    a = idRE.findall(userread)
    f.close()
    print(len(a))
    return a
# a = get_queue("/home/john/queue.txt")
# print a[5]
# b = get_visited("/home/john/visited.txt")
# print b
# print type(b)
