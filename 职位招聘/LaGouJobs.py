# -*- coding: utf-8 -*-
# @Time     :   2020/3/31 20:09
# @Author   :   Payne
# @File     :   3-31.py
# @Software :   PyCharm
import hashlib
import logging
import threading
import random
import requests
from time import sleep

from loguru import logger

thread_lock = threading.BoundedSemaphore(value=10)
api_url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
cookies_url = 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput='
# Details_url = 'https://www.lagou.com/jobs/6960880.html?show=b7d2f49d09644c77870d600ebfb0c59d'
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')


def hex5(value):
    manipulator = hashlib.md5()
    manipulator.update(value.encode('utf-8'))
    return manipulator.hexdigest()


def User_Agent():
    """
    Get random User-Agent from the list
    @return: Header
    """
    User_Agent = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
    ]
    this_ua = random.choice(User_Agent)
    header = {
        'Host': 'www.lagou.com',
        'Origin': 'https://www.lagou.com',
        'Referer': 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=',
        'User-Agent': this_ua,
    }
    return header


def Get_cookies(header):
    """
    Get cookies
    @param header:
    @return: cookies
    """
    with requests.Session() as s:
        s.get(cookies_url, headers=header)
        cookies = s.cookies
    # cookies = requests.get(cookies_url, headers=header).cookies
    return cookies


def Get_list(page):
    """
    Get list page information
    @return: list page message
    """
    data = {
        'first': 'false',
        'pn': page,
        'kd': 'python',
        'sid': '965bbc9f8fbe4914b636d1495fe89e21'
    }
    header = User_Agent()
    cookies = Get_cookies(header)
    # logging.info(f'Got cookies {cookies}')
    try:
        response = requests.post(api_url, headers=header, data=data, cookies=cookies)
        if response.status_code == 200:
            return response.json()['content']['positionResult']['result']
        logging.error('get invalid status code %s while scraping %s', response.status_code, api_url)
    except Exception as e:
        logging.error(f'Send error on request {e}')


def parse(message):
    industryField = message['industryField']
    # company_message
    positionName = message['positionName']
    companyFullName = message['companyFullName']
    companySize = message['companySize']
    financeStage = message['financeStage']
    # companyLabelList = message['companyLabelList']
    companyLabelList = '|'.join(message['companyLabelList'])
    Type = "|".join([message['firstType'], message['secondType'], message['thirdType']])
    Address = ''.join([message['city'], message['district'], ])
    salary = message['salary']
    positionAdvantage = message['positionAdvantage']
    # limitation factor
    workYear = message['workYear']
    jobNature = message['jobNature']
    education = message['education']
    items = f"{positionName}, {companyFullName}, {companySize}, {financeStage}, {companyLabelList}, {industryField}, " \
        f"{Type}, {salary}, {jobNature}, {education}"
    # items = "".join(str(
    #     [positionName, companyFullName, companySize, financeStage, companyLabelList, industryField, Type, salary,
    #      jobNature, education]))
    if items:
        # print(items)
        logging.info(items)
        # return items.replace('[', '').replace(']', '')
        return items.replace('(', '').replace(')', '')


def save_message(item):
    with open('lg3.csv', 'a+', encoding='gbk') as f:
        f.write(item + '\n')
    thread_lock.release()


# @logger.catch
def main(page):
    messages = Get_list(page)
    for message in messages:
        items = parse(message)
        thread_lock.acquire()
        # save_message(items)
        t = threading.Thread(target=save_message, args=(items,))
        t.start()
    logging.info(f'Successfully Acquired {page} Page  Next page is {page + 1}th Page')


if __name__ == '__main__':
    for page in range(1, 31):
        main(page)
        sleep(3)

    # pool = multiprocessing.Pool()
    # pages = range(1, 31)
    # pool.map(main, pages)
    # pool.close()
