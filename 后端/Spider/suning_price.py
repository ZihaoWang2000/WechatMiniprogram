# coding=UTF-8
from selenium import webdriver
import time
import datetime
from data_admin import Database

def buffer(browser):
    for i in range(10):
        time.sleep(0.3)
        browser.execute_script('window.scrollBy(0,1000)', '')

def select_link():
    Data_admin = Database()
    sql = "select goods_id,goods_link from goods_list where plat_id = 1"
    data = Data_admin.database(sql)
    return data

def insert_price(data_list):
    Data_admin = Database()
    sql = 'insert into price_list(goods_id,price_down,upd_time) values (%s, %s, %s)'
    Data_admin.database(sql, data_list=data_list)

def delete_detail(goods_id):
    Data_admin = Database()
    sql = 'delete from goods_list where goods_id={}'.format(goods_id)
    Data_admin.database(sql)

def update_datail(store_name, goods_id):
    Data_admin = Database()
    sql = "update goods_list set store_name='{}'" \
          "where goods_id={}".format(store_name,  goods_id)
    Data_admin.database(sql)

#遍历商品详情页，抓取目标数据
def detail_spider(browser,detail_url,goods_id):
    # browser.maximize_window()# 最大化窗口
    data_list = []
    browser.get(detail_url)
    browser.implicitly_wait(3)
    # buffer(browser)
    # 获取价格(当前商品价格)
    try:
        price = browser.find_element_by_class_name('mainprice').text
        today = datetime.date.today().strftime('%Y-%m-%d')
        data_list.append((goods_id, price[1:], today))
        insert_price(data_list)
        print("于{}插入goods_id为{}的价格数据成功".format(today,goods_id))
    except:
        delete_detail(goods_id)
        print("删除goods_id为{}，goods_link为{}的商品类目".format(goods_id,detail_url))
        return
    try:
        shop_name = browser.find_element_by_id('chead_indexUrl').text
        update_datail(shop_name, goods_id)
        print("于{}更新goods_id为{}的店铺数据成功".format(today, goods_id))
    except:
        return

if __name__ == '__main__':
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    option.add_argument('--no-sandbox')
    option.add_argument('--disable-dev-shm-usage')
    browser = webdriver.Chrome(options=option)
    data = select_link()
    for item in data:
        goods_id = item[0]
        goods_link = item[1]
        detail_spider(browser,goods_link,goods_id)
        #browser.close()
        # time.sleep(2)
    browser.quit()