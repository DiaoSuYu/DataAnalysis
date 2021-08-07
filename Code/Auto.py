# Builder : Sam
# Build Time: 2021-08-03
# Description： 51job data require, clean, visualization


import os  # 标准库os
import re  # 正则表达
import time  # 时间模块
import xlwt  # 处理xls
import random  # 随机模块
import datetime  # 处理日期和时间的标准库
import requests  # 获取网页信息
import collections  # 集合模块相关
import pandas as pd  # 用于数据分析的库
import matplotlib as mpl  # 用于绘图的库
import matplotlib.pyplot as plt  # 用于绘图的库
from urllib import parse  # url的解析
from wordcloud import WordCloud  # 词云


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


# 清洗数据
def cleandata(name):
    # SETP1:读取需要进行数据分析的文件
    # name = keyword_raw

    # SETP2:使用pandas读取表格,并设定第一列为index,最后将数据存储在data中
    data = pd.read_excel(name + '//' + name + '.xls', name, index_col=0)

    # SETP3:将表格数据转化为csv
    data.to_csv(name + '//' + name + '.csv', encoding='utf-8')

    # SETP4:延时1秒,避免读取过快
    time.sleep(1)

    # SETP5:将csv中的\/替换为/
    with open(name + '//' + name + '.csv', mode='r', encoding='utf8') as raw_data:
        # SETP1:读取整个csv文件
        temporary_data = raw_data.read()
        # SETP2:将整个csv文件中的\/替换为/
        temporary_data = temporary_data.replace('\/', '/')

    with open(name + '//' + name + '.csv', mode='w', encoding='utf8') as new_data:
        # SETP3:将处理过的csv数据写入原文件
        new_data.write(temporary_data)

    # SETP6:延时1秒,避免读取过快
    time.sleep(1)

    # SETP7:读取csv文件
    data = pd.read_csv(name + '//' + name + '.csv')

    # SETP8:将csv的空白处填充为暂无数据
    data = data.fillna('暂无数据')

    # SETP9:读取招聘条件列
    raw_list = data['招聘条件']

    # SETP10:创建新的招聘条件列
    lis = [[0 for i in range(0, 4)] for i in range(0, int(len(raw_list)))]

    # SETP11:将招聘条件列的数据通过','分开,再将文本内容的双引号去除,并写入新的招聘条件列
    for i in range(0, int(len(raw_list))):
        for u in range(0, raw_list[i].count(',') + 1):
            lis[i][u] = str(raw_list[i]).split(",")[u].replace('"', '')

    # SETP12:查询数据残缺行,若数据残缺则将它们存入列表,若数据正常则保存至暂存列表
    del_row = []
    condition_list = []
    for i in range(0, int(len(lis))):
        # SETP1:若数据残缺则记录在del_row列表中
        if 0 in lis[i]:
            del_row.append(i)
        # SETP2:若数据正常则记录在condition_list列表中
        else:
            condition_list.append(lis[i])

    # SETP13:删除数据残缺行
    for i in range(0, int(len(del_row))):
        data = data.drop([del_row[i]], axis=0)

    # SETP14:保存数据                              不增加序号列
    data.to_csv(name + '//' + name + '.csv', encoding='utf-8', index=False)

    # SETP15:延时1秒,避免读取过快
    time.sleep(1)

    # SETP16:读取csv文件
    data = pd.read_csv(name + '//' + name + '.csv')

    # SETP17:新建数据列
    data['经验要求'] = None
    data['学历要求'] = None
    data['招聘人数'] = None

    # SETP18:将SETP12中的正常数据存储中至SETP17新建的数据列
    for i in range(0, int(len(condition_list))):
        data['工作地点'][i] = condition_list[i][0].split('-')[0]
        data['经验要求'][i] = condition_list[i][1]
        data['学历要求'][i] = condition_list[i][2]
        data['招聘人数'][i] = condition_list[i][3]

    # SETP19:删除"招聘条件"列，因为这部分信息已经被拆分填写至"经验要求","学历要求","招聘人数"列
    data = data.drop(["招聘条件"], axis=1)

    # SETP20:将"经验要求","学历要求","招聘人数"列移动至第7,8,9列,方便查阅
    new_row = ['经验要求', '学历要求', '招聘人数']
    for i in range(0, 3):
        mid = data[new_row[i]]
        data.drop(labels=new_row[i], axis=1, inplace=True)
        data.insert(7 + i, new_row[i], mid)

    # SETP21:保存数据                              不增加序号列
    data.to_csv(name + '//' + name + '.csv', encoding='utf-8', index=False)
    print('数据清洗完毕，已保存至\'' + name + '.csv\'')


def analyzedata(name):
    # 读取需要进行数据分析的文件
    # 读取csv数据
    df = pd.read_csv(name + '//' + name + '.csv')
    print('有效数据共' '%s' '条' % df.shape[0])

    # 设置中文字体
    mpl.rcParams['font.family'] = 'SimHei'

    # 设定好填充颜色库
    colors = ['red', 'blue', 'green', 'pink', 'gold', 'violet', 'orange', 'magenta', 'cyan', 'gray']

    # 打乱填充颜色顺序
    random.shuffle(colors)

    print('图表生成中...')

    # ————————————————————————————————————————————————————————————————————————————————————————————————————————
    # 福利待遇
    data_benifit = list(df['福利待遇'].values)
    list_benifit = []
    for i in data_benifit:
        x = i.split(' ')
        for j in x:
            if j not in '暂无数据':
                list_benifit.append(j)

    list_benifit = collections.Counter(list_benifit)
    # 绘制词云
    cloud_benifit = WordCloud(
        background_color='white',  # 设置背景颜色  默认是black
        width=2000,
        height=1000,
        font_path='simhei.ttf',  # 设置字体  显示中文
        max_font_size=200,  # 设置字体最大值
        min_font_size=50,  # 设置子图最小值
        random_state=600,  # 设置随机生成状态，即多少种配色方案
    ).generate_from_frequencies(list_benifit)
    # 设置图像长宽和像素
    plt.figure(figsize=(9, 5), dpi=400)
    # 设置标题
    plt.title('招聘[' + name + ']的福利待遇', fontsize=15)
    # 显示生成的词云图片
    plt.imshow(cloud_benifit, interpolation='bilinear')
    # 显示设置词云图中无坐标轴
    plt.axis('off')
    plt.savefig(name + '//' + "招聘[" + name + "]的福利待遇.png")

    # ————————————————————————————————————————————————————————————————————————————————————————————————————————
    # 主要业务
    data_business = list(df['主要业务'].values)
    list_business = []
    for i in data_business:
        x = i.split('/')
        for j in x:
            if j not in '暂无数据':
                list_business.append(j)
    list_business = collections.Counter(list_business)
    # 绘制词云
    cloud_business = WordCloud(
        background_color='white',  # 设置背景颜色  默认是black
        width=2000,
        height=1000,
        font_path='simhei.ttf',  # 设置字体  显示中文
        max_font_size=200,  # 设置字体最大值
        min_font_size=50,  # 设置子图最小值
        random_state=600,  # 设置随机生成状态，即多少种配色方案
    ).generate_from_frequencies(list_business)
    # 设置图像长宽和像素
    plt.figure(figsize=(9, 5), dpi=400)
    # 设置标题
    plt.title('招聘[' + name + ']的公司主要业务', fontsize=15)
    # 显示生成的词云图片
    plt.imshow(cloud_business, interpolation='bilinear')
    # 显示设置词云图中无坐标轴
    plt.axis('off')
    plt.savefig(name + '//' + "招聘[" + name + "]的公司主要业务.png")

    # ————————————————————————————————————————————————————————————————————————————————————————————————————————
    # 公司类型
    data_type = df['公司类型'].value_counts()

    # 横坐标
    labels_type = []
    for i in range(0, len(data_type.index)):
        if data_type.index[i] != '暂无数据':
            labels_type.append(data_type.index[i])

    # 纵坐标
    num_type = [data_type[i] for i in labels_type]

    # 设置图像长宽和像素
    plt.figure(figsize=(9, 6), dpi=400)

    # 添加描述信息
    plt.title('招聘[' + name + ']的公司类型', fontsize=15)

    type = plt.barh(
        labels_type,  # 纵坐标
        num_type,  # 横坐标
        height=0.7,  # 图形宽度
        color=colors,  # 随机颜色
        align="center",  # 居中对齐
    )

    # 添加柱形图详细参数
    for rect in type:
        width = rect.get_width()
        plt.text(rect.get_width(), rect.get_y() + rect.get_height() / 2, '%s' % int(width), ha='left', va='center')

    plt.savefig(name + '//' + "招聘[" + name + "]的公司类型.png")

    # ————————————————————————————————————————————————————————————————————————————————————————————————————————
    # 公司规模
    data_scale = df['公司规模'].value_counts()

    # 纵坐标
    labels_scale = []
    for i in range(0, len(data_scale.index)):
        if data_scale.index[i] != '暂无数据':
            labels_scale.append(data_scale.index[i])

    # 横坐标
    num_scale = [data_scale[i] for i in labels_scale]

    # 设置图像长宽和像素
    plt.figure(figsize=(9, 5), dpi=400)

    # 绘制水平柱状图
    plt.title('招聘[' + name + ']的公司规模', fontsize=15)
    scale = plt.barh(
        labels_scale,  # 纵坐标
        num_scale,  # 横坐标
        height=0.5,  # 图形宽度
        color=colors,  # 随机颜色
        align="center",  # 居中对齐
    )

    # 添加柱形图详细参数
    for rect in scale:
        width = rect.get_width()
        plt.text(rect.get_width(), rect.get_y() + rect.get_height() / 2, '%s' % int(width), ha='left', va='center')

    plt.savefig(name + '//' + "招聘[" + name + "]的公司规模.png")

    # ————————————————————————————————————————————————————————————————————————————————————————————————————————
    # 工作地点
    data_site = df['工作地点'].value_counts()

    # 分别读取工作地点列中岗位最多的城市前十名
    city = list(data_site.index)[:10]  # 城市
    job_count = list(data_site.values)[:10]  # 岗位

    # 设置图像长宽和像素
    plt.figure(figsize=(8, 5), dpi=400)

    # 添加描述信息
    plt.title('招聘[' + name + ']最多的城市前十名', fontsize=15)

    # 绘制柱形图
    site = plt.bar(
        city,  # 横轴显示为城市
        job_count,  # 纵轴显示为岗位数
        width=0.5,  # 单个柱的显示宽度
        color=colors  # 颜色填充
    )

    # 添加柱形图详细参数
    for rect in site:
        height = rect.get_height()
        plt.text(rect.get_x() + 0.1, height * 1.005, '%s' % int(height), ha='left', va='bottom')

    plt.savefig(name + '//' + "招聘[" + name + "]最多的城市前十名.png")
    # ————————————————————————————————————————————————————————————————————————————————————————————————————————

    # 薪资水平
    data_salary = df['薪资水平']
    # 图例标题
    lable_salary = ['5K-10K', '10K-15K', '15K-20K', '20K-25K', '25K-30K', '30K-35K', '35-50K', '50K以上']
    # 初始化各个薪资区间的分布数
    level1, level2, level3, level4, level5, level6, level7, level8 = 0, 0, 0, 0, 0, 0, 0, 0
    # 初始化薪资等级
    salary = None
    # 通过计算薪资中位数来确定薪资所属的区间
    for i in data_salary.values:
        # 计算中位数
        if i[-3:] == '万/月':
            i = i.replace('万/月', '-万/月')
            x = i.split('-')
            salary = (float(x[0]) + float(x[1])) * 10 / 2
        elif i[-3:] == '千/月':
            i = i.replace('千/月', '-千/月')
            x = i.split('-')
            salary = (float(x[0]) + float(x[1])) / 2
        elif i[-3:] == '万/年':
            i = i.replace('万/年', '-万/年')
            x = i.split('-')
            salary = (float(x[0]) + float(x[1])) / 2 / 12
        else:
            continue

        # 分配薪资所属区间
        if 5 < salary <= 10:
            level1 += 1
        elif 10 < salary <= 15:
            level2 += 1
        elif 15 < salary <= 20:
            level3 += 1
        elif 20 < salary <= 25:
            level4 += 1
        elif 25 < salary <= 30:
            level5 += 1
        elif 30 < salary <= 35:
            level6 += 1
        elif 35 < salary <= 50:
            level7 += 1
        else:
            level8 += 1

    # 保存薪资在各个分布区间的个数
    num_salary = [level1, level2, level3, level4, level5, level6, level7, level8]

    # 设置图像长宽和像素
    plt.figure(figsize=(8, 6), dpi=400)

    # 添加描述信息
    plt.title('招聘[' + name + ']的薪资水平', fontsize=15)

    # 设置饼图各部分是否突出以及突出距离
    explodes = [0, 0, 0, 0.1, 0.2, 0.3, 0.4, 0.5]
    plt.pie(
        num_salary,
        pctdistance=0.75,  # 设置圆内文本距圆心距离
        colors=colors,  # 设置填充颜色
        autopct='%.2f%%',  # 设置圆里面文本
        explode=explodes,  # 设置各部分突出
        startangle=0,  # 起始角度
        labeldistance=5,  # 设置标签文本距圆心位置，1.1表示1.1倍半径
    )

    # 设置图例                  调节图例位置
    plt.legend(lable_salary, bbox_to_anchor=(1.0, 1.0))

    plt.savefig(name + '//' + "招聘[" + name + "]的薪资水平.png")

    # ————————————————————————————————————————————————————————————————————————————————————————————————————————
    # 经验要求
    data_experience = df['经验要求'].value_counts()

    # 图例标题
    lable_experience = []
    for i in range(0, len(data_experience.index)):
        if data_experience.index[i] != '在校生/应届生':
            lable_experience.append(data_experience.index[i])
    num_experience = [data_experience[i] for i in lable_experience]

    # 将在校生/应届生统筹至无需经验类
    if '在校生/应届生' in data_experience:
        num_experience[0] = num_experience[0] + data_experience['在校生/应届生']

    # 设置图像长宽和像素
    plt.figure(figsize=(8, 5), dpi=400)

    # 添加描述信息
    plt.title('招聘[' + name + ']的经验要求', fontsize=15)

    # 绘制柱形图
    experience = plt.bar(
        lable_experience,  # 横轴显示为城市
        num_experience,  # 纵轴显示为岗位数
        width=0.5,  # 单个柱的显示宽度
        color=colors  # 颜色填充
    )

    # 添加柱形图详细参数
    for rect in experience:
        height = rect.get_height()
        plt.text(rect.get_x() + 0.175, height * 1.005, '%s' % int(height), ha='left', va='bottom')

    plt.savefig(name + '//' + "招聘[" + name + "]的经验要求.png")
    # ————————————————————————————————————————————————————————————————————————————————————————————————————————

    # 学历要求
    data_edu = df['学历要求'].value_counts()

    # 纵坐标
    label_edu = data_edu.index

    # 横坐标
    num_edu = [data_edu[i] for i in label_edu]

    # 设置图像长宽和像素
    plt.figure(figsize=(9, 5), dpi=400)

    # 绘制水平柱状图
    plt.title('招聘[' + name + ']对学历的要求', fontsize=15)
    edu = plt.barh(
        label_edu,
        num_edu,
        height=0.5,
        color=colors,
        align="center",
    )
    # 添加柱形图详细参数
    for rect in edu:
        width = rect.get_width()
        plt.text(rect.get_width(), rect.get_y() + rect.get_height() / 2, '%s' % int(width), ha='left', va='center')
    plt.savefig(name + '//' + "招聘[" + name + "]的学历要求.png")
    print('制图完毕，已保存至\'' + name + '\'文件夹下')


# 主函数
def main():
    # 记录开始时间
    start = datetime.datetime.now()

    # 搜索参数设定
    keyword_raw = input("请输入需要搜索的岗位关键字：")
    pages = input("请输入需要搜索的页数：")
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

    # 清洗数据
    cleandata(keyword_raw)

    # 分析数据
    analyzedata(keyword_raw)

    # 打印总耗时
    delta = (datetime.datetime.now() - start).total_seconds()
    print("用时：{:.3f}s".format(delta))


if __name__ == '__main__':
    main()
