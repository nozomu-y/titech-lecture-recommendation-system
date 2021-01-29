import feature_search
import numpy as np
import pandas as pd
import json
import sys
import copy
from collections import defaultdict
'''

fs = feature_search.feature_search()
fs.get_features() #標準入力から特徴量を取得

subject_codes = fs.get_subject_codes() #取得した特徴量をもとに検索を行い、科目コードを取得

for i in range(len(subject_codes)):
    print(str(i) + ":" + subject_codes[i])
'''
fs = feature_search.feature_search()
fs.course_num=17
indexList=copy.deepcopy(fs.nums)
for ev in range(4):
    if(ev == 0):#教科書評価
        for i in range(3):
            if(i==0):
                print('教科書なし')
            elif(i==1):
                print('教科書あり')
            elif(i==2):
                print('Keyなし')
            fs.nums=copy.deepcopy(indexList)
            fs.is_need_textbook=i
            index_list = fs.get_index_list()
            print("----------該当講義一覧----------")
            t=0
            for x in index_list:
                t+=1
                print(t , '-  ' +  fs.d[x]["講義名"]["日本語"] )
                if(i!=2):
                    print(fs.d[x]["教科書"])
            print("--------------------------------")
            fs.is_need_textbook=-1
    elif(ev>=1 & ev<=3):#試験評価
        if(ev==1):
            text='試験'
        elif(ev==2):
            text='レポート'
        else:
            text='プレゼン'
        for i in range(3):
            if(i==0):
                print(text+'なし')
            elif(i==1):
                print(text+'あり')
            elif(i==2):
                print('Keyなし')
            fs.nums=copy.deepcopy(indexList)
            fs.is_need_assessment[ev-1] =i
            index_list = fs.get_index_list()
            print("----------該当講義一覧----------")
            t=0
            for x in index_list:
                t+=1
                print(t , '-  ' +  fs.d[x]["講義名"]["日本語"] )
                if(i!=2):
                    print(fs.d[x]["成績評価の基準及び方法"])
            print("--------------------------------")
            fs.is_need_assessment[ev-1]=-1
    print()
