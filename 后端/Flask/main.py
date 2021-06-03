# 1.导入Flask类
from flask import Flask

# 2.创建Flask对象接收一个参数__name__，它会指向程序所在的包
app = Flask(__name__)

from session import session
from login import login
from get_like_list import get_like_list
from recommend import recommend
from category import category
from detail import detail
from history import history
from update_like import update_like
from check_like import check_like
from search_content import search

app.register_blueprint(session)
app.register_blueprint(login)
app.register_blueprint(get_like_list)
app.register_blueprint(recommend)
app.register_blueprint(category)
app.register_blueprint(detail)
app.register_blueprint(history)
app.register_blueprint(update_like)
app.register_blueprint(check_like)
app.register_blueprint(search)

# 3.装饰器的作用是将路由映射到视图函数index
@app.route('/hello')
def index():
    return 'Hello World'

# 4.Flask应用程序实例的run方法,启动WEB服务器
if __name__ == '__main__':
    app.run()
