#encoding=utf-8
from selenium import webdriver
from lxml import etree
import time
import csv
import random


""" keyWord = input('please input the key word you want to search:')
pageNum = int(input('please input the page numbers you want to get:'))
url = 'https://www.lagou.com/jobs/list_' + keyWord + '?px=default&city=%E5%85%A8%E5%9B%BD#filterBox'
browser = webdriver.Chrome()

browser.get(url)
browser.implicitly_wait(10) """


def get_dates(selector):
    items = selector.xpath('//*[@id="s_position_list"]/ul/li')
    print(items)
    for item in items:
        yield{
            'Name':item.xpath('div[1]/div[1]/div[1]/a/h3/text()')[0],
            'Company':item.xpath('div[1]/div[2]/div[1]/a/text()')[0],
            'Salary': item.xpath('div[1]/div[1]/div[2]/div/span/text()')[0],
            'Education': item.xpath('div[1]/div[1]/div[2]/div//text()')[3].strip(),
            'Size': item.xpath('div[1]/div[2]/div[2]/text()')[0].strip(),
            'Welfare': item.xpath('div[2]/div[2]/text()')[0]
        }

def main(pageNum):
    i = 0
    try:
        for i in range(pageNum):
            selector = etree.HTML(browser.page_source)
            browser.find_element_by_xpath('//*[@id="order"]/li/div[4]/div[2]').click()
            time.sleep(random.randint(0,9))
            print('第{}页抓取完毕'.format(i+1))
            for item in get_dates(selector):
                print(item)
            with open('Lagou.csv', 'a', newline='',encoding='utf-8') as csvfile:    #加encoding='utf-8'解决UnicodeEncodeError: 'gbk' codec can't encode character '\xa0' in position问题
                fieldnames = ['Name', 'Company', 'Salary', 'Education', 'Size', 'Welfare']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for item in get_dates(selector):
                    writer.writerow(item)
            time.sleep(random.randint(0,9))
        print('所有{}页数据抓取完毕！'.format(pageNum))
        browser.close()
    except Exception as e:
        print(e)
        browser.close()

if __name__ == '__main__':
    
    for keyWord in ('python','Java','PHP','C#'):
        pageNum = 30 #int(input('please input the page numbers you want to get:'))
        url = 'https://www.lagou.com/jobs/list_' + keyWord
        browser = webdriver.Chrome()

        browser.get(url)
        browser.implicitly_wait(10)
        main(pageNum) 