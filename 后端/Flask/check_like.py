from flask import request, Blueprint
import requests, json
from data_admin import Database

check_like = Blueprint('api10',__name__,url_prefix='/like')

def select_like_list(session_key):
    Data_admin = Database()
    sql = "select item_id from like_list left join user_list on like_list.user_id = user_list.user_id " \
          "where user_key='{}'".format(session_key)
    data = Data_admin.database(sql)
    return data

@check_like.route('/check/', methods = ['POST','GET'])
def get_likeList():
    token = request.headers.get("X_TOKEN")  # 获取用户token
    data = json.loads(request.get_data().decode('utf-8'))
    item_id_list = []
    item_id = data['item_id']
    like_list = []
    res = {
        'errno': '',
        'data': {'likeList': like_list}
    }
    item_id_tuple = select_like_list(token)
    for item in item_id_tuple:
        item_id_list.append(item[0])
    if int(item_id) in item_id_list:
        res['errno'] = 0
    else:
        res['errno'] = 1
    print(res)
    return json.dumps(res, ensure_ascii=False)