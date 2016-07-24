#-*-coding:UTF-8-*-
'''首先在python文件下创建一个叫youmin的文件夹'''
import re
import urllib
import threading
import time
from Tkinter import *
import os
#清除文件夹youmin下面的旧图片，请手动建立该文件夹
for filename in os.listdir('youmin'):
    os.remove(os.path.join( 'youmin', filename ))

src='<img class="picact".*?src="(.*?)"'
detail1='<img class="picact".*?</a><br>.*?</p>'
titlelist=[]
urllist=[]
img=re.compile(src)
detail=re.compile(detail1)

def gethtml(url):
    #获取网页所有源码
    return urllib.urlopen(url).read()

def getimg(html,s):
    
     #下载图片
    global img
    try:
        imglist=re.findall(img,html)
        x=0
        for i in imglist:
            #下载图片
            urllib.urlretrieve(i,'.\\youmin\\'+str(s)+str(x)+i[-4:])
            x+=1
    except:
        
         pass

class getmy(threading.Thread):
     #创建多线程
    def __init__(self,url,begin,end):
        threading.Thread.__init__(self)
        self.url=url
        self.begin = begin
        self.end =end
    def run(self):
        try:
            for i in range(self.begin,self.end+1):
                s=i
                if i==1:
                    i=''
                else:
                    i='_'+str(i)
                murl = self.url[:-6]+str(i)+self.url[-6:]
                #print murl
                getimg(gethtml(murl),s)
        except:
            pass

        
root = Tk()
def printList(event):
    targeturl= urllist[lb.curselection()[0]]
    
    threads =[]
    i=1
    j=5
    #每个线程下载5页，一共下载50页
    for s in range(10):
         threads.append(getmy(targeturl,i,j))
         i+=5
         j+=5
    for t in threads:
         t.start()        
    for t in threads:
         t.join()
   
lb = Listbox(root,width=40,height=20)
lb.bind('<Double-Button-1>',printList)

def getbaseurl():
    
    url='http://www.gamersky.com/ent/'#游民每日图片发布页
    s=urllib.urlopen(url).read()
    urlhtm1='<a class="img1" target="_blank" .*?</a>'#寻找图片发布页网址所在的html区域
    urlhtm2='<a class="img2" target="_blank" .*?</a>'
    herfhtm='http:.*?shtml'#图片发布页网址
    title='<div class="txt">(.*?)</div>'
    urs1=re.compile(urlhtm1)
    urs2=re.compile(urlhtm2)    
   # urs=re.compile(herfhtm)
    urllist1=re.findall(urs1,s)#查找所有最新图片发布页网址
    urllist2=re.findall(urs2,s)
    divlist=urllist1+urllist2
    
    for i in divlist:
        urllist.append(re.search(herfhtm,i).group())
        title1=re.search(title,i).group(1)
        lb.insert(END,title1)
        titlelist.append(title1)
        #print i


getbaseurl()   
lb.pack()
root.mainloop()







