# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 17:07:19 2017

@author: Vendredi
"""
import pandas as pd
import numpy as np
from roles2vectors import word2vectors
import scipy.cluster.hierarchy as sch
from multiprocessing import Pool
from sklearn.metrics import silhouette_score
from sklearn.metrics import silhouette_samples
from sklearn.metrics.pairwise import pairwise_distances
import pickle

def find_the_best_representative_by_silou(node_dist,words):  
    words['silouette'] = silhouette_samples(node_dist,words['cluster'],metric='precomputed')
    #会出现max可能有多个
    grouped = pd.DataFrame(words['silouette'].groupby(words['cluster']).max())
    grouped['cluster'] = grouped.index
    temp = pd.merge(words,grouped,on=['cluster','silouette'],how='right')
    temp = pd.DataFrame(temp.groupby(temp['cluster']).first())
    temp['cluster'] = temp.index
    words = pd.merge(words,temp,on=['cluster'],how = 'left')
    names = ['word','cluster_label','silouette','central_word','dump']
    words.columns = names
    return words.loc[:,['word','cluster_label','silouette','central_word']]


def get_cluster_by_criterion(i):
    '''
    计算不同聚类数量下的平均轮廓系数
    '''
    global Z,node_dist,init_cluster
    n_cluster = i + init_cluster  #从初始init_cluster 开始
    cluster= sch.fcluster(Z, t=n_cluster, criterion='maxclust')  #层次聚类的阈值达到maxclust则停止聚类
    cluster_silhouette_ = silhouette_score(node_dist,cluster,metric='precomputed',sample_size=len(cluster)) #计算轮廓系数
#     需要注意计算轮廓系数时，一个点的类其轮廓系数的定义不同，导致最终的平均轮廓系数结果源也不同
#     这个规则下，定义一个点的轮廓系数为0，变相地对过度聚类进行了惩罚，所以不需要增加惩罚因子了
    evaluation = (n_cluster,1-cluster_silhouette_) #1-轮廓系数，则轮廓系数越打，该值越小
    print("evaluation :",evaluation)
    return evaluation


def assign_pool_work(n):
    cnt = 1
    optimal_evaluation_before = 10
    k_cluster_before = init_cluster
    while cnt <= 5:  #最大重复次数为5  也就是跑50次聚类
        pool = Pool(n)  
        indexs = range((cnt-1)*5,cnt*5) #设置聚类次数
        resultList =pool.map(get_cluster_by_criterion,indexs)  
        pool.close()
        pool.join()
        k_evaluation = np.array(resultList)
        evaluation = k_evaluation[:,1:]
        optimal_evaluation = np.min(evaluation)
        k_cluster = k_evaluation[np.where(evaluation == optimal_evaluation)[0]][0][0] 
        if k_cluster != k_evaluation[-1][0]:
            if optimal_evaluation_before >= optimal_evaluation :
                optimal_evaluation_before = optimal_evaluation
                k_cluster_before = k_cluster
            break
        else:
            cnt += 1
            optimal_evaluation_before = optimal_evaluation
            k_cluster_before = k_cluster
    return (optimal_evaluation_before, k_cluster_before)


def dist_cos_matrix(X, Y=None):
    '''
    X为n_samples1*n_features的array型数据，Y为n_samples2*n_features的array型数据，
    调用pairwise_distances来计算三角度量，对于两个向量，三角距离为dist(x,y)=1-cos(x,y)。
    若Y为空，则返回表示X中元素两两间距离的n_sample1阶方阵，
    若Y不为空，则返回n_samples1*n_samples2的矩阵，第(i,j)的位置是X的第i个数据与Y的第j个数据的距离
    '''
    return pairwise_distances(X, Y, metric='cosine')

def find_initial_cluster(Z):
    '''
    寻找初始聚类数，当类间距离超过1，也就是向量垂直的时候，停止聚类，此时聚类的最大数为初始聚类数
    
    '''
    init_cluster = sch.fcluster(Z, t=1, criterion='inconsistent')  
    init_cluster = max(init_cluster)
    return init_cluster


def load_data(filepath): 
    pkl_file = open(filepath, 'rb')
    dataSets = np.array(pickle.load(pkl_file))
    words = pickle.load(pkl_file)
    disMat = sch.distance.pdist(dataSets,'cosine') 
#     average:平均距离,类与类间所有pairs距离的平均
    Z=sch.linkage(disMat,method='average') 
    node_dist = dist_cos_matrix(dataSets)
    return (words,node_dist,Z)


def cluster_group(df):
    # Z 保存层次聚类的聚类信息
    # node_dist 保存节点两两间的距离，用来计算轮廓系数
    # init_cluster 初始规定的聚类数
    global Z,node_dist,init_cluster
    cluster_url = []
    cluster_url= word2vectors(df)
    
    w = []
    for url in cluster_url:
        print("cluster_url:",url)
        words,node_dist,Z = load_data(url)
        init_cluster = find_initial_cluster(Z)
        print("init_cluster:",init_cluster)
        optimal_evaluation,k_cluster = assign_pool_work(2)
        print("最优轮廓系数是 %f" % optimal_evaluation)
        print("最优聚类数是 %d" % int(k_cluster))
        words = pd.DataFrame(words,columns=['word'])
        words['cluster'] = sch.fcluster(Z, t=k_cluster, criterion='maxclust')
        words = find_the_best_representative_by_silou(node_dist,words)
        w.append(words)
    