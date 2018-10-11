# coding=utf-8
import time
import datetime
import mysql.connector
import re
import redis
from bs4 import BeautifulSoup
from selenium import webdriver
# r = redis.Redis(host='127.0.0.1', port=6379,db=0)#host自己的ip地址
driver = webdriver.Chrome()  # 打开火狐浏览器
driver.get('http://www.landchina.com/default.aspx?tabid=263&ComName=default')  # 打开界面
i = 1
l = 0
date_list = []
time.sleep(3)
driver.find_element_by_id('TAB_QueryConditionItem270').click()

def page_zh(i,l):
    # 获取本时间段内的总页数（方法）int(reg[0])
    zys = driver.find_elements_by_css_selector(".pager")
    if(zys!=[]):
        str = zys[1].text;
        reg = re.findall(r'\d+', str)
        pages = int(reg[0])
        print("总页数为:" + reg[0])
        tds = driver.find_elements_by_css_selector(".pager>input")
        # 清空文本方法
        tds[0].clear()
        tds[0].send_keys(i)
        print("第" + tds[0].get_attribute("value") + "页")
        tds[1].click()
    elif(zys==[]):
        pages=1

    time.sleep(2)
    # 获取页面html
    html = driver.find_element_by_id('TAB_contentTable').get_attribute('innerHTML')
    soup = BeautifulSoup(html, 'lxml')  # 对html进行解析
    href_ = soup.select('.queryCellBordy a')
    for line in href_:
        print("http://www.landchina.com/" + line['href'])
        # 链接redis

        # r.sadd('mylist_jg',"http://www.landchina.com/"+line['href'])

        # 连接数据库
        # connect = mysql.connector.connect(user='root', password='123456', host='127.0.0.1', database='landchina')
        # # 获取游标
        # cursor = connect.cursor()
        # # 插入数据
        # sql = "INSERT INTO  landchina_jieguogg_url (url) VALUES ( '%s')"
        # data = "http://www.landchina.com/" + line['href']
        # cursor.execute(sql % data)
        # connect.commit()
        # print('成功插入', cursor.rowcount, '条数据')
        # # 关闭连接
        # cursor.close()
        # connect.close()

    if (i < pages):
        i = i + 1
        page_zh(i, l)
    else:
        print("本次采集结束!!!")


# 关闭浏览器（selenium）
# driver.quit()

def llq_main(start,end):
    print(start,end)
    time.sleep(2)
    # 对时间条件进行赋值
    driver.find_element_by_id('TAB_queryDateItem_270_1').clear()
    driver.find_element_by_id('TAB_queryDateItem_270_1').send_keys(start)
    driver.find_element_by_id('TAB_queryDateItem_270_2').clear()
    driver.find_element_by_id('TAB_queryDateItem_270_2').send_keys(end)
    # 进行行政区的选择
    driver.find_element_by_id('TAB_QueryConditionItem256').click()
    driver.execute_script("document.getElementById('TAB_queryTblEnumItem_256_v').setAttribute('type', 'text');")
    driver.find_element_by_id('TAB_queryTblEnumItem_256_v').clear()
    driver.find_element_by_id('TAB_queryTblEnumItem_256_v').send_keys('13')
    driver.find_element_by_id('TAB_QueryButtonControl').click()  # 查询操作
    page_zh(i,l)


if __name__ == '__main__':
    # start = '2009-11-12'
    # end = '2018-09-18'
    # begin_date = datetime.datetime.strptime(start, "%Y-%m-%d")
    # end_date = datetime.datetime.strptime(end, "%Y-%m-%d")
    # while begin_date <= end_date:
    #     date_str = begin_date.strftime("%Y-%m-%d")
    #     date_list.append(date_str)
    #     begin_date += datetime.timedelta(days=1)
    # for l in range(len(date_list)):
    #     # print(date_list[l])
    #     llq_main(date_list[l],date_list[l])

    llq_main('2018-01-01','2018-09-19')