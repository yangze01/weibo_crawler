import re
userlistdir = '/home/john/userpool.txt'
userdiropen = open(userlistdir,'r')
usernameRE = re.compile('(?<=\').*?(?=\',)')
pwdRE = re.compile('(?<=,\').*?(?=\')')
userline = userdiropen.readline()
while userline:
    print userline
    usernametmp = usernameRE.findall(userline)
    pswtmp = pwdRE.findall(userline)
    print usernametmp[0],pswtmp[0]
    userline = userdiropen.readline()
