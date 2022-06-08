############# NBA 빅맨 분류 프로젝트 ################

from selenium import webdriver
import urllib
from urllib.request import urlopen
import pandas as pd
from pandas import DataFrame, Series
from bs4 import BeautifulSoup


url = 'https://www.basketball-reference.com/leagues/NBA_2022_per_game.html'
driver = webdriver.Chrome('c:/data/chromedriver.exe')
driver.get(url)

html = driver.page_source
soup = BeautifulSoup(html,'html.parser')

stat_df2 = DataFrame()
for i in soup.select('''table.sortable.stats_table.now_sortable.sticky_table.eq2.re2.le2.is_sorted > 
                     tbody >tr''')[0:103]:
                         
    name = i.select_one('td > a').text.strip()
    mp = i.select_one('td[data-stat="mp_per_g"]').text.strip()
    thrpa = i.select_one('td[data-stat="fg3a_per_g"]').text.strip()
    twopa = i.select_one('td[data-stat="fg2a_per_g"]').text.strip()
    thr = i.select_one('td[data-stat="fg3_per_g"]').text.strip()
    two = i.select_one('td[data-stat="fg2_per_g"]').text.strip()
    trb = i.select_one('td[data-stat="trb_per_g"]').text.strip()
    ast = i.select_one('td[data-stat="ast_per_g"]').text.strip()
    stl = i.select_one('td[data-stat="stl_per_g"]').text.strip()
    blk = i.select_one('td[data-stat="blk_per_g"]').text.strip()
    stat_df2 = stat_df2.append({'name':name,'mp':mp,'3pa':thrpa,'2pa':twopa,'3p':thr,'2p':two,'reb':trb,
                              'ast':ast,'stl':stl,'blk':blk},ignore_index=True)

stat_df2.to_csv('c:/data/nba_stat2.csv')

stat_df2 = pd.read_csv('c:/data/nba_stat2.csv',index_col=0)
stat_df.info()

sta = stat_df2.loc[stat_df['mp']>10,]
sta.reset_index(inplace=True)
del sta['index']
sta


from sklearn.preprocessing import MinMaxScaler
stat_scale = MinMaxScaler()
stat_scale.fit(sta.iloc[:,2:10])

stat_scale.scale_
x_scale = stat_scale.transform(sta.iloc[:,2:10])
type(x_scale)
x_scale.shape
sta2 = DataFrame(x_scale)


sta2['sum'] = sta2.sum(axis=1)

sta3 = DataFrame()
for i in range(80):
    sta3 = sta3.append(sta2.iloc[i].apply(lambda x : x/sta2['sum'][i]))

sta3

sta4 = DataFrame({'name': sta['name'],'3pa':sta3[0], '2pa':sta3[1], '3p':sta3[2],'2p':sta3[3],
                  'reb':sta3[4],'ast':sta3[5],'blk':sta3[7]})
sta4

from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np

# k = 3으로 결정
inertia = []
for k in range(1,10):
    model = KMeans(n_clusters=k)
    model.fit(sta4.iloc[:,1:])
    inertia.append(model.inertia_)
    
plt.plot(range(1,10),inertia,'-o')

model = KMeans(n_clusters=3)
model.fit(sta4.iloc[:,1:])
model.labels_
model.cluster_centers_

sta4['cluster'] = model.labels_
sta4

model.inertia_ 

# 군집별 특징 확인하기
sta_0 = sta4[sta4['cluster']==0]
class_1 = sta_0.sum()[1:8].sort_values(ascending=False)

sta_1 = sta4[sta4['cluster']==1]
class_2 = sta_1.sum()[1:8].sort_values(ascending=False)

sta_2 = sta4[sta4['cluster']==2]
class_3 = sta_2.sum()[1:8].sort_values(ascending=False)


# 중심점 중 가장 핵심이 되는 것 확인하기
model.cluster_centers_.argsort()[:,::-1][0]
model.cluster_centers_.argsort()

# 3-point-shooting center
3pa    6.455091
3p     5.511483
blk    3.081573
reb    3.006988
2p     2.841134
2pa    2.533024
ast    1.990357

# rim protector
reb    4.310379
blk    4.238831
2p     3.630211
2pa    2.861339
ast    1.101991
3pa    0.139371
3p     0.120399

# low-post attacker
reb    5.835709
2p     5.629788
2pa    5.124686
blk    3.706256
ast    3.200734
3pa    1.776999
3p     1.256102


import matplotlib.pylab as plt
from matplotlib import font_manager, rc
font_name = font_manager.FontProperties(fname='c:/windows/fonts/HMKMMAG.TTF').get_name()
rc('font',family=font_name)

class_1 = class_1.reset_index()
class_1.columns = ['index','stats']
class_1

plt.pie(class_1.stats,
        labels = class_1['index'],
        shadow=True,
        autopct='%.1f%%',
        #explode=(0.1,0.1,0,0),
        wedgeprops={'width':0.7,'linewidth':1,'edgecolor':'white'})
plt.title('3-point-shooting centers',size=15)
plt.show()

class_2 = class_2.reset_index()
class_2.columns = ['index','stats']
class_2

plt.pie(class_2.stats,
        labels = class_2['index'],
        shadow=True,
        autopct='%.1f%%',
        #explode=(0.1,0.1,0,0),
        wedgeprops={'width':0.7,'linewidth':1,'edgecolor':'white'})
plt.title('Rim Protectors',size=15)
plt.show()

class_3 = class_3.reset_index()
class_3.columns = ['index','stats']
class_3

plt.pie(class_3.stats,
        labels = class_3['index'],
        shadow=True,
        autopct='%.1f%%',
        #explode=(0.1,0.1,0,0),
        wedgeprops={'width':0.7,'linewidth':1,'edgecolor':'white'})
plt.title('Low-post Attacker',size=15)
plt.show()









