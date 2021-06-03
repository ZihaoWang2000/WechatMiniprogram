import requests, json
from flask import request
from flask import Blueprint
import math
from data_admin import Database

search = Blueprint('api11',__name__,url_prefix='/search')

# 获取某一关键词的商品信息，同一item_id只取其中一个数据
def select_query(query,tabs_now):
    Data_admin = Database()
    query = '%'+ query + '%'
    sql = ''
    print(query)
    if tabs_now == 1:
        sql = "select item_id, goods_logo, goods_name, price_down from " \
          "(select item_id, goods_list.goods_id, goods_name, goods_logo, goods_link, MAX(price_id) " \
          "as new_price_id from goods_list right join price_list on goods_list.goods_id = price_list.goods_id " \
          "where goods_name like '{}' AND goods_logo is not null AND goods_logo NOT IN ('',' ') " \
          "GROUP BY price_list.goods_id) as b left join price_list on new_price_id = price_list.price_id " \
          "ORDER BY (price_down+0)".format(query)
    elif tabs_now == 0:
        sql = "select item_id, goods_logo, goods_name, price_down from " \
              "(select item_id, goods_list.goods_id, goods_name, goods_logo, goods_link, MAX(price_id) " \
              "as new_price_id from goods_list right join price_list on goods_list.goods_id = price_list.goods_id " \
              "where goods_name like '{}' AND goods_logo is not null AND goods_logo NOT IN ('',' ') " \
              "GROUP BY price_list.goods_id) as b left join price_list on new_price_id = price_list.price_id ".format(query)
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


@search.route('/result/', methods = ['POST'])
def search_content():
    data = json.loads(request.get_data().decode('utf-8'))  # 将前端Json数据转为字典
    query = data['query']
    pagenum = data['pagenum']
    pagesize = data['pagesize']
    tabs_now = data['tabs_now']
    res = {}
    goods = []
    goods_data = select_query(query, tabs_now)
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

select_query('粉水',0)