'''
Author: Apple Zhang; from 09/04/2019 to 09/06/2019
description: 根据拉勾网中对相关python、java、PHP、C++职位结果分析：薪资，福利，经验，学历；公司规模，融资情况，城市等
'''

# -*- coding: utf-8 -*-   
from selenium import webdriver
from time import sleep
import random

def getURL(s):
    url = 'https://www.lagou.com/jobs/list_' + s
    return url

def LaunchBrowserBkgrd(url):
    #run WebDriver background
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    browser = webdriver.Chrome(chrome_options=option)
    return browser

def getPosition(browser,f,i):
    #get all positions info for each page: position,salary,location,publish_date,company,education/experience,company scale,welfare and so on
    browser.implicitly_wait(10)
    find_position= browser.find_element_by_xpath('//*[@id="s_position_list"]/ul/li[%d]/div[1]' % (i+1)).text
    f.write(find_position+'\n')

    #get welfare
    browser.implicitly_wait(10)
    find_welfare = browser.find_element_by_xpath('//*[@id="s_position_list"]/ul/li[%d]/div[2]/div[2]' % (i+1)).text
    f.write(find_welfare)
    f.write('\n------------------------------------------------------\n')

def getPositions(browser,f):
    #15 positions for each page
    for i in range(15):
        try:
            getPosition(browser,f,i)
        except BaseException as msg:
            print('search element exception %s' % msg)
            getPosition(browser,f,i)

def main():
    lis = ['python','Java','PHP','C++']
    for s in lis:
        print(s)

        url = getURL(s)
        print(url)

        browser = LaunchBrowserBkgrd(url)
        fname = 'lagou_%s.txt' % s
        f = open(fname,'w')

        try:
            browser.get(url)
            count = 0
            for n in range(30):
                #page 1
                if n == 0:
                    browser.implicitly_wait(10)
                    browser.find_element_by_xpath('//*[@id="order"]/li/div[4]/div[3]/span[1]').click()
                
                    print('loading page %d, position for %s' % (n+1,s))
                    getPositions(browser,f)

                #from page 2
                else:
                    #click next page ‘下一页’
                    browser.implicitly_wait(10)
                    browser.find_element_by_xpath('//*[@id="s_position_list"]/div[2]/div/span[6]').click()
                    
                    print('loading page %d, position for %s' % (n+1,s))
                    getPositions(browser,f)

        finally:
            sleep(random.randrange(0,10))
            browser.quit()