############# NBA 빅맨 분류 프로젝트 ################

from selenium import webdriver
import urllib
from urllib.request import urlopen
import pandas as pd
from pandas import DataFrame, Series
from bs4 import BeautifulSoup


MP, 3PA, 2PA, TRB, AST, STL, BLK

url = 'https://www.basketball-reference.com/leagues/NBA_2022_per_game.html'
driver = webdriver.Chrome('c:/data/chromedriver.exe')
driver.get(url)

html = driver.page_source
soup = BeautifulSoup(html,'html.parser')

stat_df = DataFrame()
for i in soup.select('''table.sortable.stats_table.now_sortable.sticky_table.eq2.re2.le2.is_sorted > 
                     tbody >tr''')[0:103]:
                         
    name = i.select_one('td > a').text.strip()
    mp = i.select_one('td[data-stat="mp_per_g"]').text.strip()
    thrpa = i.select_one('td[data-stat="fg3a_per_g"]').text.strip()
    twopa = i.select_one('td[data-stat="fg2a_per_g"]').text.strip()
    trb = i.select_one('td[data-stat="trb_per_g"]').text.strip()
    ast = i.select_one('td[data-stat="ast_per_g"]').text.strip()
    stl = i.select_one('td[data-stat="stl_per_g"]').text.strip()
    blk = i.select_one('td[data-stat="blk_per_g"]').text.strip()
    stat_df = stat_df.append({'name':name,'mp':mp,'3pa':thrpa,'2pa':twopa,'reb':trb,
                              'ast':ast,'stl':stl,'blk':blk},ignore_index=True)

stat_df.to_csv('c:/data/nba_stat.csv')

stat_df = pd.read_csv('c:/data/nba_stat.csv',index_col=0)

from sklearn.preprocessing import StandardScaler

s = StandardScaler()
s.fit_transform(x)

s = StandardScaler().fit(x)
r = s.transform(x)

np.mean(r)
np.std(r)

s.mean_
s.scale_
s.var_


from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np

model = KMeans(n_clusters=3)
model.fit(stat_df.iloc[:,2:])
model.labels_
model.cluster_centers_

stat_df['cluster'] = model.labels_
stat_df

colormap = np.array(['red','blue','black'])
plt.scatter(stat_df['3pa'],stat_df['2pa'],stat_df.reb,stat_df.ast,stat_df.stl,stat_df.blk,c=colormap[model.labels_],s=40)

model.inertia_ # 이 값이 작을수록 응집도가 크다
inertia 값은 군집화된 후에 각 중심점에서 군집의 데이터간의 거리를 합산한 것이므로 군집의 응집도를 나타내는 값이다.



inertia = []
for k in range(1,10):
    model = KMeans(n_clusters=k)
    model.fit(stat_df.iloc[:,2:8])
    inertia.append(model.inertia_)
    
    
plt.plot(range(1,10),inertia,'-o') # 꺾이는 지점 - 엘보우점 (보통 k값 이 근처에서 정함)









