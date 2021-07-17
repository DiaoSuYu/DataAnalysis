# Builder : Sam
# Build Time: 2021-07-17

# 用到的技术点：
# 1. requests 发送请求，从服务器获取数据
# 2. BeautifulSoup 解析整个页面的源代码
# 3. 本地文件写入与删除



import os
import sys
import shutil  # 用于删除
import requests
from bs4 import BeautifulSoup



def openFile(path,fileName):
    url = path + fileName
    if os.path.exists(url): #判断目录是否存在
        shutil.rmtree(url)  #删除目录，包括目录下的所有文件
    os.mkdir(url)   #创建目录

def netpagerequests(netaddress):
    resp = requests.get(netaddress)     # 发送请求到子页面
    resp.encoding = "utf-8"     # 转化网页编码格式
    child_page = BeautifulSoup(resp.text, "html.parser")    # 解析拉取下来的子页面html
    return child_page

def mainpagelist(main_page):
    alist = main_page.find("div", attrs={"class": "TypeList"}).findAll("a", attrs={"class": "TypeBigPics"})     # 获取主页列表
    return alist

def findfilename(child_page):
    name = child_page.find("div", attrs={"class": "ArticleTitle"}).find("strong")   # 获取文件名
    name = str(name).split(">")[1].split("<")[0]    # 去除文件名内的杂项
    return name

def findfiledownloadpath(child_page):
    src = child_page.find("div", attrs={"class": "ImageBody"}).find("img").get("src")   # 拉取文件的下载地址
    return src

def judgeiscollective(child_page):
    totalpagelist = child_page.find("div", attrs={"class": "NewPages"}).findAll("a")    # 判断是否为套图
    return totalpagelist

def findfolderaddress():
    return str(sys.argv).split("main.py")[0].split("['")[1]     # 获取当前文件夹的地址

def findtotalnum(totalpagelist):
    totalnum = (str(totalpagelist[-1])).split("_")[-1].split(".")[0]    # 获取总页码
    return totalnum

def findpagenum(href):
    pagenum = href.split(".")[0]    # 获取当前页的页码
    return pagenum

def downloadcollective(name, folderaddress, src, num):
    filename = name + "_%s.jpg" % num
    print("开始下载套图：" + name + "的第" + str(num) + "张图片")
    picture = open(folderaddress + name + "/" + filename, mode="wb+")  # "wb"表示写入的文件内容是非文本
    picture.write(requests.get(src).content)  # 向外取出数据，注意这里的数据不再是文本信息，而是需要下载的文件
    print("下载成功：" + name + "的第" + str(num) + "张图片")

def downloadsingle(name, folderaddress, src):
    filename = name + ".jpg"
    print("开始下载：" + name + "的图片")
    picture = open(folderaddress + name + "/" + filename, mode="wb+")  # "wb"表示写入的文件内容是非文本
    picture.write(requests.get(src).content)  # 向外取出数据，注意这里的数据不再是文本信息，而是需要下载的文件
    print("下载成功：" + name + "的图片")



def main():
    main_page = netpagerequests("https://www.umei.net/meinvtupian/")    # 套图测试网址
    #main_page = netpagerequests("https://www.umei.net/bizhitupian/")   # 单图测试网址

    # 拉取主页的图片队列
    alist = mainpagelist(main_page)

    # 图片数量计数器，初始值为1
    num = 1
    for a in alist:
        href = a.get("href")
        child_page = netpagerequests("https://www.umei.net/" + href)

        # 找到图片的名字
        name = findfilename(child_page) 

        # 找到图片的真实路径
        src = findfiledownloadpath(child_page)  

        # 判断是否为套图，如果是则读取此套图一共有多少图片
        totalpagelist = judgeiscollective(child_page)

        # 读取当前文件夹地址
        folderaddress = findfolderaddress()

        # 创建即将下载的文件的所属文件夹
        openFile(folderaddress, name)

        # 判断是否为套图
        if totalpagelist:
            # 读取套图的图片总数
            totalnum = findtotalnum(totalpagelist)

             # 读取图片所在页的序号
            pagenum = findpagenum(href)

            # 发送请求到服务器，将图片保存到本地
            downloadcollective(name, folderaddress, src, num)    # 下载套图的第一张图片
            num = num + 1

            for i in range(2, int(totalnum) + 1):
                child_page = netpagerequests("https://www.umei.net/" + pagenum + "_" + str(i) + ".htm")

                # 找到图片的真实路径
                src = findfiledownloadpath(child_page)

                # 发送请求到服务器，将套图保存到本地
                downloadcollective(name, folderaddress, src, num)     # 下载套图的剩余图片
                num = num + 1

            # 计数器回归初始值
            num = 1

        else:
            # 发送请求到服务器，将单图保存到本地
            downloadsingle(name, folderaddress, src)


if __name__ == '__main__':
    main()