#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 09:23:52 2019

@author: zzy
"""

import numpy as np
import pandas as pd
from tqdm import tqdm

#读取两个数据
time_file=np.load('time_select.npz.npy', allow_pickle = True) #单独提取出时刻的npy
df1 = pd.DataFrame(time_file, columns = ['road_id', 'date', 'tti', 'speed', 'time'])
len(df1)

#找出所有的路
id_roads=df1[df1['date']=='2018-01-01 00:00:00']['road_id'].values #找出来的有所有路的集合
list_roads=[] #构建一个空列表存储所有路的ID
for i in range(len(id_roads)):
    list_roads.append(id_roads[i])
print(len(list_roads))

roads_completed=df1[df1['road_id']==283406]['date'].values #有完整的时间片的路
for i in range(17280): #遍历，找到所有的路
    id_roads2=df1[df1['date']==roads_completed[i]]['road_id'].values
    for road in id_roads2:
        if (not(road in list_roads)):
            list_roads.append(road)
        print(len(list_roads))

data = np.load('桌面/1.npy', allow_pickle = True)#原始的，未提取时刻的npy
df = pd.DataFrame(data, columns = ['road_id', 'time', 'tti', 'speed'])

#for i in range(len(list_roads)): #所有路的大循环
for i in [0,4]: #挑了两条路试验
    standard=df1[df1['road_id']==283406]['date'].values #时间块齐全的路
    one=df1[df1['road_id']==list_roads[i]] #挑一条路
    one_time=one['date'].values #选出里面的时间
    length=len(one_time) #确定长度
    list_absent=[] #构建一个列表存储缺少的时间片
    for time in standard: #找出缺少的时间片
        if(not(time in one_time)):
            list_absent.append(time) #把缺少的时间片存在列表里
    time_completed=df1[df1['road_id']==283406] #时间片完整的路的信息
    time_absent=df1[df1['road_id']==list_roads[i]] #当前路的信息
    #print(list_absent)
    #print(time_absent)
    for j in range(len(list_absent)): #在当前路所缺失的时间片里分别处理
        time_absent_time=time_completed[time_completed['date']==list_absent[j]]['time'].values[0] #找出缺少的时间片对应的时间（不包括日期）
        time_absent_tti=time_absent[time_absent['time']==time_absent_time]['tti'].values #找出所有同一时刻的tti信息
        time_absent_time1=time_completed[time_completed['date']==list_absent[j]]['time'].values[0]  #同上
        time_absent_speed=time_absent[time_absent['time']==time_absent_time1]['speed'].values  
        tti = time_absent_tti.sum()/len(time_absent_tti) #求历史平均
        speed =time_absent_speed.sum()/len(time_absent_speed)
        print(tti)
        list_info=[list_roads[i],list_absent[j],tti,speed] #构建一个列表，存储信息
        df = df.append([{'road_id':list_info[0],'time':list_info[1],'tti':list_info[2],'speed':list_info[3]}], ignore_index=True)#无序添加一行数据
        print(len(df)) #看df的长度有没有变化判断有没有填进去
        print(df.tail(2)) #看df的最后两行做判断
