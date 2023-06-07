from flask import request, Blueprint
import requests, json
from data_admin import Database

login = Blueprint('api2',__name__,url_prefix='/user')

def select_session(session_key):
    Data_admin = Database()
    sql = "select * from user_list where user_key='{}'".format(session_key)
    data = Data_admin.database(sql)
    return data

def select_like_count(session_key):
    Data_admin = Database()
    sql = "select count(*) from like_list left join user_list on like_list.user_id = user_list.user_id " \
          "where user_key='{}' group by like_list.user_id".format(session_key)
    data = Data_admin.database(sql)
    return data

@login.route('/index/', methods = ['POST','GET'])
def userLogin():
    token = request.headers.get("X_TOKEN")  # 获取用户token
    print(token)
    user_info = select_session(token)
    like_count = 0
    res = {
        'errno': '',
        'data': {'likeGoodsCount': like_count}
    }
    if user_info:
        like = select_like_count(token)
        if like:
            like_count = like[0][0]
        else:
            like_count = 0
        res['errno'] = 0
        return json.dumps(res, ensure_ascii=False)
    else:
        res['errno'] = 1
        return json.dumps(res, ensure_ascii=False)