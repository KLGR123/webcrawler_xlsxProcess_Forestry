import json
import os
import pandas as pd
import re

f = open('continent.json', 'r', encoding='utf-8')
data = f.read()
data = json.loads(data) #打开地理json数据 转换为列表data

def getFileList(path): #给入相对路径 返回内部文件名列表
    filelist = []
    for file in os.listdir(path): #遍历所有子文件
        filelist.append(str(file))
    return filelist

def renewFile(file): #给入file(xlsx) 在其最后一列加入中文名信息 并保存
    matrix = pd.read_excel('download/%s' % file)
    countries = matrix.loc[:, 'country'] #此处的索引可能需要修改
    if len(countries) == 0:
        print('countries dont exist!')
    cons = [] #中文列
    for country in countries:
        con = findCh(country)
        cons.append(con)
    matrix['中文名'] = cons #末尾添加 位置也可修改
    
    #打开并写入操作
    output = pd.ExcelWriter('download/%s' % file, mode='')  # pylint: disable=abstract-class-instantiated
    matrix.to_excel(output)  
    output.save()

def findCh(country):
    ctr = str(country)
    for con in data: #注意中英文可能不同
        if con['country_name'] == ctr:
            return con['country_cname']

filels = getFileList('download') #此处可修改 选入文件 download内放入所有下载数据xlsx
for file in filels:
    renewFile(file)