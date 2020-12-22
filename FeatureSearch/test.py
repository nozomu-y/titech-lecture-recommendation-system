##################memo##################
#Description:
#特徴量検索用コード。output.jsonを参照し、入力に完全一致する講義名を出力する。
#Last update:12/22
#実装していないもの
#・一番下の同じ処理ばかりの部分を関数化したさ。
#・例えば火曜3-4と金曜1-2の許容(2回検索してくれると信じたい)。火金と1-2,3-4の許容みたいな書き方しか現状できない
#その他メモ
#・(newnums=numsとかするとポインタの値が同じになる危険)
#・reversedで後ろから要素削除が良さそう。要素0を削除してindex1に2がきて次は2を見るとかが起こらない。setだとそういうforループ内での削除ができない
#・火金の授業は火を入れている時も金を入れている時も出てくる。一方3-4Qの授業は3Qでも4Qでも出てくる
#・Periodについては開始時限で管理。1限開始か、3か5かと考えるのみ。偶数時限開始授業には未対応。開始時限以外での管理もできそう
#・参考書、講義資料等が空白の場合には出力しない。出力したいなら80,85行目not in d[x] orをin d[x] andに変更する

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
Period = [["1-","-2"],["3-","-4"],["5-","-6"],["7-","-8"],["9-","-10"]]#講義室の番号と被らないためのハイフン
Quarter = ["1","2","3","4"]
Textbooks = ["なし","ない","配布", "スライド", "資料"]
Assessment = [["試験","テスト"],["レポート","report"],["プレゼン","発表"]]

#入力で与えられるbit列、初期化。
#1は許容。0は検索範囲外なので消去

#########初期値############
bit_Academic_unit_or_major= 0 #情報工学系のみを許容
bit_Day=[0,1,1,1,1,1,1]#月曜以外を許容
bit_Period=[0,1,1,1,1]#1限以外を許容

bit_Quarter=[0,0,1,1]#3Q,4Q,3-4Qのみを許容

bit_Textbooks= 1 #教科書なしを認めない
bit_Assessment=[1,1,0]

bit_Textbooks= 1 #教科書なしを認めない。ありを認めないのが0,どちらも認めるのがそれ以外。
bit_Assessment=[1,1,0]##試験、レポートは認めるがプレゼンは認めない

#############標準入力################

input_bit_Academic_unit_or_major = input("学系選択(番号)")
bit_Academic_unit_or_major = int(input_bit_Academic_unit_or_major)
flag_Quarter=1
while(flag_Quarter):
    input_bit_Quarter=input("クオーター選択(4bit number)")
    if(len(input_bit_Quarter)!=4):
        print("入力サイズが不正です。")
    else:
        for i in range(4):
            if(input_bit_Quarter[i]!="0" and input_bit_Quarter[i]!="1"):
                print("入力文字の種類が不正です")
                break
            else:
                bit_Quarter[i]=int(input_bit_Quarter[i])
                if(i==3):
                    flag_Quarter=0


##################main##################
#開講元が情報工学系以外のとき、bit_Academic_unit_or_major[0]=0で、開講元が情報工学系のものを一掃
if(bit_Academic_unit_or_major != -1) :
    for x in reversed(nums):
        if(Academic_unit_or_major[bit_Academic_unit_or_major] != d[x]["開講元"]):
            nums.remove(x)
newnums1 = []
for i in range(len(bit_Day)):
    if bit_Day[i]==1:
        for x in nums:
            if(Day[i] in d[x]["曜日・時限(講義室)"]):
                newnums1.append(x)
nums=list(dict.fromkeys(newnums1))
for i in range(len(bit_Period)):
    if bit_Period[i]==0:
        for x in reversed(nums):
            if(Period[i][0] in d[x]["曜日・時限(講義室)"]):#7現開始ならそれ以外開始の授業を許さない
                nums.remove(x)
newnums2 = []
for i in range(len(bit_Quarter)):
    if bit_Quarter[i]==1:
        for x in nums:
            if(Quarter[i] in d[x]["開講クォーター"]):
                newnums2.append(x)
nums=list(dict.fromkeys(newnums2))
if bit_Textbooks ==0:
    for i in range(len(Textbooks)):
        for x in reversed(nums):
            if("参考書、講義資料等" not in d[x] or (Textbooks[i] not in d[x]["参考書、講義資料等"])):
                nums.remove(x)
elif bit_Textbooks == 1:
    for i in range(len(Textbooks)):
        for x in reversed(nums):
            if("参考書、講義資料等" not in d[x] or (Textbooks[i] in d[x]["参考書、講義資料等"])):
                nums.remove(x)

for i in range(len(bit_Assessment)):
    if bit_Assessment[i]==0:
        for x in reversed(nums):
            if("成績評価の基準及び方法" not in d[x] or (Assessment[i][0] in d[x]["成績評価の基準及び方法"] or Assessment[i][1] in d[x]["成績評価の基準及び方法"])):
                nums.remove(x)

for x in nums:
    print(x,d[x]["講義名"])
