import requests, json
from flask import request, Blueprint
from data_admin import Database

session = Blueprint('api',__name__,url_prefix='/auth')

def select_userid(openid):
    Data_admin = Database()
    sql = "select * from user_list where user_mys='{}'".format(openid)
    data = Data_admin.database(sql)
    return data

def insert_userinfo(data_list):
    Data_admin = Database()
    sql = 'insert into user_list(user_name, user_head, user_key, user_mys) values (%s, %s, %s, %s)'
    Data_admin.database(sql, data_list=data_list)

def update_user(user_name, user_head, session_key, openid):
    Data_admin = Database()
    sql = "update user_list set user_name='{}', user_head='{}', user_key='{}'" \
          "where user_mys='{}'".format(user_name, user_head, session_key,openid)
    Data_admin.database(sql)

@session.route('/getSessionKeyByCode/', methods = ['POST','GET'])
def getSession():
    data = json.loads(request.get_data().decode('utf-8')) #将前端Json数据转为字典
    print(data)
    appID = 'wx1be37ca8f17adf7e' #开发者关于微信小程序的appID
    appSecret = '0753daac79e8f2c362adb9258686c3e1' #开发者关于微信小程序的appSecret
    code = data['code'] #前端POST过来的微信临时登录凭证code
    user_name = data['user_info']['nickName']
    print(user_name)
    user_head = data['user_info']['avatarUrl']
    req_params = {
        'appid': appID,
        'secret': appSecret,
        'js_code': code,
        'grant_type': 'authorization_code'
    }
    wx_login_api = 'https://api.weixin.qq.com/sns/jscode2session'
    response_data = requests.get(wx_login_api, params=req_params) #向API发起GET请求
    data = response_data.json()
    openid = data['openid'] #得到用户关于当前小程序的OpenID
    session_key = data['session_key'] #得到用户关于当前小程序的会话密钥session_key

    # 下面部分是通过判断数据库中用户是否存在来确定添加或返回自定义登录态（若用户不存在则添加；若用户存在，我这里返回的是添加用户时生成的自增长字段UserID）
    if openid and session_key:
        # 在数据库用户表查询（查找得到的OpenID在数据库中是否存在）
        user_info = select_userid(openid)
        print(user_info)
        res = {}
        res['data']= {}
        res['data']['openId'] = openid
        res['data']['session_key'] = session_key
        if user_info:
            update_user(user_name, user_head, session_key, openid)
            # return json.dumps(user_info[0][0], ensure_ascii=False)  # 将UserID转为Json返回
            res['errno'] = 1
            return res
        else:
            user_info_list = []
            user_info_list.append(((user_name, user_head, session_key, openid)))
            insert_userinfo(user_info_list)
            res['errno'] = 0
            return res
    else:
        return "code失效或不正确"

