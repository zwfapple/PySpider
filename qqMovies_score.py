# -*- coding: utf-8 -*-   
import re  
import requests
from bs4 import BeautifulSoup 
import string, time  
from random import random
import os
#import pymongo  

m_site = u'qq' #全局变量,电影网站  

#根据指定的URL获取网页内容  
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

#从电影分类列表页面获取电影分类 tag = ('1', '剧情')
def getMovieTypeList(html):
    #global m_type
    soup = BeautifulSoup(html, 'html.parser')  #过滤出分类内容 
    #print(soup)  

    tags_all = soup.find_all('div', {'class' : 'filter_content' })   #找到所有div.filter_content下的a标签
    re_tags = r'<a _stat2=".*?subtype=.*?" class="item" href=".*?;subtype=(.*?)">(.*?)</a>' #(.*?)
    p = re.compile(re_tags) #, re.DOTALL句号(.)是匹配任何除换行符之外的任意字符,使用DOTALL标志，就可以让它匹配所有字符，不再排除换行符了
    tags = p.findall(str(tags_all[0]))
    #print('tags = ',tags)

    if tags:
        tags_type = {}
        for tag in tags:
            #print(tag)    #tag = ('1', '剧情')      
            tag_subtype = tag[0]
            m_type = tag[1]
            #print('m_type = ',m_type)
            tags_type[m_type] = tag_subtype 
            #print('tags_type[m_type] = ',tags_type[m_type])
    else:
        print("Not Find")
    return tags_type

#获取每个分类的页数?offset=0&subtype=2
def get_pages(url, tag_type):
    tag_url = url + '?offset=0' + '&subtype=' + tag_type 
    tag_html = getHTML(tag_url)
    soup = BeautifulSoup(tag_html, 'html.parser')  #过滤出标记页面的html
    #print(soup)

    div_page = soup.find_all('div', {'class' : 'mod_pages'})
    #print('div_page=',div_page) #len(div_page), div_page[0]
    if div_page == []:  #只有一页时没有div标签，div_page是空[]
        return 1

    re_pages = r'<a _stat2=".*?" class=".*?" href=".*?">(.*?)</a>'
    p = re.compile(re_pages)
    pages = p.findall(str(div_page[0]))
    #print(pages,len(pages))
    if len(pages) > 1:
        return pages[-2]
    else:
        return 1

#获取某个类型m_type的所有页面的url
def get_pages_url(url,m_type):
    if m_type:
        pages_url = []
        #for m_url in movie_type.items():
        #print('m_url = ', m_url)   #('剧情', '1')
        tag_url = url + '?subtype=' + m_type[1] + '&offset=0'
        #print('m_type is %s , tag_url = %s' % (m_type[0],tag_url), end = '')
        #print('tag_type=',str(m_url[1])) #m_url[0] = '剧情'
        maxpage = int(get_pages(url, str(m_type[1])))
        #print(', total pages are ', maxpage)
            
        for x in range(0,maxpage):
            #http://v.qq.com/x/list/movie?offset=30&subtype=16
            #str.replace(old, new[, max])
            page_url = tag_url.replace('0', '') + str(x*30)
            #print('page_url = ',page_url)  #某个分类下，每个页面的url，如分类为18的第四页：http://v.qq.com/x/list/movie?subtype=18&offset=90
            pages_url.append(page_url)
        return pages_url
    else:
        return "Not Find page url"

#获取每个页面的电影名和对应的m_url
def getmovielist(html): #html 分类页面文本，用gethtml(str(tag_url[1]))
    global m_site
    soup = BeautifulSoup(html, 'html.parser')
    divs = soup.find_all('ul', {'class' : 'figures_list'})  #movie的信息

    re_movie = r'<a _stat2="videos:title" href="(.*?)" target=".*?" title=".*?">(.*?)</a>' #movie_url, movie_name
    p = re.compile(re_movie, re.DOTALL) #, re.DOTALL句号(.)是匹配任何除换行符之外的任意字符,使用DOTALL标志，就可以让它匹配所有字符，不再排除换行符了
    movies = p.findall(str(divs[0]))
    #print(movies)
    return movies

def getmovieScore(html): #html 分类页面文本，用gethtml(str(tag_url[1]))
    #global m_type
    #global m_site
    soup = BeautifulSoup(html, 'html.parser')
    divs = soup.find_all('div', {'class' : 'figure_title_score'})  #movie的信息
    
    re_movie = r'.*? title="(.*?)".*?<em class="score_l">(.*?)<.*?<em class="score_s">(.*?)<.*?' #(.*?)
    p = re.compile(re_movie, re.DOTALL) #, re.DOTALL句号(.)是匹配任何除换行符之外的任意字符,使用DOTALL标志，就可以让它匹配所有字符，不再排除换行符了
    moviescore = p.findall(str(divs))
    if moviescore:
        movies_score = {}
        for movie in moviescore:
            score = movie[1]+movie[2]
            movies_score[movie[0]] = score
    else:
        print("Not Find")
    return movies_score

def main():
    #计数器
    n = 0   #to count high score movies
    NUM  = 0    #to count all movies
    start_time = time.time()
    #创建文件，用于存放抓取到的电影信息
    if ('qqMovies.txt' or 'qqMovies_high.txt')in os.listdir():
        try:
            os.remove('qqMovies.txt')   #删除文件，如果删除文件夹shutil.rmtree('文件夹名字')
            os.remove('qqMovies_high.txt')
        except:
            f = open('qqMovies.txt','a')
            p = open('qqMovies_high.txt','a')
    else:   
        f = open('qqMovies.txt','a')  #以追加的形式读写内容，指针在结尾
        p = open('qqMovies_high.txt','a')

    url = 'http://v.qq.com/x/list/movie'
    html = getHTML(url)
    movie_type = getMovieTypeList(html) #{'剧情': '1', '喜剧': '2', '动作': '3', '爱情': '4', '犯罪': '5', ...}
    
    for m_type in movie_type.items():
        pages_url = get_pages_url(url,m_type)   #获取每个类型的页面连接
        for page_url in pages_url:
            page_html = getHTML(page_url)   #每个页面的html文本信息
            movies = getmovielist(page_html)    
            movies_score = getmovieScore(page_html) #{'熊出没·变形记': '8.5', '缝纫机乐队': '8.2', '鲨海': '7.8', '猛虫过江': '7.4', ...}
            
            if movies and movies_score:
                for movie in movies:    #('https://v.qq.com/x/cover/s91b6l6rl7c31nd.html', '基督最后的诱惑')
                    for m_score in movies_score.items():    #('六弄咖啡馆', '8.0')
                        if movie[1] == m_score[0]:
                            NUM += 1
                            print('-' * 70 + ' downloading movies: %d' % NUM)
                            #values = dict(movie_title = movie[1], movie_url = movie[0], movie_site  = m_site, movie_type = m_type)   #JSON 格式存储dict
                            values = 'movie_title: %s , movie_score: %s, movie_url: %s ,movie_site: %s ,movie_type:%s' % (movie[1],m_score[1],movie[0],m_site,m_type[0]) #TXT 格式存储字符串
                            print('values = ',values)
                            f.write(values)
                            print("_" * 70)
                            f.write('\n' + '-' * 70 + str(NUM) + '\n')   #写入\n换行和-分隔符 
                            if float(m_score[1]) >=9.0: 
                                n += 1
                                print('%s --- high score!!!' % m_score[0])
                                #p.write('this is for high score movies' + '\n' + '-' * 70 + '\n')
                                p.write(values)
                                p.write('\n' + '-' * 70 + str(n) + '\n')  
            else:
                "Not Found"
            random()    #time.sleep(0.1)   #设置sleep时间，以防爬取过快被封IP
    
    f.write('total movies: %s \n' % str(NUM))  #写入最后电影总数
    p.write('total high score movies: %s \n' % str(n))
    diftime = time.time() - start_time
    f.write('\n' + 'total take time: ' + str(diftime) + '\n')   #写入花费总时间
    f.close()   #关闭文件
    p.close()



if __name__ == "__main__":
    main()