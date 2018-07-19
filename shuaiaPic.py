# -*- coding: utf-8 -*-   
'''
从每页中获取帅哥图片信息，并下载到本地disk
1. 获取每页page_url，列表
2. 解析page_url，获得图片tag信息包括图片链接和图片名
3. 下载到本地 urllib.request.urlretrieve()
'''

import requests
from bs4 import BeautifulSoup
import re
import os
from shutil import rmtree
from urllib.request import urlretrieve
import time


def getHTML(url):
    try:
        head = {'User-Agent':'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'}
        r = requests.get(url, headers = head, timeout = 30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        html = r.text
        return html
    except: 
        return ""

def getPageUrl(url):    #total 45 pages
    pages_url = []
    for num in range(1,46):
        if num == 1:
            page_url = url
        else:
            page_url = url.replace('index','index_%d' % num) #str.replace(old, new[, max])
            #print('page_url=',page_url)
        pages_url.append(page_url)
    return pages_url

def getPic(page_url):
    page_html = getHTML(page_url)
    soup = BeautifulSoup(page_html,'html.parser')
    #print(soup)
    
    a_page = soup.find_all(class_="item-img")
    #print('a_page = ',a_page)

    re_page = r'<img alt="(.*?)".*? src="(.*?)".*?/>'
    #re_page = r'<a class="item-img" href="(.*?)" .*?alt="(.*?)".*?/>'  #这种方式提取的href url，下载后图片无法打开
    p = re.compile(re_page)
    img_pages = p.findall(str(a_page))
    #print('img_page = ',img_pages) 
    return img_pages


if __name__ == "__main__":
    startTime = time.time()
    url = 'http://www.shuaia.net/index.html'

    pages_url = getPageUrl(url)
    #print(pages_url)
    if 'images':            #如果存在，删除images文件夹和目录下的文件
        rmtree('images')    
        #os.removedirs('images')
    if 'images' not in os.listdir():    #如果当前路径没有images文件夹，则创建
        os.makedirs('images')
    
    img_num = 0
    for page_url in pages_url:
        #print('page_url = ',page_url)
        img_pages = getPic(page_url)
        for img_page in img_pages:
            img_num += 1
            img_name = img_page[0] + '.jpg'
            img_url = img_page[1]
            print('Downloading\t%s' % (img_name))
            urlretrieve(img_url,filename='images/' + img_name)
    difTime = time.time() - startTime
    print('total download boys imgages\t',img_num)
    print('total time\t',difTime)
