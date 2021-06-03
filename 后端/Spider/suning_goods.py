# coding=UTF-8
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from data_admin import Database
from time import sleep
from lxml import etree
import re

# 向数据库中插入数据
def insert_content(data_list):
    Data_admin = Database()
    sql = 'insert into goods_list(plat_id,store_name,goods_name,goods_logo,goods_link,gcat_id,bcat_id) values (%s, %s, %s, %s, %s, %s, %s)'
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

def bcat_gid(bcat_id,bcat_name,bcat_enname,goods_name):
    for t in range(len(bcat_id)):
        if bcat_name[t] in goods_name:
            return bcat_id[t]
        elif bcat_enname[t] in goods_name:
            return bcat_id[t]
    return 0


class Suning_Product_Spider():
    def __init__(self):
        # self.keyword = input("请输入要采集商品的关键字：")  # 商品的关键字
        """
        proxy_arr = [
            '--proxy-server=http://112.80.248.73:80',
            '--proxy-server=http://154.16.63.16:8080'
        ]
        """
        option = ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-automation'])  # 开启实验性功能
        option.add_experimental_option('prefs', {'profile.managed_default_content_settings.images': 2})  # 禁止图片加载
        option.add_argument('--headless')
        option.add_argument('--no-sandbox')
        option.add_argument('--disable-dev-shm-usage')
        option.add_argument('--disable-gpu')  # 设置无头浏览器
        #proxy = random.choice(proxy_arr)
        #option.add_argument(proxy)
        self.bro = webdriver.Chrome(options=option)
        self.bro.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
          """
        })  # 可能失效

    def Get_Product_Data(self):
        # 获取商品类型名称
        gcat_name,gcat_id = select_gcat()
        # 获取品牌类型名称
        bcat_id, bcat_name, bcat_enname = bcat_list()
        for i in range(len(gcat_id)):
            self.keyword = gcat_name[i]
            self.cat_id = gcat_id[i]
            self.bro.get('https://search.suning.com/%s/'%(self.keyword))
            #print(self.keyword)
            try:
                page=self.bro.find_element_by_xpath('//span[@class="page-more"]').text
                page=re.findall('(\d+)',page)[0]
            except:
                print("获取页数失败")
                page = 1
            print("%s共检索到%d页数据" % (self.keyword, int(page)))
            #self.start_page = input("请输入起始页数：")
            #self.end_page = input("请输入结束页数：")
            self.start_page = 1
            self.end_page = int(page)
            for i in range(int(self.start_page),int(self.end_page) + 1):
                sleep(4)
                self.bro.execute_script('window.scrollTo(0, document.body.scrollHeight)')  # 向下滑动一屏
                sleep(4)
                self.Parser_Product_Data(bcat_id,bcat_name,bcat_enname)
                sleep(4)
                self.bro.find_element_by_xpath('//span[@class="page-more"]/input').send_keys(int(i)) #输入页数
                sleep(4)
                element = self.bro.find_element_by_xpath('//a[@class="page-more ensure"]')
                self.bro.execute_script("arguments[0].click();", element) #点击确认
        self.bro.quit()

    def Parser_Product_Data(self,bcat_id,bcat_name,bcat_enname):
        html=etree.HTML(self.bro.page_source)
        li_list=html.xpath('//ul[@class="general clearfix"]/li')
        for li in li_list:
            data_list = []
            dic={}
            try:
                dic["theme"] = "".join(
                    li.xpath('.//div[@class="res-info"]/div[@class="title-selling-point"]/a[1]//text()'))
                dic['title'] = dic["theme"].split("\n")[0]
            except:
                dic["title"]=""
            try:
                dic["shop"]=li.xpath('.//div[@class="store-stock"]/a[1]/text()')[0]
            except:
                dic["shop"]=""
            try:
                dic["img_link"]="http:"+li.xpath('.//div[@class="img-block"]/a[1]/img/@src')[0]
            except:
                dic["img_link"]=""
            try:
                if "http" in li.xpath('.//div[@class="res-info"]/div[@class="title-selling-point"]/a[1]/@href')[0]:
                    dic["detail_link"]=li.xpath('.//div[@class="res-info"]/div[@class="title-selling-point"]/a[1]/@href')[0]
                else:
                    dic["detail_link"]="http:"+li.xpath('.//div[@class="res-info"]/div[@class="title-selling-point"]/a[1]/@href')[0]
            except:
                continue
            # 获取当前商品的品牌id
            bcat = bcat_gid(bcat_id, bcat_name, bcat_enname, dic["title"])
            if bcat == 0:
                continue
            else:
                # 插入数据
                data_list.append((1,dic["shop"],dic["title"],dic["img_link"],dic["detail_link"],self.cat_id,bcat))
                insert_content(data_list)

if __name__ == '__main__':
    Spider=Suning_Product_Spider()
    Spider.Get_Product_Data()
