# coding=UTF-8
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from data_admin import Database
from time import sleep
from lxml import etree

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


class JD_Product_Spider():
    def __init__(self):
        # self.keyword = input("请输入要采集商品的关键字：")  # 商品的关键字
        option = ChromeOptions()
        option.add_experimental_option('prefs',{'profile.managed_default_content_settings.images': 2})  # 禁止图片加载，加快速度
        option.add_argument('--headless')
        option.add_argument('--no-sandbox')
        option.add_argument('--disable-dev-shm-usage')
        option.add_argument('--disable-gpu')  # 设置无头浏览器
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
        gcat_name, gcat_id = select_gcat()
        # 获取品牌类型名称
        bcat_id, bcat_name, bcat_enname = bcat_list()
        for i in range(12, len(gcat_id)):
            self.keyword = gcat_name[i]
            self.cat_id = gcat_id[i]
            #print(self.keyword)
            self.bro.maximize_window()  # 最大化浏览器
            try:
                url = "https://search.jd.com/Search?keyword=%s" % (self.keyword)
                self.bro.get(url)
                self.bro.execute_script('window.scrollTo(0, document.body.scrollHeight)')  # 向下滑动一屏
                # page循环访问 (推荐)
                sleep(1)
                page = self.bro.find_element_by_xpath('//span[@class="p-skip"]/em/b').text
            except:
                print("获取页数失败")
                page = 1
            print("%s检索到共%s页数据" % (self.keyword, int(page)))
            # start_page=input("请输入起始页数：")
            # end_page=input("请输入结束页数：")
            self.start_page = 1
            self.end_page = int(page)
            for i in range(int(self.start_page), int(self.end_page) + 1):
                sleep(5)
                print("-" * 30 + "已获取第%s页数据" % (i) + "-" * 30)
                url = "https://search.jd.com/Search?keyword=%s&page=%d" % (self.keyword, i * 2 - 1)
                self.bro.get(url)
                self.Parser_Profuct_Data(bcat_id,bcat_name,bcat_enname)
        self.bro.quit()

    def Parser_Profuct_Data(self,bcat_id,bcat_name,bcat_enname):
        html = etree.HTML(self.bro.page_source)
        li_list = html.xpath('//ul[@class="gl-warp clearfix"]/li')
        for li in li_list:
            data_list = []
            dic = {}
            try:
                dic["title"] = "".join(li.xpath('./div/div[@class="p-name p-name-type-2"]/a/em//text()'))
                if "\n" in dic["title"]:
                    dic["title"] = dic["title"].split("\n")[-1]
            except:
                dic["title"] = ""
            try:
                dic["shop"] = li.xpath('./div/div[@class="p-shop"]/span/a/text()')[0]
            except:
                dic["shop"] = ""
            try:
                dic["detail_link"] = "https:" + li.xpath('./div/div[@class="p-name p-name-type-2"]/a/@href')[0]
            except:
                continue
            # 获取当前商品的品牌id
            bcat = bcat_gid(bcat_id, bcat_name, bcat_enname, dic["title"])
            if bcat == 0:
                continue
            else:
                # 插入数据
                data_list.append((2, dic["shop"], dic["title"], "", dic["detail_link"], self.cat_id, bcat))
                insert_content(data_list)

if __name__ == "__main__":
    Spider=JD_Product_Spider()
    Spider.Get_Product_Data()