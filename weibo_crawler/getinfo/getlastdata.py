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
