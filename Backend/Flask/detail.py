from flask import Flask
import requests, json
from flask import request
from data_admin import Database
import math
from flask import Blueprint

detail = Blueprint('api6',__name__,url_prefix='/goods')

def goods_items(item_id):
    Data_admin = Database()
    sql = "select store_name, goods_name, goods_logo, goods_link, price_down, new_price_id, a.goods_id " \
          "from (select goods_list.goods_id, store_name, goods_name, goods_logo, goods_link, MAX(price_id) " \
          "as new_price_id from goods_list right join price_list on goods_list.goods_id = price_list.goods_id " \
          "where item_id = {} GROUP BY price_list.goods_id) as a left join price_list on " \
          "a.new_price_id = price_list.price_id".format(item_id)
    data = Data_admin.database(sql)
    return data

def plat_img(goods_id):
    Data_admin = Database()
    sql = "select plat_logo from plat_list RIGHT JOIN goods_list ON " \
          "plat_list.plat_id = goods_list.plat_id WHERE goods_id ={}".format(goods_id)
    data = Data_admin.database(sql)
    return data[0][0]

@detail.route('/detail/', methods = ['POST'])
def goods_detail():
    data = json.loads(request.get_data().decode('utf-8')) #将前端Json数据转为字典
    print(data)
    item_id = data['item_id']
    pagenum = data['pagenum']
    pagesize = data['pagesize']
    data = goods_items(item_id)
    res = {}
    goods = []
    res['goods_name'] = data[0][1]
    res['goods_img'] = data[0][2]
    res['goods_price'] = data[0][4]
    pagetotal = math.ceil(len(data) / pagesize)
    begin = (pagenum - 1) * pagesize
    end = pagenum * pagesize
    for item in data[begin:end]:
        goods_item = {}
        goods_item['store_name'] = item[0]
        goods_item['goods_name'] = item[1]
        goods_item['goods_img'] = item[2]
        goods_item['goods_price'] = item[4]
        goods_item['goods_id'] = item[6]
        goods_item['plat_logo'] = plat_img(item[6])
        goods.append(goods_item)
    res['goods'] = goods
    res['total'] = pagetotal
    res['pagenum'] = pagenum
    return res




