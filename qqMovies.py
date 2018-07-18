# -*- coding: utf-8 -*-  
# by mazh. my site: http://blog.csdn.net/zhongqi2513  
import re  
import requests
from bs4 import BeautifulSoup 
import string, time  
import pymongo  

NUM  = 0   #全局变量,电影数量  
#m_type = u''  #全局变量,电影类型  
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
def getMovieTypeList(url,html):
  #global m_type
  soup = BeautifulSoup(html, 'html.parser')  #过滤出分类内容 
  #print(soup)  

  #<div class="filter_content"> #电影分类信息在div这个标签下。
  tags_all = soup.find_all('div', {'class' : 'filter_content' })   #找到所有div.filter_content下的a标签
  
  #<a _stat2="filter:params|subtype=1" class="item" href="?offset=0&amp;subtype=1">剧情</a>
  re_tags = r'<a _stat2=".*?subtype=.*?" class="item" href=".*?;subtype=(.*?)">(.*?)</a>' #(.*?)
  p = re.compile(re_tags) #, re.DOTALL句号(.)是匹配任何除换行符之外的任意字符,使用DOTALL标志，就可以让它匹配所有字符，不再排除换行符了
  tags = p.findall(str(tags_all[0]))
  #print('tags = ',tags)

  if tags:
    tags_type = {}

    for tag in tags:
      #print(tag)    #tag = ('1', '剧情')
      #tag_url = url + '?offset=0&subtype=' + tag[0]   #每个电影类型的url
      #print('tag_url = ',tag_url)         
      
      tag_subtype = tag[0]
      m_type = tag[1]
      print('m_type = ',m_type)
      tags_type[m_type] = tag_subtype 
      print('tags_type[m_type] = ',tags_type[m_type])
  else:
    print("Not Find")
  return tags_type


#获取每个分类的页数?offset=0&subtype=2
def get_pages(url, tag_type):
  tag_url = url + '?offset=0' + '&subtype=' + tag_type 
  tag_html = getHTML(tag_url)
  soup = BeautifulSoup(tag_html, 'html.parser')  #过滤出标记页面的html
  #print(soup)

  #<div class="mod_pages" r-notemplate="true">
  div_page = soup.find_all('div', {'class' : 'mod_pages'})
  #print('div_page=',div_page) #len(div_page), div_page[0]
  if div_page == []:  #只有一页时没有div标签，div_page是空[]
    return 1

  #<a _stat2="paging_page|63" class="page_num" href="?subtype=2&amp;offset=1860">63</a>
  re_pages = r'<a _stat2=".*?" class=".*?" href=".*?">(.*?)</a>'
  p = re.compile(re_pages)
  pages = p.findall(str(div_page[0]))
  #print(pages,len(pages))
  if len(pages) > 1:
    return pages[-2]
  else:
    return 1

def getmovielist(m_type, html): #html 分类页面文本，用gethtml(str(tag_url[1]))
  global NUM
  #global m_type
  global m_site
  soup = BeautifulSoup(html, 'html.parser')
  
  #<ul class="figures_list">
  divs = soup.find_all('ul', {'class' : 'figures_list'})  #movie的信息
  #print(divs)

  
  #<a _stat2="videos:title" href="https://v.qq.com/x/cover/vfx3eugf3h4jiqg.html" target="_blank" title="二十二">二十二</a></strong>
  re_movie = r'<a _stat2="videos:title" href="(.*?)" target=".*?" title=".*?">(.*?)</a>' #(.*?)
  p = re.compile(re_movie, re.DOTALL) #, re.DOTALL句号(.)是匹配任何除换行符之外的任意字符,使用DOTALL标志，就可以让它匹配所有字符，不再排除换行符了
  movies = p.findall(str(divs[0]))
  #print(movies)

  f = open('qqMovies.txt','w')  #如qqMovies.txt存在则覆盖，无则新建
  if movies:
    #print(movies)
    for movie in movies:
      #print(movie)
      #print(NUM)
      NUM += 1
      print('downloading movies: %d' % NUM)
      #print("%s : %d" % ("=" * 70, NUM))
      #values = dict(movie_title = movie[1], movie_url = movie[0], movie_site  = m_site, movie_type = m_type)   #JSON 格式存储dict
      values = 'movie_title: %s , movie_url: %s ,movie_site: %s ,movie_type:%s' % (movie[1],movie[0],m_site,m_type) #TXT 格式存储字符串
      print(values)
      f = open('qqMovies.txt','a')  #以追加的形式读写内容，指针在结尾
      f.write(values)
      print("_" * 70)
      f.write('\n' + "_" * 70 + '\n')   #写入\n换行和-分隔符
  else:
    "Not Found"
  f.write('total movies: %s' % str(NUM))  #写入最后电影总数
  f.close()   #关闭文件


if __name__ == "__main__":
  
  url = 'http://v.qq.com/x/list/movie'
  html = getHTML(url)
  movie_type = getMovieTypeList(url,html)
  print('movie_type = ',movie_type)
  
  for m_url in movie_type.items():
    #print('m_url = ', m_url)
    tag_url = url + '?subtype=' + m_url[1] + '&offset=0'
    print('tag_url = %s' % tag_url, end = '')
    #print('tag_type=',str(m_url[1])) #m_url[0] = '剧情'
    maxpage = int(get_pages(url, str(m_url[1])))
    print(', total pages are ', maxpage)
    for x in range(0,maxpage):
      #http://v.qq.com/x/list/movie?offset=30&subtype=16
      #str.replace(old, new[, max])
      page_url = tag_url.replace('0', '') + str(x*30)
      #print('page_url = ',page_url)  #某个分类下，每个页面的url，如分类为18的第四页：http://v.qq.com/x/list/movie?subtype=18&offset=90
      page_html = getHTML(page_url)
      getmovielist(m_url[0],page_html)

      time.sleep(0.1)   #设置sleep时间，以防爬取过快被封IP


