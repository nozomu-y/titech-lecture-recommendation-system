# -*- coding: utf-8 -*-
import os
import numpy as np
from sklearn import tree

class classification:
    """ファイルからのデータ読み込み
        決定木での学習
        木構造を解析し質問、回答を返す
    """

    def load(self):
        
        #相対パス取得
        base = os.path.dirname(os.path.abspath(__file__))

        #ファイルパス取得
        data_file = os.path.normpath(os.path.join(base, './data/data.tsv'))
        label_file = os.path.normpath(os.path.join(base, './data/label_nm.txt'))
        feature_file = os.path.normpath(os.path.join(base, './data/feature_nm.txt'))
        
        #データ読み込み
        self.data = np.loadtxt(data_file, delimiter='\t')   #tsvは'\t'で区切られている
        self.label = open(label_file, 'r', encoding='utf-8').readlines()
        for i in range(len(self.label)):
            self.label[i] = self.label[i].rstrip("\n")  #rstrip()文字列の右側から指定した文字列を削除
        self.feature = open(feature_file, 'r', encoding='utf-8').readlines()
        for i in range(len(self.feature)):
            self.feature[i] = self.feature[i].rstrip("\n")

        #学習
        self.clf = tree.DecisionTreeClassifier()
        self.clf.fit(self.data, self.label)

    def save(self, answer, feature_nm_list, data_list):
        #answerには追加するデータのlabel名がくる
        #feature_nm_listには追加するデータの特徴名のリストがくる
        #data_listにはfeature_nm_listの質問文に対する答えがくる
        
        feature_list = self.__get_feature_list(feature_nm_list)
        #特徴名（質問文)のリストからそのインデックス(feature_nm.txtにおける何行目か)のリストを取得

        test_data = []
        for i in range(len(self.feature)):
            if i in feature_list:
                test_data.append(data_list[feature_list.index(i)])
            else:
                test_data.append("3")
        #feature_nm_listとdata_listからdata.tsvに保存するためのデータを作成.未解答の特徴名に対しては3を代入


        #相対パス取得
        base = os.path.dirname(os.path.abspath(__file__))
        #ファイルパス取得
        data_file = os.path.normpath(os.path.join(base, './data/data.tsv'))
        label_file = os.path.normpath(os.path.join(base, './data/label_nm.txt'))
        data_writer = open(data_file, 'a', encoding='utf-8') #'a'オプションはfileへのデータの追記
        label_writer = open(label_file, 'a', encoding='utf-8')

        data_tsv = ""
        for data in test_data:

            if data_tsv != "":
                data_tsv = data_tsv + "\t"
            
            data_tsv = data_tsv + data

        data_writer.write(data_tsv + "\n")
        label_writer.write(answer + "\n")   

    def answer(self, feature_nm_list, data_list):
        
        feature_list = self.__get_feature_list(feature_nm_list)
        queation, answer = self.__recursion(0, 0, feature_list, data_list)

        return answer

    def queation(self, feature_nm_list, data_list):
                
        feature_list = self.__get_feature_list(feature_nm_list)
        queation, answer = self.__recursion(0, 0, feature_list, data_list)

        return queation

    def __get_feature_list(self, feature_nm_list):
        #特徴名からindex番号のリストを取得
        feature_list = []
        for feature_nm in feature_nm_list:
            if feature_nm in self.feature:
                feature_list.append(self.feature.index(feature_nm))
        return feature_list

    def __recursion(self, node_index, class_cnt, feature_list, data_list):
        #毎回決定木の根から動作を行っている
        #node_index, class_cntを変えて再帰呼び出しを行うことで、どんどん決定木の中を調べ、解答や質問を生成する
        #node_index, class_cntの初期値は0, 0
        #feature_list, data_listはそれぞれ利用者に質問したものの質問とその解答のリスト

        #tree構造のレンジ外なら(ERROR)
        if self.clf.tree_.node_count <= node_index:
            raise "tree構造のレンジ外"

        feature_index = self.clf.tree_.feature[node_index]
        #対象のノードの要素を分岐させるためのfeatureのindexを取得
  
        #特徴が-2の場合終端ノードなので、labelを返す
        #answerを返す部分
        value_list1 = self.clf.tree_.value[node_index][0].tolist()
        value_nonzero_cnt = np.count_nonzero(value_list1)
        if str(feature_index) == "-2" or value_nonzero_cnt <= 3:
            value_list = self.clf.tree_.value[node_index][0].tolist()
            label_index = []
            for i in range(len(value_list)):
                if value_list[i] != 0:
                    label_index.append(i)

            #label_index = value_list.index(max(value_list))
            answers = ""
            for i in label_index:
                if answers != "":
                    answers = answers + "  "
                 
                answers = answers + self.clf.classes_[i]


            return "", answers

        #現在の階層より、取得済みの回答が少ない場合、問題を返す
        #questionを返す部分
        if class_cnt > len(feature_list) - 1:
            return self.feature[feature_index], ""

        #treeの特徴と回答の特徴が一致しない場合(ERROR)
        #分岐を進むための特徴（質問）と回答してもらった特徴（質問）が一致しない場合の動作
        if feature_list[class_cnt] != feature_index:
            raise "treeの特徴と回答の特徴が一致しない"

        feature_threshold = self.clf.tree_.threshold[node_index]

        #境界値以下の場合は左のノード、それ以外は右のノード
        if int(data_list[class_cnt]) <= feature_threshold:
            next_index = self.clf.tree_.children_left[node_index]
        else :
            next_index = self.clf.tree_.children_right[node_index]

        return self.__recursion(next_index, class_cnt + 1, feature_list, data_list)


if __name__ == '__main__':
    clf = classification()
    clf.load()
    print(clf.queation([], []))
    #print(clf.queation(["問1"], [2]))
    
