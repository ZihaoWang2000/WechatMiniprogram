import requests, json
from flask import request, Blueprint
from data_admin import Database
import math

category = Blueprint('api5',__name__,url_prefix='/catalog')

# 获取某一品牌的商品信息，同一item_id只取其中一个数据
def select_bcat(bcat_id,tabs_now):
    Data_admin = Database()
    sql = ''
    if tabs_now == 1:
        sql = "select item_id, goods_logo, goods_name, price_down from " \
          "(select item_id, goods_list.goods_id, goods_name, goods_logo, goods_link, MAX(price_id) " \
          "as new_price_id from goods_list right join price_list on goods_list.goods_id = price_list.goods_id " \
          "where bcat_id = {} AND goods_logo is not null AND goods_logo NOT IN ('',' ') " \
          "GROUP BY price_list.goods_id) as b left join price_list on new_price_id = price_list.price_id " \
          "ORDER BY (price_down+0)".format(bcat_id)
    elif tabs_now == 0:
        sql = "select item_id, goods_logo, goods_name, price_down from " \
              "(select item_id, goods_list.goods_id, goods_name, goods_logo, goods_link, MAX(price_id) " \
              "as new_price_id from goods_list right join price_list on goods_list.goods_id = price_list.goods_id " \
              "where bcat_id = {} AND goods_logo is not null AND goods_logo NOT IN ('',' ') " \
              "GROUP BY price_list.goods_id) as b left join price_list on new_price_id = price_list.price_id " \
              "ORDER BY price_down".format(bcat_id)
    data = Data_admin.database(sql)
    data = list(data)
    # print(data)
    item_id = []
    goods_data = []
    for item in data:
        if item[0] in item_id:
            continue
        else:
            item_id.append(item[0])
            goods_data.append(item)
    # print(item_id)
    # print(goods_data)
    return goods_data

# 获取某一商品类型的商品信息，同一item_id只取其中一个数据
def select_gcat(gcat_id,tabs_now):
    Data_admin = Database()
    sql = ''
    if tabs_now == 1:
        sql = "select item_id, goods_logo, goods_name, price_down from " \
              "(select item_id, goods_list.goods_id, goods_name, goods_logo, goods_link, MAX(price_id) " \
              "as new_price_id from goods_list right join price_list on goods_list.goods_id = price_list.goods_id " \
              "where gcat_id = {} AND goods_logo is not null AND goods_logo NOT IN ('',' ') " \
              "GROUP BY price_list.goods_id) as b left join price_list on new_price_id = price_list.price_id " \
              "ORDER BY (price_down+0)".format(gcat_id)
    elif tabs_now == 0:
        sql = "select item_id, goods_logo, goods_name, price_down from " \
              "(select item_id, goods_list.goods_id, goods_name, goods_logo, goods_link, MAX(price_id) " \
              "as new_price_id from goods_list right join price_list on goods_list.goods_id = price_list.goods_id " \
              "where gcat_id = {} AND goods_logo is not null AND goods_logo NOT IN ('',' ') " \
              "GROUP BY price_list.goods_id) as b left join price_list on new_price_id = price_list.price_id " \
              "ORDER BY price_down".format(gcat_id)
    data = Data_admin.database(sql)
    data = list(data)
    # print(data)
    item_id = []
    goods_data = []
    for item in data:
        if item[0] in item_id:
            continue
        else:
            item_id.append(item[0])
            goods_data.append(item)
    # print(item_id)
    # print(goods_data)
    return goods_data

@category.route('/current/', methods = ['POST'])
def category_detail():
    data = json.loads(request.get_data().decode('utf-8')) #将前端Json数据转为字典
    gcat_id = data['gcat_id']
    bcat_id = data['bcat_id']
    pagenum = data['pagenum']
    pagesize = data['pagesize']
    tabs_now = data['tabs_now']
    res = {}
    if gcat_id == '0':
        goods = []
        goods_data = select_bcat(bcat_id,tabs_now)
        pagetotal = math.ceil(len(goods_data) / pagesize)
        begin = (pagenum-1)*pagesize
        end = pagenum*pagesize
        for item in goods_data[begin:end]:
            goods_item = {}
            goods_item['item_id'] = item[0]
            goods_item['goods_logo'] = item[1]
            goods_item['goods_name'] = item[2]
            goods_item['goods_price'] = item[3]
            goods.append(goods_item)
        res['goods'] = goods
        res['total'] = pagetotal
        res['pagenum'] = pagenum
        return res
    elif bcat_id == '0':
        goods = []
        goods_data = select_gcat(gcat_id,tabs_now)
        # print(tabs_now)
        pagetotal = math.ceil(len(goods_data) / pagesize)
        begin = (pagenum - 1) * pagesize
        end = pagenum * pagesize
        for item in goods_data[begin:end]:
            goods_item = {}
            goods_item['item_id'] = item[0]
            goods_item['goods_logo'] = item[1]
            goods_item['goods_name'] = item[2]
            goods_item['goods_price'] = item[3]
            goods.append(goods_item)
        res['goods'] = goods
        res['total'] = pagetotal
        res['pagenum'] = pagenum
        return res
            #res['goods'] = goods
            #return res
        #res['goods'] = goods
        #res['total'] = len(goods)
        # print(res)