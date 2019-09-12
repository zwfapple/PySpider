'''
Author: Apple Zhang; from 09/04/2019 to 09/06/2019
description: 根据拉勾网中对相关python、java、PHP、C++职位结果分析：薪资，福利，经验，学历；公司规模，融资情况，城市等
'''

# -*- coding: utf-8 -*-   
'''
import 执行顺序
1. 查找执行文件所在目录
2. 查找执行文件所属的项目目录
3. 查找path环境配置的目录
'''

import sys
sys.path.append('../common') #add common folder to system env path
import spiderfunc as sf  #spiderfunc.py under common folder

from random import choice
from bs4 import BeautifulSoup
import requests

#get url for each search
def getURL(s):
    url = 'https://www.lagou.com/jobs/list_' + s
    return url

def getHTML(s):
    url = getURL(s) 
    #print(url)
    
    #print(choice(sf.getUserAgent()))
    head = {'User-Agent':choice(sf.getUserAgent())}
    r = requests.get(url,headers = head,timeout = 30)
    r.raise_for_status
    r.encoding = r.apparent_encoding
    html = r.text
    return html
         
    
#lis = ['python','Java','PHP','C++']
s = 'python'

html = getHTML(s)
#print(html)

f = open('html.txt','w')
f.write(html)

soup = BeautifulSoup(html,'html.parser')  #soup = BeautifulSoup(open(index.html)) #local html file index.html to create object
#print(soup.prettify()) #format the html file as html
print(soup.find_all('li',class_="con_list_item default_list"))   
print(soup.li.attrs)
#print(soup.name)
#print(soup.a.attrs)   #get all attributions for tag 'a' , return dictionary type
#print(soup.a['href'])  #get value for attribute 'href', ==soup.a.get('href')
#print(soup.span.string)






