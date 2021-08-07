# Builder : Sam
# Build Time: 2021-07-27
# Description： 51job data clean


import time  # 时间模块
import pandas as pd  # 用于数据分析的库


def main():
    # SETP1:读取需要进行数据分析的文件
    name = input("请输入需要进行数据清洗的文件名：")

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


if __name__ == '__main__':
    main()
