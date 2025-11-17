from selenium import webdriver#(使用selenium代替requests爬取动态网页)
from selenium.webdriver.common.by import By
from selenium.common import exceptions as ex
from tkinter import *
import time
import threading

url = "https://www.douyu.com/topic/2024CFPLSUMMER?rid=12821&dyshid=1cd411fc-ba9a9cb8b7e29bf9486c9b6e00031601"#设置网站url(斗鱼主播直播间,可自由换斗鱼主播)
def Main(width,height):
    root = Tk()
    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()
    pw = (w-width-100)/2
    ph = (h-height-70)/2
    root.geometry("%dx%d+%d+%d"%(width,height,pw,ph))
    #设置窗口大小
    def Request():
        getButton.configure(state = "disabled")#开始按钮锁定
        entrySet.configure(state = "readonly")#关键词栏锁定
        textArea.insert(END,"开始爬取..."+"\n")
        def Handle(key = entrySet.get()):
            endContent=""#文本记录内容
            while(True):
                requestTime=time.strftime('%Y-%m-%d %H:%M:%S')#获取当前时间
                #Element = driver.find_element(By.ID,"js-barrage-list")#使用selenium获取所有实时弹幕
                
                Elementcount = len(driver.find_elements(By.CLASS_NAME,"Barrage-notice--normalBarrage"))#获取弹幕数量
                for i in range(Elementcount-1,Elementcount):#循环查找弹幕
                    try:
                       temp = driver.find_elements(By.CLASS_NAME,"Barrage-notice--normalBarrage")[i].text#获取临时收取弹幕
                    except ex.StaleElementReferenceException:
                        temp = driver.find_elements(By.CLASS_NAME,"Barrage-notice--normalBarrage")[i].text#获取临时收取弹幕(异常时重新获取弹幕)
                    if temp.find(key) == -1:
                        continue#未匹配关键词则跳过循环
                    if (textArea.get("1.0",END)).find(temp) == -1:#收取不重复的弹幕
                        endContent=temp+"\n"#增加获取弹幕
                        try:
                            textArea.insert(END,requestTime+"\n"+endContent+"\n")#插入爬取内容
                        except Exception:
                            continue
                        textArea.see(END)
                    else:
                        continue#错误跳出循环
                
                time.sleep(0.1)#每0.1s刷新一次
                
        driver = webdriver.Chrome()#打开浏览器
        driver.get(url)#打开网页
        driver.implicitly_wait(10)#设置最大等待时间10s
        
        x1 = threading.Thread(target = Handle)
        x1.start()
        #调用多线程处理爬取数据

    def Clear():
        textArea.delete(1.0,END)#清除信息文本区内容

    textArea = Text(root,font = ("微软雅黑",14))
    textArea.place(x = 50,y = 100,width = 300,height = 250)
    textArea.see(END)
    #获取信息文本区域
    Scr = Scrollbar(root)
    Scr.config(command = textArea.yview)
    textArea.config(yscrollcommand = Scr.set)
    Scr.place(x = 350,y = 100,width = 40,height = 250)
    #信息文本滚动条
    entrySet = Entry(root,font =("微软雅黑",12))
    entrySet.place(x = 50,y = 30,width = 150,height = 35)
    #关键词设置区域
    setLabel = Label(root,text = "输入关键词",font = ("微软雅黑",13))
    setLabel.place(x = 210,y = 30)
    #关键词提示标签
    urlEntry = Entry(root,font = ("微软雅黑",11))
    urlEntry.place(x = 350,y = 31,width = 200,height = 31)
    urlEntry.insert(END,url)
    #网站url输入
    urlLabel = Label(root,text = "爬取url",font = ("微软雅黑",13))
    urlLabel.place(x = 560,y = 30)
    #url标签
    getButton = Button(root,text = "开始打印",font = ("微软雅黑",14),command = Request)
    getButton.place(x = 500,y = 250,width = 80,height = 40)
    #开始打印按钮
    clear = Checkbutton(root,text = "清屏",command = Clear)
    clear.place(x = 500,y = 110)
    #清屏选项
    root.mainloop()
    #主界面设置
if __name__ == "__main__":
    Main(650,400)
