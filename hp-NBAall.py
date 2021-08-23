import requests
import time
import random
import pymysql
from bs4 import BeautifulSoup


def sqldb(data_list):
    db = pymysql.connect(host="localhost", user="root", passwd="bujiangwude", database="hp", charset="utf8", port=3306)
    cursor = db.cursor()

    sql = 'INSERT INTO `hpNBA-all`(title,url,author,time,reply,view) VALUES(%s,%s,%s,%s,%s,%s)'
    try:
        cursor.executemany(sql, data_list)
        db.commit()
        print("execute successfully")
    except Exception as e:
        print("执行MySQL: %s 时出错：%s" % (sql, e))
        db.rollback()

    '''
    for data in data_list:
        title=data[0]
        url=data[1]
        author=data[2]
        time=data[3]
        reply=data[4]
        view=data[5]
        print(type(title))
        print(type(url))
        print(type(author))
        print(type(time))
        print(type(reply))
        print(type(view))
        try:
            sql = 'INSERT INTO `hpNBA-all`(title,url,author,time,reply,view)VALUES(%s,%s,%s,%s,%s,%d)'
            print(sql)
            cursor.execute(sql,(title,url,author,time,reply,view))
            db.commit()
        except Exception as e:
            print("执行MySQL: %s 时出错：%s" % (sql, e)) 
            db.rollback()
    '''
    db.close()

def get_pages(page_url):
    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'
    }
    response = requests.get(url=page_url,headers=headers)
    page_soup = BeautifulSoup(response.text,'lxml')
    return page_soup

def parse_pages(page_soup):
    data_list = []
    upperdiv = page_soup.find('div',class_='bbs-sl-web-post')
    all_list = upperdiv.find('ul')
    post_list = all_list.find_all('li')
    for post in post_list:
        post_title = post.find('a',class_='p-title').text
        post_url = 'https://bbs.hupu.com'+post.find('a',class_='p-title')['href']
        post_author_div = post.find('div',class_='post-auth')
        post_author = post_author_div.find('a').text
        post_time = post.find('div',class_='post-time').text
        post_data = post.find('div',class_='post-datum').text
        post_reply = post_data.split('/')[0].strip()
        post_reply = int(post_reply)
        post_view = post_data.split('/')[1].strip()
        post_view = int(post_view)
        data_list.append((post_title,post_url,post_author,post_time,post_reply,post_view))
    #print(data_list)
    return data_list

url = 'https://bbs.hupu.com/vote-1'
soup = get_pages(url)
result_list = parse_pages(soup)
sqldb(result_list)