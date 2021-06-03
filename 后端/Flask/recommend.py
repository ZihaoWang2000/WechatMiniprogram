from flask import request, Blueprint
import requests, json
from data_admin import Database
import random

recommend = Blueprint('api4',__name__,url_prefix='/recommend')

def select_random_goods(item_id):
    Data_admin = Database()
    sql = "select DISTINCT goods_name, goods_logo, goods_link, price_down, new_price_id, a.goods_id from " \
          "(select goods_list.goods_id, goods_name, goods_logo, goods_link, MAX(price_id) as new_price_id " \
          "from goods_list right join price_list on goods_list.goods_id = price_list.goods_id where item_id = {} " \
          "GROUP BY price_list.goods_id) as a left join price_list " \
          "on a.new_price_id = price_list.price_id ORDER BY (price_down+0);".format(item_id)
    data = Data_admin.database(sql)
    return data

def select_item_id():
    Data_admin = Database()
    sql = "select DISTINCT item_id from goods_list right join price_list on goods_list.goods_id = price_list.goods_id where goods_logo is not null AND goods_logo NOT IN ('',' ');"
    data = Data_admin.database(sql)
    return data

@recommend.route('/', methods = ['POST','GET'])
def recommend_random_goods():
    data = json.loads(request.get_data().decode('utf-8'))  # 将前端Json数据转为字典
    limit = data['limit']
    item_id_list = []
    for item in select_item_id():
        item_id = item[0]
        item_id_list.append(item_id)
    index = random.sample(item_id_list, limit)
    print(index)
    res = {
        'errno': '',
        'data':{'goods_list':[]}
    }
    try:
        for i in index:
            goods_list = {}
            data = select_random_goods(i)
            url = data[0][1]
            name = data[0][0]
            price = data[0][3]
            goods_id = data[0][4]
            if url == '' or url is None:
                continue
            else:
                goods_list['url'] = url
                goods_list['name'] = name
                goods_list['item_id'] = i
                goods_list['goods_id'] = goods_id
                if '-' in price:
                    goods_list['price'] = '￥' + price[0:price.rfind(' - ', 1)]
                else:
                    goods_list['price'] = '￥' + price
                res['data']['goods_list'].append(goods_list)
        res['errno'] = 0
    except:
        res['errno'] = 1
    return json.dumps(res, ensure_ascii=False)
