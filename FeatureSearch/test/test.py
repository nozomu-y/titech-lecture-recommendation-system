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
#・periodについては開始時限で管理。1限開始か、3か5かと考えるのみ。偶数時限開始授業には未対応。開始時限以外での管理もできそう
#・参考書、講義資料等が空白の場合には出力しない。出力したいなら80,85行目not in d[x] orをin d[x] andに変更する

#################settings#################
import numpy as np
import pandas as pd
import json
import sys
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

course = ["情報工学系","数理・計算化学系","情報通信系","システム制御系","電気電子系"]
day = ["月","火","水","木","金","土","日"]
period = ["1-","2-","3-","4-","5-","6-","7-","8-","9-","10-"]#講義室の番号と被らないためのハイフン
quarter = ["1","2","3","4","1-2","3-4","2-3","2・4","2-4","1-4"]
textbook = ["なし","ない","配布", "スライド", "資料"]
assessment = [["試験","テスト"],["レポート","report"],["プレゼン","発表"]]

#入力で与えられるbit列、初期化。
#1は許容。0は検索範囲外なので消去

#########初期値############
course_num= 0 #情報工学系のみを許容
day_select=[0,1,1,1,1,1,1]#月曜以外を許容
period_select=[0,1,1,1,1,1,1,1,1,1]#1限以外を許容

quarter_select=[0,0,1,1,0,1,0,0,0,0]#3Q,4Q,3-4Qのみを許容

is_need_textbook= 1 #教科書なしを認めない。ありを認めないのが0,どちらも認めるのがそれ以外。
is_need_assessment=[1,1,0]##試験、レポートは認めるがプレゼンは認めない

#############標準入力################
print("開講元選択(数字を入力)")
print(str(-1) + ":" + "選択しない")
for i in range(len(course)):
    print(str(i) + ":" + course[i])
course_num = int(input())
if(course_num < -1 or len(course) < course_num):
    print("入力が不正です。")
    sys.exit(1)

print("開講クォーター(10bitで答える 1:選択, 0:選択しない)")
print("ex.) 0011010000")
for i in range(len(quarter)-1):
    print(" " + quarter[i] + "Q", end = ',')
print(" " + quarter[len(quarter)-1] + "Q")
flag_quarter=1
while(flag_quarter):
    input_quarter_select=input()
    if(len(input_quarter_select)!=len(quarter)):
        print("入力サイズが不正です。")
        sys.exit(1)
    else:
        for i in range(len(quarter)):
            if(input_quarter_select[i]!="0" and input_quarter_select[i]!="1"):
                print("入力文字の種類が不正です")
                sys.exit(1)
            else:
                quarter_select[i]=int(input_quarter_select[i])
                if(i==len(quarter)-1):
                    flag_quarter=0

print("教科書の有無  1:あり, 0:なし, -1:選択しない")
is_need_textbook = int(input())
if(not(is_need_textbook == 0 or is_need_textbook == 1 or is_need_textbook == -1)):
    print("入力が不正です。")
    sys.exit(1)

print("試験の有無  1:あり, 0:なし, -1:選択しない")
is_need_assessment[0] = int(input())
if(not(is_need_assessment[0] == 0 or is_need_assessment[0] == 1 or is_need_assessment[0] == -1)):
    print("入力が不正です。")
    sys.exit(1)

print("レポートの有無  1:あり, 0:なし, -1:選択しない")
is_need_assessment[1] = int(input())
if(not(is_need_assessment[1] == 0 or is_need_assessment[1] == 1 or is_need_assessment[1] == -1)):
    print("入力が不正です。")
    sys.exit(1)

print("プレゼン・発表の有無  1:あり, 0:なし, -1:選択しない")
is_need_assessment[2] = int(input())
if(not(is_need_assessment[2] == 0 or is_need_assessment[2] == 1 or is_need_assessment[2] == -1)):
    print("入力が不正です。")
    sys.exit(1)

##################main##################
#開講元が情報工学系以外のとき、course_num[0]=0で、開講元が情報工学系のものを一掃
if(course_num != -1) :
    for x in reversed(nums):
        if(course[course_num] != d[x]["開講元"]):
            nums.remove(x)
newnums1 = []
for i in range(len(day_select)):
    if day_select[i]==1:
        for x in nums:
            if(day[i] in d[x]["曜日・時限(講義室)"]):
                newnums1.append(x)
nums=list(dict.fromkeys(newnums1))
for i in range(len(period_select)):
    if period_select[i]==0:
        for x in reversed(nums):
            if(period[i] in d[x]["曜日・時限(講義室)"]):#7現開始ならそれ以外開始の授業を許さない
                nums.remove(x)
newnums2 = []
for i in range(len(quarter_select)):
    if quarter_select[i]==1:
        for x in nums:
            if(quarter[i] in d[x]["開講クォーター"]):
                newnums2.append(x)
nums=list(dict.fromkeys(newnums2))
if is_need_textbook ==0:
    for i in range(len(textbook)):
        for x in reversed(nums):
            if("参考書、講義資料等" not in d[x] or (textbook[i] not in d[x]["参考書、講義資料等"])):
                nums.remove(x)
elif is_need_textbook == 1:
    for i in range(len(textbook)):
        for x in reversed(nums):
            if("参考書、講義資料等" not in d[x] or (textbook[i] in d[x]["参考書、講義資料等"])):
                nums.remove(x)

for i in range(len(is_need_assessment)):
    if is_need_assessment[i]==0:
        for x in reversed(nums):
            if("成績評価の基準及び方法" not in d[x] or (assessment[i][0] in d[x]["成績評価の基準及び方法"] or assessment[i][1] in d[x]["成績評価の基準及び方法"])):
                nums.remove(x)
    elif is_need_assessment[i]==1:
        for x in reversed(nums):
            if("成績評価の基準及び方法" not in d[x] or (assessment[i][0] in d[x]["成績評価の基準及び方法"] or assessment[i][1] in d[x]["成績評価の基準及び方法"])):
                nums.remove(x)
print()
print("----------該当講義一覧----------")
for x in nums:
    print(d[x]["講義名"]["日本語"])
print("--------------------------------")