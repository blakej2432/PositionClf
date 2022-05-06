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





