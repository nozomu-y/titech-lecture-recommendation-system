##################memo##################
#Description:
#特徴量検索用コード。output.jsonを参照し、入力に完全一致する講義名を出力する。
#コマンドライン引数がない場合には全科目から、ある場合には引数の科目コードの中から検索して出力。
#Last update:1/13
#実装していないもの 残りはUIのみ
#その他メモ
#・(newnums=numsとかするとポインタの値が同じになる危険)
#・reversedで後ろから要素削除が良さそう。要素0を削除してindex1に2がきて次は2を見るとかが起こらない。setだとそういうforループ内での削除ができない
#・periodについては開始時限で管理。1限開始か、3か5かと考えるのみ。偶数時限開始授業には未対応。開始時限以外での管理もできそう
#・参考書、講義資料等が空白の場合には出力しない。出力したいなら80,85行目not in d[x] orをin d[x] andに変更する

#################settings#################
import numpy as np
import pandas as pd
import json
import sys
from collections import defaultdict
import os


class feature_search:
    course = ["数学系","物理学系","化学系","地球惑星科学系",
              "機械系","システム制御系","電気電子系","情報通信系","経営工学系","工学院",
              "材料系","応用化学系",
              "数理・計算科学系","情報工学系",
              "生命理工学系",
              "建築学系","土木・環境工学系","融合理工学系",
              "日本語・日本文化科目","第二外国語科目","理工系教養科目","教職科目","英語科目","文系教養科目","広域教養科目"]
    day = ["月","火","水","木","金","土","日", "集中講義等"]
    period = ["1-","2-","3-","4-","5-","6-","7-","8-","9-","10-"]#講義室の番号と被らないためのハイフン
    quarter = ["1","2","3","4","1-2","3-4","2-3","2・4","2-4","1-4"]
    textbook = ["なし","ない","配布", "スライド", "資料"]
    assessment = [["試験","テスト"],["レポート","report"],["プレゼン","発表"]]
    #########初期値############
    course_num= 0 #情報工学系のみを許容
    day_select=[0,1,1,1,1,1,1,1]#月曜以外を許容
    period_select=[0,1,1,1,1,1,1,1,1,1]#1限以外を許容

    quarter_select=[0,0,1,1,0,1,0,0,0,0]#3Q,4Q,3-4Qのみを許容

    is_need_textbook= 1 #教科書なしを認めない。ありを認めないのが0,どちらも認めるのがそれ以外。
    is_need_assessment=[1,1,0]##試験、レポートは認めるがプレゼンは認めない

    f = None
    d = None
    nums = None

    def __init__(self, subject_codes):
        base = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.normpath(os.path.join(base, "../DataCollection/syllabus_2020.json"))
        self.f = open(filepath)
        self.d = json.load(self.f)
        #self.nums = list(range(len(self.d)))#出力するdのindex
        index_dict = defaultdict(int)#各科目コードとindexの対応表
        for i in range(len(self.d)):
            index_dict[self.d[i]["科目コード"]]=i

        initnums = []
        for x in subject_codes:
            initnums.append(index_dict[x])
        self.nums = initnums
        print("init")
        print(self.nums)

    def get_features(self):
         #############標準入力################
        print("開講元選択(数字を入力)")
        print(str(-1) + ":" + "選択しない")
        for i in range(len(self.course)):
            print(str(i) + ":" + self.course[i])
        self.course_num = int(input())
        if(self.course_num < -1 or len(self.course) < self.course_num):
            print("入力が不正です。")
            sys.exit(1)

        print("曜日(7bitで答える 1:選択, 0:選択しない")
        print("ex.)0100100")
        for i in range(len(self.day)-1):
            print(self.day[i] + " ", end = ",")
        print(self.day[len(self.day) - 1])
        input_day_select = input()
        if(len(input_day_select) != len(self.day)):
            print("入力サイズが不正です。")
            sys.exit(1)
        else:
            for i in range(len(self.day)):
                if(input_day_select[i]!="0" and input_day_select[i]!="1"):
                    print("入力文字が不正です")
                    sys.exit(1)
                else:
                    self.day_select[i] = int(input_day_select[i])


        print("開始時限(10bitで答える 1:選択, 0:選択しない)")
        print("ex.) 1010000000")
        for i in range(len(self.period)-1):
            print(str(i+1) + "限 ", end = ",")
        print(str(len(self.period)) + "限")
        flag_period=1
        while(flag_period):
            input_period_select=input()
            if(len(input_period_select)!=len(self.period)):
                print("入力サイズが不正です。")
                sys.exit(1)
            else:
                for i in range(len(self.period)):
                    if(input_period_select[i]!="0" and input_period_select[i]!="1"):
                        print("入力文字の種類が不正です")
                        sys.exit(1)
                    else:
                        self.period_select[i]=int(input_period_select[i])
                        if(i==len(self.period)-1):
                            flag_period=0



        print("開講クォーター(10bitで答える 1:選択, 0:選択しない)")
        print("ex.) 0011010000")
        for i in range(len(self.quarter)-1):
            print(" " + self.quarter[i] + "Q", end = ',')
        print(" " + self.quarter[len(self.quarter)-1] + "Q")
        flag_quarter=1
        while(flag_quarter):
            input_quarter_select=input()
            if(len(input_quarter_select)!=len(self.quarter)):
                print("入力サイズが不正です。")
                sys.exit(1)
            else:
                for i in range(len(self.quarter)):
                    if(input_quarter_select[i]!="0" and input_quarter_select[i]!="1"):
                        print("入力文字の種類が不正です")
                        sys.exit(1)
                    else:
                        self.quarter_select[i]=int(input_quarter_select[i])
                        if(i==len(self.quarter)-1):
                            flag_quarter=0

        print("教科書の有無  1:あり, 0:なし, -1:選択しない")
        self.is_need_textbook = int(input())
        if(not(self.is_need_textbook == 0 or self.is_need_textbook == 1 or self.is_need_textbook == -1)):
            print("入力が不正です。")
            sys.exit(1)

        print("試験の有無  1:あり, 0:なし, -1:選択しない")
        self.is_need_assessment[0] = int(input())
        if(not(self.is_need_assessment[0] == 0 or self.is_need_assessment[0] == 1 or self.is_need_assessment[0] == -1)):
            print("入力が不正です。")
            sys.exit(1)

        print("レポートの有無  1:あり, 0:なし, -1:選択しない")
        self.is_need_assessment[1] = int(input())
        if(not(self.is_need_assessment[1] == 0 or self.is_need_assessment[1] == 1 or self.is_need_assessment[1] == -1)):
            print("入力が不正です。")
            sys.exit(1)

        print("プレゼン・発表の有無  1:あり, 0:なし, -1:選択しない")
        self.is_need_assessment[2] = int(input())
        if(not(self.is_need_assessment[2] == 0 or self.is_need_assessment[2] == 1 or self.is_need_assessment[2] == -1)):
            print("入力が不正です。")
            sys.exit(1)

    def get_index_list(self):

        ##################main##################
        #開講元が情報工学系以外のとき、course_num[0]=0で、開講元が情報工学系のものを一掃
        if(self.course_num != -1) :
            for x in reversed(self.nums):
                if(self.course[self.course_num] != self.d[x]["開講元"]):
                    self.nums.remove(x)
        newnums1 = []
        for i in range(len(self.day_select)):
            if self.day_select[i]==1:
                for x in self.nums:
                    if(self.day[i] in self.d[x]["曜日・時限(講義室)"]):
                        newnums1.append(x)
        self.nums=list(dict.fromkeys(newnums1))
        for i in range(len(self.period_select)):
            if self.period_select[i]==0:
                for x in reversed(self.nums):
                    if(self.period[i] in self.d[x]["曜日・時限(講義室)"]):#7限開始ならそれ以外開始の授業を許さない
                        self.nums.remove(x)
        newnums2 = []
        for i in range(len(self.quarter_select)):
            if self.quarter_select[i]==1:
                for x in self.nums:
                    if(self.quarter[i] in self.d[x]["開講クォーター"]):
                        newnums2.append(x)
        self.nums=list(dict.fromkeys(newnums2))
        if self.is_need_textbook ==0:
            for x in reversed(self.nums):
                is_remove = True
                for i in range(len(self.textbook)):
                    if("教科書" not in self.d[x]):
                        break
                    if((self.textbook[i] in self.d[x]["教科書"])):
                        is_remove = False
                        break
                if(is_remove):
                    self.nums.remove(x)
        elif self.is_need_textbook == 1:
            for x in reversed(self.nums):
                is_remove = False
                for i in range(len(self.textbook)):
                    if("教科書" not in self.d[x] or (self.textbook[i] in self.d[x]["教科書"])):
                        is_remove = True
                        break
                if(is_remove):
                    self.nums.remove(x)

        for i in range(len(self.is_need_assessment)):
            if self.is_need_assessment[i]==0:
                for x in reversed(self.nums):
                    is_remove = False
                    for j in range(len(self.assessment[i])):
                        if("成績評価の基準及び方法" not in self.d[x] or self.assessment[i][j] in self.d[x]["成績評価の基準及び方法"]):
                            is_remove = True
                            break
                    if(is_remove):
                        self.nums.remove(x)
            elif self.is_need_assessment[i]==1:
                for x in reversed(self.nums):
                    is_remove = True
                    for j in range(len(self.assessment[i])):
                        if("成績評価の基準及び方法" not in self.d[x]):
                            break
                        if((self.assessment[i][j] in self.d[x]["成績評価の基準及び方法"] or self.assessment[i][j] in self.d[x]["成績評価の基準及び方法"])):
                            is_remove = False
                            break
                    if(is_remove):
                        self.nums.remove(x)

        return self.nums

    def print_result(self):
        index_list = self.get_index_list()
        print("----------該当講義一覧----------")
        for x in index_list:
            print(self.d[x]["講義名"]["日本語"])
        print("--------------------------------")
        
if __name__ == "__main__":
    f = open("../DataCollection/syllabus_2020.json")
    d = json.load(f)
    subject_codes = []
    for i in range(len(d)):
        if d[i]["開講元"] == "情報工学系":
            subject_codes.append(d[i]["科目コード"])

    fs = feature_search(subject_codes)  
    fs.get_features()                   
    fs.print_result()                   

    sys.exit(0)
