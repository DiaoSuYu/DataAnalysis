# Builder : Sam
# Build Time: 2021-07-31
# Description： 51job data require


import random  # 随机模块
import collections  # 集合模块相关
import pandas as pd  # 用于数据分析的库
import matplotlib as mpl  # 用于绘图的库
import matplotlib.pyplot as plt  # 用于绘图的库
from wordcloud import WordCloud  # 词云

# 读取需要进行数据分析的文件
name = input("请输入需要进行可视化的文件名：")

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
    if data_experience.index[i] != '暂无数据':
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
