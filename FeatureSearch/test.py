##################memo##################
#Description:
#特徴量検索用コード。output.jsonを参照し、入力に完全一致する講義名を出力する。
#Last update:12/16
#実装していないもの
#・「成績評価の基準及び方法」「参考書、講義資料等」がシステム構築演習や問題解決と意思決定などにないためkey errorが起きる
#・例えば火曜3-4と金曜1-2の許容(2回検索してくれると信じたい)。火金と1-2,3-4の許容みたいな書き方しか現状できない
#・火曜と金曜の授業を、火曜のみにチェックがついているときに部分一致のものとして出したりとか、関連度高い科目として出したりするとか
#その他メモ
#・(newnums=numsとかしてもポインタの値が同じになる)
#・reversedで後ろから要素削除が良さそう。要素0を削除してindex1に2がきて次は2を見るとかが起こらない
#・プログラミング創造演習などが開講クォーター1-2Q。一部科目が1-4限表記
#・火金の授業は火も金も許容していないとでてこない。3-4Qの授業も3Qと4Qを許容しないとでてこない
#・1-4の授業は1と4の数字があるからやはり1-2も3-4も許容していないとでてこない

#################settings#################
import numpy as np
import pandas as pd
import json
# import matplotlib.pyplot as plt
# import matplotlib.ticker as ticker
# import seaborn as sns
# from sklearn import datasets, model_selection, svm, metrics
# from sklearn.preprocessing import LabelEncoder
# from sklearn.preprocessing import LabelBinarizer
# from sklearn.model_selection import cross_validate,KFold
# from sklearn.metrics import (confusion_matrix, accuracy_score, precision_score, recall_score)
# from sklearn.model_selection import GridSearchCV
# from sklearn.decomposition import PCA
# from sklearn.preprocessing import StandardScaler
# from sklearn.model_selection import train_test_split
# from collections import OrderedDict
# import pprint

f = open("../DataCollection/output.json")
d = json.load(f)
nums = list(range(len(d)))#出力するdのindex

Academic_unit_or_major = ["情報工学系","数理・計算化学系","情報通信系","システム制御系","電気電子系"]
Day = ["月","火","水","木","金","土","日"]
Period = [["1-","-2"],["3-","-4"],["5-","-6"],["7-","-8"],["9-","-10"]]#講義室の番号対策のハイフン
Quarter = ["1","2","3","4"]
Assessment = [["試験","テスト"],["レポート","report"],["プレゼン","発表"]]
Textbooks = [["なし","ない","配布"]]
#1は許容。0は検索範囲外なので消去
bit_Academic_unit_or_major=[1,0,0,0,0]
bit_Day=[0,1,0,0,1,0,0]
bit_Period=[0,0,0,1,0]
bit_Quarter=[0,0,0,1]
bit_Assessment=[1,1,0]
bit_Textbooks=[0]

##################main##################
#開講元が情報工学系以外のとき、bit_Academic_unit_or_major[0]=0で、開講元が情報工学系のものを一掃
for i in range(len(bit_Academic_unit_or_major)) :
    if bit_Academic_unit_or_major[i]==0:
        for x in reversed(nums):
            if(Academic_unit_or_major[i] == d[x]["開講元"]):
                nums.remove(x)
for i in range(len(bit_Day)):
    if bit_Day[i]==0:
        for x in reversed(nums):
            if(Day[i] in d[x]["曜日・時限(講義室)"]):
                nums.remove(x)
for i in range(len(bit_Period)):
    if bit_Period[i]==0:
        for x in reversed(nums):
            if(Period[i][0] in d[x]["曜日・時限(講義室)"] or Period[i][1] in d[x]["曜日・時限(講義室)"]):
                nums.remove(x)
for i in range(len(bit_Quarter)):
    if bit_Quarter[i]==0:
        for x in reversed(nums):
            if(Quarter[i] in d[x]["開講クォーター"]):
                nums.remove(x)
# for i in range(len(bit_Textbooks)):
#     if bit_Textbooks[i]==0:
#         for x in reversed(nums):
#             if(Textbooks[i][0] in d[x]["参考書、講義資料等"] or Textbooks[i][1] in d[x]["参考書、講義資料等"] or Textbooks[i][2] in d[x]["参考書、講義資料等"]):
#                 nums.remove(x)
# for i in range(len(bit_Assessment)):
#     if bit_Assessment[i]==0:
#         for x in reversed(nums):
#             if(Assessment[i][0] in d[x]["成績評価の基準及び方法"] or Assessment[i][1] in d[x]["成績評価の基準及び方法"]):
#                 nums.remove(x)
for x in nums:
    print(x,d[x]["講義名"])
