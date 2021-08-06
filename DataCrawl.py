# Builder : Sam
# Build Time: 2021-07-20
# Description： 51job data require


import os           # 标准库os
import re           # 正则表达
import xlwt         # 处理xls
import datetime     # 处理日期和时间的标准库
import requests     # 获取网页信息
from urllib import parse    # url的解析


# 写入表头数据
def sheethead(sheet):
    row = ('岗位名称', '公司名称', '公司类型', '公司规模', '主要业务', '工作地点', '薪资水平', '福利待遇', '招聘条件', '公司链接', '岗位链接')
    for num in range(0, 11):
        sheet.write(0, num, row[num])  # 列名


# 获取一个列表页
def geturl(url):
    # 添加headers用来让网页识别当前请求是由用户浏览器发起的
    headers = {
        'User-Agent': 'Mozilla/5.0(Windows NT 10.0; WOW64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 90.0.4430.85 Safari / 537.36'
    }

    # 用requests.get获得整页的文本数据
    pagedata = requests.get(url=url, headers=headers).text

    return pagedata


# 获取列表页的所有岗位信息
def getdata(pagedata):
    # 用正则表达式设定读取参数的规则
    formatlist = [
        '"job_name":"(.*?)"',  # 岗位名称
        '"company_name":"(.*?)"',  # 公司名称
        '"companytype_text":"(.*?)"',  # 公司类型
        '"companysize_text":"(.*?)"',  # 公司规模
        '"companyind_text":"(.*?)"',  # 主要业务
        '"workarea_text":"(.*?)"',  # 工作地点
        '"providesalary_text":"(.*?)"',  # 薪资水平
        '"jobwelf":"(.*?)"',  # 福利待遇
        '"attribute_text":\[(.*?)\]',  # 招聘条件
        '"company_href":"(.*?)"',  # 公司链接
        '"job_href":"(.*?)"',  # 岗位链接
    ]

    # 创建数据列表
    datalist = []

    for i in range(0, len(formatlist)):
        # 第一个参数是规则，第二个参数是被检索内容，第三个参数re.S是使.匹配包括换行在内的所有字符
        datalist.append(re.findall(formatlist[i], pagedata, re.S))

    return datalist


# 保存数据
def savedata(sheet, datalist, page, num):
    for i in range(0, num):
        row = (page - 1) * 50 + (i + 1)
        for j in range(0, 11):
            data = (datalist[j])[i]
            sheet.write(row, j, data)


def main():
    start = datetime.datetime.now()
    # 搜索关键字
    keyword_raw = input("请输入需要搜索的岗位关键字：")
    pages = input("请输入需要搜索的页数：")

    # 创建文件
    filepath = keyword_raw + ".xls"

    # 创建文件夹
    if not os.path.exists(keyword_raw):
        os.makedirs(keyword_raw)

    # 创建一个workbook并设置编码
    book = xlwt.Workbook(encoding='utf-8')

    # 创建工作表
    sheet = book.add_sheet(keyword_raw)

    # 写入表格的表头数据
    sheethead(sheet)

    # 汉字编码
    keyword = parse.quote(keyword_raw)

    # 开始搜索并保存数据
    for page in range(1, int(pages) + 1):
        # 设置网页参数
        url = "https://search.51job.com/list/000000,000000,0000,00,9,99," + keyword + ",2," + str(page) + ".html"

        # 获取网页数据
        pagedata = geturl(url)

        # 获取岗位信息
        datalist = getdata(pagedata)

        # 获取信息成功
        if datalist:
            print('爬取第%d页数据成功' % page)
            #        工作表 数据列表 网页页数 单页数据总数
            savedata(sheet, datalist, page, len(datalist[0]))
            book.save(keyword_raw + '//' + filepath)
            print('存储第%d页数据成功' % page)

        # 获取信息失败
        else:
            print('无数据')
            break

    print('共存储%d页数据' % page)
    delta = (datetime.datetime.now() - start).total_seconds()
    print("用时：{:.3f}s".format(delta))

if __name__ == '__main__':
    main()
