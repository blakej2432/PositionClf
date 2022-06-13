# PositionClf

## NBA 센터 포지션 재분류(군집 분석) 프로젝트

### 1. 프로젝트 목표

* 문제정의
  * 현대 농구 전술과 개인 성향이 다양해지면서 포워드, 가드의 포지션 세분화 시도는 비교적 많으나,   
  센터 포지션의 세분화와 명명은 잘 이루어지지 않음
  * 스탯(득점, 리바운드, 블록 등)을 기준으로 성향에 따라 포지션 세분화 필요

* 분석 계획 : NBA 센터 포지션 선수들의 21-22 정규 시즌 개인 기록을 바탕으로 군집 분석을 통해 포지션 세분화

------------

### 2. 데이터 준비

* Basketball-reference.com (농구 관련 통계 정보 사이트) 출처

<img width="550" alt="사이트1" src="https://user-images.githubusercontent.com/104886103/173230499-b601e0af-2192-4d64-8644-5ac09f7ad52a.png">

<img width="630" alt="사이트2" src="https://user-images.githubusercontent.com/104886103/173230501-6a588066-d6ec-4606-81d6-913b708dc616.png">

__NBA 센터(C) 103명의 기록 데이터 수집__

__기록이 의미있도록 경기 당 평균 출전시간 10분 이상인 선수 80명 데이터로 준비__

------------

### 3. 데이터 분석

* 분석에 이용한 스탯 - <'3pa':3점슛 시도>,<'2pa':2점슛 시도>,<'3p':3점슛 득점>,<'2p':2점슛 득점>,   
<'reb':리바운드 개수>,<'ast':도움>,<'stl':가로채기>,<'blk':블록>

* MinMaxScaler를 이용하여 각 스탯을 0~1 사이의 값으로 변환하여 분석에 용이하도록 준비

* 군집 분석 - KMeans 이용

<img width="350" alt="Figure_1" src="https://user-images.githubusercontent.com/104886103/173231827-5590337e-36ac-466d-818e-a3eaa671c64e.png">

> Elbow 지점 중 K = 3 (군집 3개) 설정  

#
```python
model = KMeans(n_clusters=3)
model.fit(sta4.iloc[:,1:])
model.labels_
model.cluster_centers_

sta4['cluster'] = model.labels_
```

> 스탯 기준으로 군집 3개로 분류 뒤 cluster 컬럼에 군집 라벨링  

#

__군집별 특징 확인하기__

* 첫번째 군집

```python
sta_0 = sta4[sta4['cluster']==0]
class_1 = sta_0.sum()[1:8].sort_values(ascending=False) # 첫번째 군집의 선수들에게서 높게 나온 스탯 순서

3pa    6.455091
3p     5.511483
blk    3.081573
reb    3.006988
2p     2.841134
2pa    2.533024
ast    1.990357
```

__일반적으로 센터들에게서 기대하지 않는 3점슛 시도(3pa)와 3점슛 득점(3p)이 가장 높게 등장하는 군집__

__3-point-shooting Center__  

#

* 두번째 군집

```python
sta_1 = sta4[sta4['cluster']==1]
class_2 = sta_1.sum()[1:8].sort_values(ascending=False) # 두번째 군집의 선수들에게서 높게 나온 스탯 순서

reb    4.310379
blk    4.238831
2p     3.630211
2pa    2.861339
ast    1.101991
3pa    0.139371
3p     0.120399
```

__튕겨 나온 공을 잡는 리바운드(reb)와 상대 슛을 저지하는 블록슛(blk)이 가장 높게 나온 수비형 군집__

__Rim Protector__  

#

* 세번째 군집

```python
sta_2 = sta4[sta4['cluster']==2]
class_3 = sta_2.sum()[1:8].sort_values(ascending=False) # 세번째 군집의 선수들에게서 높게 나온 스탯 순서

reb    5.835709
2p     5.629788
2pa    5.124686
blk    3.706256
ast    3.200734
3pa    1.776999
3p     1.256102
```
__리바운드(reb)도 높지만 두번째 군집과 비교하여 2점슛 득점(2p)과 2점슛 시도(2pa)가 높은 공격형 군집__

__Post Attacker__  

#

* 대표선수

1. __3-point-shooting Center__ 

__Karl-Anthony Towns__

![towns](https://user-images.githubusercontent.com/104886103/173276076-cf3c748e-2cf8-4529-b9a6-a2f546e62509.jpg)

출처: nba.nbcsports.com  

#

2. __Rim Protector__ 

__Rudy Gobert__

<img width="250" alt="gobert" src="https://user-images.githubusercontent.com/104886103/173276471-0f4a2597-7e00-4b27-abd2-27b48feb2d73.jpg">

출처: Forbes.com  

#

3. __Post Attacker__

__Joel Embiid__

<img width="250" alt="사이트1" src="https://user-images.githubusercontent.com/104886103/173276901-12668e71-9f39-44da-bc00-cc7ebb541463.jpg">

출처: si.com

---------------------

### 4. 평가전개

* 선수 기록지를 바탕으로 특정 종류의 기록 비중이 높은 선수들을 특정 군집으로 분류 (3개)

* 3-point-shooting center / rim protector / post attacker 로 분류 가능하나,   
모든 스탯이 높은 에이스급 선수의 경우 다소 일치하지 않는 경우 존재 


