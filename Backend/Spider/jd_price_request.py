# coding=UTF-8
import time
import datetime
import requests
from data_admin import Database
from fake_useragent import UserAgent
import urllib.request
from lxml import etree
import random
import re
import xlrd

def select_link():
    Data_admin = Database()
    sql = "select goods_id, goods_link from goods_list where plat_id = 2"
    data = Data_admin.database(sql)
    return data

def insert_price(data_list):
    Data_admin = Database()
    sql = 'insert into price_list(goods_id,price_down,upd_time) values (%s, %s, %s)'
    Data_admin.database(sql, data_list=data_list)

def delete_detail(goods_id):
    Data_admin = Database()
    sql = 'delete from goods_list where goods_id={}'.format(goods_id)
    Data_admin.database(sql)

def update_datail(goods_logo, goods_id):
    Data_admin = Database()
    sql = "update goods_list set goods_logo='{}'" \
          "where goods_id={}".format(goods_logo, goods_id)
    Data_admin.database(sql)

ua = UserAgent(path='fake_useragent.json')
num_time = datetime.date.today()

def get_headers():
    headers = {
        "User-Agent": ua.random,
        "accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        # "Connection": "keep-alive",
        # "Host": "api.bilibili.com",
        "Upgrade-Insecure-Requests": "1",
    }
    return headers

def get_img_url(id):
    url = 'https://item.jd.com/{}.html'.format(id)
    headers = get_headers()
    re = requests.get(url, headers=headers)
    re.encoding = re.apparent_encoding  # 设置编码，防止由于编码问题导致文字错乱
    # print(re.text)  # 查看请求到的内容
    content = re.text
    # print(content)
    html = etree.HTML(content)
    img_url = html.xpath('//*[@id="spec-img"]/@data-origin')
    return img_url


def get_price(id):
    url = 'https://item-soa.jd.com/getWareBusiness?callback=jQuery8081669&skuId={}'.format(id)
    headers = get_headers()
    res = requests.get(url, headers=headers)
    # print(re.text)  # 查看请求到的内容
    content = res.text
    price = re.findall(r'"p":"(.*?)"', content)
    return price

def change_ip():
    ipfile='/spider/FreeIP.xls'
    ipList=xlrd.open_workbook(ipfile).sheet_by_index(0).col_values(0)
    currentIP=random.choice(ipList)
    proxy_support=urllib.request.ProxyHandler({'http':currentIP})
    opener=urllib.request.build_opener(proxy_support)
    urllib.request.install_opener(opener)
    return currentIP

def jd_spider(goods_id, goods_link):
    data_list = []
    #time.sleep(5)
    change_ip()
    id_list = re.findall(r"com/(.+?).html", goods_link)
    id = id_list[0]
    img_link = get_img_url(id)
    price = get_price(id)
    today = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data_list.append((goods_id, price[0], today))
    insert_price(data_list)
    #print("于{}插入goods_id为{}的价格数据成功".format(today, goods_id))
    update_datail(img_link[0], goods_id)
    #print("goods_id为{}的店铺数据更新成功".format(goods_id))


if __name__ == '__main__':
    try:
        # new_video_heat()
        data = select_link()
        for item in data:
            #change_ip()
            goods_id = item[0]
            goods_link = item[1]
            try:
                jd_spider(goods_id, goods_link)
                time.sleep(3)
            except:
                time.sleep(3)
                continue
    except Exception as e:
        print(e)
