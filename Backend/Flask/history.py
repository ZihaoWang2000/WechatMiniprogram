import requests, json
from flask import request
from flask import Blueprint
from data_admin import Database
import datetime

history = Blueprint('api7',__name__,url_prefix='/goods')

option = {
      'xAxis': {
        'type': 'category',
        'data': []},
      'yAxis': {
          # inverse: true,
          'type': 'value'
            },
      'series': [{
          'data': [],
            'type': 'line',
            'smooth': 'true'
      }],
   }

def select_price(goods_id):
    Data_admin = Database()
    sql = 'select price_down, upd_time from price_list RIGHT JOIN goods_list ON ' \
          'price_list.goods_id = goods_list.goods_id where goods_list.goods_id = {} ' \
          'ORDER BY (price_down+0)'.format(goods_id)
    data = Data_admin.database(sql)
    return data

def select_goods(goods_id):
    Data_admin = Database()
    sql = 'select goods_name, goods_logo, store_name, plat_name from plat_list RIGHT JOIN goods_list ON ' \
          'plat_list.plat_id = goods_list.plat_id WHERE goods_id ={}'.format(goods_id)
    data = Data_admin.database(sql)
    return data

@history.route('/history/', methods = ['POST'])
def category_detail():
    data = json.loads(request.get_data().decode('utf-8'))  # 将前端Json数据转为字典
    goods_id = data['goods_id']
    price = select_price(goods_id)
    goods = select_goods(goods_id)
    res = {}
    price_list = []
    price_down = []
    upd_time = []
    for item in price:
        price_item = {}
        price_down.append(item[0])
        price_item['price_down'] = item[0]
        upd_time.append(item[1].strftime('%Y-%m-%d'))
        price_item['upd_time'] = item[1].strftime("%Y-%m-%d %H:%M:%S")
        price_list.append(price_item)
    option['xAxis']['data'] = upd_time
    option['series'][0]['data'] = price_down
    res['option'] = option
    res['price_list'] = price_list
    res['goods_name'] = goods[0][0]
    res['goods_logo'] = goods[0][1]
    res['store_name'] = goods[0][2]
    res['plat_name'] = goods[0][3]
    res['goods_price'] = price[0][0]
    res['min_date'] = price[0][1].strftime('%Y-%m-%d')
    return  res