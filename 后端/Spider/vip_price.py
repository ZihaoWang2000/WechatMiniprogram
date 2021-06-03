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
    sql = "select goods_id,goods_link,store_name from goods_list where plat_id = 3"
    data = Data_admin.database(sql)
    return data

def update_datail(store_name, goods_logo, goods_id):
    Data_admin = Database()
    sql = "update goods_list set store_name='{}', goods_logo='{}'" \
          "where goods_id={}".format(store_name,  goods_logo, goods_id)
    Data_admin.database(sql)

def insert_price(data_list):
    Data_admin = Database()
    sql = 'insert into price_list(goods_id, price_now, price_down, upd_time) values (%s, %s, %s, %s)'
    Data_admin.database(sql, data_list=data_list)

def delete_detail(goods_id):
    Data_admin = Database()
    sql = 'delete from goods_list where goods_id={}'.format(goods_id)
    Data_admin.database(sql)


#遍历商品详情页，抓取目标数据
def detail_spider(browser,detail_url,goods_id,store_name):
    # browser.maximize_window()# 最大化窗口
    data_list = []
    browser.get(detail_url)
    browser.implicitly_wait(36)
    #buffer(browser)
    # 获取价格(当前商品价格)
    # 获取价格(当前商品价格)
    try:
        price_down = browser.find_element_by_class_name('sp-price').text
        price_now = browser.find_element_by_class_name('marketPrice').text
        today = datetime.date.today().strftime('%Y-%m-%d')
        data_list.append((goods_id, price_now, price_down, today))
        insert_price(data_list)
        print("于{}插入goods_id为{}的价格数据成功".format(today,goods_id))
    except:
        #delete_detail(goods_id)
        #print("删除goods_id为{}，goods_link为{}的商品类目".format(goods_id, detail_url))
        return
    if store_name == None:
        # 获取图片链接
        try:
            img_link = browser.find_element_by_xpath('//*[@id="J-img-content"]/div[2]/img').get_attribute('src')
        except:
            img_link = ""
        # 获取店名
        try:
            shop_name = browser.find_element_by_class_name('mp-title-storename').text
        except:
            shop_name = "唯品会自营"
            buffer(browser)
        update_datail(shop_name,img_link,goods_id)
        print("于{}更新goods_id为{}的店铺数据成功".format(today, goods_id))

if __name__ == '__main__':
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    option.add_argument('--no-sandbox')
    option.add_argument('--disable-dev-shm-usage')
    browser = webdriver.Chrome(options=option)
    data = select_link()
    for item in data:
        goods_id = item[0]
        goods_link = item[1]
        store_name = item[2]
        detail_spider(browser,goods_link,goods_id,store_name)
        #browser.close()
        #time.sleep(4)
    browser.quit()
