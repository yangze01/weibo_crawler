import re
def get_visited(userdir):
    f = open(userdir,'r')
    idRE = re.compile('(?<=\')\d+?(?=\',)')
    userread = f.read()
    a = idRE.findall(userread)
    f.close()
    id = "5357651574"
    if id in a:
        a.remove("5357651574")
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
