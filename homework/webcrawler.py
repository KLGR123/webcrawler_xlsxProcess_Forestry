import re
import json
import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Cookie': 'JSESSIONID=1A15D38C3584CF10C2148E61109CA0E6; u=1; experience=show',
    'Host': 'data.stats.gov.cn',
    'Referer': 'http://data.stats.gov.cn/easyquery.htm?cn=C01&zb=A0C07&sj=2019', 
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.40',
    'X-Requested-With': 'XMLHttpRequest'
}

def getPage(url): #给入url 返回json数据
    response = requests.request('GET', url, headers=headers)
    resp = response.apparent_encoding #encode
    response.encoding = resp
    return(response.text) #返回数据的text即json数据

def getData(data): #给入json数据表 返回其中所需数据
    data = json.loads(data)
    dic =  data['returndata']['datanodes'] #索引解包

    i = 0 #计数器
    results = []
    result = [] #result单位读取数据 results容器盛接
    results.insert(0, year) #先插入年份行数据

    for each in dic:
        result.append(each['data']['data'])
        i += 1 
        if i >= len(year): #计数器到定长度 装载一次 构成二维矩阵
            results.append(result)
            result = []
            i = 0  
    return results

def transpose(matrix): #转置矩阵 此处制图需要
    new_matrix = []
    for i in range(len(matrix[0])):
        matrix1 = []
        for j in range(len(matrix)):
            matrix1.append(matrix[j][i])
        new_matrix.append(matrix1)
    return new_matrix

def output(results): #给入矩阵 写入xlsx文件
    matrix = pd.DataFrame(results, columns=columns)
    matrix.to_excel(fname, index=False)

f = open('datastats.json', 'r', encoding='utf-8')
data = f.read()
data = json.loads(data) #打开存储网站信息json数据 转换为列表data

for each in data:
    year = each['year']
    print(year)
    url = each['url']
    print(url)
    columns = each['columns']
    print(columns)
    fname = each['fname']
    print(fname)

    html = getPage(url)
    results = getData(html)
    results = transpose(results)
    output(results)
    print('successfully done %s!' % fname)
