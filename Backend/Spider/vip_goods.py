# coding=UTF-8
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from data_admin import Database
from time import sleep
from lxml import etree

# 向数据库中插入数据
def insert_content(data_list):
    Data_admin = Database()
    sql = 'insert into goods_list(plat_id,goods_name, goods_link,gcat_id, bcat_id) values (%s, %s, %s, %s, %s)'
    Data_admin.database(sql, data_list=data_list)

# 获取商品类型名称作为关键词
def select_gcat():
    Data_admin = Database()
    sql = "select gcat_id,gcat_name from gcat_list"
    data = Data_admin.database(sql)
    gcat_name = []
    gcat_id = []
    for item in data:
        gcat_name.append(item[1])
        gcat_id.append(item[0])
    return gcat_name,gcat_id

# 获取品牌类型列表数据
def bcat_list():
    Data_admin = Database()
    sql = "select bcat_id,bcat_name,bcat_enname from bcat_list"
    data = Data_admin.database(sql)
    bcat_id = []
    bcat_name = []
    bcat_enname = []
    for item in data:
        bcat_id.append(item[0])
        bcat_name.append(item[1])
        bcat_enname.append(item[2])
    return bcat_id,bcat_name,bcat_enname

# 获取该商品的bcat_id
def bcat_gid(bcat_id,bcat_name,bcat_enname,goods_name):
    for t in range(len(bcat_id)):
        if bcat_name[t] in goods_name:
            return bcat_id[t]
        elif bcat_enname[t] in goods_name:
            return bcat_id[t]
    return 0


class Vip_Product_Spider():
    def __init__(self):
        option = ChromeOptions()
        option.add_experimental_option('prefs', {'profile.managed_default_content_settings.images': 2})
        option.add_argument('--headless')
        option.add_argument('--no-sandbox')
        option.add_argument('--disable-dev-shm-usage')
        option.add_argument("--start-maximized")
        option.add_argument('--disable-gpu')  # 设置无头浏览器
        self.bro = webdriver.Chrome(options=option)
        self.bro.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                        Object.defineProperty(navigator, 'webdriver', {
                          get: () => undefined
                        })
                      """
        })  # 可能失效


    def Get_Data(self):
        gcat_name,gcat_id = select_gcat()
        for i in range(len(gcat_id)):
            self.keyword = gcat_name[i]
            self.cat_id = gcat_id[i]
            #print(self.keyword)
            # 以商品类型名作为关键词
            url = "https://category.vip.com/suggest.php?keyword={}&page=1" . format(self.keyword)
            print(url)
            self.load_data(url)
            # 获取总页数
            page=self.bro.find_element_by_class_name('total-item-nums').text[1:-1]
            page=eval(page)
            print("%s共检索到%d页数据" % (self.keyword, int(page)))
            #self.start_page = input("请输入起始页数：")
            #self.end_page = input("请输入结束页数：")
            self.start_page = 1
            self.end_page = int(page)
            for i in range(int(self.start_page), int(self.end_page) + 1):
                sleep(3)
                url = "https://category.vip.com/suggest.php?keyword=%s&page=%d" % (self.keyword, i)
                self.load_data(url)
                bcat_id, bcat_name, bcat_enname = bcat_list()
                self.Parser_Product_Data(bcat_id, bcat_name, bcat_enname)
        self.bro.quit()
   
    # 连接网页
    def load_data(self,url):
        self.bro.get(url)
        self.bro.implicitly_wait(10)
        print(self.bro.title)
        print(self.bro.page_source)
        self.bro.execute_script('window.scrollTo(0, document.body.scrollHeight)')  # 向下拉动一屏
        self.bro.execute_script('window.scrollTo(0, document.body.scrollHeight)')  # 向下拉动一屏
        sleep(5)
    
    # 爬取列表页数据
    def Parser_Product_Data(self,bcat_id,bcat_name,bcat_enname):
        html = etree.HTML(self.bro.page_source)
        div_list = html.xpath('//section[@class="goods-list c-goods-list--normal"]/div')[1:]
        for div in div_list:
            data_list = []
            sleep(0.5)
            dic = {}
            try:
                dic["title"] = div.xpath('.//div[@class="c-goods-item__name  c-goods-item__name--two-line"]/text()')[0]
            except:
                dic["title"] = ""
            # try:
            #     dic["sale_price"] = \
            #     div.xpath('.//div[@class="c-goods-item__sale-price J-goods-item__sale-price"]//text()')[1]
            # except:
            #     dic["sale_price"] = ""
            # try:
            #     dic["market_price"] = \
            #     div.xpath('.//div[@class="c-goods-item__market-price  J-goods-item__market-price"]//text()')[1]
            # except:
            #     dic["market_price"] = ""
            # try:
            #     dic["discount"] = div.xpath('.//div[@class="c-goods-item__discount  J-goods-item__discount"]/text()')[0]
            # except:
            #     dic["discount"] = ""
            try:
                dic["detail_link"] = "https:" + div.xpath('.//a[@target="_blank"]/@href')[0]
            except:
                continue
            # 获取当前商品的品牌id
            bcat = bcat_gid(bcat_id, bcat_name, bcat_enname, dic["title"])
            if bcat == 0:
                continue
            else:
                data_list.append((3,dic["title"], dic["detail_link"],self.cat_id,bcat))
                insert_content(data_list)

if __name__ == '__main__':
    Spider=Vip_Product_Spider()
    Spider.Get_Data()
