from flask import request, Blueprint
import requests, json
from data_admin import Database

get_like_list = Blueprint('api3',__name__,url_prefix='/like')

def select_like_list(session_key):
    Data_admin = Database()
    sql = "select item_id from like_list left join user_list on like_list.user_id = user_list.user_id " \
          "where user_key='{}'".format(session_key)
    data = Data_admin.database(sql)
    return data

def select_goods_by_item(item_id):
    Data_admin = Database()
    sql = "select goods_name, goods_logo, goods_link, price_down, new_price_id, a.goods_id from " \
          "(select goods_list.goods_id, goods_name, goods_logo, goods_link, MAX(price_id) as new_price_id " \
          "from goods_list right join price_list on goods_list.goods_id = price_list.goods_id where item_id = {} " \
          "GROUP BY price_list.goods_id) as a left join price_list " \
          "on a.new_price_id = price_list.price_id ORDER BY (price_down+0);".format(item_id)
    data = Data_admin.database(sql)
    return data

@get_like_list.route('/index/', methods = ['POST','GET'])
def get_likeList():
    token = request.headers.get("X_TOKEN")  # 获取用户token
    item_id_list = []
    like_list = []
    res = {
        'errno': '',
        'data': {'likeList': like_list}
    }
    item_id_tuple = select_like_list(token)
    print(item_id_tuple)
    for item in item_id_tuple:
        item_id_list.append(item[0])
    print(item_id_list)
    for i in item_id_list:
        like_item = {}
        data = select_goods_by_item(i)
        url = data[0][1]
        name = data[0][0]
        price = data[0][3]
        goods_id = data[0][4]
        like_item['name'] = name
        like_item['item_id'] = i
        like_item['url'] = url
        like_item['goods_id'] = goods_id
        like_item['checked'] = False
        if '-' in price:
            like_item['price'] = '￥' + price[0:price.rfind(' - ', 1)]
        else:
            like_item['price'] = '￥' + price
        like_list.append(like_item)
    print(like_list)
    res['errno'] = 0
    return json.dumps(res, ensure_ascii=False)
