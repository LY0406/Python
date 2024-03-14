import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_rank_data():
    # 目标URL
    url = 'https://www.shanghairanking.cn/rankings/bcur/202311'

    # 请求头信息
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # 发送HTTP请求并获取响应数据
    response = requests.get(url, headers=headers)
    # 设置utf-8编码
    response.encoding = 'utf-8'

    # 解析HTML数据
    soup = BeautifulSoup(response.text, 'html.parser')
    tbody = soup.find('tbody')
    trs = tbody.find_all('tr')

    # 提取排名数据
    rank_data = []
    for tr in trs:
        tds = tr.find_all('td')
        if tds:
            # .replace('\n', ' ').strip() 将所有换行符替换为空格，再将所有空格去除。保证爬取到的数据为有效字符。
            rank = tds[0].get_text().replace('\n', ' ').strip()
            name = tds[1].find('a').get_text().replace('\n', ' ').strip()
            en_name = tds[1].find(class_='name-en').get_text().replace('\n', ' ').strip()
            tags = tds[1].find(class_='tags').get_text().replace('\n', ' ').strip()
            location = tds[2].get_text().replace('\n', ' ').strip()
            category = tds[3].get_text().replace('\n', ' ').strip()
            score = tds[4].get_text().replace('\n', ' ').strip()
            rank_data.append({'rank': rank, 'name': name, 'ename':en_name, 'tags':tags, 'location': location, 'category': category, 'score': score})

    return rank_data

def printInfo(rank_data):
    for data in rank_data:
        print('2023年全国高校排名（前30名）')
        print(data)


def printAnalyseInfo(rank_data):
    # 创建DataFrame
    df = pd.DataFrame(rank_data)
    # 数据概览
    # 使用head()查看前几行数据，以了解数据的结构和内容
    print("数据的前几行内容如下")
    print(df.head())
    # 使用info()获取数据的基本信息，包括列名、非空值数量和数据类型
    print("数据的基本信息如下")
    print(df.info())

    # 数据清洗
    # dropna()删除包含缺失值的行
    print('删除包含缺失值的行后如下')
    print(df.dropna())
    # fillna(value)将缺失值填充为指定的值
    print(df.fillna('缺失值'))

    # 数据分析
    # df[column_name].value_counts()统计每个类别的数量
    print('2023年全国前30名高校中位于不同省市院校各有多少所')
    print(df['location'].value_counts())
    # 按院校类别分类
    print('2023年全国前30名高校中每种类别院校各有多少所')
    print(df.groupby('category').size())



if __name__ == '__main__':
    rank_data = get_rank_data()
    printInfo(rank_data)
    printAnalyseInfo(rank_data)
    # df = pd.DataFrame(rank_data)  # 创建DataFrame
    # print(df.head())  # 打印前几行数据
    # #
    # # # 统计分析
    # # print("\n统计分析：")
    # # print(df.describe())  # 描述性统计
    # # print("\n按地点分组统计：")
    # # print(df.groupby('location').size())  # 按地点分组统计
