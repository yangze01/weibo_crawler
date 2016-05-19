# -*- coding: UTF-8 -*-
import os,re,urllib,uuid
import threading
import time
#首先定义云端的网页,以及本地保存的文件夹地址
def getUrlList(startid,endid):
    imgUrlList = list()
    for i in range(startid,endid):
        tmpurl = "http://zxpic.gtimg.com/infonew/0/media_pics_-"+str(i)+".jpg/800"
        imgUrlList.append(tmpurl)
    return imgUrlList

class savePhoto(threading.Thread):
    def __init__(self,threadname):
        threading.Thread.__init__(self)
        self.threadname = threadname
        self.localPath='/home/john/photo/'
    #生成一个文件名字符串
    def generateFileName(self):
        #print(uuid.uuid1())
        return str(uuid.uuid1())
    #根据文件名创建文件
    def createFileWithFileName(self,localPathParam,fileName):
        totalPath=localPathParam+'\\'+fileName
        if not os.path.exists(totalPath):
            file=open(totalPath,'a+')
            file.close()
            return totalPath
    #根据图片的地址，下载图片并保存在本地
    def getAndSaveImg(self,imgUrl):
        if( len(imgUrl)!= 0 ):
            self.fileName=self.generateFileName()+'.jpg'
            urllib.urlretrieve(imgUrl,self.createFileWithFileName(self.localPath,self.fileName))
    # def downloadImg(startid,endid):
    #     urlList=getUrlList(startid,endid)
    #     for urlString in urlList:
    #         print(urlString)
    #         getAndSaveImg(urlString)
    def run(self):
        global queue
        while queue:
            if queue:
                CONDITION.acquire()
                catch_url = queue.pop()
                print (self.threadname+"   :   "+catch_url)
                CONDITION.release()
                self.getAndSaveImg(catch_url)
#从一个网页url中获取图片的地址，保存在
#一个list中返回
# def getUrlList(urlParam):
#     urlStream=urllib.urlopen(urlParam)
#     htmlString=urlStream.read()
#     if( len(htmlString)!=0 ):
#         patternString=r'http://.{0,50}\.jpg'
#         searchPattern=re.compile(patternString)
#         imgUrlList=searchPattern.findall(htmlString)
#         return imgUrlList


def mainthread(num):
    threadlist=list()
    for i in range(1,num):
        tmp = savePhoto("thread"+str(i))
        threadlist.append(tmp)
    for j in threadlist:
        j.start()









#下载函数
if __name__=="__main__":
    urlPath='http://gamebar.com/'
    CONDITION = threading.Condition()
    # queue = getUrlList(13444649,13444649)
    queue = getUrlList(1109587,1119114)
    mainthread(100)
