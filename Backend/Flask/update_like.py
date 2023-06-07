from flask import request, Blueprint
import requests, json
from data_admin import Database

update_like = Blueprint('api9',__name__,url_prefix='/like')

def insert_like_list(data_list):
    Data_admin = Database()
    sql = 'insert into like_list(item_id, user_id) values (%s, %s)'
    Data_admin.database(sql, data_list=data_list)

def select_user(session_key):
    Data_admin = Database()
    sql = "select user_id from user_list where user_key='{}'".format(session_key)
    data = Data_admin.database(sql)
    return data

def delete_like(item_id, user_id):
    Data_admin = Database()
    sql = 'delete from like_list where item_id={} and user_id={}'.format(item_id, user_id)
    Data_admin.database(sql)


@update_like.route('/update/', methods = ['POST','GET'])
def add_likeList():
    token = request.headers.get("X_TOKEN")  # 获取用户token
    res = {
        'errno': ''
    }
    user_info = select_user(token)
    if user_info:
        res['errno'] = 0
        user_id = user_info[0][0]
        data = json.loads(request.get_data().decode('utf-8'))  # 将前端Json数据转为字典
        item_id = data['item_id']
        js_errno = data['errno']
        if js_errno == 0:
            print(user_id)
            print(item_id)
            data_list = []
            data_list.append((item_id, user_id))
            insert_like_list(data_list)
        if js_errno == 1:
            print(user_id)
            print(item_id)
            delete_like(item_id, user_id)
    else:
        res['errno'] = 1
    return res

