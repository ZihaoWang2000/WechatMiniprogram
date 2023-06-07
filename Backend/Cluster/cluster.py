import re
from sklearn import metrics
import numpy as np
import pandas as pd
from jieba import analyse
import jieba.posseg as pseg
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer  # 基于TF-IDF的词频转向量库
from sklearn.cluster import KMeans
from data_admin import Database


# 中文分词
def seg_sentence(text):
    # sentence_seged = jieba.cut(text)
    word_list = []  # 建立空列表用于存储分词结果
    seg_list = pseg.cut(text)  # 精确模式分词[默认模式]
    for word in seg_list:
        if word.flag not in ['mq','m']:  # 选择属性
            #print(word.flag,word.word)
            word_list.append(word.word)  # 分词追加到列表
    stopwords = [line.strip() for line in open('stopwords.txt', 'r', encoding='utf-8').readlines()]# 这里加载停用词的路径
    outstr = ''
    for word in word_list:
        if word not in stopwords:
            if word != '\t':
                outstr += word
                outstr += " "
    return outstr

# 数据清理
def data_clean(text):
    text = re.sub(r'\n+', '', text)  # remove \n，re.sub(r'a','b','c'),将c中的a部分替换为b
    text = re.sub(r' +', '', text)  # remove blank        content[i] = re.sub(r'\W+', ' ', content[i])  # 用空格替换特殊字符，即评论中的表情等
    #remove_list = []  # 要删除的词的列表
    #for re_wd in remove_list:
    #    text = re.sub(re_wd, ' ', text)  # replace symbols with blank
    return text

# 计算tf-idf，提取关键词列表
def getKeywords_tfidf(text):
    line_seg = seg_sentence(text)
    key_words_TFIDF = analyse.extract_tags(line_seg) # 提取每一句的前num个关键词
    kwds = " ".join(key_word

    s_TFIDF)
    return kwds

# 词向量模型
def vectorizer(kwds_list):
    vectorizer = TfidfVectorizer()  # 创建词向量模型
    X = vectorizer.fit_transform(kwds_list)  # 将评论关键字列表转换为词向量空间模型
    word_vectors = vectorizer.get_feature_names()  # 词向量
    word_values = X.toarray()  # 向量值
    return word_values

# K均值聚类
def cluster(kwds_list,goods_id,goods_name):
    word_values = vectorizer(kwds_list)
    column = []
    if len(word_values[0]) > 10:
        down_num = 10 # 降维维数
        if len(kwds_list) < 10:
            down_num = len(kwds_list)-1
        # 数据框标签
        i = 1
        while i <= down_num:
            column.append('pca_'+str(i))
            i += 1
        # PCA降维
        pca = PCA(n_components=down_num)  # 输出两维
        word_values = pca.fit_transform(word_values)  # 载入N维
    else:
        i = 1
        while i <= len(word_values[0]):
            column.append('pca_' + str(i))
            i += 1
    # K均值聚类
    # model_kmeans = KMeans(n_clusters=num)  # 创建聚类模型对象,num指定类簇数量
    # model_kmeans.fit(newData)  # 训练模型
    # # 聚类结果汇总
    # cluster_labels = model_kmeans.labels_  # 聚类标签结果
    best_k, cluster_labels = k_cluster(word_values)
    column.append('cluster_labels')
    column.append('keywords')
    column.append('goods_id')
    column.append('goods_name')

    kwds_list = np.array(kwds_list).reshape(word_values.shape[0], 1)
    goods_id = np.array(goods_id).reshape(word_values.shape[0], 1)
    goods_name = np.array(goods_name).reshape(word_values.shape[0], 1)
    goods_matrix = np.hstack((word_values, cluster_labels.reshape(word_values.shape[0], 1), kwds_list, goods_id, goods_name))  # 将向量值和标签值合并为新的矩阵
    #print(goods_matrix)
    #print(column)
    goods_pd = pd.DataFrame(goods_matrix, columns=column)  # 创建包含词向量和聚类标签的数据框
    # word_vectors.append('cluster_labels')  # 将新的聚类标签列表追加到词向量后面
    # comment_pd = pd.DataFrame(comment_matrix, columns=word_vectors)  # 创建包含词向量和聚类标签的数据框
    # goods_pd.to_csv('goods.csv')
    # comment_matrix = np.hstack((newData, cluster_labels.reshape(newData.shape[0], 1)))  # 将向量值和标签值合并为新的矩阵
    # comment_pd = pd.DataFrame(comment_matrix, columns=['pca_x','pca_y','cluster_labels'])  # 创建包含词向量和聚类标签的数据框
    # comment_pd.to_csv('pca.csv')
    # cluster_label = cluster_labels.reshape(newData.shape[0], 1)
    # print(cluster_label)
    # return cluster_label, newData
    return goods_pd, best_k

# KMEANS聚类
def k_cluster(data):
    score_list = list()  # 用来存储每个K下模型的平局轮廓系数
    silhouette_int = -1  # 初始化的平均轮廓系数阀值
    cluster_labels_k = []
    best_k = 0
    if len(data)>20:
        num = 20
    else:
        num = len(data)
    for n_clusters in range(2, num+1):  # 遍历从2到10几个有限组
        model_kmeans = KMeans(n_clusters=n_clusters, random_state=0)  # 建立聚类模型对象
        cluster_labels_tmp = model_kmeans.fit(data)  # 训练聚类模型
        cluster_labels = cluster_labels_tmp.labels_  # 聚类标签结果
        try:
            silhouette_tmp = metrics.silhouette_score(data, cluster_labels)  # 得到每个K下的平均轮廓系数
            if silhouette_tmp > silhouette_int:  # 如果平均轮廓系数更高
                best_k = n_clusters  # 将最好的K存储下来
                silhouette_int = silhouette_tmp  # 将最好的平均轮廓得分存储下来
                best_kmeans = model_kmeans  # 将最好的模型存储下来
                cluster_labels_k = cluster_labels  # 将最好的聚类标签存储下来
            score_list.append([n_clusters, silhouette_tmp])  # 将每次K及其得分追加到列表
        except:
            cluster_labels_k = cluster_labels
            best_k = n_clusters
            break
    #print(best_k)
    return best_k, cluster_labels_k

# 输出每一类中句子的关键词
def print_cluster(num, goods_pd):
    i = 0
    while i < num:
        #data_p = goods_pd[(goods_pd.cluster_labels == str(i))]['keywords']
        data_p = goods_pd[(goods_pd.cluster_labels == str(i))]['goods_name']
        data_p = np.array(data_p)
        print('类别',i,'：')
        print(data_p)
        i+=1

def excecute(data_1):
    kwds_list = []  # 每句评论的关键词列表
    goods_id = []
    #content_list = []
    goods_name = []
    num = len(data_1)
    for text in data_1:
        # print(type(text[1]))
        item = data_clean(text[1])  # 数据清理
        # content_list.append(seg_sentence(item))
        goods_id.append(text[0])
        goods_name.append(text[1])
        kwds_list.append(getKeywords_tfidf(item))  # 每句评论提取关键词
    # label, reduced_x = cluster(5, kwds_list)  #设置类簇数量为5
    goods_pd,best_k = cluster(kwds_list,goods_id,goods_name)  # 设置类簇数量为5
    # print_cluster(best_k,goods_pd)  # 设置类簇数量为5
    return goods_pd,best_k

def main():
    Data_admin = Database()
    item_id = 2006
    for i in range(11,45):
        for t in range(1,26):
            if i==11 and t<20:
                continue
            print(i,t)
            sql_1 = 'select goods_id, goods_name from goods_list where bcat_id = {} and gcat_id ={}'.format(i, t)
            data_1 = Data_admin.database(sql_1)
            print("bcat_id为{}的品牌，gcat_id为{}的类目的商品更新成功".format(i, t))
            if len(data_1) == 0:
                continue
            elif len(data_1) == 1:
                item_id += 1
                sql_2 = "update goods_list set item_id='{}'" \
                      "where goods_id={}".format(item_id, data_1[0][0])
                Data_admin.database(sql_2)
                print("goods_id为{}的商品更新item_id为{}成功".format(data_1[0][0],item_id))
            else:
                goods_pd,best_k = excecute(data_1)
                j = 0
                while j < best_k:
                    # data_p = goods_pd[(goods_pd.cluster_labels == str(i))]['keywords']
                    data_i = goods_pd[(goods_pd.cluster_labels == str(j))]['goods_id']
                    data_i = np.array(data_i)
                    item_id += 1
                    for item in data_i:
                        sql_2 = "update goods_list set item_id='{}'" \
                                "where goods_id={}".format(item_id, item)
                        Data_admin.database(sql_2)
                        print("goods_id为{}的商品更新item_id为{}成功".format(item, item_id))
                    j += 1
        print(item_id)

if __name__ == '__main__':
    main()
