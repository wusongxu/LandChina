# coding=utf-8
import time
import datetime
# import mysql.connector
import re
# import redis
from bs4 import BeautifulSoup
from selenium import webdriver

# r = redis.Redis(host='127.0.0.1', port=6379,db=0)#host自己的ip地址
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
driver = webdriver.Chrome(chrome_options=options)  # 打开火狐浏览器
driver.get('http://www.landchina.com/default.aspx?tabid=263&ComName=default')  # 打开界面
time.sleep(8)
i = 1
l = 0
date_list = []
time.sleep(3)
driver.find_element_by_id('TAB_QueryConditionItem270').click()

def get_page_number():
    # 获取本时间段内的总页数（方法）int(reg[0])
    zys = driver.find_elements_by_css_selector(".pager")
    if (zys != []):
        str = zys[1].text;
        reg = re.findall(r'\d+', str)
        pages = int(reg[0])
        print("总页数为:" + reg[0])
        return pages
    elif (zys == []):
        pages = 1
        return pages
def get_one_page_paper(number_page,name):
    # 获取本时间段内的总页数（方法）int(reg[0])
    zys = driver.find_elements_by_css_selector(".pager")
    if (zys != []):
        str = zys[1].text;
        reg = re.findall(r'\d+', str)
        pages = int(reg[0])
        print("总页数为:" + reg[0])
        tds = driver.find_elements_by_css_selector(".pager>input")
        # 清空文本方法
        tds[0].clear()
        tds[0].send_keys(number_page)
        print("第" + tds[0].get_attribute("value") + "页")
        tds[1].click()
    elif (zys == []):
        number_page = 1

    time.sleep(2)
    # 获取页面html
    html = driver.find_element_by_id('TAB_contentTable').get_attribute('innerHTML')
    soup = BeautifulSoup(html, 'lxml')  # 对html进行解析
    href_ = soup.select('.queryCellBordy a')
    one_page_all_paper = []

    for line in href_:
        print("http://www.landchina.com/" + line['href'])
        url = "http://www.landchina.com/" + line['href']
        result_dict = get_url_content(url)
        one_page_all_paper.append(result_dict)
        import json
        with open('test.txt', '') as f:
            f.write(json.dumps(result_dict) + '\n')
    write_content(one_page_all_paper, number_page, name)

def get_all_paper(name):
    pages = get_page_number()
    import pdb;pdb.set_trace()
    for number_page in pages:
        number_page += 1
        if number_page == 1:
            continue
        get_one_page_paper(number_page,name)

def page_zh(i, l,name):
    # 获取本时间段内的总页数（方法）int(reg[0])
    zys = driver.find_elements_by_css_selector(".pager")
    if (zys != []):
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
    elif (zys == []):
        pages = 1

    time.sleep(2)
    # 获取页面html
    html = driver.find_element_by_id('TAB_contentTable').get_attribute('innerHTML')
    soup = BeautifulSoup(html, 'lxml')  # 对html进行解析
    href_ = soup.select('.queryCellBordy a')
    one_page_all_paper = []

    for line in href_:
        # if i in [1, 2, 3,4,5]:
        #     continue
        print("http://www.landchina.com/" + line['href'])
        url = "http://www.landchina.com/" + line['href']

        result_dict = get_url_content(url)
        one_page_all_paper.append(result_dict)
        import json
        with open('test.txt','a') as f:
            f.write(json.dumps(result_dict)+'\n')
    write_content(one_page_all_paper, i, name)
    # if i not in [1,2,3,4,5,6]:
    #     write_content(one_page_all_paper, i,name)
    if (i < pages):
        i = i + 1
        page_zh(i, l,name)
    else:
        print("本次采集结束!!!")
import json
def url_content_write(name):
    one_page_content = []
    number = 0
    page_number = 6
    with open('url.txt','r') as f:
        for url in f.readlines():
            content_dict = get_url_content(url)
            with open('test_.txt', 'a') as f:
                f.write(json.dumps(content_dict)+'\n')
            one_page_content.append(content_dict)
            number +=1
            if number%30 == 0:
                page_number +=1
                write_content(one_page_content,page_number,name)


def get_url_content(url):
    tag = 1
    index = 2  # 等待指数
    try:
        result_dict = {}
        result_dict['url'] = url
        new_windows = 'window.open("' + url + '");'
        driver.execute_script(new_windows)
        # 隐式等待1min
        # driver.implicitly_wait(60)
        # 获取当前窗口的句柄
        origin_windows = driver.window_handles[0]
        current_windows = driver.window_handles[-1]
        driver.switch_to.window(current_windows)
        from selenium.webdriver.support.ui import WebDriverWait
        rowInfo = WebDriverWait(driver, 30).until(lambda driver: driver.find_elements_by_xpath(
            "//table[@id='Table1']//table[@id='mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1']/tbody/tr"))
        # [line.text for line in rowInfo] 得到结果信息
    except Exception as e:
        result_dict['flag'] = 'false'
    else:
        tag = 0
        # 读取表格数据
        for row in rowInfo[2:]:
            i = 0
            spanList = row.find_elements_by_xpath('./td/span')
            # print(spanList[i].text)
            while (i < len(spanList)):
                if spanList[i].text == "行政区:":
                    result_dict['行政区'] = spanList[i + 1].text
                    break
                elif spanList[i].text == "项目名称:":
                    result_dict['项目名称'] = spanList[i + 1].text
                    break
                elif spanList[i].text == '项目位置:':
                    result_dict['项目位置'] = spanList[i + 1].text
                    break
                elif spanList[i].text == '面积(公顷):':
                    result_dict['面积(公顷)'] = spanList[i + 1].text
                    result_dict['土地来源'] = spanList[i + 3].text
                    break
                elif spanList[i].text == '土地用途:':
                    result_dict['土地用途'] = spanList[i + 1].text
                    result_dict['供地方式'] = spanList[i + 3].text
                    break
                elif spanList[i].text == '土地使用年限:':
                    result_dict['土地使用年限'] = spanList[i + 1].text
                    result_dict['行业分类'] = spanList[i + 3].text
                    break
                elif spanList[i].text == '土地级别:':
                    result_dict['土地级别'] = spanList[i + 1].text
                    result_dict['成交价格(万元)'] = spanList[i + 3].text
                    break
                elif spanList[i].text == '约定容积率:':
                    subspanList = row.find_elements_by_xpath('./td/table//span')
                    result_dict['约定容积率'] = subspanList[i+1].text+'-'+ subspanList[i+3].text
                    break
                elif spanList[i].text == '批准单位:':
                    result_dict['合同签订日期'] = spanList[i+3].text
                    break
                else:
                    i+=2
        result_dict['flag'] = 'true'
        driver.close()
        driver.switch_to.window(origin_windows)
    print('采集一篇文章成功')
    return result_dict

import os
def write_content(content, page_name,name):
    import csv
    temp_list = ['url', '行政区', '项目名称', '项目位置', '面积(公顷)', '土地来源', '土地用途', '供地方式',
                 '土地使用年限', '行业分类', '土地级别', '成交价格(万元)','约定容积率','合同签订日期', 'flag']
    if os.path.isdir(name):
        pass
    else:
        os.mkdir(name)
    with open(name + '/'+str(page_name) + '.csv', 'w')as f:
        writer = csv.DictWriter(f, temp_list)
        writer.writeheader()
        for temp_dict in content:
            writer.writerow(temp_dict)
    print('写入成功')

def llq_main(start, end):
    print(start, end)
    time.sleep(15)
    # 对时间条件进行赋值
    position = '3302▓'
    attribute = '06▓'
    driver.find_element_by_id('TAB_queryDateItem_270_1').clear()
    driver.find_element_by_id('TAB_queryDateItem_270_1').send_keys(start)
    driver.find_element_by_id('TAB_queryDateItem_270_2').clear()
    driver.find_element_by_id('TAB_queryDateItem_270_2').send_keys(end)
    # 进行行政区的选择
    driver.find_element_by_id('TAB_QueryConditionItem256').click()
    driver.execute_script("document.getElementById('TAB_queryTblEnumItem_256_v').setAttribute('type', 'text');")
    driver.find_element_by_id('TAB_queryTblEnumItem_256_v').clear()
    driver.find_element_by_id('TAB_queryTblEnumItem_256_v').send_keys(position)
    driver.find_element_by_id('TAB_QueryConditionItem212').click()
    driver.execute_script("document.getElementById('TAB_queryTblEnumItem_212_v').setAttribute('type', 'text');")
    driver.find_element_by_id('TAB_queryTblEnumItem_212_v').clear()
    time.sleep(2)
    driver.find_element_by_id('TAB_queryTblEnumItem_212_v').send_keys(attribute)
    driver.find_element_by_id('TAB_QueryButtonControl').click()  # 查询操作
    name = '宁波市-工业仓储用地-'+start+'--'+end
    # get_all_paper(name)
    page_zh(i, l,name)
    # url_content_write(name)
#<input type="hidden" id="TAB_queryTblEnumItem_212_v" value="06▓">
if __name__ == '__main__':
    position = []
    attribute = []
    start = '2013-01-01'
    end ='2013-12-31'
    name = '宁波市-工业仓储用地-' + start + '--' + end
    # url_content_write(name)
    llq_main(start, end)
